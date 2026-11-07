import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración Base de Datos Origen (SQL Server Express OLTP) ---
OLTP_SERVER = os.getenv("OLTP_SERVER", r"localhost\SQLEXPRESS")
OLTP_DB = os.getenv("OLTP_DB", "AdventureWorks2022")
OLTP_DRIVER = os.getenv("OLTP_DRIVER", "ODBC Driver 17 for SQL Server")
OLTP_TRUSTED = os.getenv("OLTP_TRUSTED", "yes")

# Si se usa usuario/clave SQL en vez de Windows Auth:
OLTP_USER = os.getenv("OLTP_USER", "")
OLTP_PASSWORD = os.getenv("OLTP_PASSWORD", "")

# --- Configuración Base de Datos Destino (PostgreSQL DW / Datamart) ---
OLAP_HOST = os.getenv("OLAP_HOST", "localhost")
OLAP_PORT = os.getenv("OLAP_PORT", "5432")
OLAP_DB = os.getenv("OLAP_DB", "AdventureWorksDW")
OLAP_USER = os.getenv("OLAP_USER", "postgres")
OLAP_PASSWORD = os.getenv("OLAP_PASSWORD", "")
OLAP_SCHEMA = os.getenv("OLAP_SCHEMA", "public")

def get_oltp_engine():
    """Genera la conexión SQLAlchemy para SQL Server Express usando Windows Authentication o SQL Auth."""
    # Buscar el driver ODBC instalado compatible
    driver = OLTP_DRIVER
    if OLTP_TRUSTED.lower() in ("yes", "true", "1"):
        # Autenticación integrada de Windows (sin necesidad de usuario ni clave)
        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={OLTP_SERVER};"
            f"DATABASE={OLTP_DB};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    else:
        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={OLTP_SERVER};"
            f"DATABASE={OLTP_DB};"
            f"UID={OLTP_USER};"
            f"PWD={OLTP_PASSWORD};"
            "TrustServerCertificate=yes;"
        )
    params = urllib.parse.quote_plus(conn_str)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

def get_olap_engine():
    """Genera la conexión SQLAlchemy para PostgreSQL (OLAP)."""
    engine_url = f"postgresql+psycopg2://{OLAP_USER}:{OLAP_PASSWORD}@{OLAP_HOST}:{OLAP_PORT}/{OLAP_DB}"
    return create_engine(engine_url)
