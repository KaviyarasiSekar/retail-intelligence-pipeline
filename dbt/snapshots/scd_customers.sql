{% snapshot customer_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='check',
      check_cols=['email', 'full_name', 'country', 'city']
    )
}}

select *
from {{ ref('stg_customers') }}

{% endsnapshot %}