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

## dbt Transformation Status

The dbt layer has been implemented and validated successfully.

| Area         | Result                             |
| ------------ | ---------------------------------- |
| Sources      | 5 raw Snowflake sources configured |
| Models       | 8 dbt models built                 |
| Staging      | 5 Silver views                     |
| Intermediate | 1 intermediate view                |
| Marts        | 2 Gold tables                      |
| Tests        | 13 data quality tests passed       |
| Docs         | dbt docs generated successfully    |

### dbt Model Schemas

| Layer        | Snowflake Schema | Materialization |
| ------------ | ---------------- | --------------- |
| Silver       | DBT_SILVER       | Views           |
| Intermediate | DBT_INTERMEDIATE | Views           |
| Gold         | DBT_GOLD         | Tables          |



