from django import template
from core.models import Settings

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    return value.split(arg)

@register.simple_tag
def get_global_settings():
    return Settings.objects.first()
