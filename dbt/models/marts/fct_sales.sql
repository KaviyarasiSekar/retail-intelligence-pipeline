-- Fact Table enriched with Sales Channel Mapping Seed

with orders as (
    select * 
    from {{ ref('stg_orders') }}
),

order_item_summary as (
    select
        order_id,
        sum(line_total) as gross_revenue,
        sum(quantity) as total_items,
        count(distinct product_id) as unique_products_count
    from {{ ref('int_order_items') }}
    group by 1
),

-- Seed
channel_mapping as(
    select * 
    from {{ ref('sales_channel_mapping') }} 
)

select 
    o.order_id,
    o.customer_id,
    o.placed_at,
    o.order_status,
    o.sales_channel,
    cm.channel_group, -- from seed mapping
    s.gross_revenue,
    s.total_items,
    s.unique_products_count
from orders o
left join order_item_summary s on o.order_id = s.order_id
-- join to the seed
left join channel_mapping cm on o.sales_channel = cm.sales_channel