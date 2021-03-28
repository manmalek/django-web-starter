from django import template
from store.models import *

register = template.Library()

@register.filter(name='treeview_children')
def treeview_children(category,level):
	print ("**************************"+str(level))
	return Category.objects.filter(parent_id=category.id)