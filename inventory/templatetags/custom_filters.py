from django import template
from urllib.parse import unquote

register = template.Library()

@register.filter
def get_value_from_dict(dictionary, key):
    return dictionary.get(key, 0)


@register.filter(name='calculate_gains')
def calculate_gains(data):
    total_quantity, category, prix_unitaires_encoded = data.split(',')
    prix_unitaires = dict(item.split('=') for item in unquote(prix_unitaires_encoded).split(','))
    prix_unitaire = int(prix_unitaires.get(category, 0))
    return int(total_quantity) * prix_unitaire