# Business Glossary - McDonald's HK GenBI

## Key Business Metrics

**Average Order Value (AOV)**: Total revenue divided by number of orders. Calculate as SUM(line_total) / COUNT(DISTINCT transaction_id). Typical range: HKD 40-80.

**Basket Size**: Number of items per order. Use order_item_count from the transaction or COUNT line items per transaction_id.

**COGS (Cost of Goods Sold)**: Direct cost of food ingredients and packaging. Stored in cogs_amount at the line item level.

**Food Cost Percentage**: COGS as a percentage of selling price. Stored in dim_menu_item.food_cost_pct. Industry target: 28-35%.

**Gross Margin**: (Revenue - COGS) / Revenue × 100. QSR benchmark: 60-70%.

**EBITDA**: Earnings Before Interest, Tax, Depreciation & Amortization. The primary store-level operating profitability metric.

**Net Margin**: Net profit after all expenses / Revenue × 100. Target: 10-15% for healthy McDonald's stores.

**Same-Store Sales (SSS)**: Revenue comparison for the same store year-over-year. Since this dataset covers only 2023, compare month-over-month or quarter-over-quarter.

**Labor Productivity**: Orders handled per labor hour. Calculate as SUM(orders_handled) / SUM(actual_hours).

**Labor Cost Ratio**: Labor cost as percentage of revenue. Target: below 30%.

**Waste Rate**: Percentage of inventory consumed that was wasted. Target: below 3%.

**Customer Satisfaction Score (CSAT)**: Average of overall_rating (1-5 scale). Target: 4.0+.

**Net Promoter Score (NPS) Proxy**: Percentage of would_recommend=TRUE minus percentage of would_recommend=FALSE.

## Hong Kong Market Context

**Regions**: Hong Kong is divided into three regions:
- HK Island: Central business district, high-rent, high-traffic tourist/office areas
- Kowloon: Dense residential and commercial, highest population density
- New Territories: Suburban, newer developments, growing population

**Payment Methods**: Octopus card is the dominant payment method in HK (~35% of transactions). Cash is declining (~15%). Mobile payments (Apple Pay, Alipay, WeChat Pay) are growing.

**Order Channels**:
- Counter: Traditional walk-in ordering (~30%)
- Kiosk: Self-service ordering machines (~35%, highest share)
- Mobile App: Order ahead for pickup (~15%)
- Delivery: Third-party and own delivery (~12%)
- Drive-thru: Only available at drive_thru store type (~8%)

**Currency**: All monetary values are in Hong Kong Dollars (HKD). 1 USD ≈ 7.8 HKD.

**Tax**: Hong Kong has no sales tax/VAT. All prices are final prices.

**Minimum Wage**: HKD 40/hour in 2023.

**Public Holidays**: 17 statutory holidays in 2023. Key periods:
- Lunar New Year (late Jan): Highest traffic period
- Summer (Jun-Aug): Higher dessert/beverage sales, tourist season
- Christmas (Dec): Promotional period, second-highest traffic
