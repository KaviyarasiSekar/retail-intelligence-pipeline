select * 
from {{ source ('raw_retail', 'reviews') }}
