import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

def detect_outliers():
    query = """
        SELECT p.name AS produkt, SUM(oi.quantity) AS gesamtmenge
        FROM product p
        JOIN order_item oi ON p.id = oi.product_id
        GROUP BY p.name
    """
    df = pd.read_sql(query, engine)
    df["zscore"] = (df["gesamtmenge"] - df["gesamtmenge"].mean()) / df["gesamtmenge"].std()
    outliers = df[np.abs(df["zscore"]) > 2]
    print("Ausreißer (Z-Score > 2):")
    print(outliers[["produkt", "gesamtmenge", "zscore"]])

if __name__ == "__main__":
    detect_outliers()