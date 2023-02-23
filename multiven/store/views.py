import djangoflutterwave
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models
from django.conf import settings
# function Q helps search for two products
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from .forms import OrderForm, Payform
from .models import Category, Product, Order, OrderItem, PaymentMade, Cart, CartItem
import requests
import json

from django.http import JsonResponse

# def add_to_cart(request, product_id):
#     cart = Cart(request)
#     cart.add(product_id)

#     return redirect('frontpage')

def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1
        cart = Cart(request)
        cart.add(product_id, quantity, True)

    return redirect ('cart_view')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect ('cart_view')

# def cart_view(request):
#     cart = Cart(request)

#     return render(request, 'store/cart_view.html', {
#         'cart': cart
#     })

# @login_required
# def checkout(request):
#     cart = Cart(request)


#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         cart = Cart.objects.get_or_create(user=request.user, completed=False)


#         if form.is_valid():
#             total_price = 0

#             for item in cart:
#                 product = item['product']
#                 total_price += product.price * int(item['quantity'])

#             order = form.save(commit=False)
#             order.created_by = request.user
#             order.paid_amount = total_price
#             order.save()

#             for item in cart:
#                 product = item['product']
#                 quantity = int(item['quantity'])
#                 price = product.price * quantity

#                 item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            
#             return redirect('pay')
#     else:
#         form = OrderForm()

#     return render(request, 'store/checkout.html', {
#         'cart': cart,
#         'form': form
#     })

# @login_required
# def pay(request):
#     cart = Cart(request)

#     if request.method == 'POST':
#         form = Payform(request.POST)
#         if form.is_valid():
#             total_price = 0

#             for item in cart:
#                 product = item['product']
#                 total_price += product.price * int(item['quantity'])

#             order = form.save(commit=False)
#             order.created_by = request.user
#             order.paid_amount = total_price
#             order.save()

#         for item in cart:
#             product = item['product']
#             quantity = int(item['quantity'])
#             price = product.price * quantity
#             # item = OrderItem.objects.create(product=product, price=price, quantity=quantity)

#         cart.clear()

#         return redirect('checkup')
#     else:
#         form = Payform()

#     return render(request, 'store/pay.html', {
#         'cart': cart,
#         'form': form
#     })


@login_required
def pay(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the payment details from the request
        payment_details = request.POST

        # Set the Flutterwave API endpoint and the required headers
        endpoint = 'https://api.flutterwave.com/v3/payments'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer FLWPUBK_TEST-4fd674a5860754826095020b0d39f5fa-X'
        }

        # Make the payment request to the Flutterwave API
        response = requests.post(endpoint, json=payment_details, headers=headers)

        # Check if the payment was successful
        if response.status_code == 200:
            # Payment was successful, clear the cart
            cart = Cart.objects.get(user=request.user)
            cart.item.clear()
            cart.save()
            return redirect('frontpage')
        else:
            # Payment failed, return an error message
            return render(request, 'store/pay.html', {'error': 'Payment failed'})
    else:
        # Render the payment form
        return render(request, 'store/pay.html')


@login_required
def checkup(request):
    return render(request, 'store/checkup.html')
    
@login_required
def search(request):
    find = request.GET.get('find', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=find) | Q(description__icontains=find))
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    return render(request, 'store/search.html', {
        'find':find,
        'products':products,
        'cart': cart
    })

@login_required
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products,
        'cart': cart
    })

def product_detail(request, category_slug, slug):
    # cart = Cart(request)
    # print(cart.get_total_cost)
    # to create a basic 404 error page
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    return render(request, 'store/product_detail.html', {
        'product': product,
        'cart':cart
    })


def cart(request):
    
    cart = None
    cartitems = []
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()
    
    context = {"cart":cart, "itemss":cartitems}
    return render(request, "store/cart.html", context)

def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created =CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        
        
        num_of_item = cart.num_of_items
        
        print(cartitem)
    return JsonResponse(num_of_item, safe=False)


def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.completed = True
    cart.save()
    messages.success(request, "Payment made successfully")
    return redirect("frontpage")