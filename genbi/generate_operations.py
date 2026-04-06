"""
McDonald's HK GenBI - Synthetic Operations Data Generator

Generates 4 CSV files with operational data:
1. inventory_daily.csv - Daily inventory tracking (2.19M rows)
2. labor_schedules.csv - Labor scheduling and actuals (584K rows)
3. service_times.csv - Customer service metrics (1.24M rows)
4. equipment_logs.csv - Equipment maintenance logs (2K rows)
"""

import csv
import random
import os
from datetime import datetime, timedelta
from collections import defaultdict

from config import (
    STORES, MENU_ITEMS, HOUR_WEIGHTS, DAY_WEIGHTS, MONTH_WEIGHTS,
    DATE_START, DATE_END, WASTE_REASONS, EQUIPMENT_TYPES, ROLES, ROLE_WEIGHTS,
    HOURLY_RATES, SHIFTS, SERVICE_WAIT_TIMES, MAINTENANCE_MONTHS
)

# Set seed for reproducibility
random.seed(42)

# Parse date range
start_date = datetime.strptime(DATE_START, "%Y-%m-%d")
end_date = datetime.strptime(DATE_END, "%Y-%m-%d")

OUTPUT_DIR = "/Users/danshek/mcdhk-dashboard/genbi/raw/operations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("McDonald's HK GenBI - Operations Data Generator")
print(f"Generating data from {DATE_START} to {DATE_END}")
print(f"Stores: {len(STORES)} | Menu Items: {len(MENU_ITEMS)}")
print()

# ============================================================================
# 1. INVENTORY DAILY CSV
# ============================================================================
def generate_inventory_daily():
    """Generate inventory tracking data by month for efficiency."""
    print("Generating inventory_daily.csv...")

    output_file = os.path.join(OUTPUT_DIR, "inventory_daily.csv")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                'date', 'store_id', 'item_id', 'opening_stock', 'units_received',
                'units_sold', 'units_wasted', 'closing_stock', 'waste_reason'
            ]
        )
        writer.writeheader()

        # Track closing stock per store/item for continuity
        closing_stock_tracker = defaultdict(lambda: defaultdict(lambda: random.randint(50, 200)))

        current_date = start_date
        month_count = 0

        while current_date <= end_date:
            month_count += 1
            month_data = []

            # Process entire month
            month_start = current_date
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            if month_end > end_date:
                month_end = end_date

            print(f"  Processing {month_start.strftime('%Y-%m')} ({month_end - month_start + timedelta(days=1)}) days)...", end='', flush=True)

            process_date = month_start
            while process_date <= month_end:
                day_of_week = process_date.weekday()
                month = process_date.month

                # Get weights for this day
                day_weight = DAY_WEIGHTS[day_of_week]
                month_weight = MONTH_WEIGHTS[month]

                for store in STORES:
                    store_id = store['store_id']
                    base_daily_orders = store['avg_daily_orders']
                    daily_orders = int(base_daily_orders * day_weight * month_weight * random.uniform(0.9, 1.1))

                    for item in MENU_ITEMS:
                        item_id = item['item_id']

                        # Determine waste percentage based on category
                        category = item['category_id']
                        if category == 'salad':
                            waste_pct = random.uniform(0.04, 0.08)
                        elif category == 'chicken':
                            waste_pct = random.uniform(0.02, 0.05)
                        elif category == 'dessert':
                            waste_pct = random.uniform(0.03, 0.06)
                        elif category == 'beverage':
                            waste_pct = random.uniform(0.01, 0.03)
                        else:  # frozen/burger
                            waste_pct = random.uniform(0.01, 0.03)

                        # Calculate units sold (distributed across 30 items)
                        units_sold = max(0, int(daily_orders / 30 * random.uniform(0.7, 1.3)))
                        units_wasted = max(0, int(units_sold * waste_pct))

                        # Get opening stock from previous day
                        opening_stock = closing_stock_tracker[store_id][item_id]

                        # Replenishment logic
                        units_received = 0
                        temp_stock = opening_stock - units_sold - units_wasted
                        if temp_stock < 30:
                            units_received = random.randint(100, 300)

                        closing_stock = opening_stock - units_sold - units_wasted + units_received

                        # Determine waste reason
                        if units_wasted > 0:
                            waste_reason = random.choice(WASTE_REASONS)
                        else:
                            waste_reason = None

                        # Track for next day
                        closing_stock_tracker[store_id][item_id] = closing_stock

                        month_data.append({
                            'date': process_date.strftime('%Y-%m-%d'),
                            'store_id': store_id,
                            'item_id': item_id,
                            'opening_stock': opening_stock,
                            'units_received': units_received,
                            'units_sold': units_sold,
                            'units_wasted': units_wasted,
                            'closing_stock': closing_stock,
                            'waste_reason': waste_reason if waste_reason else ''
                        })

                process_date += timedelta(days=1)

            # Write month data
            writer.writerows(month_data)
            print(f" Done ({len(month_data)} rows)")

            # Move to next month
            current_date = month_end + timedelta(days=1)

    print(f"Saved: {output_file}")
    print()


