#!/usr/bin/env python3
"""
McDonald's HK GenBI - Market and Financial Data Generation
Generates synthetic market indicators, competitor pricing, and financial data
for 200 McDonald's stores across Hong Kong for 2023.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

from config import STORES, MENU_ITEMS, DATE_START, DATE_END


# Output directories
MARKET_DIR = Path(__file__).parent / "raw" / "market"
FINANCIAL_DIR = Path(__file__).parent / "raw" / "financial"

# Configuration
random.seed(42)
COMPETITORS = [
    {"name": "KFC", "items_count": 18, "price_multiplier": 0.92},
    {"name": "Burger King", "items_count": 20, "price_multiplier": 1.05},
    {"name": "MOS Burger", "items_count": 15, "price_multiplier": 1.08},
    {"name": "Jollibee", "items_count": 16, "price_multiplier": 0.88},
    {"name": "Shake Shack", "items_count": 12, "price_multiplier": 1.40},
]

HK_DISTRICTS = [
    "Central_Western", "Wan_Chai", "Eastern", "Southern", "Yau_Tsim_Mong",
    "Sham_Shui_Po", "Kowloon_City", "Wong_Tai_Sin", "Kwun_Tong", "Sha_Tin",
    "Tai_Po", "North", "Sai_Kung", "Yuen_Long", "Tuen_Mun", "Tsuen_Wan",
    "Kwai_Tsing", "Islands"
]

TOURIST_DISTRICTS = {"Central_Western", "Wan_Chai", "Yau_Tsim_Mong"}

EXPENSE_CATEGORIES = [
    "labor", "rent", "utilities", "maintenance", "marketing",
    "insurance", "supplies", "technology", "training", "miscellaneous"
]

SUPPLIERS = [
    "HK Food Supply Co",
    "Pacific Meats Ltd",
    "Fresh Produce HK",
    "Golden Dragon Beverages",
    "Star Foods Distribution",
    "North Asian Logistics",
    "Premium Dairy Solutions",
    "Sunshine Grains Ltd",
    "Ocean Fresh Seafood",
    "Chef's Choice Ingredients"
]

MENU_EQUIVALENTS = {
    "Big Mac": ["Big Mac", "Signature Burger", "Premium Burger", "Chicken Burger"],
    "Chicken McNuggets": ["Crispy Chicken", "Fried Chicken", "Chicken Strips"],
    "Fries": ["Fries", "Chips", "Shoestring Potatoes"],
    "Soft Drink": ["Coca-Cola", "Soft Drink", "Beverage", "Soda"],
    "McCafé Coffee": ["Coffee", "Cappuccino", "Espresso"],
}

MONTHS = [
    ("2023-01-01", 31), ("2023-02-01", 28), ("2023-03-01", 31),
    ("2023-04-01", 30), ("2023-05-01", 31), ("2023-06-01", 30),
    ("2023-07-01", 31), ("2023-08-01", 31), ("2023-09-01", 30),
    ("2023-10-01", 31), ("2023-11-01", 30), ("2023-12-01", 31),
]


def ensure_directories():
    """Ensure output directories exist."""
    MARKET_DIR.mkdir(parents=True, exist_ok=True)
    FINANCIAL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directories ready: {MARKET_DIR}, {FINANCIAL_DIR}")


def get_district_unemployment(district):
    """Get base unemployment rate by district."""
    unemployment_base = {
        "Central_Western": 3.1, "Wan_Chai": 3.2, "Eastern": 3.4,
        "Southern": 3.5, "Yau_Tsim_Mong": 3.6, "Sham_Shui_Po": 4.2,
        "Kowloon_City": 3.8, "Wong_Tai_Sin": 4.0, "Kwun_Tong": 3.9,
        "Sha_Tin": 3.5, "Tai_Po": 3.7, "North": 3.9,
        "Sai_Kung": 3.3, "Yuen_Long": 4.1, "Tuen_Mun": 4.3,
        "Tsuen_Wan": 3.8, "Kwai_Tsing": 3.6, "Islands": 3.9,
    }
    return unemployment_base.get(district, 3.7)


def get_district_income(district):
    """Get base median household income by district."""
    income_base = {
        "Central_Western": 42000, "Wan_Chai": 40000, "Eastern": 38000,
        "Southern": 35000, "Yau_Tsim_Mong": 32000, "Sham_Shui_Po": 28000,
        "Kowloon_City": 31000, "Wong_Tai_Sin": 30000, "Kwun_Tong": 32000,
        "Sha_Tin": 36000, "Tai_Po": 35000, "North": 33000,
        "Sai_Kung": 37000, "Yuen_Long": 31000, "Tuen_Mun": 29000,
        "Tsuen_Wan": 34000, "Kwai_Tsing": 33000, "Islands": 30000,
    }
    return income_base.get(district, 35000)


def get_district_population(district):
    """Get approximate population by district."""
    population_base = {
        "Central_Western": 243000, "Wan_Chai": 180000, "Eastern": 580000,
        "Southern": 310000, "Yau_Tsim_Mong": 360000, "Sham_Shui_Po": 340000,
        "Kowloon_City": 390000, "Wong_Tai_Sin": 460000, "Kwun_Tong": 620000,
        "Sha_Tin": 640000, "Tai_Po": 310000, "North": 300000,
        "Sai_Kung": 420000, "Yuen_Long": 560000, "Tuen_Mun": 480000,
        "Tsuen_Wan": 430000, "Kwai_Tsing": 320000, "Islands": 240000,
    }
    return population_base.get(district, 400000)


def get_foot_traffic_multiplier(month_num):
    """Get seasonal foot traffic multiplier (100=baseline)."""
    if month_num in [7, 8, 12]:  # July, August, December (tourism & holidays)
        return random.uniform(110, 130)
    elif month_num in [1, 2]:  # January, February (winter tourism)
        return random.uniform(105, 120)
    else:  # Regular months
        return random.uniform(95, 110)


def generate_competitor_pricing():
    """Generate competitor pricing data."""
    print("Generating competitor pricing data...")
    rows = []

    for date_str, _ in MONTHS:
        snapshot_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        for competitor in COMPETITORS:
            comp_name = competitor["name"]
            items_count = competitor["items_count"]
            price_mult = competitor["price_multiplier"]

            # Select random menu items for this competitor
            selected_items = random.sample(range(len(MENU_ITEMS)), min(items_count, len(MENU_ITEMS)))

            for item_idx in selected_items:
                item = MENU_ITEMS[item_idx]
                mcd_price = item["unit_price"]

                # Add some variance to competitor pricing
                comp_price = mcd_price * price_mult * random.uniform(0.95, 1.05)
                price_diff = comp_price - mcd_price
                price_index = mcd_price / comp_price if comp_price > 0 else 0

                rows.append({
                    "snapshot_date": snapshot_date,
                    "competitor_name": comp_name,
                    "item_equivalent": item["item_name"],
                    "competitor_price_hkd": round(comp_price, 2),
                    "mcdonalds_price_hkd": mcd_price,
                    "price_difference": round(price_diff, 2),
                    "price_index": round(price_index, 3),
                })

    output_file = MARKET_DIR / "competitor_pricing.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "snapshot_date", "competitor_name", "item_equivalent",
            "competitor_price_hkd", "mcdonalds_price_hkd", "price_difference", "price_index"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Generated {len(rows)} competitor pricing records -> {output_file}")


def generate_market_indicators():
    """Generate market indicators by district and month."""
    print("Generating market indicators...")
    rows = []

    for date_str, days_in_month in MONTHS:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        month_num = dt.month

        for district in HK_DISTRICTS:
            base_unemployment = get_district_unemployment(district)
            unemployment = base_unemployment + random.uniform(-0.3, 0.3)

            base_income = get_district_income(district)
            median_income = base_income * random.uniform(0.98, 1.02)

            population = get_district_population(district)

            foot_traffic_index = get_foot_traffic_multiplier(month_num)

            retail_sales_index = 100 + random.uniform(-15, 20)
            if month_num in [11, 12]:
                retail_sales_index = 100 + random.uniform(20, 40)

            tourist_arrivals = None
            if district in TOURIST_DISTRICTS:
                base_arrivals = 50000 if district == "Central_Western" else 30000
                if month_num in [7, 8, 12]:
                    tourist_arrivals = int(base_arrivals * random.uniform(1.3, 1.6))
                else:
                    tourist_arrivals = int(base_arrivals * random.uniform(0.8, 1.2))

            new_businesses = random.randint(5, 25)

            rows.append({
                "month": date_str,
                "district": district,
                "unemployment_rate_pct": round(unemployment, 2),
                "median_household_income_hkd": round(median_income, 0),
                "population": int(population),
                "foot_traffic_index": round(foot_traffic_index, 1),
                "retail_sales_index": round(retail_sales_index, 1),
                "tourist_arrivals": tourist_arrivals,
                "new_businesses_opened": new_businesses,
            })

    output_file = MARKET_DIR / "market_indicators.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "month", "district", "unemployment_rate_pct", "median_household_income_hkd",
            "population", "foot_traffic_index", "retail_sales_index", "tourist_arrivals",
            "new_businesses_opened"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Generated {len(rows)} market indicator records -> {output_file}")


def generate_store_pnl():
    """Generate store P&L data."""
    print("Generating store P&L data...")
    rows = []

    for date_str, days_in_month in MONTHS:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        month_num = dt.month

        # Seasonal multipliers
        if month_num in [7, 8, 12]:
            season_mult = random.uniform(1.08, 1.15)
        elif month_num in [1, 2]:
            season_mult = random.uniform(1.05, 1.10)
        else:
            season_mult = random.uniform(0.95, 1.05)

        for store in STORES:
            store_id = store["store_id"]
            avg_daily_orders = store["avg_daily_orders"]
            rent_monthly = store["rent_monthly"]
            store_type = store["store_type"]

            # Calculate revenue
            avg_order_value = 55  # HK$
            base_revenue = avg_daily_orders * avg_order_value * days_in_month
            revenue = base_revenue * season_mult * random.uniform(0.95, 1.05)

            # COGS (32-38% of revenue)
            cogs_pct = random.uniform(0.32, 0.38)
            cogs = revenue * cogs_pct

            gross_profit = revenue - cogs
            gross_margin_pct = (gross_profit / revenue * 100) if revenue > 0 else 0

            # Labor cost (25-30% of revenue, slightly higher for mall stores)
            labor_pct = random.uniform(0.25, 0.30) if store_type == "mall" else random.uniform(0.24, 0.28)
            labor_cost = revenue * labor_pct

            # Utilities (higher in summer)
            if month_num in [6, 7, 8]:
                utilities = random.uniform(35000, 50000)
            else:
                utilities = random.uniform(15000, 30000)

            # Marketing allocation (3-5% of revenue)
            marketing = revenue * random.uniform(0.03, 0.05)

            # Other opex
            other_opex = random.uniform(8000, 20000)

            # EBITDA
            ebitda = revenue - cogs - labor_cost - rent_monthly - utilities - marketing - other_opex

            # Depreciation
            depreciation = random.uniform(8000, 15000)

            # Net profit
            net_profit = ebitda - depreciation
            net_margin_pct = (net_profit / revenue * 100) if revenue > 0 else 0

            rows.append({
                "month": date_str,
                "store_id": store_id,
                "revenue": round(revenue, 2),
                "cogs": round(cogs, 2),
                "gross_profit": round(gross_profit, 2),
                "labor_cost": round(labor_cost, 2),
                "rent": round(rent_monthly, 2),
                "utilities": round(utilities, 2),
                "marketing_allocation": round(marketing, 2),
                "other_opex": round(other_opex, 2),
                "ebitda": round(ebitda, 2),
                "depreciation": round(depreciation, 2),
                "net_profit": round(net_profit, 2),
                "gross_margin_pct": round(gross_margin_pct, 2),
                "net_margin_pct": round(net_margin_pct, 2),
            })

    output_file = FINANCIAL_DIR / "store_pnl.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "month", "store_id", "revenue", "cogs", "gross_profit", "labor_cost",
            "rent", "utilities", "marketing_allocation", "other_opex", "ebitda",
            "depreciation", "net_profit", "gross_margin_pct", "net_margin_pct"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Generated {len(rows)} store P&L records -> {output_file}")


def generate_cogs_detail():
    """Generate COGS detail by item and month."""
    print("Generating COGS detail...")
    rows = []

    for date_str, _ in MONTHS:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        month_num = dt.month

        # Supply chain variance by season (±5%)
        if month_num in [7, 8, 9]:  # Typhoon season
            supply_variance = random.uniform(-0.05, 0.03)
            supply_reliability = random.uniform(0.92, 0.96)
        else:
            supply_variance = random.uniform(-0.03, 0.05)
            supply_reliability = random.uniform(0.95, 0.99)

        for item in MENU_ITEMS:
            item_id = item["item_id"]
            item_name = item["item_name"]
            category_id = item["category_id"]
            base_cogs = item["cogs"]
            unit_price = item["unit_price"]

            # Apply supply variance
            avg_unit_cogs = base_cogs * (1 + supply_variance)
            food_cost_pct = (avg_unit_cogs / unit_price * 100) if unit_price > 0 else 0

            supplier = random.choice(SUPPLIERS)

            rows.append({
                "month": date_str,
                "item_id": item_id,
                "item_name": item_name,
                "category_id": category_id,
                "avg_unit_cogs": round(avg_unit_cogs, 2),
                "avg_unit_price": unit_price,
                "food_cost_pct": round(food_cost_pct, 2),
                "supplier_name": supplier,
                "supply_reliability_pct": round(supply_reliability * 100, 1),
            })

    output_file = FINANCIAL_DIR / "cogs_detail.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "month", "item_id", "item_name", "category_id", "avg_unit_cogs",
            "avg_unit_price", "food_cost_pct", "supplier_name", "supply_reliability_pct"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Generated {len(rows)} COGS detail records -> {output_file}")


def generate_opex_breakdown():
    """Generate detailed opex breakdown by store, month, and category."""
    print("Generating opex breakdown...")
    rows = []

    for date_str, _ in MONTHS:
        for store in STORES:
            store_id = store["store_id"]
            rent_monthly = store["rent_monthly"]

            for category in EXPENSE_CATEGORIES:
                # Generate category-specific expenses
                if category == "labor":
                    base = random.uniform(120000, 200000)
                elif category == "rent":
                    base = rent_monthly
                elif category == "utilities":
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    if dt.month in [6, 7, 8]:
                        base = random.uniform(35000, 50000)
                    else:
                        base = random.uniform(15000, 30000)
                elif category == "maintenance":
                    base = random.uniform(10000, 25000)
                elif category == "marketing":
                    base = random.uniform(20000, 40000)
                elif category == "insurance":
                    base = random.uniform(15000, 25000)
                elif category == "supplies":
                    base = random.uniform(25000, 50000)
                elif category == "technology":
                    base = random.uniform(5000, 15000)
                elif category == "training":
                    base = random.uniform(3000, 12000)
                else:  # miscellaneous
                    base = random.uniform(8000, 20000)

                # Budget variance (±10% typically)
                variance_pct = random.uniform(-10, 10)
                amount_hkd = base * (1 + variance_pct / 100)
                budget_hkd = base

                rows.append({
                    "month": date_str,
                    "store_id": store_id,
                    "expense_category": category,
                    "amount_hkd": round(amount_hkd, 2),
                    "budget_hkd": round(budget_hkd, 2),
                    "variance_pct": round(variance_pct, 2),
                })

    output_file = FINANCIAL_DIR / "opex_breakdown.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "month", "store_id", "expense_category", "amount_hkd", "budget_hkd", "variance_pct"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Generated {len(rows)} opex breakdown records -> {output_file}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("McDonald's HK GenBI - Market & Financial Data Generation")
    print("=" * 70)

    ensure_directories()

    generate_competitor_pricing()
    generate_market_indicators()
    generate_store_pnl()
    generate_cogs_detail()
    generate_opex_breakdown()

    print("\n" + "=" * 70)
    print("Data generation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
