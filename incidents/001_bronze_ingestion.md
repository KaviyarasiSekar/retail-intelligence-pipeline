# Ticket 001: Bronze Ingestion

## Goal

Read raw CSV files from `data/landing` and write them into `data/bronze` as Parquet using PySpark.

## Input

data/landing/<entity>/2026-05-09/\*.csv

## Output

data/bronze/<entity>/load_date=2026-05-09/

## Entities

- customers
- orders
- order_items
- products
- reviews

## Requirements

- Read CSV with header
- Add load_date
- Add ingestion_timestamp
- Write Parquet
- Partition by load_date
- Produce row count validation file

## Interview topics

- Bronze layer
- PySpark read/write
- Parquet
- Partitioning
- Audit columns
