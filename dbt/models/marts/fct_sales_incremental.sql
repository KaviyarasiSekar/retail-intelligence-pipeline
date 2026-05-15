{{ config(
    materialized='incremental',
    unique_key='order_id',
    schema='gold'
) }}

with orders as(
    select * from {{ ref('stg_orders') }}
),

channel_mapping as(
    select *
    from {{ ref('sales_channel_mapping') }}
)

select 
    order_id,
    customer_id,
    placed_at,
    order_status,
    order_total,
    cm.channel_group,
    current_timestamp() as dbt_updated_at
from orders o
left join channel_mapping cm
    on o.sales_channel = cm.sales_channel

{% if is_incremental() %}
    -- Only grab records newer than the last one we have
    where placed_at > (
        select coalesce(max(placed_at), '1900-01-01'::timestamp) 
        from {{ this }}
    )
{% endif %}
