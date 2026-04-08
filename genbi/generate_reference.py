"""
ABC Restaurant Group GenBI Project - Reference Data Generator
Generates CSV files for dimension/reference tables
"""

import csv
import os
from config import (
    STORES,
    MENU_ITEMS,
    CATEGORIES,
    CHANNELS,
    PAYMENT_METHODS,
    PROMOTIONS,
)

# Output directory
OUTPUT_DIR = "/Users/danshek/mcdhk-dashboard/genbi/raw/reference"

def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_stores_csv():
    """Generate stores.csv with all 200 store records."""
    filepath = os.path.join(OUTPUT_DIR, "stores.csv")
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "store_id",
                "store_name",
                "district",
                "region",
                "store_type",
                "avg_daily_orders",
                "open_date",
                "rent_monthly",
            ],
        )
        writer.writeheader()
        writer.writerows(STORES)
    
    print(f"Generated {filepath} with {len(STORES)} stores")


def generate_menu_items_csv():
    """Generate menu_items.csv with all 30 items."""
    filepath = os.path.join(OUTPUT_DIR, "menu_items.csv")
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["item_id", "item_name", "category_id", "unit_price", "cogs", "is_lto"],
        )
        writer.writeheader()
        for item in MENU_ITEMS:
            # Convert boolean to 0/1 for CSV
            item_row = item.copy()
            item_row["is_lto"] = 1 if item_row["is_lto"] else 0
            writer.writerow(item_row)
    
    print(f"Generated {filepath} with {len(MENU_ITEMS)} items")


def generate_categories_csv():
    """Generate categories.csv with all 8 categories."""
    filepath = os.path.join(OUTPUT_DIR, "categories.csv")
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["category_id", "category_name"],
        )
        writer.writeheader()
        writer.writerows(CATEGORIES)
    
    print(f"Generated {filepath} with {len(CATEGORIES)} categories")


def generate_channels_csv():
    """Generate channels.csv with all 5 channels."""
    filepath = os.path.join(OUTPUT_DIR, "channels.csv")
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["channel_id", "channel_name"],
        )
        writer.writeheader()
        writer.writerows(CHANNELS)
    
    print(f"Generated {filepath} with {len(CHANNELS)} channels")


def generate_payment_methods_csv():
    """Generate payment_methods.csv with all 7 payment methods."""
    filepath = os.path.join(OUTPUT_DIR, "payment_methods.csv")
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["payment_id", "payment_name"],
        )
        writer.writeheader()
        writer.writerows(PAYMENT_METHODS)
    
    print(f"Generated {filepath} with {len(PAYMENT_METHODS)} payment methods")


def generate_promotions_csv():
    """Generate promotions.csv with all 12 promotions."""
    filepath = os.path.join(OUTPUT_DIR, "promotions.csv")
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "promo_id",
                "promo_name",
                "promo_type",
                "discount_pct",
                "start_date",
                "end_date",
                "applicable_items",
            ],
        )
        writer.writeheader()
        writer.writerows(PROMOTIONS)
    
    print(f"Generated {filepath} with {len(PROMOTIONS)} promotions")


def main():
    """Generate all reference CSV files."""
    ensure_output_dir()
    
    print("Generating ABC Restaurant Group GenBI reference data...")
    print(f"Output directory: {OUTPUT_DIR}\n")
    
    generate_stores_csv()
    generate_menu_items_csv()
    generate_categories_csv()
    generate_channels_csv()
    generate_payment_methods_csv()
    generate_promotions_csv()
    
    print("\nAll reference data generated successfully!")


if __name__ == "__main__":
    main()
