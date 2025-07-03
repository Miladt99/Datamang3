from faker import Faker
from pymongo import MongoClient
import random

fake = Faker()

# MongoDB-Verbindung
client = MongoClient("mongodb://localhost:27017/")
db = client["supplychain"]
orderslips = db["orderslips"]

def generate_orderslips(n=20):
    for _ in range(n):
        orderslip = {
            "orderslip_id": fake.uuid4(),
            "customer_name": fake.name(),  # Kann von SQL abweichen!
            "product_name": fake.word().capitalize(),  # Kann von SQL abweichen!
            "quantity": random.randint(1, 100),
            "order_date": fake.date_between(start_date='-60d', end_date='today').isoformat(),
            "delivery_address": fake.address(),
            "note": fake.sentence()
        }
        orderslips.insert_one(orderslip)

if __name__ == "__main__":
    generate_orderslips()
    print("Bestellscheine erfolgreich in MongoDB gespeichert!")