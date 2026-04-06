"""
McDonald's HK GenBI - Customer Data Generator
Generates synthetic customer profiles, loyalty transactions, and feedback surveys
Run with: python3 generate_customer.py
"""

import random
import csv
from datetime import datetime, timedelta
from config import STORES, DATE_START, DATE_END, MONTH_WEIGHTS, DAY_WEIGHTS, HOUR_WEIGHTS
import os

# Set seed for reproducibility
random.seed(42)

# Configuration
NUM_CUSTOMERS = 50000
NUM_LOYALTY_TXN_MULTIPLIER = 4  # ~200K transactions
SURVEY_RATE = 0.015  # ~1.5% of orders result in a survey

# Age distribution
AGE_DISTRIBUTION = {
    "under_18": 0.15,
    "18_24": 0.25,
    "25_34": 0.30,
    "35_44": 0.15,
    "45_54": 0.10,
    "55_plus": 0.05,
}

# Loyalty tier distribution and behavior
LOYALTY_TIERS = {
    "bronze": {"weight": 0.50, "orders": (5, 30), "frequency": (1, 3), "earn_rate": 0.60},
    "silver": {"weight": 0.30, "orders": (30, 80), "frequency": (3, 6), "earn_rate": 0.65},
    "gold": {"weight": 0.15, "orders": (80, 200), "frequency": (6, 12), "earn_rate": 0.70},
    "platinum": {"weight": 0.05, "orders": (200, 500), "frequency": (12, 25), "earn_rate": 0.75},
}

# Reward redemptions
REWARD_TYPES = {
    "free_item": {"weight": 0.5, "points": 50},
    "discount": {"weight": 0.35, "points": 30},
    "upgrade": {"weight": 0.15, "points": 20},
}

# Survey feedback templates
FEEDBACK_TEMPLATES = [
    "Great food, fast service!",
    "Long wait time during lunch",
    "Ice cream machine was broken again",
    "Love the new Bulgogi Burger!",
    "Staff were very friendly",
    "Order was wrong, missing fries",
    "Clean restaurant, nice atmosphere",
    "Portions are getting smaller",
    "Best McDonald's in HK",
    "Service was slow today",
    "Food was hot and fresh",
    "Prices are too high",
    "Very convenient location",
    "Cashier was helpful and polite",
    "Quality varies too much",
    "Great place for family breakfast",
    "WiFi connection is unstable",
    "Seating area is always packed",
    "Good value for money",
    "Delivery took too long",
    "Loved the limited-time offer burger",
    "Order accuracy could be better",
    "Restaurant was clean and well-maintained",
    "Staff knowledge about menu is weak",
    "Perfect spot for quick lunch",
    "Fries were soggy",
    "Excellent customer service",
    "Too noisy, hard to have a conversation",
    "Happy Meal toys were great",
    "Kiosk ordering is convenient",
    "Always fresh ingredients",
    "Drive-thru line was too long",
    "Would come back for sure",
    "Parking is difficult here",
    "Mobile app ordering is smooth",
    "Bathroom facilities need improvement",
    "Great combo deals",
    "Service was impeccable",
    "Not as good as before",
    "Must-visit location",
    "Staff training needs improvement",
    "Food quality is consistent",
    "Ambiance could be better",
    "Friendly manager helped with my issue",
    "App promotions are great",
    "Would definitely recommend",
    "Crowded but worth the wait",
    "New menu items are delicious",
    "Online ordering is easy",
    "Excellent breakfast options",
]

# HK Districts
HK_DISTRICTS = [
    "Central", "Wan Chai", "Causeway Bay", "Admiralty", "Repulse Bay",
    "Stanley", "Tsim Sha Tsui", "Mong Kok", "Yau Tong", "Kwun Tong",
    "Sha Tin", "Tai Wai", "New Territories", "Lantau", "Tuen Mun",
    "Yuen Long", "Shatin Central", "Sha Tin Wai", "Tai Po", "Fanling",
    "Hung Hom", "Sham Shui Po", "Kowloon Tong", "Wong Tai Sin", "Lam Tin",
    "Tseung Kwan O", "Sai Kung", "Clear Water Bay", "North Point", "Quarry Bay",
]

# Helper functions
def parse_date(date_str):
    """Parse date string to datetime"""
    return datetime.strptime(date_str, "%Y-%m-%d")

def get_nearby_stores(customer_district, stores, max_distance=2):
    """Get stores in same or nearby districts"""
    customer_stores = [s for s in stores if s["district"] == customer_district]
    if len(customer_stores) >= 3:
        return customer_stores
    # If not enough in same district, add some from other districts
    other_stores = [s for s in stores if s["district"] != customer_district]
    return customer_stores + other_stores[:5]

