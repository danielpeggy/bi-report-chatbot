"""
Glue PySpark ETL Script: Load Dimension Tables
Loads dimension tables from S3 CSV to Redshift Serverless
Database: genbi_mart schema in dev database
"""

import sys
from datetime import datetime, timedelta
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.types import (
    StructType, StructField, IntegerType, StringType, DateType,
    DoubleType, BooleanType, TimestampType
)
from pyspark.sql.functions import (
    col, lit, year, month, dayofmonth, dayofweek, date_format,
    weekofyear, to_date, concat, when, coalesce, upper, trim,
    row_number
)
from pyspark.sql.window import Window
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Glue job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'redshift_password'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Configuration
S3_SOURCE_BUCKET = "s3://genbi-mcdhk-raw-530977327410"
S3_STAGING = "s3://genbi-mcdhk-scripts-530977327410/tmp/"
REDSHIFT_ENDPOINT = "demo-sales-related.530977327410.us-east-1.redshift-serverless.amazonaws.com"
REDSHIFT_PORT = "5439"
REDSHIFT_DB = "dev"
REDSHIFT_SCHEMA = "genbi_mart"
REDSHIFT_USER = "admin"
REDSHIFT_PASSWORD = args.get('redshift_password', '')

logger.info(f"Starting Glue ETL job: {args['JOB_NAME']}")
logger.info(f"Target: {REDSHIFT_SCHEMA} in {REDSHIFT_DB}")


def write_to_redshift(dynamic_frame, table_name, mode="overwrite"):
    """
    Write DynamicFrame to Redshift using COPY method

    Args:
        dynamic_frame: Glue DynamicFrame to write
        table_name: Target table name (without schema)
        mode: Write mode (overwrite, append)
    """
    try:
        redshift_url = f"jdbc:redshift://{REDSHIFT_ENDPOINT}:{REDSHIFT_PORT}/{REDSHIFT_DB}"

        logger.info(f"Writing to Redshift table: {REDSHIFT_SCHEMA}.{table_name}")

        glueContext.write_dynamic_frame.from_options(
            frame=dynamic_frame,
            connection_type="redshift",
            connection_options={
                "url": redshift_url,
                "dbtable": f"{REDSHIFT_SCHEMA}.{table_name}",
                "user": REDSHIFT_USER,
                "password": REDSHIFT_PASSWORD,
                "redshiftTmpDir": S3_STAGING,
                "aws_iam_role": "arn:aws:iam::530977327410:role/GlueExecutionRole"
            },
            format="parquet",
            format_options={"compression": "snappy"}
        )
        logger.info(f"Successfully wrote to {REDSHIFT_SCHEMA}.{table_name}")
    except Exception as e:
        logger.error(f"Error writing to Redshift table {table_name}: {str(e)}")
        raise


