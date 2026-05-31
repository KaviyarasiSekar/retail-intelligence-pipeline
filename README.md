## Retail Intelligence Pipeline with Snowflake and dbt

This project is a retail analytics data warehouse built using Snowflake and dbt.

The goal of this project is to load raw retail data into Snowflake, transform it using dbt, apply data quality checks and create business-ready tables for analytics.

### Project Overview

This project uses synthetic retail data such as customers, products, orders, order items and reviews.

#### The pipeline follows this flow:

CSV files -> Snowflake RAW tables -> dbt staging models -> dbt intermediate models -> dbt gold marts

#### The project includes:

    * Snowflake raw data loading
    * dbt staging, intermediate, and gold models
    * dbt data quality tests
    * dbt incremental model
    * dbt snapshot for SCD Type 2 history tracking
    * dbt seed for reference data
    * dbt macro for reusable SQL logic
    * dbt source freshness check
    * dbt documentation and lineage graph

### Total Stack

    * Snowflake
    * dbt Core
    * Python
    * SQL
    * Git and GitHub

### Project Architecture

This project follows a Medallion Architecture pattern.

RAW -> SILVER -> INTERMEDIATE -> GOLD

### RAW Layer

The RAW layer stores source data as loaded from CSV files.

#### Tables:

    * RAW.CUSTOMERS
    * RAW.PRODUCTS
    * RAW.ORDERS
    * RAW.ORDER_ITEMS
    * RAW.REVIEWS

### SILVER Layer

The Silver layer contains cleaned staging models created by dbt.

#### This layer is used for:

    * renaming columns
    * standardizing fields
    * preparing data for downstream models

#### Schema:

DBT_SILVER

### INTERMEDIATE Layer

The intermediate layer contains reusable transformation logic.

#### Schema:

DBT_INTERMEDIATE

### GOLD Layer

The Gold layer contains business-ready tables for reporting and analytics.

#### Schema:

DBT_GOLD

#### Gold models include:

    * FCT_SALES
    * FCT_SALES_INCREMENTAL
    * MART_CUSTOMER_CLV

## Current Validation Status

### Local Data Generation

Generated synthetic retail datasets:

| Dataset     | Row Count |
| ----------- | --------: |
| customers   |       500 |
| products    |       200 |
| orders      |     3,000 |
| order_items |    10,500 |
| reviews     |     3,704 |

### Snowflake Raw Layer Validation

Manual upload through SnowSight completed successfully.

| Raw Table       | Row Count |
| --------------- | --------: |
| RAW.CUSTOMERS   |       500 |
| RAW.PRODUCTS    |       200 |
| RAW.ORDERS      |     3,000 |
| RAW.ORDER_ITEMS |    10,500 |
| RAW.REVIEWS     |     3,704 |

## dbt Validation Status

The dbt layer has been implemented and validated successfully.

| Area         | Result                             |
| ------------ | ---------------------------------- |
| Sources      | 5 raw Snowflake sources configured |
| Models       | 8 dbt models built                 |
| Staging      | 5 Silver views                     |
| Intermediate | 1 intermediate view                |
| Marts        | 2 Gold tables                      |
| Tests        | 13 data quality tests passed       |
| dbt Docs     | Generated successfully             |

### dbt Layers

| Layer        | Snowflake Schema | Materialization |
| ------------ | ---------------- | --------------- |
| Silver       | DBT_SILVER       | Views           |
| Intermediate | DBT_INTERMEDIATE | Views           |
| Gold         | DBT_GOLD         | Tables          |

### dbt Features Used

### Models

dbt models are used to transform raw Snowflake tables into cleaned and business-ready tables.

### Tests

dbt tests are used to check data quality.

#### Examples:

    * not_null test on primary keys
    * unique test on IDs
    * relationships test between orders, customers and products

### Incremental Model

The project includes an incremental model:

FCT_SALES_INCREMENTAL
