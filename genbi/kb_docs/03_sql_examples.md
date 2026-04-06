# SQL Query Examples for Common Business Questions

## Revenue Queries

### Total revenue by month
```sql
SELECT d.month, d.month_name, SUM(f.line_total) AS revenue, SUM(f.gross_profit) AS gross_profit
FROM genbi_mart.fact_sales f
JOIN genbi_mart.dim_date d ON f.date_key = d.date_key
GROUP BY d.month, d.month_name
ORDER BY d.month;
```

### Revenue by store region
```sql
SELECT s.region, SUM(f.line_total) AS revenue, COUNT(DISTINCT f.transaction_id) AS total_orders
FROM genbi_mart.fact_sales f
JOIN genbi_mart.dim_store s ON f.store_id = s.store_id
GROUP BY s.region
ORDER BY revenue DESC;
```

### Top 10 stores by revenue
```sql
SELECT s.store_id, s.store_name, s.district, s.region,
       SUM(f.line_total) AS revenue, SUM(f.gross_profit) AS profit,
       COUNT(DISTINCT f.transaction_id) AS orders
FROM genbi_mart.fact_sales f
JOIN genbi_mart.dim_store s ON f.store_id = s.store_id
GROUP BY s.store_id, s.store_name, s.district, s.region
ORDER BY revenue DESC
LIMIT 10;
```

### Revenue by menu category
```sql
SELECT m.category_name, SUM(f.line_total) AS revenue, SUM(f.quantity) AS units_sold,
       SUM(f.gross_profit) AS profit,
       ROUND(SUM(f.gross_profit) / NULLIF(SUM(f.line_total), 0) * 100, 2) AS margin_pct
FROM genbi_mart.fact_sales f
JOIN genbi_mart.dim_menu_item m ON f.item_id = m.item_id
GROUP BY m.category_name
ORDER BY revenue DESC;
```

### Revenue by channel
```sql
SELECT c.channel_name, SUM(f.line_total) AS revenue, COUNT(DISTINCT f.transaction_id) AS orders,
       ROUND(AVG(f.line_total), 2) AS avg_item_value
FROM genbi_mart.fact_sales f
JOIN genbi_mart.dim_channel c ON f.channel_id = c.channel_id
GROUP BY c.channel_name
ORDER BY revenue DESC;
```

### Revenue by payment method
```sql
SELECT p.payment_name, SUM(f.line_total) AS revenue, COUNT(DISTINCT f.transaction_id) AS orders
FROM genbi_mart.fact_sales f
JOIN genbi_mart.dim_payment_method p ON f.payment_id = p.payment_id
GROUP BY p.payment_name
ORDER BY revenue DESC;
```

## Time Analysis Queries

### Revenue by hour of day
```sql
SELECT f.order_hour, SUM(f.line_total) AS revenue, COUNT(DISTINCT f.transaction_id) AS orders
FROM genbi_mart.fact_sales f
GROUP BY f.order_hour
ORDER BY f.order_hour;
```

### Holiday vs non-holiday comparison
```sql
SELECT d.is_holiday,
       COUNT(DISTINCT d.full_date) AS num_days,
       SUM(f.line_total) AS total_revenue,
       ROUND(SUM(f.line_total) / COUNT(DISTINCT d.full_date), 2) AS avg_daily_revenue
FROM genbi_mart.fact_sales f
JOIN genbi_mart.dim_date d ON f.date_key = d.date_key
GROUP BY d.is_holiday;
```

### Weekend vs weekday performance
```sql
SELECT d.is_weekend,
       COUNT(DISTINCT d.full_date) AS num_days,
       SUM(f.line_total) AS total_revenue,
       ROUND(SUM(f.line_total) / COUNT(DISTINCT d.full_date), 2) AS avg_daily_revenue
FROM genbi_mart.fact_sales f
JOIN genbi_mart.dim_date d ON f.date_key = d.date_key
GROUP BY d.is_weekend;
```

## Operations Queries

### Average service wait time by store (top 10 slowest)
```sql
SELECT s.store_name, s.district,
       ROUND(AVG(sp.avg_counter_secs), 1) AS avg_counter_wait,
       ROUND(AVG(sp.avg_kiosk_secs), 1) AS avg_kiosk_wait,
       ROUND(AVG(sp.peak_wait_secs), 0) AS avg_peak_wait
FROM genbi_mart.fact_service_performance sp
JOIN genbi_mart.dim_store s ON sp.store_id = s.store_id
GROUP BY s.store_name, s.district
ORDER BY avg_counter_wait DESC
LIMIT 10;
```

