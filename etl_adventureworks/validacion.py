import logging
import math
import os
from decimal import Decimal

import pandas as pd

from .config import (
    ENTREGA3_SCHEMA,
    OLAP_SCHEMA,
    get_entrega3_engine,
    get_olap_engine,
)

TOLERANCE = float(os.getenv("VALIDATION_TOLERANCE", "0.01"))


def get_row_count(engine, table_name: str, schema: str = None) -> int:
    qualified_table = f'"{schema}"."{table_name}"' if schema else table_name
    query = f"SELECT COUNT(*) FROM {qualified_table};"
    df = pd.read_sql(query, con=engine)
    return int(df.iloc[0, 0])


def _get_metric(engine, table_name: str, column_name: str, schema: str = None):
    qualified_table = f'"{schema}"."{table_name}"' if schema else table_name
    query = (
        f'SELECT COALESCE(SUM("{column_name.lower()}"), 0) '
        f"FROM {qualified_table};"
    )
    value = pd.read_sql(query, con=engine).iloc[0, 0]
    return Decimal(str(value))


def _is_within_tolerance(actual: Decimal, expected: Decimal) -> bool:
    return math.isclose(
        float(actual),
        float(expected),
        rel_tol=0,
        abs_tol=TOLERANCE,
    )


def _print_validation(label: str, actual: Decimal, expected: Decimal) -> bool:
    difference = actual - expected
    passed = _is_within_tolerance(actual, expected)
    status = "PASS" if passed else "FAIL"
    print(
        f"[{status}] {label}: datamart={actual} | "
        f"bodega_entrega3={expected} | diferencia={difference}"
    )
    if passed:
        logging.info("%s PASS: actual=%s esperado=%s diferencia=%s",
                     label, actual, expected, difference)
    else:
        logging.error("%s FAIL: actual=%s esperado=%s diferencia=%s",
                      label, actual, expected, difference)
    return passed


def validate_etl() -> bool:
    """Compara las métricas cargadas en PostgreSQL contra la bodega de Entrega 3."""
    olap_engine = get_olap_engine()
    entrega3_engine = get_entrega3_engine()
    print("==========================================")
    print("VALIDACIÓN DE DATAMARTS CONTRA ENTREGA 3")
    print("==========================================")

    all_passed = True
    tables_to_check = [
        "dimproduct",
        "dimcustomer",
        "dimreseller",
        "dimdate",
        "factinternetsales",
        "factresellersales",
    ]
    for table in tables_to_check:
        try:
            count = get_row_count(olap_engine, table, OLAP_SCHEMA)
            print(f"[{table}] Total de registros cargados: {count}")
        except Exception:
            logging.exception("Error validando conteo de %s", table)
            print(f"[FAIL] {table}: no fue posible validar el conteo")
            all_passed = False

    metric_checks = [
        ("Internet SalesAmount", "factinternetsales", "SalesAmount",
         "FactInternetSales"),
        ("Reseller SalesAmount", "factresellersales", "SalesAmount",
         "FactResellerSales"),
        ("Internet OrderQuantity", "factinternetsales", "OrderQuantity",
         "FactInternetSales"),
        ("Reseller OrderQuantity", "factresellersales", "OrderQuantity",
         "FactResellerSales"),
    ]
    for label, olap_table, column, entrega3_table in metric_checks:
        try:
            actual = _get_metric(olap_engine, olap_table, column, OLAP_SCHEMA)
            reference = _get_metric(
                entrega3_engine,
                f"[{ENTREGA3_SCHEMA}].[{entrega3_table}]",
                column,
            )
            all_passed = _print_validation(label, actual, reference) and all_passed
        except Exception:
            logging.exception("Error validando %s", label)
            print(f"[FAIL] {label}: no fue posible consultar ambas bodegas")
            all_passed = False

    print(f"\nResultado general: {'PASS' if all_passed else 'FAIL'}")
    return all_passed


if __name__ == "__main__":
    validate_etl()
