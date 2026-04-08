"""
POS Transaction Data Generator for ABC Restaurant Group GenBI Project

Generates synthetic POS transaction and line item data for all stores across 2023.
Data is partitioned by month (12 files each for transactions and line items).

Scale: ~200 stores × ~80 avg orders/day × 365 days ≈ 5.8M orders
Performance optimized: processes by store/month, uses batch writing
"""

import os
import csv
import random
from datetime import datetime, timedelta
from collections import defaultdict

# Import config from same directory
from config import (
    STORES, MENU_ITEMS, CATEGORIES, CHANNELS, PAYMENT_METHODS, PROMOTIONS,
    HOUR_WEIGHTS, DAY_WEIGHTS, MONTH_WEIGHTS, DATE_START, DATE_END
)

# Set random seed for reproducibility
random.seed(42)

# Constants
OUTPUT_DIR = "/Users/danshek/mcdhk-dashboard/genbi/raw/pos"
BATCH_SIZE = 5000  # Write to CSV in batches

# Channel distribution (percentages)
CHANNEL_DISTRIBUTION = {
    'counter': 0.30,
    'kiosk': 0.35,
    'mobile_app': 0.15,
    'delivery': 0.12,
    'drive_thru': 0.08
}

# Payment method distribution (percentages)
PAYMENT_DISTRIBUTION = {
    'cash': 0.15,
    'octopus': 0.35,
    'visa': 0.15,
    'mastercard': 0.10,
    'apple_pay': 0.12,
    'alipay': 0.08,
    'wechat_pay': 0.05
}

# Item quantity distribution
QUANTITY_DISTRIBUTION = {
    1: 0.15,  # 15% single item
    2: 0.45,  # 45% double
    3: 0.30,  # 30% triple
    4: 0.10   # 10% quad
}

# Breakfast category ID (typically 5)
BREAKFAST_CATEGORY_ID = 5

# Loyalty customer probability
LOYALTY_PROBABILITY = 0.40


def parse_date(date_str):
    """Parse date string to datetime"""
    return datetime.strptime(date_str, "%Y-%m-%d")


def get_date_range():
    """Get all dates in the range"""
    start = parse_date(DATE_START)
    end = parse_date(DATE_END)
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def generate_transaction_id(year, month, day, store_id, seq):
    """Generate transaction ID: TXN-YYYYMMDD-SXXX-NNNNN"""
    date_str = f"{year:04d}{month:02d}{day:02d}"
    store_code = store_id if isinstance(store_id, str) else f"S{store_id:03d}"
    seq_code = f"{seq:05d}"
    return f"TXN-{date_str}-{store_code}-{seq_code}"


def get_applicable_promotions(order_date, item_ids):
    """Get active promotions for a given date and items"""
    applicable = []
    for promo in PROMOTIONS:
        promo_start = parse_date(promo['start_date'])
        promo_end = parse_date(promo['end_date'])

        if promo_start <= order_date <= promo_end:
            # Check if any of the order items are in applicable items
            raw = promo.get('applicable_items', [])
            applicable_items = set(int(x) for x in raw.split(',')) if isinstance(raw, str) else set(raw)
            if applicable_items and any(item_id in applicable_items for item_id in item_ids):
                applicable.append(promo)

    return applicable


def get_channel_for_store(store_type):
    """Get channel distribution for a store type"""
    channels_dist = CHANNEL_DISTRIBUTION.copy()

    # If not a drive-thru store, redistribute drive_thru probability to counter
    if store_type != 'drive_thru':
        drive_thru_prob = channels_dist.pop('drive_thru', 0)
        channels_dist['counter'] += drive_thru_prob

    return channels_dist


def select_weighted_item(candidates, weights_dict):
    """Select an item from candidates based on weights"""
    if not candidates:
        return None

    weights = [weights_dict.get(item.get('item_id'), 1.0) for item in candidates]
    return random.choices(candidates, weights=weights, k=1)[0]


def get_available_items(hour, menu_items):
    """Filter menu items based on availability (breakfast hours)"""
    available = []
    for item in menu_items:
        category_id = item.get('category_id')

        # Breakfast only 7-11
        if category_id == BREAKFAST_CATEGORY_ID and (hour < 7 or hour >= 11):
            continue

        available.append(item)

    return available


def get_menu_weights(month, available_items):
    """Get item popularity weights based on month"""
    weights = {}
    is_summer = month in [6, 7, 8]  # June, July, August

    for item in available_items:
        item_id = item['item_id']
        category_id = item.get('category_id')

        # Base weights by category (burgers most popular)
        if category_id == 1:  # Burgers
            weights[item_id] = 3.0
        elif category_id == 2:  # Chicken
            weights[item_id] = 2.5
        elif category_id == 3:  # Sides
            weights[item_id] = 1.5
        elif category_id == 4:  # Beverages
            weights[item_id] = 2.0
        elif category_id == 5:  # Breakfast
            weights[item_id] = 2.0
        elif category_id == 6:  # Desserts
            weights[item_id] = 1.0 if not is_summer else 2.5
        else:
            weights[item_id] = 1.0

    return weights


