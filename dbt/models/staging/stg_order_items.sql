select *
from {{ source ('raw_retail', 'order_items') }}