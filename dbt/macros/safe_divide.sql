{% macro safe_divide(numerator, denominator) %}
    case
        when {{ denominator }} = 0 then 0
        else round({{ numerator }} / {{ denominator }}, 2)
    end
{% endmacro %}