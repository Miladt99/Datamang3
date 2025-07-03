from sqlalchemy import create_engine, text

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

def check_null_customers():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id FROM customer WHERE name IS NULL"))
        ids = [row[0] for row in result]
        print(f"Kunden mit fehlendem Namen: {ids}")

def check_duplicate_customers():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT name, COUNT(*) FROM customer
            WHERE name IS NOT NULL
            GROUP BY name
            HAVING COUNT(*) > 1
        """))
        duplicates = [row[0] for row in result]
        print(f"Doppelte Kundennamen: {duplicates}")

def check_invalid_product_supplier():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id FROM product
            WHERE supplier_id NOT IN (SELECT id FROM supplier)
        """))
        invalid = [row[0] for row in result]
        print(f"Produkte mit ungültigem supplier_id: {invalid}")

def check_typo_customers():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, name FROM customer
            WHERE name ~ '[0-9]'
        """))
        typos = [(row[0], row[1]) for row in result]
        print(f"Kunden mit möglichem Tippfehler (Zahl im Namen): {typos}")

if __name__ == "__main__":
    check_null_customers()
    check_duplicate_customers()
    check_invalid_product_supplier()
    check_typo_customers()