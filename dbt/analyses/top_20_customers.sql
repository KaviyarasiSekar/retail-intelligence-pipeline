select 
    customer_id,
    full_name,
    total_revenue,
    total_orders
from {{ ref('mart_customer_clv') }}
where total_revenue > 0
order by total_revenue desc
limit 20