def load_dim_date():
    """
    Generate dim_date table programmatically for 2023
    365 rows (2023 is not a leap year)
    """
    logger.info("Loading dim_date...")

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    # HK Public Holidays 2023
    hk_holidays_2023 = [
        datetime(2023, 1, 1),   # New Year's Day
        datetime(2023, 1, 23),  # Chinese New Year
        datetime(2023, 1, 24),  # Chinese New Year
        datetime(2023, 1, 25),  # Chinese New Year
        datetime(2023, 4, 4),   # Children's Day
        datetime(2023, 4, 5),   # Ching Ming Festival
        datetime(2023, 4, 10),  # Easter Monday
        datetime(2023, 5, 1),   # Labour Day
        datetime(2023, 5, 26),  # Buddha's Birthday
        datetime(2023, 6, 10),  # Dragon Boat Festival
        datetime(2023, 9, 29),  # National Day
        datetime(2023, 9, 30),  # Day following Mid-Autumn Festival
        datetime(2023, 10, 11), # Chung Yeung Festival
        datetime(2023, 12, 25), # Christmas Day
        datetime(2023, 12, 26), # Boxing Day
    ]

    dates = []
    current_date = start_date

    while current_date <= end_date:
        date_key = int(current_date.strftime("%Y%m%d"))
        full_date = current_date.date()
        year_val = current_date.year
        quarter = (current_date.month - 1) // 3 + 1
        month_val = current_date.month
        month_name = current_date.strftime("%B")
        week_of_year = current_date.strftime("%U")
        day_of_month = current_date.day
        day_of_week = current_date.weekday() + 1  # 1=Monday, 7=Sunday
        day_name = current_date.strftime("%A")
        is_weekend = 1 if day_of_week in [6, 7] else 0
        is_holiday = 1 if current_date in hk_holidays_2023 else 0

        dates.append((
            date_key, full_date, year_val, quarter, month_val, month_name,
            int(week_of_year), day_of_month, day_of_week, day_name,
            is_weekend, is_holiday
        ))

        current_date += timedelta(days=1)

    schema = StructType([
        StructField("date_key", IntegerType(), False),
        StructField("full_date", DateType(), False),
        StructField("year", IntegerType(), True),
        StructField("quarter", IntegerType(), True),
        StructField("month", IntegerType(), True),
        StructField("month_name", StringType(), True),
        StructField("week_of_year", IntegerType(), True),
        StructField("day_of_month", IntegerType(), True),
        StructField("day_of_week", IntegerType(), True),
        StructField("day_name", StringType(), True),
        StructField("is_weekend", IntegerType(), True),
        StructField("is_holiday", IntegerType(), True)
    ])

    df = spark.createDataFrame(dates, schema=schema)
    row_count = df.count()
    logger.info(f"dim_date: {row_count} rows")

    dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dim_date")
    write_to_redshift(dynamic_frame, "dim_date", mode="overwrite")


def load_dim_store():
    """Load dim_store from stores.csv"""
    logger.info("Loading dim_store...")

    try:
        s3_path = f"{S3_SOURCE_BUCKET}/reference/stores/stores.csv"
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(s3_path)

        # Clean column names and trim whitespace
        df = df.select([col(c).alias(c.lower()) for c in df.columns])
        for col_name in df.columns:
            if df.schema[col_name].dataType == StringType():
                df = df.withColumn(col_name, trim(col(col_name)))

        row_count = df.count()
        logger.info(f"dim_store: {row_count} rows")

        dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dim_store")
        write_to_redshift(dynamic_frame, "dim_store", mode="overwrite")
    except Exception as e:
        logger.error(f"Error loading dim_store: {str(e)}")
        raise


def load_dim_menu_item():
    """Load dim_menu_item from menu_items and categories"""
    logger.info("Loading dim_menu_item...")

    try:
        # Load menu items
        menu_items_path = f"{S3_SOURCE_BUCKET}/reference/menu_items/"
        menu_df = spark.read.option("header", "true").option("inferSchema", "true").csv(menu_items_path)

        # Load categories
        categories_path = f"{S3_SOURCE_BUCKET}/reference/categories/"
        categories_df = spark.read.option("header", "true").option("inferSchema", "true").csv(categories_path)

        # Clean column names
        menu_df = menu_df.select([col(c).alias(c.lower()) for c in menu_df.columns])
        categories_df = categories_df.select([col(c).alias(c.lower()) for c in categories_df.columns])

        # Join on category_id
        df = menu_df.join(
            categories_df.select(col("category_id"), col("category_name")),
            on="category_id",
            how="left"
        )

        # Calculate food_cost_pct (cogs/unit_price * 100)
        df = df.withColumn(
            "food_cost_pct",
            when(col("unit_price") != 0,
                 (col("cogs") / col("unit_price") * 100).cast(DoubleType())
            ).otherwise(lit(0.0))
        )

        # Trim string columns
        for col_name in df.columns:
            if df.schema[col_name].dataType == StringType():
                df = df.withColumn(col_name, trim(col(col_name)))

        row_count = df.count()
        logger.info(f"dim_menu_item: {row_count} rows")

        dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dim_menu_item")
        write_to_redshift(dynamic_frame, "dim_menu_item", mode="overwrite")
    except Exception as e:
        logger.error(f"Error loading dim_menu_item: {str(e)}")
        raise


