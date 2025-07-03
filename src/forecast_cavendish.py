import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

def forecast_cavendish():
    query = """
        SELECT o.order_date, SUM(oi.quantity) AS menge
        FROM product p
        JOIN order_item oi ON p.id = oi.product_id
        JOIN "order" o ON oi.order_id = o.id
        WHERE p.name = 'Cavendish'
        GROUP BY o.order_date
        ORDER BY o.order_date
    """
    df = pd.read_sql(query, engine, parse_dates=["order_date"])
    df = df.set_index("order_date").resample("W").sum().fillna(0)
    df["menge"].plot(marker='o')
    plt.title("Absatz Cavendish-Bananen (wöchentlich)")
    plt.ylabel("Menge")
    plt.xlabel("Datum")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    forecast_cavendish()