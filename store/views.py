from django.shortcuts import render, get_object_or_404, get_list_or_404
from . models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData, guestOrder, mainDetailes
from django.conf import settings
from django.db.models import Q

# Create your views here.
def store(request):
     data = cartData(request)
     cartItems = data['cartItems']
     products = Product.objects.all()
     context = {
          'products':products,
          'cartItems':cartItems,
          #'categories_level_0':category_level_0
          }

     maindetailes = mainDetailes(request)
     context = maindetailes | context
     return render(request, 'store/store.html', context)

def cart(request):
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = data # {'items':items,'order':order,'cartItems':cartItems}

     maindetailes = mainDetailes(request)
     context = maindetailes | context

     return render(request, 'store/cart.html', context)

def checkout(request):
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items,'order':order,'cartItems':cartItems}

     maindetailes = mainDetailes(request)
     context = maindetailes | context

     return render(request, 'store/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']
     quantity = data['quantity']

     print('Action:', action)
     print('Product:', productId)
     print('quantity:', quantity)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + int(quantity))
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)


def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
     else:
          customer, order = guestOrder(request, data)

     total = float(data['form']['total'])
     order.transaction_id = transaction_id

     if total == float(order.get_cart_total):
          print('******************* Completed ******************')
          order.complete = True
     else:
          print('>>>>>>>total: ', total, '>>>>>>>>get_cart_total:', order.get_cart_total)
     order.save()

     if order.shipping == True:
          ShippingAddress.objects.create(
          customer=customer,
          order=order,
          address=data['shipping']['address'],
          city=data['shipping']['city'],
          state=data['shipping']['state'],
          zipcode=data['shipping']['zipcode'],
          )
     
     return JsonResponse('Payment completed', safe=False)

# -- My Codes -------------------------------------------------------
def category(request, slug):
     data = cartData(request)
     cartItems = data['cartItems']

     category = get_object_or_404(Category, slug=slug)
     products = get_list_or_404(Product,category=category)
     context = {'products':products,'cartItems':cartItems, 'category':category}

     maindetailes = mainDetailes(request)
     context = maindetailes | context
     return render(request, 'store/store.html', context)

def product(request, slug):
     data = cartData(request)
     cartItems = data['cartItems']

     product = get_object_or_404(Product, slug=slug)

     context = {'product':product,'cartItems':cartItems}
     maindetailes = mainDetailes(request)
     context = maindetailes | context
     return render(request, 'store/product_details.html', context)



#-- Error Pages -----------------------------------------------------
def my_custom_page_not_found_view(request, exception=None):
     context = {'exception':exception}

     maindetailes = mainDetailes(request)
     context = maindetailes | context
     return render(request, 'store/not_found.html', context)