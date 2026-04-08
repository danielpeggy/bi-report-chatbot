"""
Glue PySpark ETL Script: Load Metadata and Lineage for GenBI Chatbot
Populates critical metadata tables in Redshift genbi_mart schema:
- etl_job_registry: All ETL jobs and their data lineage
- etl_column_lineage: Column-level transformations and calculations
- data_dictionary: Business-friendly definitions for all tables and columns
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
import boto3
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Get Glue job parameters
args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "redshift_password",
        "TempDir",
    ],
)

# Initialize Spark and Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Redshift connection parameters
REDSHIFT_HOST = "demo-sales-related.530977327410.us-east-1.redshift-serverless.amazonaws.com"
REDSHIFT_PORT = 5439
REDSHIFT_DB = "dev"
REDSHIFT_USER = "awsuser"
REDSHIFT_PASSWORD = args["redshift_password"]
REDSHIFT_SCHEMA = "genbi_mart"
S3_TEMP_DIR = args["TempDir"]

logger.info(f"Connecting to Redshift: {REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}")

try:
    # ==========================================
    # 1. ETL JOB REGISTRY TABLE
    # ==========================================
    logger.info("Creating etl_job_registry data")

    etl_jobs = [
        {
            "job_name": "load_dim_date",
            "source": "programmatic",
            "target": "genbi_mart.dim_date",
            "description": "Generates date dimension for 2023 calendar year with HK public holidays",
            "job_type": "dimension",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_dim_store",
            "source": "raw_reference_stores",
            "target": "genbi_mart.dim_store",
            "description": "Loads 200 ABC Restaurant HK store locations with district, region, and type classification",
            "job_type": "dimension",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_dim_menu_item",
            "source": "raw_reference_menu_items + raw_reference_categories",
            "target": "genbi_mart.dim_menu_item",
            "description": "Joins menu items with categories, calculates food cost percentage",
            "job_type": "dimension",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_dim_customer",
            "source": "raw_customer_customer_profiles",
            "target": "genbi_mart.dim_customer",
            "description": "Extracts customer demographics and loyalty tier from profiles",
            "job_type": "dimension",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_fact_sales",
            "source": "raw_pos_transactions + raw_pos_line_items",
            "target": "genbi_mart.fact_sales",
            "description": "Joins POS transactions with line items, calculates discount allocation, COGS, and gross profit per item",
            "job_type": "fact",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_fact_inventory",
            "source": "raw_operations_inventory_daily",
            "target": "genbi_mart.fact_inventory",
            "description": "Loads daily inventory levels, calculates waste rate as wasted/(sold+wasted)",
            "job_type": "fact",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_fact_labor",
            "source": "raw_operations_labor_schedules",
            "target": "genbi_mart.fact_labor",
            "description": "Loads shift schedules with actual hours and labor cost calculations",
            "job_type": "fact",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_fact_service",
            "source": "raw_operations_service_times",
            "target": "genbi_mart.fact_service_performance",
            "description": "Loads hourly service time metrics across all channels",
            "job_type": "fact",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_fact_feedback",
            "source": "raw_customer_feedback_surveys",
            "target": "genbi_mart.fact_customer_feedback",
            "description": "Loads customer survey responses with sentiment classification",
            "job_type": "fact",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_fact_loyalty",
            "source": "raw_customer_loyalty_transactions",
            "target": "genbi_mart.fact_loyalty",
            "description": "Loads loyalty point earn/redeem transactions",
            "job_type": "fact",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_fact_equipment",
            "source": "raw_operations_equipment_logs",
            "target": "genbi_mart.fact_equipment",
            "description": "Loads equipment maintenance and breakdown events",
            "job_type": "fact",
            "created_at": datetime.now(),
            "status": "active"
        },
        {
            "job_name": "load_fact_financial",
            "source": "raw_financial_store_pnl",
            "target": "genbi_mart.fact_financial",
            "description": "Loads monthly store P&L with revenue, COGS, labor, rent, and profitability",
            "job_type": "fact",
            "created_at": datetime.now(),
            "status": "active"
        },
    ]

    jobs_df = spark.createDataFrame(etl_jobs)
    logger.info(f"Created {len(etl_jobs)} ETL job records")

    # ==========================================
    # 2. ETL COLUMN LINEAGE TABLE
    # ==========================================
    logger.info("Creating etl_column_lineage data")

    column_lineage = [
        # fact_sales lineage
        {
            "target_table": "fact_sales",
            "target_column": "gross_profit",
            "source_tables": "pos_transactions, pos_line_items",
            "source_columns": "total_amount, cogs_amount, discount_amount",
            "transformation": "(line_total - (discount_amount / order_item_count) - cogs_amount)",
            "business_logic": "Revenue per item minus allocated discount and food cost (COGS)"
        },
        {
            "target_table": "fact_sales",
            "target_column": "net_profit",
            "source_tables": "pos_transactions, pos_line_items",
            "source_columns": "gross_profit",
            "transformation": "gross_profit * margin_factor",
            "business_logic": "Gross profit adjusted for overhead allocation factor"
        },
        {
            "target_table": "fact_sales",
            "target_column": "discount_amount",
            "source_tables": "pos_transactions",
            "source_columns": "discount_amount, item_count",
            "transformation": "Transaction-level discount allocated proportionally across line items",
            "business_logic": "Discount distributed evenly across items in order"
        },
        {
            "target_table": "fact_sales",
            "target_column": "line_total",
            "source_tables": "pos_line_items",
            "source_columns": "unit_price, quantity",
            "transformation": "unit_price * quantity",
            "business_logic": "Price per item multiplied by quantity ordered"
        },
        {
            "target_table": "fact_sales",
            "target_column": "cogs_amount",
            "source_tables": "pos_line_items, raw_reference_menu_items",
            "source_columns": "quantity, food_cost",
            "transformation": "quantity * food_cost",
            "business_logic": "Food cost per item multiplied by quantity sold"
        },
        {
            "target_table": "fact_sales",
            "target_column": "margin_pct",
            "source_tables": "pos_line_items",
            "source_columns": "gross_profit, line_total",
            "transformation": "(gross_profit / line_total) * 100",
            "business_logic": "Profitability percentage before overhead costs"
        },
        {
            "target_table": "fact_sales",
            "target_column": "item_count",
            "source_tables": "pos_transactions",
            "source_columns": "transaction_id",
            "transformation": "COUNT(line_items) per transaction",
            "business_logic": "Number of distinct items in each order"
        },
        {
            "target_table": "fact_sales",
            "target_column": "transaction_date",
            "source_tables": "pos_transactions",
            "source_columns": "transaction_timestamp",
            "transformation": "DATE(transaction_timestamp)",
            "business_logic": "Date when transaction occurred, extracted from timestamp"
        },
        {
            "target_table": "fact_sales",
            "target_column": "store_id",
            "source_tables": "pos_transactions",
            "source_columns": "store_id",
            "transformation": "Direct pass-through",
            "business_logic": "Identifies which ABC Restaurant location this sale occurred at"
        },
        {
            "target_table": "fact_sales",
            "target_column": "channel",
            "source_tables": "pos_transactions",
            "source_columns": "channel_code",
            "transformation": "CASE WHEN channel_code IN ('C', 'DT') THEN 'counter' ELSE 'delivery'",
            "business_logic": "Sales channel: counter (in-store) or delivery (online/app)"
        },

        # fact_inventory lineage
        {
            "target_table": "fact_inventory",
            "target_column": "waste_rate",
            "source_tables": "inventory_daily",
            "source_columns": "units_wasted, units_sold",
            "transformation": "CASE WHEN (units_sold + units_wasted) = 0 THEN 0 ELSE units_wasted / (units_sold + units_wasted) END",
            "business_logic": "Percentage of items wasted vs total items that moved (sold or wasted)"
        },
        {
            "target_table": "fact_inventory",
            "target_column": "inventory_value",
            "source_tables": "inventory_daily, raw_reference_menu_items",
            "source_columns": "quantity_on_hand, food_cost",
            "transformation": "quantity_on_hand * food_cost",
            "business_logic": "Monetary value of inventory at food cost"
        },
        {
            "target_table": "fact_inventory",
            "target_column": "turnover_rate",
            "source_tables": "inventory_daily",
            "source_columns": "units_sold, avg_inventory",
            "transformation": "units_sold / avg_inventory",
            "business_logic": "How many times inventory is sold and replaced during period"
        },
        {
            "target_table": "fact_inventory",
            "target_column": "units_sold",
            "source_tables": "inventory_daily",
            "source_columns": "units_sold",
            "transformation": "Direct pass-through",
            "business_logic": "Number of units sold during the day"
        },
        {
            "target_table": "fact_inventory",
            "target_column": "units_wasted",
            "source_tables": "inventory_daily",
            "source_columns": "units_wasted",
            "transformation": "Direct pass-through",
            "business_logic": "Number of units wasted (expired, damaged, overproduced)"
        },
        {
            "target_table": "fact_inventory",
            "target_column": "quantity_on_hand",
            "source_tables": "inventory_daily",
            "source_columns": "quantity_on_hand",
            "transformation": "Direct pass-through",
            "business_logic": "Units in stock at end of day"
        },
        {
            "target_table": "fact_inventory",
            "target_column": "avg_inventory",
            "source_tables": "inventory_daily",
            "source_columns": "quantity_on_hand",
            "transformation": "AVG(quantity_on_hand) over 30-day window",
            "business_logic": "Average stock level over past month"
        },
        {
            "target_table": "fact_inventory",
            "target_column": "inventory_date",
            "source_tables": "inventory_daily",
            "source_columns": "inventory_date",
            "transformation": "Direct pass-through",
            "business_logic": "Date of inventory count"
        },

        # fact_labor lineage
        {
            "target_table": "fact_labor",
            "target_column": "labor_cost",
            "source_tables": "labor_schedules",
            "source_columns": "actual_hours, hourly_rate, overtime_multiplier",
            "transformation": "(regular_hours * hourly_rate) + (overtime_hours * hourly_rate * overtime_multiplier)",
            "business_logic": "Total labor cost including overtime at 1.5x rate"
        },
        {
            "target_table": "fact_labor",
            "target_column": "actual_hours",
            "source_tables": "labor_schedules",
            "source_columns": "check_in_time, check_out_time",
            "transformation": "(check_out_time - check_in_time) / 60",
            "business_logic": "Hours employee actually worked (in minutes, converted to hours)"
        },
        {
            "target_table": "fact_labor",
            "target_column": "scheduled_hours",
            "source_tables": "labor_schedules",
            "source_columns": "scheduled_hours",
            "transformation": "Direct pass-through",
            "business_logic": "Hours employee was scheduled to work"
        },
        {
            "target_table": "fact_labor",
            "target_column": "overtime_hours",
            "source_tables": "labor_schedules",
            "source_columns": "actual_hours",
            "transformation": "CASE WHEN actual_hours > 8 THEN actual_hours - 8 ELSE 0 END",
            "business_logic": "Hours worked beyond 8-hour shift"
        },
        {
            "target_table": "fact_labor",
            "target_column": "labor_productivity",
            "source_tables": "labor_schedules, fact_sales",
            "source_columns": "actual_hours, item_count",
            "transformation": "item_count / actual_hours",
            "business_logic": "Number of items processed per labor hour"
        },
        {
            "target_table": "fact_labor",
            "target_column": "hourly_rate",
            "source_tables": "labor_schedules",
            "source_columns": "hourly_rate",
            "transformation": "Direct pass-through",
            "business_logic": "Employee's hourly wage rate"
        },
        {
            "target_table": "fact_labor",
            "target_column": "employee_id",
            "source_tables": "labor_schedules",
            "source_columns": "employee_id",
            "transformation": "Direct pass-through",
            "business_logic": "Unique employee identifier"
        },
        {
            "target_table": "fact_labor",
            "target_column": "shift_date",
            "source_tables": "labor_schedules",
            "source_columns": "shift_date",
            "transformation": "Direct pass-through",
            "business_logic": "Date of the shift"
        },

        # fact_service_performance lineage
        {
            "target_table": "fact_service_performance",
            "target_column": "avg_service_time",
            "source_tables": "service_times",
            "source_columns": "service_time",
            "transformation": "AVG(service_time) by hour, store, channel",
            "business_logic": "Average time from order to delivery per channel"
        },
        {
            "target_table": "fact_service_performance",
            "target_column": "p95_service_time",
            "source_tables": "service_times",
            "source_columns": "service_time",
            "transformation": "PERCENTILE_CONT(0.95) of service_time by hour",
            "business_logic": "95th percentile service time - most customers served within this time"
        },
        {
            "target_table": "fact_service_performance",
            "target_column": "orders_per_hour",
            "source_tables": "service_times",
            "source_columns": "order_id",
            "transformation": "COUNT(order_id) by hour, store, channel",
            "business_logic": "Number of orders processed in each hour"
        },
        {
            "target_table": "fact_service_performance",
            "target_column": "on_time_pct",
            "source_tables": "service_times",
            "source_columns": "service_time, sla_minutes",
            "transformation": "COUNT(CASE WHEN service_time <= sla_minutes THEN 1 END) / COUNT(*) * 100",
            "business_logic": "Percentage of orders meeting service level agreement"
        },
        {
            "target_table": "fact_service_performance",
            "target_column": "channel",
            "source_tables": "service_times",
            "source_columns": "channel_code",
            "transformation": "CASE WHEN channel_code = 'C' THEN 'counter' WHEN channel_code = 'DT' THEN 'drive_thru' ELSE 'delivery' END",
            "business_logic": "Service channel: counter, drive-through, or delivery"
        },

        # fact_customer_feedback lineage
        {
            "target_table": "fact_customer_feedback",
            "target_column": "sentiment_score",
            "source_tables": "feedback_surveys",
            "source_columns": "overall_satisfaction, cleanliness_rating, service_rating",
            "transformation": "(overall_satisfaction * 0.5 + cleanliness_rating * 0.25 + service_rating * 0.25) / 10",
            "business_logic": "Weighted average sentiment (0-1 scale) from satisfaction and quality ratings"
        },
        {
            "target_table": "fact_customer_feedback",
            "target_column": "nps_score",
            "source_tables": "feedback_surveys",
            "source_columns": "recommendation_rating",
            "transformation": "CASE WHEN recommendation_rating >= 9 THEN 'promoter' WHEN recommendation_rating >= 7 THEN 'passive' ELSE 'detractor' END",
            "business_logic": "Net Promoter Score segment based on recommendation likelihood"
        },
        {
            "target_table": "fact_customer_feedback",
            "target_column": "issue_category",
            "source_tables": "feedback_surveys",
            "source_columns": "feedback_text",
            "transformation": "ML classification (food quality, wait time, staff, cleanliness, other)",
            "business_logic": "Categorization of customer issues mentioned in survey"
        },
        {
            "target_table": "fact_customer_feedback",
            "target_column": "store_id",
            "source_tables": "feedback_surveys",
            "source_columns": "store_id",
            "transformation": "Direct pass-through",
            "business_logic": "Identifies which store the feedback is about"
        },
        {
            "target_table": "fact_customer_feedback",
            "target_column": "feedback_date",
            "source_tables": "feedback_surveys",
            "source_columns": "feedback_date",
            "transformation": "Direct pass-through",
            "business_logic": "Date feedback was submitted"
        },

        # fact_loyalty lineage
        {
            "target_table": "fact_loyalty",
            "target_column": "points_earned",
            "source_tables": "loyalty_transactions",
            "source_columns": "transaction_amount, earning_rate",
            "transformation": "transaction_amount * earning_rate / 100",
            "business_logic": "Loyalty points earned from purchase (e.g., 1 point per HKD spent)"
        },
        {
            "target_table": "fact_loyalty",
            "target_column": "points_redeemed",
            "source_tables": "loyalty_transactions",
            "source_columns": "points_redeemed",
            "transformation": "Direct pass-through",
            "business_logic": "Loyalty points used in redemption transactions"
        },
        {
            "target_table": "fact_loyalty",
            "target_column": "loyalty_tier",
            "source_tables": "loyalty_transactions, customer_profiles",
            "source_columns": "loyalty_lifetime_value",
            "transformation": "CASE WHEN lifetime_value >= 5000 THEN 'gold' WHEN lifetime_value >= 2000 THEN 'silver' ELSE 'bronze' END",
            "business_logic": "Customer tier based on lifetime spending (bronze/silver/gold)"
        },
        {
            "target_table": "fact_loyalty",
            "target_column": "remaining_points",
            "source_tables": "loyalty_transactions",
            "source_columns": "points_earned, points_redeemed",
            "transformation": "LAG(remaining_points) + points_earned - points_redeemed",
            "business_logic": "Running balance of available loyalty points"
        },
        {
            "target_table": "fact_loyalty",
            "target_column": "transaction_date",
            "source_tables": "loyalty_transactions",
            "source_columns": "transaction_date",
            "transformation": "Direct pass-through",
            "business_logic": "Date of earn or redemption transaction"
        },

        # fact_equipment lineage
        {
            "target_table": "fact_equipment",
            "target_column": "downtime_hours",
            "source_tables": "equipment_logs",
            "source_columns": "failure_time, repair_completion_time",
            "transformation": "(repair_completion_time - failure_time) / 60",
            "business_logic": "Total hours equipment was offline due to malfunction"
        },
        {
            "target_table": "fact_equipment",
            "target_column": "maintenance_cost",
            "source_tables": "equipment_logs",
            "source_columns": "repair_hours, labor_rate, parts_cost",
            "transformation": "(repair_hours * labor_rate) + parts_cost",
            "business_logic": "Total cost of maintenance including labor and parts"
        },
        {
            "target_table": "fact_equipment",
            "target_column": "equipment_age_days",
            "source_tables": "equipment_logs, raw_reference_equipment",
            "source_columns": "current_date, install_date",
            "transformation": "current_date - install_date",
            "business_logic": "Days since equipment was installed"
        },
        {
            "target_table": "fact_equipment",
            "target_column": "mtbf_days",
            "source_tables": "equipment_logs",
            "source_columns": "failure_dates",
            "transformation": "AVG(days_between_failures)",
            "business_logic": "Mean time between failures - average days equipment runs"
        },
        {
            "target_table": "fact_equipment",
            "target_column": "equipment_type",
            "source_tables": "equipment_logs",
            "source_columns": "equipment_type",
            "transformation": "Direct pass-through",
            "business_logic": "Type of equipment (fryer, grill, register, etc.)"
        },

        # fact_financial lineage
        {
            "target_table": "fact_financial",
            "target_column": "net_margin_pct",
            "source_tables": "store_pnl",
            "source_columns": "net_profit, revenue",
            "transformation": "(net_profit / revenue) * 100",
            "business_logic": "Percentage of revenue remaining as profit after ALL costs"
        },
        {
            "target_table": "fact_financial",
            "target_column": "gross_profit",
            "source_tables": "store_pnl",
            "source_columns": "revenue, cogs",
            "transformation": "revenue - cogs",
            "business_logic": "Revenue minus food cost (first level of profitability)"
        },
        {
            "target_table": "fact_financial",
            "target_column": "ebitda",
            "source_tables": "store_pnl",
            "source_columns": "revenue, cogs, labor, rent, utilities, marketing",
            "transformation": "revenue - cogs - labor - rent - utilities - marketing",
            "business_logic": "Earnings before interest, tax, depreciation, amortization"
        },
        {
            "target_table": "fact_financial",
            "target_column": "labor_pct",
            "source_tables": "store_pnl",
            "source_columns": "labor_cost, revenue",
            "transformation": "(labor_cost / revenue) * 100",
            "business_logic": "Labor as percentage of revenue (target: 25-30%)"
        },
        {
            "target_table": "fact_financial",
            "target_column": "rent_pct",
            "source_tables": "store_pnl",
            "source_columns": "rent_cost, revenue",
            "transformation": "(rent_cost / revenue) * 100",
            "business_logic": "Rent as percentage of revenue (varies by location)"
        },
        {
            "target_table": "fact_financial",
            "target_column": "cogs_pct",
            "source_tables": "store_pnl",
            "source_columns": "cogs, revenue",
            "transformation": "(cogs / revenue) * 100",
            "business_logic": "Food cost as percentage of revenue (target: 28-32%)"
        },
        {
            "target_table": "fact_financial",
            "target_column": "net_profit",
            "source_tables": "store_pnl",
            "source_columns": "revenue, cogs, labor, rent, utilities, marketing, other_expenses",
            "transformation": "revenue - (cogs + labor + rent + utilities + marketing + other_expenses)",
            "business_logic": "Bottom line profit after all operating costs"
        },
        {
            "target_table": "fact_financial",
            "target_column": "revenue",
            "source_tables": "store_pnl",
            "source_columns": "revenue",
            "transformation": "Direct pass-through",
            "business_logic": "Total sales revenue for the month"
        },
        {
            "target_table": "fact_financial",
            "target_column": "financial_month",
            "source_tables": "store_pnl",
            "source_columns": "report_month",
            "transformation": "Direct pass-through",
            "business_logic": "Month and year for this financial report"
        },

        # dim_date lineage
        {
            "target_table": "dim_date",
            "target_column": "is_hk_holiday",
            "source_tables": "programmatic",
            "source_columns": "date",
            "transformation": "Hardcoded Hong Kong public holidays for 2023 (New Year, Chinese New Year, Easter, Ching Ming, Labour Day, Dragon Boat, Mid-Autumn, National Day, Chung Yeung)",
            "business_logic": "Flag indicating if date is a Hong Kong public holiday"
        },
        {
            "target_table": "dim_date",
            "target_column": "day_of_week",
            "source_tables": "programmatic",
            "source_columns": "date",
            "transformation": "DAYOFWEEK(date) (1=Sunday, 7=Saturday)",
            "business_logic": "Day of week name for the date"
        },
        {
            "target_table": "dim_date",
            "target_column": "quarter",
            "source_tables": "programmatic",
            "source_columns": "date",
            "transformation": "QUARTER(date)",
            "business_logic": "Financial quarter (Q1-Q4)"
        },

        # dim_store lineage
        {
            "target_table": "dim_store",
            "target_column": "store_type",
            "source_tables": "raw_reference_stores",
            "source_columns": "store_type_code",
            "transformation": "CASE WHEN store_type_code = 'M' THEN 'mall' WHEN store_type_code = 'S' THEN 'street' ELSE 'drive_thru' END",
            "business_logic": "Physical format: mall (inside shopping center), street (standalone), or drive-through"
        },
        {
            "target_table": "dim_store",
            "target_column": "district",
            "source_tables": "raw_reference_stores",
            "source_columns": "district_code",
            "transformation": "Lookup from district master (HK districts)",
            "business_logic": "Hong Kong district where store is located"
        },
        {
            "target_table": "dim_store",
            "target_column": "region",
            "source_tables": "raw_reference_stores",
            "source_columns": "district_code",
            "transformation": "CASE classification by district: Kowloon, HK Island, New Territories",
            "business_logic": "Major geographic region for reporting"
        },

        # dim_menu_item lineage
        {
            "target_table": "dim_menu_item",
            "target_column": "food_cost_pct",
            "source_tables": "raw_reference_menu_items, raw_reference_categories",
            "source_columns": "food_cost, selling_price",
            "transformation": "(food_cost / selling_price) * 100",
            "business_logic": "Food cost as percentage of selling price (target: 30-35%)"
        },
        {
            "target_table": "dim_menu_item",
            "target_column": "category",
            "source_tables": "raw_reference_categories",
            "source_columns": "category_id",
            "transformation": "Direct join from categories table",
            "business_logic": "Product category (Burgers, Chicken, Breakfast, Beverages, Sides, Desserts)"
        },

        # dim_customer lineage
        {
            "target_table": "dim_customer",
            "target_column": "loyalty_tier",
            "source_tables": "raw_customer_customer_profiles",
            "source_columns": "lifetime_spend",
            "transformation": "CASE WHEN lifetime_spend >= 5000 THEN 'gold' WHEN lifetime_spend >= 2000 THEN 'silver' ELSE 'bronze' END",
            "business_logic": "Customer tier based on total lifetime spending"
        },
        {
            "target_table": "dim_customer",
            "target_column": "acquisition_channel",
            "source_tables": "raw_customer_customer_profiles",
            "source_columns": "first_purchase_channel",
            "transformation": "Direct pass-through",
            "business_logic": "How customer first engaged (app, in-store, delivery partner)"
        },
    ]

    lineage_df = spark.createDataFrame(column_lineage)
    logger.info(f"Created {len(column_lineage)} column lineage records")

    # ==========================================
    # 3. DATA DICTIONARY TABLE
    # ==========================================
    logger.info("Creating data_dictionary data")

    data_dictionary = [
        # fact_sales table
        {
            "table_name": "fact_sales",
            "column_name": "gross_profit",
            "data_type": "DECIMAL(15,2)",
            "definition": "Revenue minus food cost (COGS) and promotional discounts for each menu item sold. This is the primary profitability metric before overhead costs.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_sales",
            "column_name": "net_profit",
            "data_type": "DECIMAL(15,2)",
            "definition": "Gross profit after allocating store-level overhead costs. Represents true profitability at item level.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_sales",
            "column_name": "line_total",
            "data_type": "DECIMAL(15,2)",
            "definition": "Total price charged for this menu item line (unit_price × quantity), before any promotional discounts are applied.",
            "business_unit": "Sales",
            "pii": False
        },
        {
            "table_name": "fact_sales",
            "column_name": "discount_amount",
            "data_type": "DECIMAL(15,2)",
            "definition": "Promotional discount allocated to this item line. Transaction-level discounts are split proportionally across all items in the order.",
            "business_unit": "Marketing",
            "pii": False
        },
        {
            "table_name": "fact_sales",
            "column_name": "cogs_amount",
            "data_type": "DECIMAL(15,2)",
            "definition": "Cost of Goods Sold - the food cost to prepare this item. Used to calculate gross profit and profit margins.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_sales",
            "column_name": "margin_pct",
            "data_type": "DECIMAL(5,2)",
            "definition": "Gross profit margin as percentage of line total. Shows profitability before overhead. Target varies by menu category.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_sales",
            "column_name": "item_count",
            "data_type": "INTEGER",
            "definition": "Number of distinct menu items ordered in this transaction. Used for basket analysis and labor productivity calculations.",
            "business_unit": "Sales",
            "pii": False
        },
        {
            "table_name": "fact_sales",
            "column_name": "transaction_date",
            "data_type": "DATE",
            "definition": "Date when the transaction occurred. Used for daily sales trends and comparisons.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_sales",
            "column_name": "store_id",
            "data_type": "VARCHAR(10)",
            "definition": "Unique identifier for the ABC Restaurant store location where this sale occurred.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_sales",
            "column_name": "channel",
            "data_type": "VARCHAR(20)",
            "definition": "Sales channel for the transaction. Counter (in-store), Drive-Through, or Delivery (third-party or app).",
            "business_unit": "Sales",
            "pii": False
        },

        # fact_inventory table
        {
            "table_name": "fact_inventory",
            "column_name": "waste_rate",
            "data_type": "DECIMAL(5,4)",
            "definition": "Percentage of inventory that was wasted (expired, damaged, overproduced) vs total items that moved. Lower is better. Target below 3%.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_inventory",
            "column_name": "inventory_value",
            "data_type": "DECIMAL(15,2)",
            "definition": "Monetary value of inventory on hand at food cost. High values indicate overstocking; low values indicate risk of stockouts.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_inventory",
            "column_name": "turnover_rate",
            "data_type": "DECIMAL(8,2)",
            "definition": "How many times inventory is completely sold and replaced during the measurement period. Higher is better (indicates freshness).",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_inventory",
            "column_name": "units_sold",
            "data_type": "INTEGER",
            "definition": "Number of units sold during this day. Used to calculate waste rate and inventory turnover.",
            "business_unit": "Sales",
            "pii": False
        },
        {
            "table_name": "fact_inventory",
            "column_name": "units_wasted",
            "data_type": "INTEGER",
            "definition": "Number of units wasted during the day (expired, damaged, or destroyed). Higher waste indicates forecast accuracy issues.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_inventory",
            "column_name": "quantity_on_hand",
            "data_type": "INTEGER",
            "definition": "Number of units in stock at end of day. Used to calculate turnover and identify overstocking situations.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_inventory",
            "column_name": "avg_inventory",
            "data_type": "DECIMAL(10,2)",
            "definition": "Average inventory level over the past 30 days. Used for trend analysis and demand forecasting.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_inventory",
            "column_name": "inventory_date",
            "data_type": "DATE",
            "definition": "Date of the inventory count. Used to track inventory trends over time.",
            "business_unit": "Operations",
            "pii": False
        },

        # fact_labor table
        {
            "table_name": "fact_labor",
            "column_name": "labor_cost",
            "data_type": "DECIMAL(15,2)",
            "definition": "Total labor cost for this shift including overtime at time-and-a-half. Labor is typically 25-30% of revenue.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_labor",
            "column_name": "actual_hours",
            "data_type": "DECIMAL(8,2)",
            "definition": "Hours employee actually worked (clock in to clock out). May differ from scheduled hours due to breaks or early clock-out.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_labor",
            "column_name": "scheduled_hours",
            "data_type": "DECIMAL(8,2)",
            "definition": "Hours employee was scheduled to work. Difference from actual hours indicates scheduling accuracy.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_labor",
            "column_name": "overtime_hours",
            "data_type": "DECIMAL(8,2)",
            "definition": "Hours worked beyond 8-hour shift, compensated at 1.5x rate. High overtime indicates understaffing.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_labor",
            "column_name": "labor_productivity",
            "data_type": "DECIMAL(10,2)",
            "definition": "Number of menu items processed per labor hour. Used to identify underperforming staff or need for training.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_labor",
            "column_name": "hourly_rate",
            "data_type": "DECIMAL(8,2)",
            "definition": "Employee hourly wage rate (includes base salary + any special allowances). Used for labor cost calculations.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_labor",
            "column_name": "employee_id",
            "data_type": "VARCHAR(20)",
            "definition": "Unique identifier for the employee. Used to track labor costs by individual.",
            "business_unit": "HR",
            "pii": True
        },
        {
            "table_name": "fact_labor",
            "column_name": "shift_date",
            "data_type": "DATE",
            "definition": "Date of the shift. Used to analyze labor costs and productivity by day of week.",
            "business_unit": "Operations",
            "pii": False
        },

        # fact_service_performance table
        {
            "table_name": "fact_service_performance",
            "column_name": "avg_service_time",
            "data_type": "DECIMAL(8,2)",
            "definition": "Average time in seconds from order placement to delivery/pickup. Lower is better. Target varies by channel (counter/drive-thru/delivery).",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_service_performance",
            "column_name": "p95_service_time",
            "data_type": "DECIMAL(8,2)",
            "definition": "95th percentile service time - 95% of customers are served within this time. Key SLA metric.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_service_performance",
            "column_name": "orders_per_hour",
            "data_type": "INTEGER",
            "definition": "Number of orders processed per hour. Indicates store traffic and throughput.",
            "business_unit": "Sales",
            "pii": False
        },
        {
            "table_name": "fact_service_performance",
            "column_name": "on_time_pct",
            "data_type": "DECIMAL(5,2)",
            "definition": "Percentage of orders delivered within Service Level Agreement time. Target is 95%+.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_service_performance",
            "column_name": "channel",
            "data_type": "VARCHAR(20)",
            "definition": "Service channel (counter, drive-through, delivery). Each channel has different service time targets.",
            "business_unit": "Sales",
            "pii": False
        },

        # fact_customer_feedback table
        {
            "table_name": "fact_customer_feedback",
            "column_name": "sentiment_score",
            "data_type": "DECIMAL(3,2)",
            "definition": "Weighted customer sentiment score from 0 (very negative) to 1 (very positive). Based on satisfaction, cleanliness, and service ratings.",
            "business_unit": "Marketing",
            "pii": False
        },
        {
            "table_name": "fact_customer_feedback",
            "column_name": "nps_score",
            "data_type": "VARCHAR(20)",
            "definition": "Net Promoter Score segment: Promoter (would recommend), Passive (neutral), or Detractor (might discourage others).",
            "business_unit": "Marketing",
            "pii": False
        },
        {
            "table_name": "fact_customer_feedback",
            "column_name": "issue_category",
            "data_type": "VARCHAR(50)",
            "definition": "Category of customer issue mentioned: Food Quality, Wait Time, Staff Attitude, Cleanliness, or Other.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_customer_feedback",
            "column_name": "store_id",
            "data_type": "VARCHAR(10)",
            "definition": "Store location for this feedback. Used to identify stores with service issues.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_customer_feedback",
            "column_name": "feedback_date",
            "data_type": "DATE",
            "definition": "Date feedback was submitted. Used to track sentiment trends over time.",
            "business_unit": "Marketing",
            "pii": False
        },

        # fact_loyalty table
        {
            "table_name": "fact_loyalty",
            "column_name": "points_earned",
            "data_type": "DECIMAL(10,2)",
            "definition": "Loyalty points earned from this purchase (typically 1 point per HKD spent). Used to calculate customer lifetime value.",
            "business_unit": "Marketing",
            "pii": False
        },
        {
            "table_name": "fact_loyalty",
            "column_name": "points_redeemed",
            "data_type": "DECIMAL(10,2)",
            "definition": "Loyalty points used in this redemption transaction. Used to calculate program ROI.",
            "business_unit": "Marketing",
            "pii": False
        },
        {
            "table_name": "fact_loyalty",
            "column_name": "loyalty_tier",
            "data_type": "VARCHAR(20)",
            "definition": "Customer loyalty tier (Bronze/Silver/Gold) based on lifetime spending. Gold customers receive special benefits.",
            "business_unit": "Marketing",
            "pii": False
        },
        {
            "table_name": "fact_loyalty",
            "column_name": "remaining_points",
            "data_type": "DECIMAL(10,2)",
            "definition": "Current balance of available loyalty points. Used to identify inactive accounts and customer engagement.",
            "business_unit": "Marketing",
            "pii": False
        },
        {
            "table_name": "fact_loyalty",
            "column_name": "transaction_date",
            "data_type": "DATE",
            "definition": "Date of the earn or redemption transaction. Used to analyze loyalty program trends.",
            "business_unit": "Marketing",
            "pii": False
        },

        # fact_equipment table
        {
            "table_name": "fact_equipment",
            "column_name": "downtime_hours",
            "data_type": "DECIMAL(10,2)",
            "definition": "Total hours equipment was offline due to failure or maintenance. Downtime directly impacts sales and customer satisfaction.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_equipment",
            "column_name": "maintenance_cost",
            "data_type": "DECIMAL(15,2)",
            "definition": "Total cost of maintenance including labor and parts. Used to track equipment lifecycle costs and replacement decisions.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_equipment",
            "column_name": "equipment_age_days",
            "data_type": "INTEGER",
            "definition": "Days since equipment was installed. Used to predict maintenance needs and depreciation.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_equipment",
            "column_name": "mtbf_days",
            "data_type": "DECIMAL(10,2)",
            "definition": "Mean Time Between Failures - average days equipment runs without breaking. Higher is better (more reliable).",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "fact_equipment",
            "column_name": "equipment_type",
            "data_type": "VARCHAR(50)",
            "definition": "Type of equipment (fryer, grill, ice cream machine, POS register, etc.). Used for maintenance scheduling by type.",
            "business_unit": "Operations",
            "pii": False
        },

        # fact_financial table
        {
            "table_name": "fact_financial",
            "column_name": "net_margin_pct",
            "data_type": "DECIMAL(5,2)",
            "definition": "Percentage of revenue remaining as profit after ALL costs including food, labor, rent, utilities, and marketing. Target is 8-15% for healthy stores.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_financial",
            "column_name": "gross_profit",
            "data_type": "DECIMAL(15,2)",
            "definition": "Revenue minus food cost (COGS). The first level of profitability before fixed overhead costs.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_financial",
            "column_name": "ebitda",
            "data_type": "DECIMAL(15,2)",
            "definition": "Earnings Before Interest, Tax, Depreciation and Amortization. Key metric for comparing store profitability independent of capital structure and financing.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_financial",
            "column_name": "labor_pct",
            "data_type": "DECIMAL(5,2)",
            "definition": "Labor cost as percentage of revenue. Benchmark target is 25-30%. Higher percentages indicate overstaffing or inefficiency.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_financial",
            "column_name": "rent_pct",
            "data_type": "DECIMAL(5,2)",
            "definition": "Rent cost as percentage of revenue. Varies significantly by location (mall vs street locations). Used for location profitability analysis.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_financial",
            "column_name": "cogs_pct",
            "data_type": "DECIMAL(5,2)",
            "definition": "Food cost (COGS) as percentage of revenue. Benchmark target is 28-32%. Higher percentages indicate food waste or unfavorable mix.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_financial",
            "column_name": "net_profit",
            "data_type": "DECIMAL(15,2)",
            "definition": "Bottom line profit after all operating costs. Represents true store profitability available for debt service and owner return.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_financial",
            "column_name": "revenue",
            "data_type": "DECIMAL(15,2)",
            "definition": "Total sales revenue for the month from all channels (counter, drive-thru, delivery, catering).",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "fact_financial",
            "column_name": "financial_month",
            "data_type": "VARCHAR(7)",
            "definition": "Month and year for this financial report (YYYY-MM format). Used for monthly and quarterly trend analysis.",
            "business_unit": "Finance",
            "pii": False
        },

        # dim_date table
        {
            "table_name": "dim_date",
            "column_name": "is_hk_holiday",
            "data_type": "BOOLEAN",
            "definition": "Flag indicating if this date is a Hong Kong public holiday. Used to analyze holiday sales uplift or dips.",
            "business_unit": "Sales",
            "pii": False
        },
        {
            "table_name": "dim_date",
            "column_name": "day_of_week",
            "data_type": "VARCHAR(10)",
            "definition": "Day of week (Monday-Sunday). Used to analyze day-of-week sales patterns and staffing needs.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "dim_date",
            "column_name": "quarter",
            "data_type": "VARCHAR(2)",
            "definition": "Financial quarter (Q1-Q4). Used for quarterly business reviews and year-end reporting.",
            "business_unit": "Finance",
            "pii": False
        },

        # dim_store table
        {
            "table_name": "dim_store",
            "column_name": "store_type",
            "data_type": "VARCHAR(20)",
            "definition": "Physical format of the store: 'mall' (inside shopping center), 'street' (standalone street-level), or 'drive_thru' (with drive-through lane). Store type affects revenue potential and operating costs.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "dim_store",
            "column_name": "district",
            "data_type": "VARCHAR(50)",
            "definition": "Hong Kong district where store is located (18 districts total). Used for geographic analysis and localized promotions.",
            "business_unit": "Operations",
            "pii": False
        },
        {
            "table_name": "dim_store",
            "column_name": "region",
            "data_type": "VARCHAR(20)",
            "definition": "Major geographic region: Hong Kong Island, Kowloon, or New Territories. Used for regional management and comparisons.",
            "business_unit": "Operations",
            "pii": False
        },

        # dim_menu_item table
        {
            "table_name": "dim_menu_item",
            "column_name": "food_cost_pct",
            "data_type": "DECIMAL(5,2)",
            "definition": "Food cost as percentage of selling price. Lower percentages indicate higher profit margins. Benchmark target is 30-35%.",
            "business_unit": "Finance",
            "pii": False
        },
        {
            "table_name": "dim_menu_item",
            "column_name": "category",
            "data_type": "VARCHAR(50)",
            "definition": "Product category for menu mix analysis: Burgers, Chicken, Breakfast, Beverages, Sides, or Desserts. Used for sales and profitability by category.",
            "business_unit": "Sales",
            "pii": False
        },

        # dim_customer table
        {
            "table_name": "dim_customer",
            "column_name": "loyalty_tier",
            "data_type": "VARCHAR(20)",
            "definition": "Customer tier based on lifetime spending: Bronze (under HKD 2000), Silver (HKD 2000-5000), Gold (over HKD 5000). Gold customers typically drive 30-40% of revenue.",
            "business_unit": "Marketing",
            "pii": False
        },
        {
            "table_name": "dim_customer",
            "column_name": "acquisition_channel",
            "data_type": "VARCHAR(50)",
            "definition": "How customer first engaged with ABC Restaurant: Mobile App, In-Store, Third-Party Delivery, or Other. Used to analyze channel effectiveness.",
            "business_unit": "Marketing",
            "pii": False
        },
    ]

    dictionary_df = spark.createDataFrame(data_dictionary)
    logger.info(f"Created {len(data_dictionary)} data dictionary records")

    # ==========================================
    # Write to Redshift
    # ==========================================

    def write_to_redshift(df, table_name, mode="overwrite"):
        """Write DataFrame to Redshift table"""
        connection_options = {
            "url": f"jdbc:redshift://{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}",
            "user": REDSHIFT_USER,
            "password": REDSHIFT_PASSWORD,
            "dbtable": f"{REDSHIFT_SCHEMA}.{table_name}",
            "tempdir": S3_TEMP_DIR,
        }

        logger.info(f"Writing {len(df.collect())} records to {table_name}")
        df.write \
            .format("com.databricks.spark.redshift") \
            .mode(mode) \
            .option("url", connection_options["url"]) \
            .option("user", connection_options["user"]) \
            .option("password", connection_options["password"]) \
            .option("dbtable", connection_options["dbtable"]) \
            .option("tempdir", connection_options["tempdir"]) \
            .save()

        logger.info(f"Successfully wrote {table_name}")

    # Write all tables to Redshift
    try:
        write_to_redshift(jobs_df, "etl_job_registry", mode="overwrite")
        write_to_redshift(lineage_df, "etl_column_lineage", mode="overwrite")
        write_to_redshift(dictionary_df, "data_dictionary", mode="overwrite")

        logger.info("All metadata tables successfully loaded to Redshift")
    except Exception as e:
        logger.error(f"Error writing to Redshift: {str(e)}")
        raise

    # ==========================================
    # Summary Statistics
    # ==========================================
    logger.info("=" * 60)
    logger.info("METADATA LOAD SUMMARY")
    logger.info("=" * 60)
    logger.info(f"ETL Job Registry: {len(etl_jobs)} jobs registered")
    logger.info(f"Column Lineage: {len(column_lineage)} transformations documented")
    logger.info(f"Data Dictionary: {len(data_dictionary)} table/column definitions")
    logger.info(f"Total Metadata Records: {len(etl_jobs) + len(column_lineage) + len(data_dictionary)}")
    logger.info("=" * 60)
    logger.info("Metadata loaded successfully for GenBI Chatbot!")
    logger.info("=" * 60)

except Exception as e:
    logger.error(f"Fatal error in metadata load job: {str(e)}", exc_info=True)
    raise

finally:
    job.commit()