def generate_customer_profiles():
    """Generate customer profile data"""
    print("Generating customer profiles...")
    customers = []
    start_date = parse_date(DATE_START)
    end_date = parse_date(DATE_END)

    for i in range(1, NUM_CUSTOMERS + 1):
        customer_id = f"CUST-{i:05d}"
        age_group = random.choices(
            list(AGE_DISTRIBUTION.keys()),
            weights=list(AGE_DISTRIBUTION.values())
        )[0]
        gender = random.choice(["M", "F", "other"])
        home_district = random.choice(HK_DISTRICTS)

        # Get preferred store (usually in same or nearby district)
        nearby_stores = get_nearby_stores(home_district, STORES)
        preferred_store = random.choice(nearby_stores)
        preferred_store_id = preferred_store["store_id"]

        # Loyalty tier
        tier = random.choices(
            list(LOYALTY_TIERS.keys()),
            weights=[v["weight"] for v in LOYALTY_TIERS.values()]
        )[0]
        tier_info = LOYALTY_TIERS[tier]

        # Registration date
        registration_date = start_date + timedelta(days=random.randint(0, 200))

        # First visit date (same or after registration)
        first_visit_date = registration_date + timedelta(days=random.randint(0, 30))

        # Lifetime orders based on tier
        total_lifetime_orders = random.randint(tier_info["orders"][0], tier_info["orders"][1])

        # Order values (HK$)
        avg_order_value = round(random.uniform(35, 85), 2)
        total_lifetime_spend = round(total_lifetime_orders * avg_order_value, 2)

        # Visit frequency
        visit_frequency_monthly = random.randint(tier_info["frequency"][0], tier_info["frequency"][1])

        customers.append({
            "customer_id": customer_id,
            "age_group": age_group,
            "gender": gender,
            "home_district": home_district,
            "preferred_store_id": preferred_store_id,
            "loyalty_tier": tier,
            "registration_date": registration_date.strftime("%Y-%m-%d"),
            "first_visit_date": first_visit_date.strftime("%Y-%m-%d"),
            "total_lifetime_orders": total_lifetime_orders,
            "total_lifetime_spend": total_lifetime_spend,
            "avg_order_value": avg_order_value,
            "visit_frequency_monthly": visit_frequency_monthly,
        })

        if i % 5000 == 0:
            print(f"  Generated {i} customers...")

    return customers

def generate_loyalty_transactions(customers):
    """Generate loyalty transaction data"""
    print("Generating loyalty transactions...")

    transactions = []
    start_date = parse_date(DATE_START)
    end_date = parse_date(DATE_END)

    txn_id = 1

    for customer in customers:
        customer_id = customer["customer_id"]
        lifetime_orders = customer["total_lifetime_orders"]
        tier = customer["loyalty_tier"]
        tier_info = LOYALTY_TIERS[tier]
        earn_rate = tier_info["earn_rate"]
        avg_order_value = customer["avg_order_value"]
        preferred_store_id = customer["preferred_store_id"]
        first_visit = parse_date(customer["first_visit_date"])

        # Determine number of earning transactions (~60-75% earn rate)
        earning_txns = int(lifetime_orders * earn_rate)

        # Track which transactions are redeems (~15% of total transactions)
        redeem_indices = set()
        num_redeems = max(0, int(lifetime_orders * 0.18))  # Slightly higher to account for skipped redeems
        if num_redeems > 0 and earning_txns < lifetime_orders:
            redeem_indices = set(random.sample(range(earning_txns, lifetime_orders), min(num_redeems, lifetime_orders - earning_txns)))

        points_balance = 0

        for order_num in range(lifetime_orders):
            # Randomly pick a transaction date
            days_offset = random.randint(0, (end_date - first_visit).days)
            txn_date = first_visit + timedelta(days=days_offset)

            # Skip if outside date range
            if txn_date > end_date or txn_date < start_date:
                continue

            # Randomly pick a store (prefer from same district)
            nearby_stores = get_nearby_stores(customer["home_district"], STORES)
            store_id = random.choice(nearby_stores)["store_id"]

            # Decide if this is an earn or redeem transaction
            if order_num < earning_txns:
                # Earn transaction
                points_earned = int(avg_order_value / 10)  # 1 point per HK$10
                points_balance += points_earned

                transactions.append({
                    "loyalty_txn_id": f"LTX-{txn_id:07d}",
                    "customer_id": customer_id,
                    "store_id": store_id,
                    "transaction_date": txn_date.strftime("%Y-%m-%d"),
                    "transaction_type": "earn",
                    "points_amount": points_earned,
                    "points_balance_after": points_balance,
                    "reward_type": "",
                    "associated_order_value": avg_order_value,
                })
                txn_id += 1
            elif order_num in redeem_indices and points_balance > 0:
                # Redeem transaction
                reward_type = random.choices(
                    list(REWARD_TYPES.keys()),
                    weights=[v["weight"] for v in REWARD_TYPES.values()]
                )[0]
                points_needed = REWARD_TYPES[reward_type]["points"]

                if points_balance >= points_needed:
                    points_balance -= points_needed

                    transactions.append({
                        "loyalty_txn_id": f"LTX-{txn_id:07d}",
                        "customer_id": customer_id,
                        "store_id": store_id,
                        "transaction_date": txn_date.strftime("%Y-%m-%d"),
                        "transaction_type": "redeem",
                        "points_amount": points_needed,
                        "points_balance_after": points_balance,
                        "reward_type": reward_type,
                        "associated_order_value": 0,
                    })
                    txn_id += 1

    print(f"  Generated {len(transactions)} loyalty transactions")
    return transactions

