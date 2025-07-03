import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

def top_customers():
    query = """
        SELECT c.name AS kunde, SUM(oi.quantity) AS gesamtmenge
        FROM customer c
        JOIN "order" o ON c.id = o.customer_id
        JOIN order_item oi ON o.id = oi.order_id
        GROUP BY c.name
        ORDER BY gesamtmenge DESC
        LIMIT 10
    """
    df = pd.read_sql(query, engine)
    print(df)
    df.plot(kind='bar', x='kunde', y='gesamtmenge', legend=False)
    plt.ylabel("Bestellte Menge")
    plt.title("Top 10 Kunden nach Bestellmenge")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    top_customers()