# ============================================================================
# 2. LABOR SCHEDULES CSV
# ============================================================================
def generate_labor_schedules():
    """Generate labor schedule and actuals."""
    print("Generating labor_schedules.csv...")

    output_file = os.path.join(OUTPUT_DIR, "labor_schedules.csv")

    # Pre-generate employee pool for each store
    store_employees = {}
    for store in STORES:
        store_id = store['store_id']
        num_employees = random.randint(15, 25)
        store_employees[store_id] = [f"EMP-{store_id}-{i:03d}" for i in range(1, num_employees + 1)]

    schedule_id_counter = 1

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                'schedule_id', 'store_id', 'employee_id', 'date', 'shift_start_hour',
                'shift_end_hour', 'role', 'scheduled_hours', 'actual_hours', 'hourly_rate',
                'labor_cost', 'orders_handled'
            ]
        )
        writer.writeheader()

        current_date = start_date
        row_count = 0

        while current_date <= end_date:
            # Determine staff count for the day (more on weekends)
            day_of_week = current_date.weekday()
            if day_of_week >= 5:  # Weekend
                shifts_per_store = random.randint(9, 12)
            else:
                shifts_per_store = random.randint(7, 10)

            for store in STORES:
                store_id = store['store_id']
                employees = store_employees[store_id]
                daily_orders = int(store['avg_daily_orders'] * DAY_WEIGHTS.get(day_of_week, 1.0) * random.uniform(0.9, 1.1))

                # Assign shifts for the day
                assigned_employees = set()
                for _ in range(shifts_per_store):
                    # Pick random employee and role
                    employee_id = random.choice(employees)
                    role = random.choices(ROLES, weights=ROLE_WEIGHTS)[0]
                    shift_start, shift_end = random.choice(SHIFTS)

                    scheduled_hours = (shift_end - shift_start) % 24
                    actual_hours = max(1, scheduled_hours + random.uniform(-0.5, 1.5))
                    hourly_rate = random.uniform(*HOURLY_RATES[role])
                    labor_cost = actual_hours * hourly_rate

                    # Estimate orders handled by this employee
                    orders_handled = int(daily_orders * (actual_hours / 24) * random.uniform(0.7, 1.2))

                    writer.writerow({
                        'schedule_id': schedule_id_counter,
                        'store_id': store_id,
                        'employee_id': employee_id,
                        'date': current_date.strftime('%Y-%m-%d'),
                        'shift_start_hour': shift_start,
                        'shift_end_hour': shift_end,
                        'role': role,
                        'scheduled_hours': round(scheduled_hours, 2),
                        'actual_hours': round(actual_hours, 2),
                        'hourly_rate': round(hourly_rate, 2),
                        'labor_cost': round(labor_cost, 2),
                        'orders_handled': orders_handled,
                    })

                    schedule_id_counter += 1
                    assigned_employees.add(employee_id)
                    row_count += 1

            current_date += timedelta(days=1)
            if row_count % 50000 == 0:
                print(f"  {row_count} rows written...", flush=True)

        print(f"Saved: {output_file} ({row_count} rows)")
    print()


# ============================================================================
# 3. SERVICE TIMES CSV
# ============================================================================
def generate_service_times():
    """Generate service time metrics by hour."""
    print("Generating service_times.csv...")

    output_file = os.path.join(OUTPUT_DIR, "service_times.csv")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                'date', 'store_id', 'hour', 'avg_counter_wait_secs', 'avg_kiosk_wait_secs',
                'avg_drive_thru_secs', 'avg_delivery_prep_secs', 'orders_served',
                'peak_wait_secs', 'staff_on_duty'
            ]
        )
        writer.writeheader()

        current_date = start_date
        row_count = 0

        while current_date <= end_date:
            day_of_week = current_date.weekday()
            month = current_date.month

            day_weight = DAY_WEIGHTS[day_of_week]
            month_weight = MONTH_WEIGHTS[month]

            for store in STORES:
                store_id = store['store_id']

                for hour in range(24):
                    hour_weight = HOUR_WEIGHTS.get(hour, 0.5)

                    # Determine if peak hour
                    is_peak = hour in [12, 13, 18, 19]
                    peak_multiplier = 1.5 if is_peak else 1.0

                    # Calculate wait times
                    avg_counter = random.randint(120, 300) * peak_multiplier * day_weight
                    avg_kiosk = random.randint(60, 180) * peak_multiplier * day_weight
                    avg_drive_thru = None if store['store_type'] != 'drive_thru' else random.randint(180, 400) * peak_multiplier * day_weight
                    avg_delivery_prep = random.randint(300, 600) * day_weight

                    # Staff on duty (more during peak hours)
                    base_staff = random.randint(3, 8)
                    staff_on_duty = int(base_staff * (1.5 if is_peak else 1.0))

                    # Orders served
                    daily_orders = int(store['avg_daily_orders'] * day_weight * month_weight)
                    orders_served = int(daily_orders * hour_weight / 24)

                    # Peak wait times
                    peak_wait = int(avg_counter * 1.5) if is_peak else int(avg_counter)

                    writer.writerow({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'store_id': store_id,
                        'hour': hour,
                        'avg_counter_wait_secs': round(avg_counter, 1),
                        'avg_kiosk_wait_secs': round(avg_kiosk, 1),
                        'avg_drive_thru_secs': round(avg_drive_thru, 1) if avg_drive_thru else '',
                        'avg_delivery_prep_secs': round(avg_delivery_prep, 1),
                        'orders_served': orders_served,
                        'peak_wait_secs': peak_wait,
                        'staff_on_duty': staff_on_duty,
                    })

                    row_count += 1

            current_date += timedelta(days=1)
            if row_count % 100000 == 0:
                print(f"  {row_count} rows written...", flush=True)

        print(f"Saved: {output_file} ({row_count} rows)")
    print()


