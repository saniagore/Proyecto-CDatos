import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

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

# --- Configuración Bodega Entrega 3 (SQL Server) ---
ENTREGA3_SERVER = os.getenv("ENTREGA3_SERVER", OLTP_SERVER)
ENTREGA3_DB = os.getenv("ENTREGA3_DB", "AdventureWorksDW")
ENTREGA3_DRIVER = os.getenv("ENTREGA3_DRIVER", OLTP_DRIVER)
ENTREGA3_TRUSTED = os.getenv("ENTREGA3_TRUSTED", OLTP_TRUSTED)
ENTREGA3_USER = os.getenv("ENTREGA3_USER", OLTP_USER)
ENTREGA3_PASSWORD = os.getenv("ENTREGA3_PASSWORD", OLTP_PASSWORD)
ENTREGA3_SCHEMA = os.getenv("ENTREGA3_SCHEMA", "dbo")

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
    engine_url = URL.create(
        "postgresql+psycopg2",
        username=OLAP_USER,
        password=OLAP_PASSWORD,
        host=OLAP_HOST,
        port=int(OLAP_PORT),
        database=OLAP_DB,
    )
    return create_engine(
        engine_url,
        connect_args={"options": "-c client_encoding=UTF8"},
    )


def get_entrega3_engine():
    """Genera la conexión SQLAlchemy para la bodega SQL Server de la Entrega 3."""
    if ENTREGA3_TRUSTED.lower() in ("yes", "true", "1"):
        conn_str = (
            f"DRIVER={{{ENTREGA3_DRIVER}}};"
            f"SERVER={ENTREGA3_SERVER};"
            f"DATABASE={ENTREGA3_DB};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    else:
        conn_str = (
            f"DRIVER={{{ENTREGA3_DRIVER}}};"
            f"SERVER={ENTREGA3_SERVER};"
            f"DATABASE={ENTREGA3_DB};"
            f"UID={ENTREGA3_USER};"
            f"PWD={ENTREGA3_PASSWORD};"
            "TrustServerCertificate=yes;"
        )
    params = urllib.parse.quote_plus(conn_str)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
