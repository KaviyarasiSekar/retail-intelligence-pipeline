{% macro clv_band(lifetime_value) %}
    case
        when {{ lifetime_value }} >= 30000 then 'VIP'
        when {{ lifetime_value }} >= 15000 then 'Loyal'
        else 'Regular'
    end
{% endmacro %}