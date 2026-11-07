import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración Base de Datos Origen (SQL Server OLTP) ---
OLTP_HOST = os.getenv("OLTP_HOST", "localhost")
OLTP_PORT = os.getenv("OLTP_PORT", "1433")
OLTP_DB = os.getenv("OLTP_DB", "AdventureWorks2025")
OLTP_USER = os.getenv("OLTP_USER", "sa")
OLTP_PASSWORD = os.getenv("OLTP_PASSWORD", "")
OLTP_DRIVER = os.getenv("OLTP_DRIVER", "ODBC Driver 17 for SQL Server")

# --- Configuración Base de Datos Destino (PostgreSQL DW / Datamart) ---
OLAP_HOST = os.getenv("OLAP_HOST", "localhost")
OLAP_PORT = os.getenv("OLAP_PORT", "5432")
OLAP_DB = os.getenv("OLAP_DB", "AdventureWorksDW2025")
OLAP_USER = os.getenv("OLAP_USER", "postgres")
OLAP_PASSWORD = os.getenv("OLAP_PASSWORD", "")
OLAP_SCHEMA = os.getenv("OLAP_SCHEMA", "public")

def get_oltp_engine():
    """Genera la conexión SQLAlchemy para SQL Server (OLTP)."""
    connection_string = (
        f"DRIVER={{{OLTP_DRIVER}}};"
        f"SERVER={OLTP_HOST},{OLTP_PORT};"
        f"DATABASE={OLTP_DB};"
        f"UID={OLTP_USER};"
        f"PWD={OLTP_PASSWORD};"
        "TrustServerCertificate=yes;"
    )
    params = urllib.parse.quote_plus(connection_string)
    engine_url = f"mssql+pyodbc:///?odbc_connect={params}"
    return create_engine(engine_url)

def get_olap_engine():
    """Genera la conexión SQLAlchemy para PostgreSQL (OLAP)."""
    engine_url = f"postgresql+psycopg2://{OLAP_USER}:{OLAP_PASSWORD}@{OLAP_HOST}:{OLAP_PORT}/{OLAP_DB}"
    return create_engine(engine_url)
