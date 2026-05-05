select 
    order_id,
    customer_id,
    order_status,
    order_ts as placed_at,
    currency,
    order_total,
    sales_channel
from {{ source('raw_retail', 'orders') }}