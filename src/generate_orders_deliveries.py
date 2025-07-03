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

def insert_orders(n=20):
    with engine.begin() as conn:
        customer_ids = [row[0] for row in conn.execute(text("SELECT id FROM customer"))]
        for _ in range(n):
            customer_id = random.choice(customer_ids)
            order_date = fake.date_between(start_date='-60d', end_date='today')
            conn.execute(
                text("INSERT INTO \"order\" (customer_id, order_date) VALUES (:customer_id, :order_date)"),
                {"customer_id": customer_id, "order_date": order_date}
            )

def insert_deliveries(n=20):
    with engine.begin() as conn:
        order_ids = [row[0] for row in conn.execute(text("SELECT id FROM \"order\""))]
        warehouse_ids = [row[0] for row in conn.execute(text("SELECT id FROM warehouse"))]
        for _ in range(n):
            order_id = random.choice(order_ids)
            warehouse_id = random.choice(warehouse_ids)
            delivery_date = fake.date_between(start_date='-30d', end_date='today')
            conn.execute(
                text("INSERT INTO delivery (order_id, warehouse_id, delivery_date) VALUES (:order_id, :warehouse_id, :delivery_date)"),
                {"order_id": order_id, "warehouse_id": warehouse_id, "delivery_date": delivery_date}
            )

if __name__ == "__main__":
    insert_orders()
    insert_deliveries()
    print("Bestellungen und Lieferungen erfolgreich generiert!")