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

## dbt Validation

| Check        | Result |
| ------------ | ------ |
| dbt run      | PASS   |
| dbt test     | PASS   |
| Models Built | 8      |
| Tests Passed | 13     |

## dbt Layers

| Layer        | Schema           |
| ------------ | ---------------- |
| Staging      | DBT_SILVER       |
| Intermediate | DBT_INTERMEDIATE |
| Gold         | DBT_GOLD         |

## 🏗 Project Architecture

I implemented a Medallion Architecture (Silver/Gold) to transform raw retail data into actionable business insights.

![dbt Lineage](./assets/dbt-lineage-graph.png)

## 🛡 Data Quality & Governance

Data integrity is enforced through 13 automated dbt tests, ensuring referential integrity between orders, customers, and products.

![dbt Test Results](./assets/dbt-test-results.png)

## ❄️ Snowflake Implementation

The final models are materialized in Snowflake across three distinct schemas to separate cleaning logic from business logic.

![Snowflake Structure](./assets/snowflake-schema-structure.png)

### 📊 Data Validation (Snowflake Gold Layer)

![Snowflake Validation Output](./assets/snowflake-gold-layer-validation.png)

Source freshness check is configured on RAW.ORDERS using order_ts.
The check warns when source data is older than 24 hours and errors after 48 hours.
