-- This table provides a 360-degree view of the customer,
-- including their first order date and their total lifetime value (LTV).

with customers as (
    select * from {{ ref('stg_customers') }}
),

customer_orders as (
    select 
        customer_id,
        min(placed_at) as first_order_date,
        max(placed_at) as most_recent_order_date,
        count(order_id) as number_of_orders,
        sum(gross_revenue) as lifetime_value
    from {{ ref('fct_sales') }}
    group by 1
)

select 
    c.customer_id,
    c.full_name,
    c.email,
    c.country,
    co.first_order_date,
    co.most_recent_order_date,
    co.number_of_orders,
    co.lifetime_value
from customers c
left join customer_orders co on c.customer_id = co.customer_id