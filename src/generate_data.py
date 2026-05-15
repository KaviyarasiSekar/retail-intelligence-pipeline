import csv
import os
import random
from datetime import datetime, timedelta, timezone, date
from faker import Faker
import argparse

SEED = 42

N_CUSTOMERS = 500
N_PRODUCTS = 200
N_ORDERS = 3000
MAX_ITEMS_PER_ORDER = 6
REVIEW_RATE = 0.35  # % of order_items that get a review

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def entity_dir(entity: str, run_date: str) -> str:
    # run_date must be "YYYY-MM-DD"
    return os.path.join(OUTPUT_DIR, "landing", entity, run_date)


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _utc_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--run-date",
        default=date.today().isoformat(),
        help="Partition date for landing output, format YYYY-MM-DD (default: today)"
    )
    return p.parse_args()


def main() -> None:
    random.seed(SEED)
    fake = Faker()
    Faker.seed(SEED)

    args = parse_args()
    run_date = args.run_date

    _ensure_dir(OUTPUT_DIR)

    customers_dir = entity_dir("customers", run_date)
    products_dir = entity_dir("products", run_date)
    orders_dir = entity_dir("orders", run_date)
    order_items_dir = entity_dir("order_items", run_date)
    reviews_dir = entity_dir("reviews", run_date)

    for d in [customers_dir, products_dir, orders_dir, order_items_dir, reviews_dir]:
        _ensure_dir(d)
    # ---------- customers ----------
    customers_path = os.path.join(customers_dir, "customers.csv")
    customers = []
    for i in range(1, N_CUSTOMERS + 1):
        created_at = fake.date_time_between(
            start_date="-2y", end_date="-30d", tzinfo=timezone.utc)
        customers.append(
            {
                "customer_id": i,
                "email": fake.unique.email(),
                "full_name": fake.name(),
                "country": fake.country_code(),
                "city": fake.city(),
                "created_at": _utc_iso(created_at),
            }
        )

    with open(customers_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(customers[0].keys()))
        w.writeheader()
        w.writerows(customers)

    # ---------- products ----------
    products_path = os.path.join(products_dir, "products.csv")
    categories = ["Electronics", "Home",
                  "Office", "Grocery", "Fashion", "Sports"]
    products = []
    for i in range(1, N_PRODUCTS + 1):
        category = random.choice(categories)
        base_price = round(random.uniform(5, 800), 2)
        products.append(
            {
                "product_id": i,
                "sku": f"SKU-{i:05d}",
                "product_name": f"{fake.word().title()} {fake.word().title()}",
                "category": category,
                "unit_price": base_price,
                "active": random.choice([True] * 9 + [False]),
            }
        )

    with open(products_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(products[0].keys()))
        w.writeheader()
        w.writerows(products)

    # ---------- orders + order_items ----------
    orders_path = os.path.join(orders_dir, "orders.csv")
    order_items_path = os.path.join(order_items_dir, "order_items.csv")
    now = datetime.now(timezone.utc)
    order_statuses = ["PLACED", "PAID", "SHIPPED",
                      "DELIVERED", "CANCELLED", "RETURNED"]
    status_weights = [0.05, 0.10, 0.20, 0.55, 0.05, 0.05]

    orders = []
    order_items = []
    item_id = 1

    for order_id in range(1, N_ORDERS + 1):
        customer = random.choice(customers)
        placed_at = now - \
            timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))
        status = random.choices(order_statuses, weights=status_weights, k=1)[0]

        n_items = random.randint(1, MAX_ITEMS_PER_ORDER)

        # build items first to compute order total
        order_total = 0.0
        for _ in range(n_items):
            p = random.choice(products)
            qty = random.randint(1, 4)
            discount_pct = random.choice([0, 0, 0, 5, 10, 15, 20])  # mostly 0
            unit_price = float(p["unit_price"])
            line_subtotal = unit_price * qty
            line_discount = round(line_subtotal * (discount_pct / 100.0), 2)
            line_total = round(line_subtotal - line_discount, 2)
            order_total += line_total

            order_items.append(
                {
                    "order_item_id": item_id,
                    "order_id": order_id,
                    "product_id": p["product_id"],
                    "quantity": qty,
                    "unit_price": round(unit_price, 2),
                    "discount_pct": discount_pct,
                    "line_total": line_total,
                }
            )
            item_id += 1

        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer["customer_id"],
                "order_status": status,
                "order_ts": _utc_iso(placed_at),
                "currency": "GBP",
                "order_total": round(order_total, 2),
                "sales_channel": random.choice(["web", "mobile", "store"]),
            }
        )

    with open(orders_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(orders[0].keys()))
        w.writeheader()
        w.writerows(orders)

    with open(order_items_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(order_items[0].keys()))
        w.writeheader()
        w.writerows(order_items)

    # ---------- reviews (for later sentiment / data quality examples) ----------
    reviews_path = os.path.join(reviews_dir, "reviews.csv")
    reviews = []
    review_id = 1

    for oi in order_items:
        if random.random() > REVIEW_RATE:
            continue
        rating = random.choices([1, 2, 3, 4, 5], weights=[
                                0.05, 0.08, 0.17, 0.35, 0.35], k=1)[0]
        reviews.append(
            {
                "review_id": review_id,
                "order_item_id": oi["order_item_id"],
                "rating": rating,
                "review_text": fake.sentence(nb_words=random.randint(6, 18)),
                "review_ts": _utc_iso(now - timedelta(days=random.randint(0, 365))),
            }
        )
        review_id += 1

    with open(reviews_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(
            reviews[0].keys()) if reviews else ["review_id"])
        w.writeheader()
        w.writerows(reviews)

    print("Wrote:")
    print(f"- {customers_path} ({len(customers)} rows)")
    print(f"- {products_path} ({len(products)} rows)")
    print(f"- {orders_path} ({len(orders)} rows)")
    print(f"- {order_items_path} ({len(order_items)} rows)")
    print(f"- {reviews_path} ({len(reviews)} rows)")


if __name__ == "__main__":
    main()
