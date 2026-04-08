# ABC Restaurant Group GenBI - Operations Data Generation

## Overview

This directory contains Python scripts for generating synthetic operational data for the ABC Restaurant Group GenBI (General Business Intelligence) dashboard project. The system generates realistic, interconnected operational datasets covering inventory, labor, service metrics, and equipment maintenance across 200 Hong Kong stores.

## Files

### Core Generation Scripts
- **config.py** - Master configuration file with store, menu, and temporal weights
- **generate_operations.py** - Main operations data generator (this file)

### Generated Data Files
All CSV files are located in `raw/operations/`:

1. **inventory_daily.csv** - Daily inventory tracking
   - 2,190,000 rows (200 stores × 30 items × 365 days)
   - Daily stock levels with replenishment logic
   - Waste tracking by category

2. **labor_schedules.csv** - Labor scheduling and actuals
   - 665,600 rows (all shifts across all stores)
   - Employee scheduling with rates and actual hours
   - Productivity metrics

3. **service_times.csv** - Customer service metrics
   - 1,752,000 rows (hourly data across all stores)
   - Wait times by service channel
   - Staffing levels and order volumes

4. **equipment_logs.csv** - Equipment maintenance
   - 10,054 rows (maintenance and breakdowns)
   - Preventive maintenance schedule
   - Equipment failure events

## Quick Start

### Generate All Data
```bash
cd /Users/danshek/mcdhk-dashboard/genbi
python generate_operations.py
```

### Output
The script will:
1. Create output directory if needed: `raw/operations/`
2. Generate CSV files with progress indicators
3. Print summary statistics
4. Show total row counts for each file

### Generation Time
Typical runtime: ~2-3 minutes for full year of data

### Data Reproducibility
- Random seed: 42 (set in generate_operations.py)
- Ensures identical data on repeated runs
- All temporal patterns are deterministic

## Data Structure

### 1. Inventory Daily
```
date, store_id, item_id, opening_stock, units_received, units_sold,
units_wasted, closing_stock, waste_reason
```
- Opening stock carries forward from previous day
- Replenishment triggered when stock < 30 units
- Waste percentage by category: salads 4-8%, chicken 2-5%, others 1-3%

### 2. Labor Schedules
```
schedule_id, store_id, employee_id, date, shift_start_hour, shift_end_hour,
role, scheduled_hours, actual_hours, hourly_rate, labor_cost, orders_handled
```
- Employees: 15-25 per store (format: EMP-SXXX-NNN)
- Roles: crew (70%), shift_manager (20%), store_manager (10%)
- Rates: crew HK$60-75/hr, manager HK$85-110/hr, store_manager HK$130-160/hr
- Actual hours include overtime (0-1.5 hours extra)

### 3. Service Times
```
date, store_id, hour, avg_counter_wait_secs, avg_kiosk_wait_secs,
avg_drive_thru_secs, avg_delivery_prep_secs, orders_served,
peak_wait_secs, staff_on_duty
```
- All wait times in seconds
- Peak hours (12-13, 18-19): 1.5-2x longer waits
- Staff on duty: 3-8 based on hour, more during peaks
- Drive-thru only populated for drive_thru store types

### 4. Equipment Logs
```
event_id, store_id, equipment_type, event_date, event_type, downtime_minutes,
repair_cost, technician_id, description
```
- Event types: breakdown, preventive_maintenance, repair, inspection
- Preventive maintenance: quarterly for all equipment
- Breakdowns: 1-3 random events per store per month
- Ice cream machines: break down more frequently (meme-accurate!)
- Repair costs: HK$0-15,000

## Configuration Reference

### Temporal Weights
Affects volume and staffing calculations:

- **Hour weights**: Peak demand at lunch (12-13) and dinner (18-19)
- **Day weights**: Weekends (1.3-1.4x) vs weekdays (0.8-0.9x)
- **Month weights**: Summer and December peaks (1.1-1.2x)

### Store Parameters
- 200 stores across Hong Kong
- Average daily orders: 400-1,200 per store
- Monthly rent: HK$50K-300K
- Store types: standard, express, drive_thru, kiosk
- Regions: Hong Kong Island, Kowloon, New Territories

### Menu
- 30 items with categories: burger, chicken, salad, beverage, dessert
- Unit prices: HK$15-85
- COGS: HK$5-35
- LTO (Limited Time Offer) indicators

## Data Quality

### Validation Checks
- Stock formula: closing = opening - sold - wasted + received
- Labor costs: calculated as actual_hours × hourly_rate
- Dates: all within 2023-01-01 to 2023-12-31
- No null values in required fields
- Waste reasons only when units_wasted > 0

### Realistic Patterns
- Day-of-week seasonality (weekend peaks)
- Monthly seasonality (holiday peaks)
- Hourly demand peaks (lunch and dinner rush)
- Waste varies by food category (fresh vs frozen)
- Labor overtime on weekends
- Ice cream machine failures are disproportionately high

## Performance Notes

### File Sizes
- Total: ~240 MB
- Largest: inventory_daily.csv (85 MB)
- Format: CSV with gzip-compatible structure

### Memory Usage
- Generation processes month-by-month for large files
- Typical peak memory: <500 MB
- Closes and flushes after each month

### Scalability
To generate more/less data:
1. Modify store count in config.py: `STORES` list
2. Modify menu size in config.py: `MENU_ITEMS` list
3. Modify date range: `DATE_START` and `DATE_END`
4. Re-run generate_operations.py

## Integration

### With Dashboard
1. Import CSV files into data warehouse
2. Use store_id as foreign key to store master
3. Join labor schedules with employee master
4. Aggregate service_times by store/hour for trending

### For Analysis
- Inventory turnover by store and category
- Labor cost per store and per order
- Customer experience trends by time and location
- Equipment maintenance ROI analysis

## Troubleshooting

### File Already Exists
- Script overwrites existing files
- Back up before re-running if needed

### Memory Issues
- Reduce date range to subset of year
- Reduce store count for testing
- Process files one at a time

### Data Looks Unrealistic
- Check temporal weights in config.py
- Verify store avg_daily_orders are reasonable
- Inspect sample rows for patterns

## Next Steps

1. **Load into Database**: Import CSVs into PostgreSQL or similar
2. **Create Star Schema**: Build dimensional model from flat CSVs
3. **Build Aggregations**: Pre-aggregate for dashboard performance
4. **Create Visualizations**: Connect Tableau/PowerBI to data warehouse
5. **Generate Reports**: Leverage GenBI analysis layer

## Contact

For issues or questions about data generation, check:
1. This README
2. DATA_GENERATION_SUMMARY.md (statistics)
3. Script comments in generate_operations.py
