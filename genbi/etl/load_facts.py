"""
Glue PySpark ETL Script: Load Fact Tables from S3 to Redshift
Loads: fact_sales, fact_inventory, fact_labor, fact_service_performance,
       fact_customer_feedback, fact_loyalty, fact_equipment, fact_financial
"""

import sys
import logging
from datetime import datetime
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    col, to_date, date_format, when, coalesce, lit, concat_ws,
    year, month, dayofmonth, from_unixtime, unix_timestamp,
    sum as spark_sum, count, avg
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, DateType

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get job parameters
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'redshift_password'
])

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Configuration
S3_SOURCE_BUCKET = "s3://genbi-mcdhk-raw-530977327410"
REDSHIFT_URL = "jdbc:redshift://demo-sales-related.530977327410.us-east-1.redshift-serverless.amazonaws.com:5439/dev"
REDSHIFT_SCHEMA = "genbi_mart"
REDSHIFT_USER = "admin"
REDSHIFT_PASSWORD = args['redshift_password']
REDSHIFT_TMP_DIR = "s3://genbi-mcdhk-scripts-530977327410/tmp/"

# Logging helper
def log_info(message):
    """Log info message"""
    logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def log_error(message):
    """Log error message"""
    logger.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# Write to Redshift helper
def write_to_redshift(df, table_name, mode="append"):
    """Write DataFrame to Redshift"""
    try:
        log_info(f"Writing {df.count()} rows to {REDSHIFT_SCHEMA}.{table_name}")

        dynamic_frame = DynamicFrame.fromDF(df, glueContext, table_name)

        glueContext.write_dynamic_frame.from_options(
            frame=dynamic_frame,
            connection_type="redshift",
            connection_options={
                "url": REDSHIFT_URL,
                "dbtable": f"{REDSHIFT_SCHEMA}.{table_name}",
                "user": REDSHIFT_USER,
                "password": REDSHIFT_PASSWORD,
                "redshiftTmpDir": REDSHIFT_TMP_DIR,
                "aws_iam_role": "arn:aws:iam::530977327410:role/AWSGlueServiceRole"
            },
            format="redshift",
            format_options={
                "preactions": f"BEGIN; DELETE FROM {REDSHIFT_SCHEMA}.{table_name} WHERE date_key = CAST(TO_CHAR(CURRENT_DATE, 'YYYYMMDD') AS INT);" if mode == "upsert" else ""
            }
        )

        log_info(f"Successfully wrote to {REDSHIFT_SCHEMA}.{table_name}")
        return True
    except Exception as e:
        log_error(f"Failed to write {table_name}: {str(e)}")
        return False

# ============================================================================
# FACT_SALES
# ============================================================================
def load_fact_sales():
    """Load fact_sales from transactions and line_items"""
    try:
        log_info("Starting fact_sales load...")

        # Read transactions
        transactions = spark.read.option("header", "true").option("inferSchema", "true") \
            .csv(f"{S3_SOURCE_BUCKET}/pos/transactions/")

        # Read line items
        line_items = spark.read.option("header", "true").option("inferSchema", "true") \
            .csv(f"{S3_SOURCE_BUCKET}/pos/line_items/")

        log_info(f"Transactions: {transactions.count()} rows")
        log_info(f"Line items: {line_items.count()} rows")

        # Join on transaction_id
        fact_sales = transactions.join(
            line_items,
            on="transaction_id",
            how="inner"
        )

        # Calculate transformations
        fact_sales = fact_sales.withColumn(
            "date_key",
            date_format(col("order_date"), "yyyyMMdd").cast(IntegerType())
        ).withColumn(
            "discount_amount",
            coalesce(col("discount"), lit(0.0))
        ).withColumn(
            "cogs_amount",
            coalesce(col("cogs"), lit(0.0))
        ).withColumn(
            "gross_profit",
            col("line_total") - coalesce(col("discount_per_item"), lit(0.0)) - col("cogs_amount")
        ).select(
            "date_key",
            "transaction_id",
            "product_id",
            "store_id",
            "quantity",
            "line_total",
            "discount_amount",
            "cogs_amount",
            "gross_profit",
            col("order_date").alias("transaction_date")
        )

        # Repartition for performance (largest table)
        fact_sales = fact_sales.repartition(32, "date_key")

        row_count = fact_sales.count()
        log_info(f"fact_sales prepared: {row_count} rows")

        # Write to Redshift
        write_to_redshift(fact_sales, "fact_sales", mode="append")

        return True
    except Exception as e:
        log_error(f"Error loading fact_sales: {str(e)}")
        return False

