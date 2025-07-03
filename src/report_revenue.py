import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import random

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

# Beispielpreise pro Sorte (EUR pro Stück)
preise = {
    "Cavendish": 0.25,
    "Plantain": 0.30,
    "Red Banana": 0.40,
    "Apple Banana": 0.35,
    "Blue Java": 0.50,
    "Manzano": 0.45,
    "Burro": 0.28,
    "Goldfinger": 0.32
}

def umsatzreport():
    query = """
        SELECT p.name AS produkt, SUM(oi.quantity) AS gesamtmenge
        FROM product p
        JOIN order_item oi ON p.id = oi.product_id
        GROUP BY p.name
    """
    df = pd.read_sql(query, engine)
    df["preis"] = df["produkt"].map(preise)
    df["umsatz"] = df["gesamtmenge"] * df["preis"]
    print(df[["produkt", "umsatz"]])

    df.plot(kind='bar', x='produkt', y='umsatz', legend=False)
    plt.ylabel("Umsatz (€)")
    plt.title("Umsatz pro Bananensorte")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    umsatzreport()