from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime, timedelta

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")
fake = Faker()

BANANA_SORTEN = [
    "Cavendish", "Plantain", "Red Banana", "Apple Banana", "Blue Java", "Manzano", "Burro", "Goldfinger"
]
LAGER = ['Lager A', 'Lager B', 'Lager C']
LIEFERANTEN = ['BananaCorp', 'TropiFruits', 'GreenWorld', 'SunBanana']

# 1. Lieferanten
def insert_suppliers(n=5):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM supplier"))
        for _ in range(n):
            name = fake.company()
            country = fake.country()
            conn.execute(
                text("INSERT INTO supplier (name, country) VALUES (:name, :country)"),
                {"name": name, "country": country}
            )

# 2. Produkte (Bananensorten)
def insert_products():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM product"))
        supplier_ids = [row[0] for row in conn.execute(text("SELECT id FROM supplier"))]
        for sorte in BANANA_SORTEN:
            category = "Banane"
            supplier_id = random.choice(supplier_ids)
            conn.execute(
                text("INSERT INTO product (name, category, supplier_id) VALUES (:name, :category, :supplier_id)"),
                {"name": sorte, "category": category, "supplier_id": supplier_id}
            )

# 3. Lager
def insert_warehouses():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM warehouse"))
        for location in LAGER:
            conn.execute(
                text("INSERT INTO warehouse (location) VALUES (:location)"),
                {"location": location}
            )

# 4. Kunden
def insert_customers(n=20):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM customer"))
        for _ in range(n):
            name = fake.name()
            city = fake.city()
            conn.execute(
                text("INSERT INTO customer (name, city) VALUES (:name, :city)"),
                {"name": name, "city": city}
            )

# 5. Bestellungen
def insert_orders(n=40):
    with engine.begin() as conn:
        conn.execute(text('DELETE FROM "order"'))
        customer_ids = [row[0] for row in conn.execute(text("SELECT id FROM customer"))]
        for _ in range(n):
            customer_id = random.choice(customer_ids)
            order_date = fake.date_between(start_date='-30d', end_date='today')
            conn.execute(
                text('INSERT INTO "order" (customer_id, order_date) VALUES (:customer_id, :order_date)'),
                {"customer_id": customer_id, "order_date": order_date}
            )

# 6. Lieferungen
def insert_deliveries(n=40):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM delivery"))
        order_ids = [row[0] for row in conn.execute(text('SELECT id FROM "order"'))]
        warehouse_ids = [row[0] for row in conn.execute(text("SELECT id FROM warehouse"))]
        for _ in range(n):
            order_id = random.choice(order_ids)
            warehouse_id = random.choice(warehouse_ids)
            delivery_date = fake.date_between(start_date='-20d', end_date='today')
            conn.execute(
                text("INSERT INTO delivery (order_id, warehouse_id, delivery_date) VALUES (:order_id, :warehouse_id, :delivery_date)"),
                {"order_id": order_id, "warehouse_id": warehouse_id, "delivery_date": delivery_date}
            )

# 7. Bestellpositionen
def insert_order_items():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM order_item"))
        order_ids = [row[0] for row in conn.execute(text('SELECT id FROM "order"'))]
        product_ids = [row[0] for row in conn.execute(text("SELECT id FROM product"))]
        for order_id in order_ids:
            for product_id in random.sample(product_ids, random.randint(1, 3)):
                quantity = random.randint(1, 50)
                conn.execute(
                    text("INSERT INTO order_item (order_id, product_id, quantity) VALUES (:order_id, :product_id, :quantity)"),
                    {"order_id": order_id, "product_id": product_id, "quantity": quantity}
                )

# 8. Logistikdaten
def insert_logistikdaten(n=120):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM logistikdaten"))
        start = datetime.now() - timedelta(days=30)
        intervall = timedelta(hours=6)
        aktuelle_zeit = start
        for _ in range(n):
            lager = random.choice(LAGER)
            sorte = random.choice(BANANA_SORTEN)
            menge = random.randint(50, 200)
            lieferant = random.choice(LIEFERANTEN)
            zeitstempel = aktuelle_zeit
            conn.execute(
                text("INSERT INTO logistikdaten (zeitstempel, lager, bananensorte, menge, lieferant) VALUES (:zeitstempel, :lager, :bananensorte, :menge, :lieferant)"),
                {"zeitstempel": zeitstempel, "lager": lager, "bananensorte": sorte, "menge": menge, "lieferant": lieferant}
            )
            aktuelle_zeit += intervall

def clear_all_tables():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM order_item"))
        conn.execute(text("DELETE FROM delivery"))
        conn.execute(text('DELETE FROM "order"'))
        conn.execute(text("DELETE FROM product"))
        conn.execute(text("DELETE FROM warehouse"))
        conn.execute(text("DELETE FROM customer"))
        conn.execute(text("DELETE FROM logistikdaten"))
        conn.execute(text("DELETE FROM supplier"))

if __name__ == "__main__":
    clear_all_tables()
    insert_suppliers()
    insert_products()
    insert_warehouses()
    insert_customers()
    insert_orders()
    insert_deliveries()
    insert_order_items()
    insert_logistikdaten()
    print("Alle SQL-Tabellen erfolgreich mit Testdaten befüllt!") 