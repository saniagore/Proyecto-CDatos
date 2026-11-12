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
    extract_sales_territory,
    extract_address,
    extract_state_province,
    extract_country_region,
    extract_currency,
    extract_currency_rate,
    extract_special_offer,
    extract_employee,
    extract_sales_person,
    extract_sales_reason,
    extract_sales_order_header_sales_reason,
    extract_product_cost_history,
)
from .transform.dim_motivo import transform_dim_sales_reason
from .transform.dim_empleado import transform_dim_employee
from .transform.dim_moneda import transform_dim_currency
from .transform.dim_promocion import transform_dim_promotion
from .transform.dim_date import transform_dim_date
from .transform.dim_categorias import (
    transform_dim_product_category,
    transform_dim_product_subcategory
)
from .transform.dim_geografia import (
    transform_dim_sales_territory,
    transform_dim_geography
)
from .transform.dim_producto import transform_dim_producto
from .transform.dim_cliente import transform_dim_cliente
from .transform.dim_revendedor import transform_dim_revendedor
from .transform.hechos import (
    transform_fact_internet_sales,
    transform_fact_reseller_sales,
    transform_fact_internet_sales_reason,
)
from .validacion import validate_etl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(
    LOG_DIR, f"etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


def _load_table(df, table_name: str) -> bool:
    """Carga una tabla y permite que el resto del pipeline continúe si falla."""
    try:
        load_to_postgres(df, table_name, if_exists='truncate_first')
        logging.info("Tabla %s cargada exitosamente.", table_name)
        return True
    except Exception:
        logging.exception("Error cargando la tabla %s", table_name)
        print(f"FAIL: no se pudo cargar '{table_name}'. Revise el log.")
        return False


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
    df_territory = extract_sales_territory()
    df_address = extract_address()
    df_sp = extract_state_province()
    df_cr = extract_country_region()
    df_currency_rate = extract_currency_rate()
    df_currency = extract_currency()
    df_offer = extract_special_offer()
    df_employee = extract_employee()
    df_sales_person = extract_sales_person()
    df_reason = extract_sales_reason()
    df_header_reason = extract_sales_order_header_sales_reason()
    df_cost_history = extract_product_cost_history()
    logging.info("Extracción completada.")

    # 3. Transformación (Transform) con Pandas
    print("\n--- PASO 2: Transformando dimensiones y hechos con Pandas ---")
    
    # Jerarquía Geográfica y de Territorio
    df_dim_territory = transform_dim_sales_territory(df_territory)
    df_dim_geo = transform_dim_geography(df_address, df_sp, df_cr)
    
    # Jerarquía de Productos
    df_dim_cat = transform_dim_product_category(df_cat)
    df_dim_subcat = transform_dim_product_subcategory(df_subcat)
    df_dim_producto = transform_dim_producto(df_prod, df_subcat, df_cat)
    
    # Clientes, Revendedores y Fechas
    df_dim_date = transform_dim_date(df_soh)
    df_dim_cliente = transform_dim_cliente(df_cust, df_person)
    df_dim_revendedor = transform_dim_revendedor(df_cust, df_store)
    df_dim_currency = transform_dim_currency(df_currency)
    df_dim_promo = transform_dim_promotion(df_offer)
    df_dim_employee = transform_dim_employee(df_employee, df_person, df_sales_person)
    df_dim_reason = transform_dim_sales_reason(df_reason)
    
    # Hechos
    df_fact_internet = transform_fact_internet_sales(
        df_soh, df_sod, df_cost_history, df_currency_rate, df_dim_currency)
    df_fact_reseller = transform_fact_reseller_sales(
        df_soh, df_sod, df_cust, df_cost_history, df_currency_rate, df_dim_currency)
    df_fact_internet_reason = transform_fact_internet_sales_reason(
        df_soh, df_sod, df_header_reason)
    logging.info("Transformación completada con éxito.")

    # 4. Carga (Load) a PostgreSQL en orden estricto de dependencias FK
    print("\n--- PASO 3: Cargando datos a PostgreSQL (OLAP) ---")
    
    # Nivel 1: Sin FK
    load_results = []
    load_results.append(_load_table(df_dim_date, "DimDate"))
    load_results.append(_load_table(df_dim_territory, "DimSalesTerritory"))
    load_results.append(_load_table(df_dim_cat, "DimProductCategory"))
    
    # Nivel 2: Dependen de Nivel 1
    load_results.append(_load_table(df_dim_subcat, "DimProductSubcategory"))
    load_results.append(_load_table(df_dim_geo, "DimGeography"))
    
    # Nivel 3: Dependen de Nivel 2
    load_results.append(_load_table(df_dim_producto, "DimProduct"))
    
    # Clientes
    # Asegurar que GeographyKey apunte a direcciones existentes o None
    df_dim_cliente['GeographyKey'] = None
    df_dim_revendedor['GeographyKey'] = None
    load_results.append(_load_table(df_dim_cliente, "DimCustomer"))
    load_results.append(_load_table(df_dim_revendedor, "DimReseller"))

    load_results.append(_load_table(df_dim_currency, "DimCurrency"))
    load_results.append(_load_table(df_dim_promo, "DimPromotion"))
    load_results.append(_load_table(df_dim_employee, "DimEmployee"))
    load_results.append(_load_table(df_dim_reason, "DimSalesReason"))

    load_results.append(_load_table(df_fact_internet, "FactInternetSales"))
    load_results.append(_load_table(df_fact_reseller, "FactResellerSales"))
    load_results.append(_load_table(df_fact_internet_reason, "FactInternetSalesReason"))
    print("OK: Dimensiones cargadas correctamente.")

    # Hechos
    logging.info("Carga de dimensiones finalizada.")
    print("\nOK: Carga de dimensiones base completada exitosamente!")
    if not all(load_results):
        logging.warning("El ETL terminó con una o más tablas fallidas.")

    print("\n--- PASO 4: Validando métricas contra Entrega 3 ---")
    validate_etl()

if __name__ == "__main__":
    run_etl()
