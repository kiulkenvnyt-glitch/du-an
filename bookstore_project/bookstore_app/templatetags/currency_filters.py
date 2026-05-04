from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def vnd(value):
    try:
        amount = Decimal(str(value))
    except (TypeError, ValueError, InvalidOperation):
        return value

    rounded_amount = amount.quantize(Decimal('1'))
    formatted = f"{int(rounded_amount):,}".replace(",", ".")
    return f"{formatted} đ"

@register.filter
def usd_to_vnd(value):
    try:
        amount = Decimal(str(value))
    except (TypeError, ValueError, InvalidOperation):
        return value

    rate = Decimal('25000')
    return amount * rate