def generate_order_date_time(order_date, hour_weights):
    """Generate realistic order time based on hour weights"""
    # Select hour based on weights
    hours = list(range(24))
    hour_dist = [hour_weights.get(h, 0.1) for h in hours]
    hour = random.choices(hours, weights=hour_dist, k=1)[0]

    # Select minute randomly
    minute = random.randint(0, 59)

    return hour, minute


def generate_quantity():
    """Generate item quantity based on distribution"""
    quantities = list(QUANTITY_DISTRIBUTION.keys())
    weights = list(QUANTITY_DISTRIBUTION.values())
    return random.choices(quantities, weights=weights, k=1)[0]


def generate_line_items(order_date, hour, available_items, menu_weights, num_items):
    """Generate line items for an order"""
    items = []

    for _ in range(num_items):
        item = select_weighted_item(available_items, menu_weights)
        if item is None:
            continue

        quantity = generate_quantity()
        line_total = item['unit_price'] * quantity
        cogs_amount = item['cogs'] * quantity

        items.append({
            'item_id': item['item_id'],
            'item_name': item['item_name'],
            'category_id': item['category_id'],
            'quantity': quantity,
            'unit_price': item['unit_price'],
            'line_total': line_total,
            'cogs_amount': cogs_amount
        })

    return items


def generate_transactions_for_store_month(store, year, month, menu_weights, available_items, hour_weights):
    """Generate all transactions for a store in a given month"""
    transactions = []

    # Get number of days in the month
    if month == 12:
        next_month = parse_date(f"{year+1}-01-01")
    else:
        next_month = parse_date(f"{year}-{month+1:02d}-01")

    current_month = parse_date(f"{year}-{month:02d}-01")
    days_in_month = (next_month - current_month).days

    # Generate transactions for each day in the month
    for day in range(1, days_in_month + 1):
        order_date = current_month + timedelta(days=day-1)
        day_of_week = order_date.strftime("%A")

        # Calculate number of orders for this day
        avg_daily = store['avg_daily_orders']
        day_weight = DAY_WEIGHTS.get(day_of_week, 1.0)
        month_weight = MONTH_WEIGHTS.get(month, 1.0)

        # Random variation: 50-150% of calculated average
        variation = random.uniform(0.5, 1.5)
        num_orders = max(1, int(avg_daily * day_weight * month_weight * variation))

        # Generate transactions
        for seq in range(1, num_orders + 1):
            hour, minute = generate_order_date_time(order_date, hour_weights)

            # Select channel
            channel_dist = get_channel_for_store(store['store_type'])
            channel_name = random.choices(
                list(channel_dist.keys()),
                weights=list(channel_dist.values()),
                k=1
            )[0]
            channel_id = next(c['channel_id'] for c in CHANNELS if c['channel_name'] == channel_name)

            # Select payment method
            payment_name = random.choices(
                list(PAYMENT_DISTRIBUTION.keys()),
                weights=list(PAYMENT_DISTRIBUTION.values()),
                k=1
            )[0]
            payment_id = next(p['payment_id'] for p in PAYMENT_METHODS if p['payment_name'] == payment_name)

            # Generate line items
            num_items = generate_quantity()
            line_items = generate_line_items(order_date, hour, available_items, menu_weights, num_items)

            if not line_items:
                continue

            # Calculate totals
            subtotal = sum(item['line_total'] for item in line_items)

            # Check for applicable promotions
            item_ids = [item['item_id'] for item in line_items]
            applicable_promos = get_applicable_promotions(order_date, item_ids)

            promo_id = None
            discount_amount = 0
            if applicable_promos:
                promo = random.choice(applicable_promos)
                promo_id = promo['promo_id']
                # Apply discount to applicable items
                raw_ai = promo.get('applicable_items', [])
                applicable_item_ids = set(int(x) for x in raw_ai.split(',')) if isinstance(raw_ai, str) else set(raw_ai)
                discount_amount = sum(
                    item['line_total'] * (promo['discount_pct'] / 100)
                    for item in line_items
                    if item['item_id'] in applicable_item_ids
                )

            # Tax is 0% in HK
            tax_amount = 0

            # Total
            total_amount = subtotal - discount_amount + tax_amount

            # Loyalty customer (~40% have customer_id)
            customer_id = None
            if random.random() < LOYALTY_PROBABILITY:
                customer_id = f"CUST-{random.randint(100000, 999999)}"

            transaction = {
                'transaction_id': generate_transaction_id(year, month, day, store['store_id'], seq),
                'store_id': store['store_id'],
                'order_date': order_date.strftime("%Y-%m-%d"),
                'order_hour': hour,
                'order_minute': minute,
                'day_of_week': day_of_week,
                'channel_id': channel_id,
                'payment_id': payment_id,
                'promo_id': promo_id,
                'customer_id': customer_id,
                'subtotal': round(subtotal, 2),
                'discount_amount': round(discount_amount, 2),
                'tax_amount': 0,
                'total_amount': round(total_amount, 2),
                'order_item_count': len(line_items),
                'line_items': line_items
            }

            transactions.append(transaction)

    return transactions