### Inventory waste rate by category
```sql
SELECT m.category_name,
       ROUND(AVG(i.waste_rate), 2) AS avg_waste_rate,
       SUM(i.units_wasted) AS total_wasted,
       SUM(i.units_sold) AS total_sold
FROM genbi_mart.fact_inventory i
JOIN genbi_mart.dim_menu_item m ON i.item_id = m.item_id
GROUP BY m.category_name
ORDER BY avg_waste_rate DESC;
```

### Labor cost per order by store
```sql
SELECT s.store_name, s.district,
       ROUND(SUM(l.labor_cost), 2) AS total_labor_cost,
       SUM(l.orders_handled) AS total_orders,
       ROUND(SUM(l.labor_cost) / NULLIF(SUM(l.orders_handled), 0), 2) AS cost_per_order
FROM genbi_mart.fact_labor l
JOIN genbi_mart.dim_store s ON l.store_id = s.store_id
GROUP BY s.store_name, s.district
ORDER BY cost_per_order DESC
LIMIT 10;
```

## Customer Queries

### Customer satisfaction by region
```sql
SELECT s.region,
       ROUND(AVG(fb.overall_rating), 2) AS avg_rating,
       ROUND(AVG(fb.food_rating), 2) AS avg_food,
       ROUND(AVG(fb.service_rating), 2) AS avg_service,
       COUNT(*) AS num_surveys
FROM genbi_mart.fact_customer_feedback fb
JOIN genbi_mart.dim_store s ON fb.store_id = s.store_id
GROUP BY s.region
ORDER BY avg_rating DESC;
```

### Loyalty tier distribution and spend
```sql
SELECT c.loyalty_tier, COUNT(*) AS members,
       ROUND(AVG(l.order_value), 2) AS avg_order_value,
       SUM(CASE WHEN l.txn_type = 'redeem' THEN 1 ELSE 0 END) AS redemptions
FROM genbi_mart.dim_customer c
JOIN genbi_mart.fact_loyalty l ON c.customer_id = l.customer_id
GROUP BY c.loyalty_tier
ORDER BY avg_order_value DESC;
```

## Financial Queries

### Monthly P&L summary (all stores)
```sql
SELECT d.month_name,
       ROUND(SUM(f.revenue), 0) AS revenue,
       ROUND(SUM(f.gross_profit), 0) AS gross_profit,
       ROUND(SUM(f.ebitda), 0) AS ebitda,
       ROUND(SUM(f.net_profit), 0) AS net_profit,
       ROUND(AVG(f.gross_margin_pct), 1) AS avg_gross_margin,
       ROUND(AVG(f.net_margin_pct), 1) AS avg_net_margin
FROM genbi_mart.fact_financial f
JOIN genbi_mart.dim_date d ON f.month_key = d.date_key
GROUP BY d.month, d.month_name
ORDER BY d.month;
```

### Stores with negative net profit
```sql
SELECT s.store_name, s.district, s.region,
       SUM(f.net_profit) AS annual_net_profit,
       AVG(f.net_margin_pct) AS avg_net_margin
FROM genbi_mart.fact_financial f
JOIN genbi_mart.dim_store s ON f.store_id = s.store_id
GROUP BY s.store_name, s.district, s.region
HAVING SUM(f.net_profit) < 0
ORDER BY annual_net_profit;
```

## Important Query Patterns

### Joining fact tables with dimensions
Always join fact tables to dim_date using date_key (integer):
```sql
FROM genbi_mart.fact_sales f
JOIN genbi_mart.dim_date d ON f.date_key = d.date_key
```

### Filtering by date range
```sql
WHERE d.full_date BETWEEN '2023-01-01' AND '2023-03-31'
-- OR using date_key directly:
WHERE f.date_key BETWEEN 20230101 AND 20230331
```

### Counting distinct transactions
Since fact_sales has one row per line item, count distinct transaction_id for order counts:
```sql
COUNT(DISTINCT f.transaction_id) AS order_count
```