def generate_feedback_surveys(customers):
    """Generate feedback survey data"""
    print("Generating feedback surveys...")

    surveys = []
    start_date = parse_date(DATE_START)
    end_date = parse_date(DATE_END)

    survey_id = 1

    for customer in customers:
        customer_id = customer["customer_id"]
        lifetime_orders = customer["total_lifetime_orders"]
        preferred_store_id = customer["preferred_store_id"]
        first_visit = parse_date(customer["first_visit_date"])

        # Generate surveys for random subset of orders (~1-2%)
        num_surveys = int(lifetime_orders * SURVEY_RATE)

        for _ in range(num_surveys):
            # Random survey date
            days_offset = random.randint(0, (end_date - first_visit).days)
            survey_date = first_visit + timedelta(days=days_offset)

            if survey_date > end_date or survey_date < start_date:
                continue

            # Visit date is slightly before survey date
            visit_date = survey_date - timedelta(days=random.randint(0, 5))

            # Store (usually preferred, sometimes elsewhere)
            if random.random() < 0.8:
                store_id = preferred_store_id
            else:
                store_id = random.choice(STORES)["store_id"]

            # Ratings (skewed positive, mean ~3.8)
            # Use a more aggressive approach to get higher average
            rating_bias = random.gauss(3.8, 0.7)
            overall_rating = max(1, min(5, round(rating_bias)))
            food_quality_rating = max(1, min(5, round(overall_rating + random.gauss(0, 0.3))))
            service_speed_rating = max(1, min(5, round(overall_rating - random.gauss(0.2, 0.4))))
            cleanliness_rating = max(1, min(5, round(overall_rating + random.gauss(0, 0.3))))
            value_rating = max(1, min(5, round(overall_rating - random.gauss(0.1, 0.4))))

            # Would recommend
            would_recommend = "yes" if overall_rating >= 3 else ("yes" if random.random() < 0.3 else "no")

            # Sentiment based on overall rating
            if overall_rating <= 2:
                sentiment = "negative"
            elif overall_rating == 3:
                sentiment = "neutral"
            else:
                sentiment = "positive"

            # Free text comment
            free_text_comment = random.choice(FEEDBACK_TEMPLATES) if random.random() < 0.7 else ""

            surveys.append({
                "survey_id": f"SRV-{survey_id:07d}",
                "customer_id": customer_id,
                "store_id": store_id,
                "survey_date": survey_date.strftime("%Y-%m-%d"),
                "visit_date": visit_date.strftime("%Y-%m-%d"),
                "overall_rating": overall_rating,
                "food_quality_rating": food_quality_rating,
                "service_speed_rating": service_speed_rating,
                "cleanliness_rating": cleanliness_rating,
                "value_rating": value_rating,
                "would_recommend": would_recommend,
                "free_text_comment": free_text_comment,
                "sentiment": sentiment,
            })
            survey_id += 1

    print(f"  Generated {len(surveys)} feedback surveys")
    return surveys

def write_csv(filename, fieldnames, rows):
    """Write data to CSV file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Written {len(rows)} rows to {filename}")

def main():
    print("=" * 70)
    print("McDonald's HK GenBI - Customer Data Generator")
    print("=" * 70)
    print()

    # Generate data
    customers = generate_customer_profiles()
    print()

    loyalty_txns = generate_loyalty_transactions(customers)
    print()

    surveys = generate_feedback_surveys(customers)
    print()

    # Write CSV files
    output_dir = "/Users/danshek/mcdhk-dashboard/genbi/raw/customer"
    os.makedirs(output_dir, exist_ok=True)

    print("Writing CSV files...")
    print()

    # Customer profiles
    write_csv(
        f"{output_dir}/customer_profiles.csv",
        [
            "customer_id", "age_group", "gender", "home_district",
            "preferred_store_id", "loyalty_tier", "registration_date",
            "first_visit_date", "total_lifetime_orders", "total_lifetime_spend",
            "avg_order_value", "visit_frequency_monthly"
        ],
        customers
    )

    # Loyalty transactions
    write_csv(
        f"{output_dir}/loyalty_transactions.csv",
        [
            "loyalty_txn_id", "customer_id", "store_id", "transaction_date",
            "transaction_type", "points_amount", "points_balance_after",
            "reward_type", "associated_order_value"
        ],
        loyalty_txns
    )

    # Feedback surveys
    write_csv(
        f"{output_dir}/feedback_surveys.csv",
        [
            "survey_id", "customer_id", "store_id", "survey_date", "visit_date",
            "overall_rating", "food_quality_rating", "service_speed_rating",
            "cleanliness_rating", "value_rating", "would_recommend",
            "free_text_comment", "sentiment"
        ],
        surveys
    )

    print()
    print("=" * 70)
    print("Data Generation Complete")
    print("=" * 70)
    print(f"Customers: {len(customers):,}")
    print(f"Loyalty transactions: {len(loyalty_txns):,}")
    print(f"Feedback surveys: {len(surveys):,}")
    print()
    print(f"Output directory: {output_dir}/")
    print()

if __name__ == "__main__":
    main()
