# ABC Restaurant Group GenBI Data Mart - Schema Overview

## Database: Amazon Redshift Serverless
- Workgroup: demo-sales-related
- Database: dev
- Schema: genbi_mart

## Star Schema Design
The data mart uses a star schema with 7 dimension tables, 8 fact tables, and 4 metadata/lineage tables.

### Dimension Tables

#### dim_date (365 rows)
Date dimension for all of 2023. Key: date_key (YYYYMMDD integer, e.g., 20230101).
Columns: date_key, full_date, year, quarter, month, month_name, week_of_year, day_of_month, day_of_week, day_name, is_weekend, is_holiday.
Note: is_holiday flags 17 Hong Kong public holidays including Lunar New Year (Jan 23-25), Easter (Apr 7-10), HKSAR Day (Jul 1), National Day (Oct 2), Christmas (Dec 25-26).

#### dim_store (200 rows)
All ABC Restaurant Group locations across three regions.
Columns: store_key, store_id (S001-S200), store_name, district, region (HK_Island, Kowloon, New_Territories), store_type (mall, street, drive_thru), avg_daily_orders, open_date, rent_monthly.
Note: Only drive_thru stores have drive-through channel orders.

#### dim_menu_item (30 rows)
Menu items across 8 categories.
Columns: item_key, item_id, item_name, category_id, category_name, unit_price, cogs, food_cost_pct, is_lto.
Categories: 1=Burgers, 2=Chicken, 3=Sides, 4=Beverages, 5=Breakfast, 6=Desserts, 7=Value Meals, 8=Limited Time.
food_cost_pct = cogs / unit_price * 100 (lower is more profitable).

#### dim_channel (5 rows)
Order channels: 1=counter, 2=kiosk, 3=mobile_app, 4=delivery, 5=drive_thru.

#### dim_payment_method (7 rows)
Payment methods: 1=cash, 2=octopus, 3=visa, 4=mastercard, 5=apple_pay, 6=alipay, 7=wechat_pay.
Note: Octopus is Hong Kong's dominant contactless payment card.

#### dim_promotion (12 rows)
Promotions run throughout 2023. Columns: promo_key, promo_id, promo_name, promo_type, discount_pct, start_date, end_date.

#### dim_customer (50,000 rows)
Loyalty program members. Columns: customer_key, customer_id, age_group, gender, home_district, preferred_store_id, loyalty_tier (bronze/silver/gold/platinum), registration_date, first_visit_date.

### Fact Tables

#### fact_sales (17.5M rows) - PRIMARY FACT TABLE
Transaction-level sales data joining POS transactions with line items.
Columns: sale_key, transaction_id, date_key, store_id, item_id, customer_id, channel_id, payment_id, promo_id, order_hour, quantity, unit_price, line_total, discount_amount, cogs_amount, gross_profit.
Key metrics: line_total = unit_price × quantity; gross_profit = line_total - cogs_amount - discount_amount.
Note: customer_id is NULL for ~60% of transactions (non-loyalty customers).

#### fact_inventory (2.19M rows)
Daily inventory snapshots per store per item.
Columns: inventory_key, date_key, store_id, item_id, opening_stock, units_received, units_sold, units_wasted, closing_stock, waste_reason, waste_rate.
waste_rate = units_wasted / (units_sold + units_wasted) * 100. Target: below 3%.

#### fact_labor (665K rows)
Employee shift records.
Columns: labor_key, date_key, store_id, employee_id, role, shift_start, shift_end, scheduled_hours, actual_hours, hourly_rate, labor_cost, orders_handled.
labor_cost = actual_hours × hourly_rate.

#### fact_service_performance (1.75M rows)
Hourly service time metrics per store.
Columns: service_key, date_key, store_id, hour, avg_counter_secs, avg_kiosk_secs, avg_drive_thru_secs, avg_delivery_secs, orders_served, peak_wait_secs, staff_on_duty.

#### fact_customer_feedback (28K rows)
Customer satisfaction surveys.
Columns: feedback_key, date_key, store_id, customer_id, overall_rating (1-5), food_rating, service_rating, cleanliness_rating, value_rating, would_recommend (boolean), sentiment (positive/neutral/negative).

#### fact_loyalty (2.49M rows)
Loyalty program transactions.
Columns: loyalty_key, date_key, store_id, customer_id, txn_type (earn/redeem/bonus), points_amount, points_balance, reward_type, order_value.

#### fact_equipment (10K rows)
Equipment maintenance and breakdown events.
Columns: equipment_key, date_key, store_id, equipment_type, event_type, downtime_minutes, repair_cost.

#### fact_financial (2.4K rows)
Monthly store-level P&L statements.
Columns: financial_key, month_key, store_id, revenue, cogs, gross_profit, labor_cost, rent, utilities, marketing, other_opex, ebitda, net_profit, gross_margin_pct, net_margin_pct.
