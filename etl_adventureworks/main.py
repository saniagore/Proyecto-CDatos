import logging
import os
from datetime import datetime

from .config import OLAP_SCHEMA
from .load import execute_sql_file, load_to_postgres
from .extract import (
    extract_sales_order_header,
    extract_sales_order_detail,
    extract_customer,
    extract_person,
    extract_store,
    extract_product,
    extract_product_subcategory,
    extract_product_category,
)
from .transform.dim_date import transform_dim_date
from .transform.dim_producto import transform_dim_producto
from .transform.dim_cliente import transform_dim_cliente
from .transform.dim_revendedor import transform_dim_revendedor
from .transform.hechos import (
    transform_fact_internet_sales,
    transform_fact_reseller_sales
)
from .validacion import validate_etl

# Configuración de logging
os.makedirs("etl_adventureworks/logs", exist_ok=True)
log_file = f"etl_adventureworks/logs/etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def run_etl():
    print("Iniciando pipeline ETL para Datamarts de AdventureWorks...")
    logging.info("Inicio del proceso ETL")

    # 1. Crear tablas en PostgreSQL si no existen (DDL)
    ddl_path = os.path.join(os.path.dirname(__file__), "ddl", "crear_tablas.sql")
    if os.path.exists(ddl_path):
        print("-> Verificando/creando tablas DDL en PostgreSQL...")
        try:
            execute_sql_file(ddl_path)
            logging.info("DDL ejecutado exitosamente.")
        except Exception as e:
            logging.warning(f"Aviso en DDL: {e}")

    # 2. Extracción (Extract) con Pandas
    print("\n--- PASO 1: Extrayendo datos operacionales (SQL Server) ---")
    df_soh = extract_sales_order_header()
    df_sod = extract_sales_order_detail()
    df_cust = extract_customer()
    df_person = extract_person()
    df_store = extract_store()
    df_prod = extract_product()
    df_subcat = extract_product_subcategory()
    df_cat = extract_product_category()
    logging.info("Extracción completada.")

    # 3. Transformación (Transform) con Pandas
    print("\n--- PASO 2: Transformando dimensiones y hechos con Pandas ---")
    
    # Dimensiones
    df_dim_date = transform_dim_date(df_soh)
    df_dim_producto = transform_dim_producto(df_prod, df_subcat, df_cat)
    df_dim_cliente = transform_dim_cliente(df_cust, df_person)
    df_dim_revendedor = transform_dim_revendedor(df_cust, df_store)

    # Hechos
    df_fact_internet = transform_fact_internet_sales(df_soh, df_sod)
    df_fact_reseller = transform_fact_reseller_sales(df_soh, df_sod)
    logging.info("Transformación completada con éxito.")

    # 4. Carga (Load) a PostgreSQL
    # Orden de carga: Dimensiones primero, luego Tablas de Hechos
    print("\n--- PASO 3: Cargando datos a PostgreSQL (OLAP) ---")
    load_to_postgres(df_dim_date, "DimDate")
    load_to_postgres(df_dim_producto, "DimProduct")
    load_to_postgres(df_dim_cliente, "DimCustomer")
    load_to_postgres(df_dim_revendedor, "DimReseller")
    load_to_postgres(df_fact_internet, "FactInternetSales")
    load_to_postgres(df_fact_reseller, "FactResellerSales")
    logging.info("Carga completada con éxito.")

    # 5. Validación
    print("\n--- PASO 4: Validación y control de calidad ---")
    validate_etl()
    logging.info("Validación finalizada.")
    print("\n¡Pipeline ETL completado exitosamente!")

if __name__ == "__main__":
    run_etl()
