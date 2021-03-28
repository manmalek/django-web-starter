from django.contrib.admin import AdminSite
# Register your models here.

from .models import *

class CategoryAdmin(admin.ModelAdmin):
	#fields  = ('name', 'available',)
	list_display = ('name', 'available',)
	prepopulated_fields = {'slug':('name',)}

class ProductFeatureInLine(admin.StackedInline):
	model = ProductFeature

class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductFeatureInLine]

class ShopAdminSite(AdminSite):
    site_header = "پنل مدیریتی"
    site_title = "پنل مدیریتی فروشگاه"
    index_title = "به پنل مدیریتی فروشگاه خوش آمدید"

shop_admin_site = ShopAdminSite(name="shop_admin")

shop_admin_site.register(Customer)
shop_admin_site.register(Category, CategoryAdmin)
shop_admin_site.register(Product, ProductAdmin)
shop_admin_site.register(Order)