def load_dim_customer():
    """Load dim_customer from customer_profiles"""
    logger.info("Loading dim_customer...")

    try:
        customer_path = f"{S3_SOURCE_BUCKET}/customer/customer_profiles/"
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(customer_path)

        # Select only dimension columns
        dimension_columns = [
            "customer_id", "age_group", "gender", "home_district",
            "preferred_store_id", "loyalty_tier", "registration_date", "first_visit_date"
        ]

        # Filter to available columns
        available_cols = [col for col in dimension_columns if col in df.columns]
        df = df.select([col(c).alias(c.lower()) for c in available_cols])

        # Trim string columns
        for col_name in df.columns:
            if df.schema[col_name].dataType == StringType():
                df = df.withColumn(col_name, trim(col(col_name)))

        row_count = df.count()
        logger.info(f"dim_customer: {row_count} rows")

        dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dim_customer")
        write_to_redshift(dynamic_frame, "dim_customer", mode="overwrite")
    except Exception as e:
        logger.error(f"Error loading dim_customer: {str(e)}")
        raise


def load_dim_channel():
    """Load dim_channel from channels"""
    logger.info("Loading dim_channel...")

    try:
        channel_path = f"{S3_SOURCE_BUCKET}/reference/channels/"
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(channel_path)

        # Clean column names
        df = df.select([col(c).alias(c.lower()) for c in df.columns])

        # Trim string columns
        for col_name in df.columns:
            if df.schema[col_name].dataType == StringType():
                df = df.withColumn(col_name, trim(col(col_name)))

        row_count = df.count()
        logger.info(f"dim_channel: {row_count} rows")

        dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dim_channel")
        write_to_redshift(dynamic_frame, "dim_channel", mode="overwrite")
    except Exception as e:
        logger.error(f"Error loading dim_channel: {str(e)}")
        raise


def load_dim_payment_method():
    """Load dim_payment_method from payment_methods"""
    logger.info("Loading dim_payment_method...")

    try:
        payment_path = f"{S3_SOURCE_BUCKET}/reference/payment_methods/"
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(payment_path)

        # Clean column names
        df = df.select([col(c).alias(c.lower()) for c in df.columns])

        # Trim string columns
        for col_name in df.columns:
            if df.schema[col_name].dataType == StringType():
                df = df.withColumn(col_name, trim(col(col_name)))

        row_count = df.count()
        logger.info(f"dim_payment_method: {row_count} rows")

        dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dim_payment_method")
        write_to_redshift(dynamic_frame, "dim_payment_method", mode="overwrite")
    except Exception as e:
        logger.error(f"Error loading dim_payment_method: {str(e)}")
        raise


def load_dim_promotion():
    """Load dim_promotion from promotions"""
    logger.info("Loading dim_promotion...")

    try:
        promotion_path = f"{S3_SOURCE_BUCKET}/reference/promotions/"
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(promotion_path)

        # Clean column names
        df = df.select([col(c).alias(c.lower()) for c in df.columns])

        # Trim string columns
        for col_name in df.columns:
            if df.schema[col_name].dataType == StringType():
                df = df.withColumn(col_name, trim(col(col_name)))

        row_count = df.count()
        logger.info(f"dim_promotion: {row_count} rows")

        dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dim_promotion")
        write_to_redshift(dynamic_frame, "dim_promotion", mode="overwrite")
    except Exception as e:
        logger.error(f"Error loading dim_promotion: {str(e)}")
        raise


def main():
    """Execute all dimension loads"""
    try:
        # Load all dimensions
        load_dim_date()
        load_dim_store()
        load_dim_menu_item()
        load_dim_customer()
        load_dim_channel()
        load_dim_payment_method()
        load_dim_promotion()

        logger.info("All dimensions loaded successfully!")
        job.commit()
    except Exception as e:
        logger.error(f"Job failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