# ============================================================================
# FACT_INVENTORY
# ============================================================================
def load_fact_inventory():
    """Load fact_inventory from inventory_daily"""
    try:
        log_info("Starting fact_inventory load...")

        inventory = spark.read.option("header", "true").option("inferSchema", "true") \
            .csv(f"{S3_SOURCE_BUCKET}/operations/inventory_daily/")

        inventory = inventory.withColumn(
            "date_key",
            date_format(col("date"), "yyyyMMdd").cast(IntegerType())
        ).withColumn(
            "waste_rate",
            when(
                (col("units_sold") + col("units_wasted")) > 0,
                col("units_wasted") / (col("units_sold") + col("units_wasted"))
            ).otherwise(lit(0.0))
        ).select(
            "date_key",
            "store_id",
            "product_id",
            "units_on_hand",
            "units_sold",
            "units_wasted",
            "waste_rate"
        )

        row_count = inventory.count()
        log_info(f"fact_inventory prepared: {row_count} rows")

        write_to_redshift(inventory, "fact_inventory", mode="append")
        return True
    except Exception as e:
        log_error(f"Error loading fact_inventory: {str(e)}")
        return False

# ============================================================================
# FACT_LABOR
# ============================================================================
def load_fact_labor():
    """Load fact_labor from labor_schedules"""
    try:
        log_info("Starting fact_labor load...")

        labor = spark.read.option("header", "true").option("inferSchema", "true") \
            .csv(f"{S3_SOURCE_BUCKET}/operations/labor_schedules/")

        labor = labor.withColumn(
            "date_key",
            date_format(col("date"), "yyyyMMdd").cast(IntegerType())
        ).withColumn(
            "shift_start",
            col("shift_start_hour")
        ).withColumn(
            "shift_end",
            col("shift_end_hour")
        ).select(
            "date_key",
            "store_id",
            "employee_id",
            "shift_start",
            "shift_end",
            col("hours_scheduled").alias("scheduled_hours"),
            col("hours_worked").alias("worked_hours")
        )

        row_count = labor.count()
        log_info(f"fact_labor prepared: {row_count} rows")

        write_to_redshift(labor, "fact_labor", mode="append")
        return True
    except Exception as e:
        log_error(f"Error loading fact_labor: {str(e)}")
        return False

# ============================================================================
# FACT_SERVICE_PERFORMANCE
# ============================================================================
def load_fact_service_performance():
    """Load fact_service_performance from service_times"""
    try:
        log_info("Starting fact_service_performance load...")

        service = spark.read.option("header", "true").option("inferSchema", "true") \
            .csv(f"{S3_SOURCE_BUCKET}/operations/service_times/")

        service = service.withColumn(
            "date_key",
            date_format(col("date"), "yyyyMMdd").cast(IntegerType())
        ).withColumn(
            "avg_counter_secs",
            col("avg_counter_wait_secs")
        ).select(
            "date_key",
            "store_id",
            "avg_counter_secs",
            col("avg_drive_thru_wait_secs").alias("avg_drivethrough_secs"),
            col("avg_order_prep_secs").alias("avg_prep_secs"),
            col("peak_hour_wait_secs").alias("peak_wait_secs")
        )

        row_count = service.count()
        log_info(f"fact_service_performance prepared: {row_count} rows")

        write_to_redshift(service, "fact_service_performance", mode="append")
        return True
    except Exception as e:
        log_error(f"Error loading fact_service_performance: {str(e)}")
        return False

# ============================================================================
# FACT_CUSTOMER_FEEDBACK
# ============================================================================
def load_fact_customer_feedback():
    """Load fact_customer_feedback from feedback_surveys"""
    try:
        log_info("Starting fact_customer_feedback load...")

        feedback = spark.read.option("header", "true").option("inferSchema", "true") \
            .csv(f"{S3_SOURCE_BUCKET}/customer/feedback_surveys/")

        feedback = feedback.withColumn(
            "date_key",
            date_format(col("survey_date"), "yyyyMMdd").cast(IntegerType())
        ).withColumn(
            "would_recommend",
            when(col("recommendation") == "yes", True).when(col("recommendation") == "no", False).otherwise(None)
        ).select(
            "date_key",
            "store_id",
            "customer_id",
            col("satisfaction_score").alias("satisfaction"),
            col("food_quality_score").alias("food_quality"),
            col("service_score").alias("service"),
            col("cleanliness_score").alias("cleanliness"),
            "would_recommend",
            col("feedback_comment").alias("comments")
        )

        row_count = feedback.count()
        log_info(f"fact_customer_feedback prepared: {row_count} rows")

        write_to_redshift(feedback, "fact_customer_feedback", mode="append")
        return True
    except Exception as e:
        log_error(f"Error loading fact_customer_feedback: {str(e)}")
        return False

