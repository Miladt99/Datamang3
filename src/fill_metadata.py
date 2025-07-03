from sqlalchemy import create_engine, text

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

# Beispielhafte Metadaten
metadata_entries = [
    # Tabelle, Spalte, Datentyp, Skalenniveau
    ("supplier", "id", "integer", "metrisch"),
    ("supplier", "name", "string", "nominal"),
    ("supplier", "country", "string", "nominal"),
    ("product", "id", "integer", "metrisch"),
    ("product", "name", "string", "nominal"),
    ("product", "category", "string", "nominal"),
    ("product", "supplier_id", "integer", "metrisch"),
    ("warehouse", "id", "integer", "metrisch"),
    ("warehouse", "location", "string", "nominal"),
    ("customer", "id", "integer", "metrisch"),
    ("customer", "name", "string", "nominal"),
    ("customer", "city", "string", "nominal"),
    ("order", "id", "integer", "metrisch"),
    ("order", "customer_id", "integer", "metrisch"),
    ("order", "order_date", "date", "metrisch"),
    ("delivery", "id", "integer", "metrisch"),
    ("delivery", "order_id", "integer", "metrisch"),
    ("delivery", "warehouse_id", "integer", "metrisch"),
    ("delivery", "delivery_date", "date", "metrisch"),
]

def fill_metadata():
    with engine.begin() as conn:
        for table, column, dtype, scale in metadata_entries:
            conn.execute(
                text("INSERT INTO metadata (table_name, column_name, data_type, scale_level) VALUES (:table, :column, :dtype, :scale)"),
                {"table": table, "column": column, "dtype": dtype, "scale": scale}
            )

if __name__ == "__main__":
    fill_metadata()
    print("Metadatentabelle erfolgreich befüllt!")