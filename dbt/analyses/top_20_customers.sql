select 
    customer_id,
    full_name,
    lifetime_value,
    number_of_orders
from {{ ref('mart_customer_clv') }}
where lifetime_value > 0
order by lifetime_value desc
limit 20