# ============================================================================
# FACT_LOYALTY
# ============================================================================
def load_fact_loyalty():
    """Load fact_loyalty from loyalty_transactions"""
    try:
        log_info("Starting fact_loyalty load...")

        loyalty = spark.read.option("header", "true").option("inferSchema", "true") \
            .csv(f"{S3_SOURCE_BUCKET}/customer/loyalty_transactions/")

        loyalty = loyalty.withColumn(
            "date_key",
            date_format(col("transaction_date"), "yyyyMMdd").cast(IntegerType())
        ).withColumn(
            "txn_type",
            col("transaction_type")
        ).withColumn(
            "points_balance",
            col("points_balance_after")
        ).withColumn(
            "order_value",
            col("associated_order_value")
        ).select(
            "date_key",
            "loyalty_member_id",
            "store_id",
            "txn_type",
            col("points_earned").alias("points_earned"),
            col("points_redeemed").alias("points_redeemed"),
            "points_balance",
            "order_value"
        )

        row_count = loyalty.count()
        log_info(f"fact_loyalty prepared: {row_count} rows")

        write_to_redshift(loyalty, "fact_loyalty", mode="append")
        return True
    except Exception as e:
        log_error(f"Error loading fact_loyalty: {str(e)}")
        return False

# ============================================================================
# FACT_EQUIPMENT
# ============================================================================
def load_fact_equipment():
    """Load fact_equipment from equipment_logs"""
    try:
        log_info("Starting fact_equipment load...")

        equipment = spark.read.option("header", "true").option("inferSchema", "true") \
            .csv(f"{S3_SOURCE_BUCKET}/operations/equipment_logs/")

        equipment = equipment.withColumn(
            "date_key",
            date_format(col("event_date"), "yyyyMMdd").cast(IntegerType())
        ).select(
            "date_key",
            "store_id",
            "equipment_id",
            col("equipment_type").alias("type"),
            col("event_type").alias("event"),
            col("hours_operating").alias("operating_hours"),
            col("maintenance_required").alias("requires_maintenance")
        )

        row_count = equipment.count()
        log_info(f"fact_equipment prepared: {row_count} rows")

        write_to_redshift(equipment, "fact_equipment", mode="append")
        return True
    except Exception as e:
        log_error(f"Error loading fact_equipment: {str(e)}")
        return False

# ============================================================================
# FACT_FINANCIAL
# ============================================================================
def load_fact_financial():
    """Load fact_financial from store_pnl"""
    try:
        log_info("Starting fact_financial load...")

        financial = spark.read.option("header", "true").option("inferSchema", "true") \
            .csv(f"{S3_SOURCE_BUCKET}/financial/store_pnl/")

        financial = financial.withColumn(
            "month_key",
            date_format(col("month"), "yyyyMM").cast(IntegerType())
        ).select(
            "month_key",
            "store_id",
            col("total_revenue").alias("revenue"),
            col("cost_of_goods").alias("cogs"),
            col("labor_cost").alias("labor"),
            col("operating_cost").alias("operating_costs"),
            col("gross_profit").alias("gross_profit"),
            col("operating_profit").alias("operating_profit"),
            col("net_profit").alias("net_profit"),
            col("profit_margin").alias("margin")
        )

        row_count = financial.count()
        log_info(f"fact_financial prepared: {row_count} rows")

        write_to_redshift(financial, "fact_financial", mode="append")
        return True
    except Exception as e:
        log_error(f"Error loading fact_financial: {str(e)}")
        return False

# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """Main ETL orchestration"""
    log_info("Starting GenBI Fact Tables ETL Job")

    results = {
        "fact_sales": False,
        "fact_inventory": False,
        "fact_labor": False,
        "fact_service_performance": False,
        "fact_customer_feedback": False,
        "fact_loyalty": False,
        "fact_equipment": False,
        "fact_financial": False
    }

    # Execute all fact table loads
    results["fact_sales"] = load_fact_sales()
    results["fact_inventory"] = load_fact_inventory()
    results["fact_labor"] = load_fact_labor()
    results["fact_service_performance"] = load_fact_service_performance()
    results["fact_customer_feedback"] = load_fact_customer_feedback()
    results["fact_loyalty"] = load_fact_loyalty()
    results["fact_equipment"] = load_fact_equipment()
    results["fact_financial"] = load_fact_financial()

    # Summary
    log_info("="*60)
    log_info("ETL Job Summary")
    log_info("="*60)
    for table, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        log_info(f"{table}: {status}")

    passed = sum(1 for v in results.values() if v)
    total = len(results)
    log_info(f"Total: {passed}/{total} tables loaded successfully")
    log_info("="*60)

    # Job completion
    job.commit()

if __name__ == "__main__":
    main()
