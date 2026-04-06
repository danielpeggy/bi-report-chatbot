# McDonald's HK GenBI - Operations Data Generation Summary

## Generated Files

Generated on: 2026-03-30
Data Period: 2023-01-01 to 2023-12-31 (365 days)
Random Seed: 42 (reproducible)

### 1. inventory_daily.csv
- **Rows**: 2,190,000 (200 stores × 30 items × 365 days)
- **File Size**: ~85 MB
- **Frequency**: Daily snapshots at store/item level
- **Key Metrics**:
  - Opening stock carried forward from previous day
  - Units sold based on store average daily orders and item popularity
  - Units received triggered when stock falls below 30 units (replenishment logic)
  - Waste percentage varies by category (fresh items 4-8%, frozen items 1-3%)
  - Waste reasons: expired, damaged, overproduction
- **Usage**: Inventory tracking, stock optimization, waste analysis

### 2. labor_schedules.csv
- **Rows**: 665,600 (varies by day and store)
- **File Size**: ~47 MB
- **Frequency**: Per shift per store per day
- **Key Metrics**:
  - 15-25 employees per store (unique employee IDs: EMP-SXXX-NNN)
  - 7-12 shifts per store per day (more on weekends)
  - 3 role types: crew (70%), shift_manager (20%), store_manager (10%)
  - Hourly rates: crew HK$60-75, shift_manager HK$85-110, store_manager HK$130-160
  - Scheduled vs actual hours (overtime common on weekends)
  - Orders handled calculated based on daily volume and shift hours
- **Usage**: Labor cost analysis, staffing patterns, productivity metrics

### 3. service_times.csv
- **Rows**: 1,752,000 (200 stores × 24 hours × 365 days)
- **File Size**: ~81 MB
- **Frequency**: Hourly aggregates
- **Key Metrics**:
  - Counter wait times: 120-300 secs avg (1.5-2x during peak hours 12-13, 18-19)
  - Kiosk wait times: 60-180 secs avg
  - Drive-thru wait times: 180-400 secs (only for drive_thru store types)
  - Delivery prep times: 300-600 secs
  - Staff on duty: 3-8 based on hour (increases during peaks)
  - Orders served: distributed by hourly weights (peak hours: 12-13, 18-19)
- **Usage**: Customer experience analysis, staffing optimization, channel performance

### 4. equipment_logs.csv
- **Rows**: 10,054 (~5-50 events per store per year)
- **File Size**: ~1 MB
- **Frequency**: Event-based (maintenance + breakdowns)
- **Key Metrics**:
  - Equipment types: grill, fryer, ice_cream_machine, drink_dispenser, pos_terminal, hvac, walk_in_cooler
  - Event types: breakdown, preventive_maintenance, repair, inspection
  - Preventive maintenance: quarterly for all equipment types
  - Random breakdowns: 1-3 per store per month
  - Ice cream machines break down more frequently (meme-accurate!)
  - Downtime: 15-480 minutes per event
  - Repair costs: HK$0-15,000
- **Usage**: Equipment maintenance tracking, cost analysis, downtime planning

## Data Generation Logic

### Temporal Patterns
- **Hour weights**: Peak hours (lunch 12-13, dinner 18-19) have 1.5-2x volume
- **Day weights**: Weekends (Sat-Sun) have 1.3-1.4x vs weekdays (0.8-0.9x)
- **Month weights**: Summer (Jul-Aug) and Dec have higher volumes (1.1-1.2x)

### Store Data
- 200 stores across Hong Kong
- Districts: Central, Wan Chai, Causeway Bay, Tsim Sha Tsui, etc.
- Regions: Hong Kong Island, Kowloon, New Territories
- Store types: standard, express, drive_thru, kiosk
- Average daily orders: 400-1,200 per store
- Monthly rent: HK$50K-300K

### Menu Items
- 30 items with categories: burger, chicken, salad, beverage, dessert
- Unit prices: HK$15-85
- COGS: HK$5-35
- LTO (Limited Time Offer) flags included

## Data Quality
- All dates fall within 2023-01-01 to 2023-12-31 range
- Store IDs: S001-S200
- Employee IDs: EMP-SXXX-NNN format (randomized per store)
- Menu IDs: M001-M030
- No null values in required fields (waste_reason and drive_thru nullable)
- Closing stock properly calculated: opening - sold - wasted + received
- Labor costs calculated: actual_hours × hourly_rate
- Temporal relationships maintained (sequential dates, consistent weights)

## Directory Structure
```
/Users/danshek/mcdhk-dashboard/genbi/
├── config.py                 # Configuration with STORES, MENU_ITEMS, weights
├── generate_operations.py    # Main generation script
├── raw/operations/
│   ├── inventory_daily.csv   # 2.19M rows
│   ├── labor_schedules.csv   # 665K rows
│   ├── service_times.csv     # 1.75M rows
│   └── equipment_logs.csv    # 10K rows
└── DATA_GENERATION_SUMMARY.md
```

## Notes
- Random seed (42) ensures reproducible data generation
- All timestamps in ISO format (YYYY-MM-DD HH:MM:SS)
- Monetary values in HK$ with 2 decimal places
- Time in 24-hour format (0-23)
- Generated efficiently by month for large files to manage memory
