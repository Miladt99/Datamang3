import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

def delivery_time():
    query = """
        SELECT p.name AS produkt, AVG(d.delivery_date - o.order_date) AS avg_lieferzeit
        FROM product p
        JOIN order_item oi ON p.id = oi.product_id
        JOIN "order" o ON oi.order_id = o.id
        JOIN delivery d ON o.id = d.order_id
        GROUP BY p.name
        ORDER BY avg_lieferzeit
    """
    df = pd.read_sql(query, engine)
    print(df)
    df.plot(kind='bar', x='produkt', y='avg_lieferzeit', legend=False)
    plt.ylabel("Ø Lieferzeit (Tage)")
    plt.title("Durchschnittliche Lieferzeit pro Bananensorte")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    delivery_time()