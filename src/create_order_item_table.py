from sqlalchemy import create_engine, text
import random

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

def insert_order_items():
    with engine.begin() as conn:
        order_ids = [row[0] for row in conn.execute(text('SELECT id FROM "order"'))]
        product_ids = [row[0] for row in conn.execute(text("SELECT id FROM product"))]
        for order_id in order_ids:
            # Jede Bestellung bekommt 1–3 verschiedene Bananensorten
            for product_id in random.sample(product_ids, random.randint(1, 3)):
                quantity = random.randint(1, 50)
                conn.execute(
                    text("INSERT INTO order_item (order_id, product_id, quantity) VALUES (:order_id, :product_id, :quantity)"),
                    {"order_id": order_id, "product_id": product_id, "quantity": quantity}
                )

if __name__ == "__main__":
    insert_order_items()
    print("Order-Items erfolgreich generiert!")