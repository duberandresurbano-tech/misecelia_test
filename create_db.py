"""Crea la base de datos de Miscelia en PostgreSQL usando DATABASE_URL del .env."""
import psycopg
from psycopg import sql
from sqlalchemy.engine import make_url

from config import Config


def crear_base_de_datos():
    if not Config.SQLALCHEMY_DATABASE_URI:
        raise SystemExit("Falta DATABASE_URL en el archivo .env (mira .env.example).")

    url = make_url(Config.SQLALCHEMY_DATABASE_URI)
    nombre_db = url.database

    try:
        # Nos conectamos a la base 'postgres' (siempre existe) para poder crear la nuestra.
        with psycopg.connect(
            dbname='postgres',
            user=url.username,
            password=url.password,
            host=url.host or 'localhost',
            port=url.port or 5432,
            autocommit=True,
        ) as conn:
            existe = conn.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s", (nombre_db,)
            ).fetchone()

            if existe:
                print(f"La base de datos '{nombre_db}' ya existe en PostgreSQL.")
            else:
                conn.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(nombre_db)))
                print(f"¡Base de datos '{nombre_db}' creada exitosamente en PostgreSQL!")
    except psycopg.Error as e:
        raise SystemExit(f"Error conectando a PostgreSQL: {e}")


if __name__ == '__main__':
    crear_base_de_datos()
