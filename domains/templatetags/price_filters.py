from django import template

register = template.Library()

@register.filter
def format_price(value):
    try:
        value = float(value)
        if value < 1000:
            return f"{int(value)}"
        elif value < 1000000:
            return f"{value / 1000:.1f}K".rstrip('0').rstrip('.')
        else:
            return f"{value / 1000000:.1f}M".rstrip('0').rstrip('.')
    except (ValueError, TypeError):
        return value  # Return the original value if it cannot be formatted
