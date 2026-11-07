# Proyecto de Ciencia de Datos - Entrega 4: Herramienta ETL con Pandas

Este repositorio contiene la implementación del pipeline ETL para construir los Datamarts de **Ventas por Internet (Internet Sales)** y **Ventas por Revendedores (Reseller Sales)** a partir de la base de datos operacional **AdventureWorks (OLTP en SQL Server)** hacia la bodega de datos en **PostgreSQL (OLAP)**.

## Estructura del Proyecto

```text
etl_adventureworks/
├── config.py             # Conexiones (lee claves y credenciales desde variables de entorno)
├── ddl/
│   └── crear_tablas.sql  # Esquema DDL del datamart en PostgreSQL
├── extract.py            # Funciones read_sql con Pandas contra la base operacional (OLTP)
├── transform/            # Lógica modular de transformación con DataFrames de Pandas
│   ├── dim_producto.py   # Transformación y desnormalización de producto, subcategoría y categoría
│   ├── dim_cliente.py    # Transformación de clientes individuales (Internet Sales)
│   ├── dim_revendedor.py # Transformación de clientes comerciales / tiendas (Reseller Sales)
│   ├── dim_date.py       # Generación de la dimensión calendario
│   └── hechos.py         # Transformación de FactInternetSales y FactResellerSales
├── load.py               # Carga de DataFrames a PostgreSQL (df.to_sql)
├── main.py               # Orquestador del pipeline y orden de carga
├── validacion.py         # Conteos y sumas de control contra la bodega de la entrega 3
└── logs/                 # Registro de ejecuciones y trazabilidad
```

## Requisitos Previos

- Python 3.10+
- Acceso a la base de datos operacional en SQL Server (`AdventureWorks`).
- Acceso a la base de datos destino en PostgreSQL (`AdventureWorksDW`).

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

## Ejecución

Para correr el proceso completo de extracción, transformación, carga y validación:

```bash
python -m etl_adventureworks.main
```
