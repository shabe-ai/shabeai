import os
import sqlalchemy as sa

url = os.getenv("DATABASE_URL")
engine = sa.create_engine(url.replace("+asyncpg", ""))  # sync driver for CLI
with engine.connect() as conn:
    tables = conn.execute(sa.text(
        "select table_name from information_schema.tables "
        "where table_schema='public'"
    )).fetchall()
    print("Tables:", tables) 