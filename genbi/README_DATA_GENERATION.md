# ABC Restaurant Group GenBI - Data Generation Script

## Overview
`generate_market_financial.py` generates synthetic market and financial data for ABC Restaurant Group (200 stores) for 2023.

## Output Files

### Market Data (raw/market/)

1. **competitor_pricing.csv** (~600 rows)
   - Snapshot dates: 1st of each month (12 months)
   - Competitors: KFC, Burger King, MOS Burger, Jollibee, Shake Shack
   - Pricing comparisons with ABC Restaurant prices
   - ~20 comparable items per competitor
   - Pricing variance: ±15% (KFC cheaper on chicken, Shake Shack 30-50% premium)

2. **market_indicators.csv** (216 rows = 18 districts × 12 months)
   - Districts: 18 Hong Kong districts (Central_Western, Wan_Chai, Eastern, etc.)
   - Metrics: unemployment rate, median income, population, foot traffic index, retail sales, tourist arrivals, new businesses
   - Seasonal variations: peak in Jul-Aug (tourism), Dec (holidays)
   - Tourist districts (Central, TST, Wan Chai) include tourist arrival data

### Financial Data (raw/financial/)

3. **store_pnl.csv** (2,400 rows = 200 stores × 12 months)
   - P&L metrics: revenue, COGS, gross/net profit, all expense categories
   - Revenue drivers: store's avg_daily_orders, seasonal multipliers
   - COGS: 32-38% of revenue (supply chain based)
   - Labor: 25-30% of revenue (mall stores slightly higher)
   - Utilities: HK$15K-40K/month (peak in summer: Jun-Aug)
   - Net margins: 8-15% (mall stores lower due to rent, drive-thru higher)

4. **cogs_detail.csv** (360 rows = 30 items × 12 months)
   - Item-level COGS tracking
   - Supply reliability: 92-99% (lower during typhoon season: Jul-Sep)
   - Suppliers: 10 named suppliers (HK Food Supply Co, Pacific Meats Ltd, etc.)
   - Supply variance: ±5% (reflects chain fluctuations)

5. **opex_breakdown.csv** (24,000 rows = 200 stores × 12 months × 10 categories)
   - Detailed expense categories: labor, rent, utilities, maintenance, marketing, insurance, supplies, technology, training, miscellaneous
   - Budget tracking with variance analysis (typically ±10%)
   - Seasonal spikes: utilities in Jun-Aug, higher maintenance during certain events

## Dependencies
- Requires `config.py` in the same directory
- Config must provide: STORES, MENU_ITEMS, CATEGORIES, DATE_START, DATE_END

## Running the Script
```bash
python3 generate_market_financial.py
```

## Data Characteristics
- Random seed: 42 (reproducible)
- Base year: 2023
- Currency: Hong Kong Dollars (HKD)
- Stores: 200 ABC Restaurant locations
- Menu items: 30 items tracked
- Time periods: 12 months
- Realistic distributions and seasonal patterns
- Built-in variance for realistic variation

## Notes
- Unemployment rates: 3-5% (Central lower, NT higher)
- Median income: HK$25K-45K by district
- Foot traffic seasonal: higher summer/December
- Supply reliability drops during typhoon season (Jul-Sep)
- All financial metrics realistic for QSR industry