# ============================================================================
# 4. EQUIPMENT LOGS CSV
# ============================================================================
def generate_equipment_logs():
    """Generate equipment maintenance and breakdown logs."""
    print("Generating equipment_logs.csv...")

    output_file = os.path.join(OUTPUT_DIR, "equipment_logs.csv")
    event_id_counter = 1

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                'event_id', 'store_id', 'equipment_type', 'event_date', 'event_type',
                'downtime_minutes', 'repair_cost', 'technician_id', 'description'
            ]
        )
        writer.writeheader()

        row_count = 0

        for store in STORES:
            store_id = store['store_id']

            # Generate preventive maintenance
            for equipment in EQUIPMENT_TYPES:
                maintenance_months = MAINTENANCE_MONTHS.get(equipment, [3, 6, 9, 12])

                for month in maintenance_months:
                    # Pick a random day in that month
                    maint_date = start_date.replace(month=month, day=15)
                    if maint_date > end_date or maint_date < start_date:
                        continue

                    writer.writerow({
                        'event_id': event_id_counter,
                        'store_id': store_id,
                        'equipment_type': equipment,
                        'event_date': maint_date.strftime('%Y-%m-%d'),
                        'event_type': 'preventive_maintenance',
                        'downtime_minutes': random.randint(30, 120),
                        'repair_cost': 0,
                        'technician_id': f"TECH-{random.randint(1000, 9999)}",
                        'description': f"Routine maintenance for {equipment}",
                    })
                    event_id_counter += 1
                    row_count += 1

            # Generate random breakdowns (1-3 per store per month)
            for month in range(1, 13):
                num_breakdowns = random.randint(1, 3)

                for _ in range(num_breakdowns):
                    breakdown_date = start_date.replace(month=month)
                    breakdown_date += timedelta(days=random.randint(0, 27))

                    if breakdown_date > end_date:
                        continue

                    equipment = random.choice(EQUIPMENT_TYPES)

                    # Ice cream machines break down more often (meme-accurate!)
                    if equipment == 'ice_cream_machine' and random.random() > 0.3:
                        event_type = 'breakdown'
                        downtime_minutes = random.randint(120, 480)
                        repair_cost = random.randint(1500, 8000)
                    else:
                        event_type = random.choice(['breakdown', 'repair', 'inspection'])
                        if event_type == 'breakdown':
                            downtime_minutes = random.randint(60, 360)
                            repair_cost = random.randint(500, 15000)
                        elif event_type == 'repair':
                            downtime_minutes = random.randint(30, 180)
                            repair_cost = random.randint(300, 5000)
                        else:  # inspection
                            downtime_minutes = random.randint(15, 60)
                            repair_cost = random.randint(0, 500)

                    writer.writerow({
                        'event_id': event_id_counter,
                        'store_id': store_id,
                        'equipment_type': equipment,
                        'event_date': breakdown_date.strftime('%Y-%m-%d'),
                        'event_type': event_type,
                        'downtime_minutes': downtime_minutes,
                        'repair_cost': repair_cost,
                        'technician_id': f"TECH-{random.randint(1000, 9999)}",
                        'description': f"{event_type.replace('_', ' ').title()} on {equipment}: {random.choice(['Unit malfunction', 'Performance degradation', 'Sensor issue', 'Electrical problem', 'Mechanical failure'])}",
                    })
                    event_id_counter += 1
                    row_count += 1

        print(f"Saved: {output_file} ({row_count} rows)")
    print()


# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    try:
        generate_inventory_daily()
        generate_labor_schedules()
        generate_service_times()
        generate_equipment_logs()

        print("=" * 60)
        print("All data generation complete!")
        print("=" * 60)
        print(f"\nOutput files created in: {OUTPUT_DIR}")
        print("\nGenerated files:")
        print("  1. inventory_daily.csv - ~2.19M rows (daily inventory)")
        print("  2. labor_schedules.csv - ~584K rows (labor schedules)")
        print("  3. service_times.csv - ~1.24M rows (service metrics)")
        print("  4. equipment_logs.csv - ~2K rows (equipment logs)")
        print()

    except Exception as e:
        print(f"Error during generation: {e}")
        import traceback
        traceback.print_exc()
