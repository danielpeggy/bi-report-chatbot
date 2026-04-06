# Dashboard Catalog - QuickSight Dashboards

## Overview
There are 5 QuickSight dashboards available. Each dashboard is designed for a specific audience and purpose. When a user asks which dashboard to use, recommend based on their question topic.

---

## 1. Executive Summary Dashboard
**Dashboard ID**: genbi-exec-dashboard
**Tab**: Executive Summary
**Audience**: Senior leadership, regional managers
**Purpose**: High-level overview of business performance across all stores and regions

**Visuals included**:
- **Total Revenue (HKD)** KPI: Sum of all revenue from fact_sales.line_total
- **Total Orders** KPI: Count of distinct transaction_id from fact_sales
- **Gross Profit (HKD)** KPI: Sum of gross_profit from fact_sales
- **Revenue by Region** bar chart: Revenue broken down by dim_store.region (HK_Island, Kowloon, NT)
- **Monthly Revenue Trend** line chart: Revenue by dim_date.month_name showing Jan-Dec 2023 trend
- **Orders by Store Type** pie chart: Order distribution across store types (mall, street, drive_thru, food_court)

**Data sources**: fact_sales JOIN dim_date JOIN dim_store
**Use when**: User asks about overall business performance, revenue totals, regional comparisons, or monthly trends

---

## 2. Sales & Menu Analytics Dashboard
**Dashboard ID**: genbi-sales-dashboard
**Tab**: Sales & Menu
**Audience**: Marketing team, menu planning, category managers
**Purpose**: Deep dive into product performance, channel mix, and sales patterns

**Visuals included**:
- **Revenue by Category** bar chart: Revenue by dim_menu_item.category_name (Burgers, Chicken, Drinks, Fries, Desserts, Wraps, Sides, Breakfast)
- **Top Menu Items by Revenue** bar chart: Individual item revenue from dim_menu_item.item_name
- **Revenue by Order Channel** pie chart: Distribution across dim_channel.channel_name (Counter, Kiosk, Mobile App, Delivery, Drive-thru)
- **Revenue by Payment Method** pie chart: Distribution across dim_payment_method.payment_name (Cash, Octopus, Visa, Mastercard, Apple Pay, Alipay, WeChat Pay)
- **Sales by Hour of Day** line chart: Revenue by fact_sales.order_hour showing daily sales curve

**Data sources**: fact_sales JOIN dim_date JOIN dim_store JOIN dim_menu_item JOIN dim_channel JOIN dim_payment_method
**Use when**: User asks about menu item performance, category revenue, channel mix, payment preferences, hourly sales patterns, or product profitability

---

## 3. Operations & Efficiency Dashboard
**Dashboard ID**: genbi-ops-dashboard
**Tab**: Operations
**Audience**: Operations managers, store managers, HR
**Purpose**: Labor efficiency, staffing patterns, and operational metrics

**Visuals included**:
- **Avg Actual Hours/Shift** KPI: Average of fact_labor.actual_hours across all shifts
- **Avg Orders Handled/Shift** KPI: Average of fact_labor.orders_handled per shift
- **Labor Cost by Region** bar chart: Total labor_cost by dim_store.region
- **Orders by Role** bar chart: Total orders_handled by fact_labor.role (crew, shift_manager, kitchen, drive_thru_crew, cashier)
- **Monthly Labor Cost Trend** line chart: Labor cost by dim_date.month_name

**Data sources**: fact_labor JOIN dim_date JOIN dim_store
**Use when**: User asks about labor costs, staffing efficiency, shift productivity, workforce utilization, or operational efficiency metrics

---

## 4. Customer Intelligence Dashboard
**Dashboard ID**: genbi-cust-dashboard
**Tab**: Customer Intelligence
**Audience**: Customer experience team, marketing, quality assurance
**Purpose**: Customer satisfaction, feedback analysis, and sentiment tracking

**Visuals included**:
- **Avg Customer Rating** KPI: Average of fact_customer_feedback.overall_rating (1-5 scale)
- **Avg Rating by Region** bar chart: Overall rating by dim_store.region
- **Sentiment by Quarter** bar chart: Average sentiment score by dim_date.quarter
- **Would Recommend** pie chart: Distribution of fact_customer_feedback.would_recommend (TRUE/FALSE)

**Data sources**: fact_customer_feedback JOIN dim_date JOIN dim_store
**Use when**: User asks about customer satisfaction, CSAT scores, NPS, sentiment analysis, food/service ratings, or customer experience trends

---

## 5. Financial Performance Dashboard
**Dashboard ID**: genbi-fin-dashboard
**Tab**: Financial Performance
**Audience**: Finance team, CFO, store P&L owners
**Purpose**: Profitability analysis, cost management, and financial KPIs

**Visuals included**:
- **Total EBITDA (HKD)** KPI: Sum of fact_financial.ebitda
- **Net Profit (HKD)** KPI: Sum of fact_financial.net_profit
- **Monthly P&L Trend** line chart: Three lines showing total_revenue, total_cogs, and net_profit by month
- **Cost Breakdown by Region** bar chart: Stacked bar showing labor_cost, rent, utilities by region
- **Gross Margin % by Region** bar chart: Average gross_margin_pct by dim_store.region

**Data sources**: fact_financial JOIN dim_date JOIN dim_store
**Use when**: User asks about profitability, EBITDA, net margin, cost structure, P&L, rent costs, or financial performance by region

---

## Dashboard Recommendation Guide

| Question Topic | Recommended Dashboard |
|---|---|
| Total revenue, overall performance | Executive Summary |
| Regional comparison | Executive Summary |
| Monthly/quarterly trends | Executive Summary or Financial Performance |
| Menu item sales, best sellers | Sales & Menu |
| Order channels (kiosk, delivery, etc.) | Sales & Menu |
| Payment methods | Sales & Menu |
| Hourly sales patterns | Sales & Menu |
| Labor costs, staffing | Operations |
| Shift productivity | Operations |
| Customer ratings, CSAT | Customer Intelligence |
| NPS, would recommend | Customer Intelligence |
| Sentiment analysis | Customer Intelligence |
| EBITDA, net profit | Financial Performance |
| Cost breakdown, P&L | Financial Performance |
| Gross/net margin | Financial Performance |