def write_transactions_batch(file_handle, transactions, write_header=False):
    """Write transaction batch to CSV"""
    writer = csv.writer(file_handle)

    if write_header:
        writer.writerow([
            'transaction_id', 'store_id', 'order_date', 'order_hour', 'order_minute',
            'day_of_week', 'channel_id', 'payment_id', 'promo_id', 'customer_id',
            'subtotal', 'discount_amount', 'tax_amount', 'total_amount', 'order_item_count'
        ])

    for txn in transactions:
        writer.writerow([
            txn['transaction_id'],
            txn['store_id'],
            txn['order_date'],
            txn['order_hour'],
            txn['order_minute'],
            txn['day_of_week'],
            txn['channel_id'],
            txn['payment_id'],
            txn['promo_id'] or '',
            txn['customer_id'] or '',
            txn['subtotal'],
            txn['discount_amount'],
            txn['tax_amount'],
            txn['total_amount'],
            txn['order_item_count']
        ])


def write_line_items_batch(file_handle, line_item_id_counter, transactions, write_header=False):
    """Write line items batch to CSV"""
    writer = csv.writer(file_handle)

    if write_header:
        writer.writerow([
            'line_item_id', 'transaction_id', 'item_id', 'item_name', 'category_id',
            'quantity', 'unit_price', 'line_total', 'cogs_amount'
        ])

    for txn in transactions:
        for item in txn['line_items']:
            line_item_id = f"LI-{line_item_id_counter:08d}"
            line_item_id_counter += 1

            writer.writerow([
                line_item_id,
                txn['transaction_id'],
                item['item_id'],
                item['item_name'],
                item['category_id'],
                item['quantity'],
                item['unit_price'],
                item['line_total'],
                item['cogs_amount']
            ])

    return line_item_id_counter


def main():
    """Main entry point"""
    print(f"Starting POS data generation...")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Date range: {DATE_START} to {DATE_END}")
    print(f"Number of stores: {len(STORES)}")
    print(f"Number of menu items: {len(MENU_ITEMS)}")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Parse date range
    start_date = parse_date(DATE_START)
    end_date = parse_date(DATE_END)

    # Get month/year combinations
    months_to_process = []
    current = start_date
    while current <= end_date:
        months_to_process.append((current.year, current.month))
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    # Get hour weights from config
    hour_weights = HOUR_WEIGHTS if HOUR_WEIGHTS else {h: 1.0 for h in range(24)}

    # Track global line item counter
    line_item_id_counter = 1
    total_transactions = 0
    total_line_items = 0

    # Process each month
    for month_idx, (year, month) in enumerate(months_to_process):
        print(f"\nProcessing {year}-{month:02d}...")

        txn_file_path = os.path.join(OUTPUT_DIR, f"pos_transactions_{year}_{month:02d}.csv")
        li_file_path = os.path.join(OUTPUT_DIR, f"pos_line_items_{year}_{month:02d}.csv")

        # Open files for writing
        txn_file = open(txn_file_path, 'w', newline='', buffering=1)
        li_file = open(li_file_path, 'w', newline='', buffering=1)

        txn_writer_initialized = False
        li_writer_initialized = False

        # Process each store
        for store_idx, store in enumerate(STORES):
            if (store_idx + 1) % 10 == 0:
                print(f"  Processing store {store_idx + 1}/{len(STORES)}...")

            # Get available items (handle breakfast hours)
            available_items = get_available_items(12, MENU_ITEMS)  # Use midday for general availability

            # Get menu weights for this month
            menu_weights = get_menu_weights(month, available_items)

            # Generate transactions for this store and month
            transactions = generate_transactions_for_store_month(
                store, year, month, menu_weights, available_items, hour_weights
            )

            if transactions:
                # Write transactions
                write_transactions_batch(
                    txn_file,
                    transactions,
                    write_header=(not txn_writer_initialized)
                )
                txn_writer_initialized = True

                # Write line items
                line_item_id_counter = write_line_items_batch(
                    li_file,
                    line_item_id_counter,
                    transactions,
                    write_header=(not li_writer_initialized)
                )
                li_writer_initialized = True

                total_transactions += len(transactions)
                total_line_items += sum(txn['order_item_count'] for txn in transactions)

        # Close files
        txn_file.close()
        li_file.close()

        print(f"  Completed {year}-{month:02d}")
        print(f"    Transactions file: {txn_file_path}")
        print(f"    Line items file: {li_file_path}")

    print(f"\nData generation completed!")
    print(f"Total transactions: {total_transactions:,}")
    print(f"Total line items: {total_line_items:,}")
    print(f"Files written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
