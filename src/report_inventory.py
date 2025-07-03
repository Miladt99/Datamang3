import pandas as pd
from sqlalchemy import create_engine

import matplotlib.pyplot as plt

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

# Beispiel: Anzahl Bestellungen pro Produkt
def bestandsreport():
    query = """
        SELECT p.name AS produkt, SUM(oi.quantity) AS anzahl_bestellungen
        FROM product p
        JOIN order_item oi ON p.id = oi.product_id
        GROUP BY p.name
        ORDER BY anzahl_bestellungen DESC
    """
    df = pd.read_sql(query, engine)
    print(df)
    df.plot(kind='bar', x='produkt', y='anzahl_bestellungen', legend=False)
    plt.ylabel("Bestellte Menge")
    plt.title("Bestandsreport: Bestellte Menge pro Bananensorte")
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    bestandsreport()