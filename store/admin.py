from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.conf import settings
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.models import TreeManyToManyField
from django.forms import CheckboxSelectMultiple
# Register your models here.

from .models import *

#@admin.register(Category)
#class CategoryAdmin(admin.ModelAdmin):
#	fields  = ('name', 'available')
#	list_display = ('name','available','product_count')
#	list_filter = ("available",)
#	readonly_fields = ["slug"]
#
#	def get_queryset(self, request):
#		queryset=super().get_queryset(request)
#		queryset = queryset.annotate(
#			_product_count=Count("product", distinct=True)
#			)
#		return queryset
#
#	def product_count(self,obj):
#		return obj._product_count
#
#	product_count.admin_order_field = '_product_count'
#	list_per_page = 50

class CategoryAdmin(DjangoMpttAdmin):
	tree_auto_open = 0
	#fields  = ('name', 'available')
	ordering = ("name",)
	list_display = ('name','available','product_count')
	list_filter = ("available",)
	readonly_fields = ["slug"]

#    def has_change_permission(self, request, obj=None):
#        return request.user.is_superuser
#
	def get_tree_animation_speed(self):
		if getattr(settings, "DJANGO_TESTING", False):
			return 0
		else:
			return None

	def get_tree_mouse_delay(self):
		if getattr(settings, "DJANGO_TESTING", False):
			return 0
		else:
			return None

	def get_queryset(self, request):
		queryset=super().get_queryset(request)
		queryset = queryset.annotate(
			_product_count=Count("product", distinct=True)
			)
		return queryset

	def product_count(self,obj):
		return obj._product_count

	product_count.admin_order_field = '_product_count'
	list_per_page = 50





class ProductFeatureInLine(admin.TabularInline):
	model = ProductFeature#.objects.filter()

class ProductImagesInLine(admin.TabularInline):
	model = ProductImage#.objects.filter()

#@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	exclude = ['slug']
	list_display = ('name', 'orderItem_count')
	inlines = [ProductFeatureInLine,ProductImagesInLine]
	formfield_overrides = { TreeManyToManyField:{'widget':CheckboxSelectMultiple},}

	def get_queryset(self, request):
		queryset=super().get_queryset(request)
		queryset = queryset.annotate(
			_orderItem_count=Count("orderitem", distinct=True)
			)
		return queryset

	def orderItem_count(self,obj):
		return obj._orderItem_count

	readonly_fields = ["base_image"]

	def base_image(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
            )
    	)

	orderItem_count.admin_order_field = '_orderItem_count'
	list_per_page = 50





admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Feature)
admin.site.register(ProductFeature)
admin.site.register(SiteSetting)
admin.site.register(ProductImage)

#---------------------------------------------------
class ShopAdminSite(AdminSite):
    site_header = "پنل مدیریتی"
    site_title = "پنل مدیریتی فروشگاه"
    index_title = "به پنل مدیریتی فروشگاه خوش آمدید"

shop_admin_site = ShopAdminSite(name="shop_admin")

shop_admin_site.register(Customer)
shop_admin_site.register(Category, CategoryAdmin)
shop_admin_site.register(Product, ProductAdmin)
shop_admin_site.register(Order)
shop_admin_site.register(SiteSetting)
shop_admin_site.register(Feature)
shop_admin_site.register(ProductImage)
#---------------------------------------------------
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)