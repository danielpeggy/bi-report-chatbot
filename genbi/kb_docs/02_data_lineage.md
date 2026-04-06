# Data Lineage - How Numbers Are Calculated

This document explains where each key metric comes from, what transformations are applied, and how to trace any number back to its source.

## ETL Pipeline Overview
Raw data flows: S3 CSV files → Redshift staging tables → Star schema (genbi_mart)
All ETL runs daily at 02:00-03:00 HKT. Financial data loads monthly on the 1st.

## Key Calculated Metrics

### Revenue & Profitability (fact_sales)

**gross_profit** = line_total - cogs_amount - discount_amount
- line_total comes from pos_line_items.line_total (= unit_price × quantity)
- cogs_amount comes from pos_line_items.cogs_amount (= unit COGS from menu × quantity)
- discount_amount = transaction-level discount evenly split across line items in that order
- Source: JOIN of pos_transactions + pos_line_items on transaction_id

**discount_amount** (per line item) = transaction.discount_amount / transaction.order_item_count
- Promotions are applied at the transaction level
- The discount is divided equally among all items in the order
- If no promotion, discount_amount = 0

### Inventory & Waste (fact_inventory)

**waste_rate** = units_wasted / (units_sold + units_wasted) × 100
- Represents the percentage of consumed stock that was wasted
- A waste_rate of 3% means: for every 100 units consumed, 3 were wasted and 97 were sold
- Target: below 3%
- Source: inventory_daily CSV with item_id prefix 'M' stripped (M001→1)

**closing_stock** = opening_stock + units_received - units_sold - units_wasted
- This calculation happens in the source data generation
- If closing_stock doesn't match this formula, it indicates shrinkage

### Labor Productivity (fact_labor)

**labor_cost** = actual_hours × hourly_rate
- Source: labor_schedules CSV
- Note: actual_hours may differ from scheduled_hours (overtime or early leave)
- HK minimum wage: HKD 40/hour (2023)

**labor_productivity** = orders_handled / actual_hours (not stored, calculate in queries)

### Financial P&L (fact_financial)

**gross_profit** = revenue - cogs
**ebitda** = gross_profit - labor_cost - rent - utilities - marketing - other_opex
**net_profit** = ebitda - depreciation
**gross_margin_pct** = gross_profit / revenue × 100 (benchmark: 60-70% for QSR)
**net_margin_pct** = net_profit / revenue × 100 (target: 10-15% for healthy stores)

### Date Key Mapping

**date_key** = YYYYMMDD integer (e.g., January 15, 2023 = 20230115)
- All fact tables join to dim_date via date_key
- fact_financial uses month_key which maps to the first day of the month (e.g., 20230101 for January)
- Use dim_date.full_date for human-readable dates

## Data Freshness
- POS sales data: Available next day after midnight batch
- Inventory: Daily snapshot at end of business
- Labor: Updated after shift completion
- Financial P&L: Monthly, available by 4th of following month
- Customer feedback: Within 24 hours of survey submission

## Known Data Characteristics
- ~60% of fact_sales rows have NULL customer_id (non-loyalty transactions)
- Drive-through channel (channel_id=5) only appears for stores with store_type='drive_thru'
- Breakfast items (category_id=5) have orders concentrated between 7:00-11:00
- Holiday periods show 20-40% traffic increase
- Summer months (Jun-Aug) show higher dessert category sales
