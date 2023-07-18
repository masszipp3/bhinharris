from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def mul(value, arg):
    return round(value * arg,2)

@register.filter
def calculate_vat(total):
    vat_rate = float(0.05)  # VAT rate of 5%
    vat_amount = total * vat_rate

    return round(vat_amount,2)


@register.filter
def calculate_total_with_vat(total):
    vat_rate = float('0.05') # VAT rate of 5%
    vat_amount = total * vat_rate
    total_with_vat = total + vat_amount
    return round(total_with_vat,2)


    
