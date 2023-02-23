from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from userprofile.models import *
from django.utils.text import slugify
from .forms import ConfirmForm
from store.models import *


from store.forms import ProductForm
from store.models import Product, Category, OrderItem, Order
from userprofile.forms import SignUpForm





def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    return render(request, 'userprofile/vendor_detail.html', {
        'user': user,
        'products': products,
        'cart': cart
    })


#@login required block unauthorized user from accessing the pages
@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    order_items = OrderItem.objects.filter(product__user=request.user)

    return render(request, 'userprofile/my_store.html', {
        'products': products,
        'order_items': order_items
    })

@login_required 
def my_store_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'userprofile/my_store_order_detail.html', {
        'order': order,
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')

            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'Product successfully added')

            return redirect('my_store')
    else:
        form = ProductForm()

    return render(request, 'userprofile/add_product.html',{
        'title': 'Add Product',
        'form': form
    })

@login_required 
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            messages.success(request, 'Product Edited')

            return redirect('my_store') 
    else:
        form = ProductForm(instance=product)

    return render(request, 'userprofile/add_product.html',{
        'title': 'Edit Product',
        'product': product,
        'form': form
    })

@login_required 
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()

    messages.success(request, 'Product Deleted')

    return redirect('my_store')

@login_required
def myaccount(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    return render(request, 'userprofile/myaccount.html', {
        'cart': cart
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            userprofile = Userprofile.objects.create(user=user)

            return redirect('frontpage')
    else:
        form = SignUpForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })

@login_required
def clear(request):
    cart = Cart(request)


    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        cart = Cart.objects.get_or_create(user=request.user, completed=False)


        if form.is_valid():
            total_price = 0

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()
            
            return redirect('frontpage')
    else:
        form = ConfirmForm()

    return render(request, 'userprofile/clear.html', {
        'cart': cart,
        'form': form
    })



    return render(request, 'userprofile/clear.html',)