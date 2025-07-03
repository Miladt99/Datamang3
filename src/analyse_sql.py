import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

# Beispiel: Logistikdaten laden
df = pd.read_sql("SELECT * FROM logistikdaten", engine)
print(df.head())

# Gruppiere nach Tag und summiere die Menge
df["zeitstempel"] = pd.to_datetime(df["zeitstempel"])
df["datum"] = df["zeitstempel"].dt.date
menge_pro_tag = df.groupby("datum")["menge"].sum()

menge_pro_tag.plot(kind="line", marker="o")
plt.title("Menge pro Tag (aus PostgreSQL)")
plt.ylabel("Menge")
plt.xlabel("Datum")
plt.tight_layout()
plt.show()