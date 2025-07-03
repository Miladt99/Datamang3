import sqlalchemy

# Verbindungsdaten (wie in docker-compose.yml)
USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

# Verbindung aufbauen
engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

try:
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT version();"))
        print("Verbindung erfolgreich! PostgreSQL Version:", result.scalar())
except Exception as e:
    print("Fehler bei der Verbindung:", e)