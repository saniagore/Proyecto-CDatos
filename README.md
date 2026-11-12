# Proyecto de Ciencia de Datos - Entrega 4: Herramienta ETL con Pandas

Este repositorio contiene la implementación del pipeline ETL para construir los Datamarts de **Ventas por Internet (Internet Sales)** y **Ventas por Revendedores (Reseller Sales)** a partir de la base de datos operacional **AdventureWorks (OLTP en SQL Server)** hacia la bodega de datos en **PostgreSQL (OLAP)**.

## Estructura del Proyecto
etl_adventureworks/
├── config.py               # Conexiones (lee claves y credenciales desde variables de entorno)
├── extract.py              # Consultas con Pandas contra la base operacional (OLTP)
├── load.py                 # Carga de DataFrames a PostgreSQL (df.to_sql)
├── main.py                 # Orquestador del pipeline y orden de carga
├── validacion.py           # Conteos y sumas de control contra la bodega de la entrega 3
├── ddl/
│   └── crear_tablas.sql    # Esquema DDL del datamart en PostgreSQL
├── transform/              # Transformaciones modulares con DataFrames de Pandas
│   ├── dim_categorias.py   # Categorías y subcategorías de producto
│   ├── dim_cliente.py      # Clientes individuales (Internet Sales)
│   ├── dim_date.py         # Dimensión calendario
│   ├── dim_empleado.py     # Empleados y vendedores
│   ├── dim_geografia.py    # Territorios y geografía
│   ├── dim_moneda.py       # Monedas (DimCurrency)
│   ├── dim_motivo.py       # Motivos de venta (DimSalesReason)
│   ├── dim_producto.py     # Producto desnormalizado con subcategoría y categoría
│   ├── dim_promocion.py    # Ofertas especiales (DimPromotion)
│   ├── dim_revendedor.py   # Revendedores / tiendas (Reseller Sales)
│   └── hechos.py           # FactInternetSales, FactResellerSales y FactInternetSalesReason
└── logs/                   # Logs de ejecución (no se suben al repositorio)
```
## Requisitos Previos

- Python 3.10+
- Acceso a la base de datos operacional en SQL Server (`AdventureWorks`).
- Acceso a la base de datos destino en PostgreSQL (`AdventureWorksDW`).
- Acceso a la bodega SQL Server de la Entrega 3 para ejecutar las validaciones.

## Instalación

1. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   # En Windows PowerShell:
   .venv\Scripts\Activate.ps1
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   Copiar `.env.example` como `.env` y configurar las credenciales:
   ```bash
   cp .env.example .env
   ```
   Configure también `ENTREGA3_SERVER`, `ENTREGA3_DB` y sus credenciales.
   `VALIDATION_TOLERANCE` define la diferencia absoluta máxima aceptada (por defecto, `0.01`).

## Ejecución

Para correr el proceso completo de extracción, transformación, carga y validación:

```bash
python -m etl_adventureworks.main
```
