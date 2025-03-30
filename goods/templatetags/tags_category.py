from goods.models import Categories, Product
from django import template

register = template.Library()
@register.simple_tag()
def tag_categories():
    return Categories.objects.all()