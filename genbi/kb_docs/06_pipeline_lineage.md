# End-to-End Data Pipeline Lineage

This document traces every metric from its source system, through the raw data landing zone, AWS Glue ETL transformation, Redshift data mart, and finally to the BI dashboard aggregation layer.

## Pipeline Architecture

Source Systems (POS terminals, HR/workforce, CRM/loyalty, Finance/ERP, Ops/inventory) →

S3 Raw Landing Zone (s3://genbi-mcdhk-raw-530977327410/) — CSV files organized by domain (pos/, operations/, customer/, financial/, reference/) →

AWS Glue PySpark ETL Jobs (3 jobs: load_dimensions, load_facts, load_metadata) — JOINs, type casting, calculated fields, data quality →

Amazon Redshift Serverless (dev.genbi_mart — star schema: 7 dim + 8 fact tables) →

BI Layer (QuickSight dashboards / GenBI SQL queries) — Aggregations: SUM, COUNT DISTINCT, AVG, GROUP BY

---

## 1. FACT_SALES — Sales Transaction Data

### Source System
POS (Point of Sale) terminals across 200 stores. Each transaction generates two records: a transaction header and one or more line items.

### S3 Raw Landing
- **Transactions**: `s3://genbi-mcdhk-raw-530977327410/pos/transactions/` — monthly CSV partitions (pos_transactions_YYYY_MM.csv)
  - Columns: transaction_id, store_id, order_date, order_hour, channel_id, payment_method_id, customer_id, promo_id, discount_amount, order_item_count
- **Line Items**: `s3://genbi-mcdhk-raw-530977327410/pos/line_items/` — monthly CSV partitions (pos_line_items_YYYY_MM.csv)
  - Columns: transaction_id, item_id, quantity, unit_price, line_total, cogs

### Glue ETL (load_facts.py → load_fact_sales)
1. **Read** both CSVs from S3 with schema inference
2. **JOIN** transactions + line_items ON transaction_id (INNER JOIN)
3. **Transform**:
   - `date_key` = FORMAT(order_date, 'yyyyMMdd') cast to INT (e.g., 2023-03-15 → 20230315)
   - `discount_amount` = COALESCE(discount, 0.0) — null-safe
   - `cogs_amount` = COALESCE(cogs, 0.0) — null-safe
   - `gross_profit` = line_total - discount_per_item - cogs_amount
4. **Write** to Redshift `genbi_mart.fact_sales` via COPY (repartitioned by date_key, 32 partitions)

### Redshift Data Mart (genbi_mart.fact_sales — 17.5M rows)
- Primary key: sale_key (auto-generated)
- Grain: one row per line item per transaction
- Key columns: transaction_id, date_key, store_id, item_id, customer_id, channel_id, payment_id, promo_id, order_hour, quantity, unit_price, line_total, discount_amount, cogs_amount, gross_profit

### BI Dashboard Aggregation
- **Total Revenue**: `SUM(line_total)` from fact_sales
- **Total Orders**: `COUNT(DISTINCT transaction_id)` — CRITICAL: each transaction has multiple line items, so must use DISTINCT
- **Gross Profit**: `SUM(gross_profit)` = SUM(line_total - cogs_amount - discount_amount)
- **Avg Order Value**: `SUM(line_total) / COUNT(DISTINCT transaction_id)`
- **Revenue by Region**: GROUP BY dim_store.region after JOIN on store_id
- **Revenue by Category**: GROUP BY dim_menu_item.category_name after JOIN on item_id
- **Revenue by Hour**: GROUP BY order_hour
- **Monthly Trend**: GROUP BY dim_date.month after JOIN on date_key

---

## 2. FACT_INVENTORY — Daily Inventory Snapshots

### Source System
Inventory management system. Daily end-of-business snapshots per store per menu item.

### S3 Raw Landing
- `s3://genbi-mcdhk-raw-530977327410/operations/inventory_daily/` — inventory_daily.csv
  - Columns: date, store_id, product_id, units_on_hand, units_sold, units_wasted, opening_stock, units_received, closing_stock, waste_reason

### Glue ETL (load_facts.py → load_fact_inventory)
1. **Read** CSV from S3
2. **Transform**:
   - `date_key` = FORMAT(date, 'yyyyMMdd') cast to INT
   - `waste_rate` = CASE WHEN (units_sold + units_wasted) > 0 THEN units_wasted / (units_sold + units_wasted) ELSE 0 END
3. **Write** to Redshift `genbi_mart.fact_inventory`

### Redshift Data Mart (genbi_mart.fact_inventory — 2.19M rows)
- Grain: one row per store per item per day
- Key columns: date_key, store_id, item_id, opening_stock, units_received, units_sold, units_wasted, closing_stock, waste_reason, waste_rate

### BI Dashboard Aggregation
- **Avg Waste Rate**: `AVG(waste_rate)` or `SUM(units_wasted) / SUM(units_sold + units_wasted)`
- **Waste by Category**: GROUP BY dim_menu_item.category_name after JOIN on item_id
- **Inventory Value**: SUM(closing_stock * dim_menu_item.cogs) after JOIN on item_id

---

## 3. FACT_LABOR — Employee Shift Records

### Source System
HR / workforce management system. Records employee clock-in/clock-out per shift.

### S3 Raw Landing
- `s3://genbi-mcdhk-raw-530977327410/operations/labor_schedules/` — labor_schedules.csv
  - Columns: date, store_id, employee_id, shift_start_hour, shift_end_hour, hours_scheduled, hours_worked, role, hourly_rate, orders_handled

### Glue ETL (load_facts.py → load_fact_labor)
1. **Read** CSV from S3
2. **Transform**:
   - `date_key` = FORMAT(date, 'yyyyMMdd') cast to INT
   - `shift_start` = shift_start_hour (rename)
   - `shift_end` = shift_end_hour (rename)
   - `scheduled_hours` = hours_scheduled (rename)
   - `worked_hours` = hours_worked (rename)
3. **Write** to Redshift `genbi_mart.fact_labor`

### Redshift Data Mart (genbi_mart.fact_labor — 665K rows)
- Grain: one row per employee per shift
- Key columns: date_key, store_id, employee_id, role, shift_start, shift_end, scheduled_hours, actual_hours, hourly_rate, labor_cost, orders_handled
- Derived: labor_cost = actual_hours * hourly_rate

### BI Dashboard Aggregation
- **Total Labor Cost**: `SUM(labor_cost)` from fact_labor
- **Labor Cost per Order**: `SUM(labor_cost) / SUM(orders_handled)`
- **Avg Hours/Shift**: `AVG(actual_hours)`
- **By Region**: GROUP BY dim_store.region after JOIN on store_id
- **By Role**: GROUP BY role
- **Monthly Trend**: GROUP BY dim_date.month after JOIN on date_key

---

## 4. FACT_SERVICE_PERFORMANCE — Hourly Service Metrics

### Source System
Store operations system. Tracks average service times per hour per store.

### S3 Raw Landing
- `s3://genbi-mcdhk-raw-530977327410/operations/service_times/` — service_times.csv
  - Columns: date, store_id, hour, avg_counter_wait_secs, avg_kiosk_secs, avg_drive_thru_wait_secs, avg_delivery_secs, orders_served, peak_hour_wait_secs, staff_on_duty

### Glue ETL (load_facts.py → load_fact_service_performance)
1. **Read** CSV from S3
2. **Transform**:
   - `date_key` = FORMAT(date, 'yyyyMMdd') cast to INT
   - `avg_counter_secs` = avg_counter_wait_secs (rename)
   - `avg_drivethrough_secs` = avg_drive_thru_wait_secs (rename)
   - `avg_prep_secs` = avg_order_prep_secs (rename)
   - `peak_wait_secs` = peak_hour_wait_secs (rename)
3. **Write** to Redshift `genbi_mart.fact_service_performance`

### Redshift Data Mart (genbi_mart.fact_service_performance — 1.75M rows)
- Grain: one row per store per hour per day
- Key columns: date_key, store_id, hour, avg_counter_secs, avg_kiosk_secs, avg_drive_thru_secs, avg_delivery_secs, orders_served, peak_wait_secs, staff_on_duty

### BI Dashboard Aggregation
- **Avg Wait Time**: `AVG(avg_counter_secs)` or by channel
- **Peak Wait**: `AVG(peak_wait_secs)` or MAX
- **By Store/Region**: GROUP BY dim_store.region or store_name

---

## 5. FACT_CUSTOMER_FEEDBACK — Customer Satisfaction Surveys

### Source System
Customer feedback app / survey system. Submitted post-visit.

### S3 Raw Landing
- `s3://genbi-mcdhk-raw-530977327410/customer/feedback_surveys/` — feedback CSV files
  - Columns: survey_date, store_id, customer_id, satisfaction_score, food_quality_score, service_score, cleanliness_score, recommendation, feedback_comment

### Glue ETL (load_facts.py → load_fact_customer_feedback)
1. **Read** CSV from S3
2. **Transform**:
   - `date_key` = FORMAT(survey_date, 'yyyyMMdd') cast to INT
   - `would_recommend` = CASE WHEN recommendation = 'yes' THEN TRUE WHEN 'no' THEN FALSE ELSE NULL
   - Column renames: satisfaction_score → satisfaction, food_quality_score → food_quality, service_score → service, cleanliness_score → cleanliness, feedback_comment → comments
3. **Write** to Redshift `genbi_mart.fact_customer_feedback`

### Redshift Data Mart (genbi_mart.fact_customer_feedback — 28K rows)
- Grain: one row per survey response
- Key columns: date_key, store_id, customer_id, overall_rating, food_rating, service_rating, cleanliness_rating, value_rating, would_recommend, sentiment

### BI Dashboard Aggregation
- **Avg CSAT**: `AVG(overall_rating)` (1-5 scale)
- **NPS**: Derived from would_recommend distribution
- **Sentiment**: GROUP BY sentiment (positive/neutral/negative)
- **By Region**: GROUP BY dim_store.region after JOIN on store_id

---

## 6. FACT_LOYALTY — Loyalty Program Transactions

### Source System
CRM / Loyalty platform. Tracks point earn/redeem events.

### S3 Raw Landing
- `s3://genbi-mcdhk-raw-530977327410/customer/loyalty_transactions/` — loyalty CSV files
  - Columns: transaction_date, loyalty_member_id, store_id, transaction_type, points_earned, points_redeemed, points_balance_after, associated_order_value

### Glue ETL (load_facts.py → load_fact_loyalty)
1. **Read** CSV from S3
2. **Transform**:
   - `date_key` = FORMAT(transaction_date, 'yyyyMMdd') cast to INT
   - `txn_type` = transaction_type (rename)
   - `points_balance` = points_balance_after (rename)
   - `order_value` = associated_order_value (rename)
3. **Write** to Redshift `genbi_mart.fact_loyalty`

### Redshift Data Mart (genbi_mart.fact_loyalty — 2.49M rows)
- Grain: one row per loyalty event
- Key columns: date_key, store_id, customer_id, txn_type, points_amount, points_balance, reward_type, order_value

### BI Dashboard Aggregation
- **Redemption Rate**: COUNT(txn_type='redeem') / COUNT(*)
- **Avg Order Value by Tier**: AVG(order_value) GROUP BY dim_customer.loyalty_tier
- **Points Issued**: SUM(points_earned) WHERE txn_type = 'earn'

---

## 7. FACT_EQUIPMENT — Equipment Maintenance Logs

### Source System
Facility management / CMMS system. Logs maintenance events, breakdowns, repairs.

### S3 Raw Landing
- `s3://genbi-mcdhk-raw-530977327410/operations/equipment_logs/` — equipment_logs.csv
  - Columns: event_date, store_id, equipment_id, equipment_type, event_type, hours_operating, maintenance_required

### Glue ETL (load_facts.py → load_fact_equipment)
1. **Read** CSV from S3
2. **Transform**:
   - `date_key` = FORMAT(event_date, 'yyyyMMdd') cast to INT
   - Column renames: equipment_type → type, event_type → event, hours_operating → operating_hours, maintenance_required → requires_maintenance
3. **Write** to Redshift `genbi_mart.fact_equipment`

### Redshift Data Mart (genbi_mart.fact_equipment — 10K rows)
- Grain: one row per equipment event
- Key columns: date_key, store_id, equipment_type, event_type, downtime_minutes, repair_cost

### BI Dashboard Aggregation
- **Total Downtime**: SUM(downtime_minutes) by equipment_type
- **Repair Costs**: SUM(repair_cost) GROUP BY store/region
- **Breakdown Frequency**: COUNT(*) WHERE event_type = 'breakdown'

---

## 8. FACT_FINANCIAL — Monthly Store P&L

### Source System
Finance / ERP system. Monthly P&L statements per store.

### S3 Raw Landing
- `s3://genbi-mcdhk-raw-530977327410/financial/store_pnl/` — store_pnl.csv
  - Columns: month, store_id, total_revenue, cost_of_goods, labor_cost, operating_cost, gross_profit, operating_profit, net_profit, profit_margin

### Glue ETL (load_facts.py → load_fact_financial)
1. **Read** CSV from S3
2. **Transform**:
   - `month_key` = FORMAT(month, 'yyyyMM') cast to INT — NOTE: uses month_key not date_key
   - Column renames: total_revenue → revenue, cost_of_goods → cogs, labor_cost → labor, operating_cost → operating_costs, operating_profit, net_profit, profit_margin → margin
3. **Write** to Redshift `genbi_mart.fact_financial`

### Redshift Data Mart (genbi_mart.fact_financial — 2.4K rows)
- Grain: one row per store per month (200 stores × 12 months)
- Key columns: month_key, store_id, revenue, cogs, gross_profit, labor_cost, rent, utilities, marketing, other_opex, ebitda, net_profit, gross_margin_pct, net_margin_pct

### BI Dashboard Aggregation
- **Total Revenue**: `SUM(revenue)` from fact_financial
- **EBITDA**: `SUM(ebitda)` = SUM(gross_profit - labor_cost - rent - utilities - marketing - other_opex)
- **Net Margin %**: `AVG(net_margin_pct)` or SUM(net_profit)/SUM(revenue)*100
- **Cost Breakdown**: SUM of each cost component GROUP BY region
- **Monthly Trend**: GROUP BY dim_date.month_name after JOIN month_key = dim_date.date_key

---

## Dimension Tables Pipeline

### dim_date (Glue: load_dimensions.py → load_dim_date)
- **Source**: Programmatically generated (no S3 source)
- **ETL**: Python generates 365 rows for 2023, HK public holidays hardcoded
- **Target**: genbi_mart.dim_date (365 rows)

### dim_store (Glue: load_dimensions.py → load_dim_store)
- **Source**: `s3://genbi-mcdhk-raw-530977327410/reference/stores/stores.csv`
- **ETL**: Read CSV, lowercase columns, trim whitespace
- **Target**: genbi_mart.dim_store (200 rows)

### dim_menu_item (Glue: load_dimensions.py → load_dim_menu_item)
- **Source**: `s3://genbi-mcdhk-raw-530977327410/reference/menu_items/` + `reference/categories/`
- **ETL**: JOIN menu_items + categories ON category_id, calculate food_cost_pct = cogs/unit_price*100
- **Target**: genbi_mart.dim_menu_item (30 rows)

### dim_customer (Glue: load_dimensions.py → load_dim_customer)
- **Source**: `s3://genbi-mcdhk-raw-530977327410/customer/customer_profiles/`
- **ETL**: Select dimension columns, trim whitespace
- **Target**: genbi_mart.dim_customer (50,000 rows)

### dim_channel (Glue: load_dimensions.py → load_dim_channel)
- **Source**: `s3://genbi-mcdhk-raw-530977327410/reference/channels/`
- **ETL**: Read CSV, lowercase, trim
- **Target**: genbi_mart.dim_channel (5 rows)

### dim_payment_method (Glue: load_dimensions.py → load_dim_payment_method)
- **Source**: `s3://genbi-mcdhk-raw-530977327410/reference/payment_methods/`
- **ETL**: Read CSV, lowercase, trim
- **Target**: genbi_mart.dim_payment_method (7 rows)

### dim_promotion (Glue: load_dimensions.py → load_dim_promotion)
- **Source**: `s3://genbi-mcdhk-raw-530977327410/reference/promotions/`
- **ETL**: Read CSV, lowercase, trim
- **Target**: genbi_mart.dim_promotion (12 rows)

---

## ETL Schedule
- **Dimensions**: Run once on initial setup, then on-demand for changes
- **Facts**: Daily at 02:00-03:00 HKT (except fact_financial which runs monthly on the 1st)
- **Metadata**: Run after any schema or lineage changes

## Glue Job Configuration
- **Glue version**: 4.0 (PySpark)
- **Workers**: 10 G.1X
- **S3 staging**: s3://genbi-mcdhk-scripts-530977327410/tmp/
- **IAM role**: arn:aws:iam::530977327410:role/AWSGlueServiceRole
- **Redshift target**: demo-sales-related workgroup, dev database, genbi_mart schema
