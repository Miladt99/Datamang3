from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, ForeignKey

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")
metadata = MetaData()

supplier = Table(
    "supplier", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("country", String)
)

product = Table(
    "product", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("category", String),
    Column("supplier_id", Integer, ForeignKey("supplier.id"))
)

warehouse = Table(
    "warehouse", metadata,
    Column("id", Integer, primary_key=True),
    Column("location", String, nullable=False)
)

customer = Table(
    "customer", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("city", String)
)

order = Table(
    "order", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey("customer.id")),
    Column("order_date", Date)
)

delivery = Table(
    "delivery", metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", Integer, ForeignKey("order.id")),
    Column("warehouse_id", Integer, ForeignKey("warehouse.id")),
    Column("delivery_date", Date)
)

# Beispiel für eine Metadatentabelle
metadata_table = Table(
    "metadata", metadata,
    Column("id", Integer, primary_key=True),
    Column("table_name", String),
    Column("column_name", String),
    Column("data_type", String),
    Column("scale_level", String)  # z.B. nominal, ordinal, metrisch
)

if __name__ == "__main__":
    metadata.create_all(engine)
    print("Tabellen erfolgreich erstellt!")