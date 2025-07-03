from sqlalchemy import text
from sqlalchemy import create_engine
from faker import Faker
import random

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")
fake = Faker()

def insert_suppliers(n=5):
    with engine.begin() as conn:
        for _ in range(n):
            name = fake.company()
            country = fake.country()
            conn.execute(
                text("INSERT INTO supplier (name, country) VALUES (:name, :country)"),
                {"name": name, "country": country}
            )

BANANA_SORTEN = [
    "Cavendish", "Plantain", "Red Banana", "Apple Banana", "Blue Java", "Manzano", "Burro", "Goldfinger"
]

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

def insert_customers(n=10, error_rate=0.):
    with engine.begin() as conn:
        for _ in range(n):
            # Fehler: 10% der Namen sind leer, 10% haben Tippfehler
            if random.random() < error_rate:
                name = None  # Fehlender Name
            elif random.random() < error_rate:
                name = fake.name() + str(random.randint(0, 9))  # Tippfehler (Zahl am Ende)
            else:
                name = fake.name()
            city = fake.city()
            conn.execute(
                text("INSERT INTO customer (name, city) VALUES (:name, :city)"),
                {"name": name, "city": city}
            )

def insert_warehouses(n=3):
    with engine.begin() as conn:
        for _ in range(n):
            location = fake.city()
            conn.execute(
                text("INSERT INTO warehouse (location) VALUES (:location)"),
                {"location": location}
            )

if __name__ == "__main__":
    insert_suppliers()
    insert_warehouses()
    insert_customers()
    insert_products()
    print("Stammdaten erfolgreich generiert!")