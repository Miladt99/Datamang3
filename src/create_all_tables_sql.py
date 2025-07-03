from sqlalchemy import create_engine, text

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

table_sqls = [
    '''
    CREATE TABLE IF NOT EXISTS supplier (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        country VARCHAR(100)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS product (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        category VARCHAR(50),
        supplier_id INTEGER REFERENCES supplier(id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS warehouse (
        id SERIAL PRIMARY KEY,
        location VARCHAR(100)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS customer (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        city VARCHAR(100)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS "order" (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customer(id),
        order_date DATE
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS delivery (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES "order"(id),
        warehouse_id INTEGER REFERENCES warehouse(id),
        delivery_date DATE
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS order_item (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES "order"(id),
        product_id INTEGER REFERENCES product(id),
        quantity INTEGER
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS logistikdaten (
        id SERIAL PRIMARY KEY,
        zeitstempel TIMESTAMP,
        lager VARCHAR(50),
        bananensorte VARCHAR(50),
        menge INTEGER,
        lieferant VARCHAR(50)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS metadata (
        id SERIAL PRIMARY KEY,
        table_name VARCHAR(100),
        column_name VARCHAR(100),
        data_type VARCHAR(50),
        scale_level VARCHAR(50)
    );
    '''
]

with engine.begin() as conn:
    for sql in table_sqls:
        conn.execute(text(sql))

print("Alle Tabellen wurden (falls nötig) angelegt.") 