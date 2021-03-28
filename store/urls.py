from django.urls import path, re_path
from .admin import shop_admin_site
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('shop-admin/', shop_admin_site.urls),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	re_path(r'product/(?P<slug>[-\w]+)/', views.product, name="product"),
	re_path(r'(?P<slug>[-\w]+)/', views.category, name="category"),
]