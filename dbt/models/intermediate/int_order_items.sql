-- join order items with product details.

with order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

enriched as (
    select 
        oi.order_item_id,
        oi.order_id,
        oi.product_id,
        p.product_name,
        p.category as product_category,
        oi.quantity,
        oi.line_total,
        p.unit_price as current_product_price
    from order_items oi
    left join products p on oi.product_id = p.product_id
)

select * from enriched
