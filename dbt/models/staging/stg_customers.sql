select
    customer_id,
    email, 
    full_name,
    country,
    city,
    created_at
from {{ source('raw_retail', 'customers') }}
