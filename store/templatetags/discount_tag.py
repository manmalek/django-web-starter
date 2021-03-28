from django import template

register = template.Library()

@register.filter(name='discount_percent')
def discount_percent(value, arg):
    return int((100*int(value)/int(arg)))