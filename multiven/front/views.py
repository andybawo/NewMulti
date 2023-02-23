from django.shortcuts import render
from store.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import * 


@login_required
def frontpage(request):
    products = Product.objects.filter(status=Product.ACTIVE)[0:6]
    # messages.success(request, "Payment made successfully")
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    return render(request, 'front/frontpage.html', {
        'cart':cart,
        'products': products,
    })

def about(request):
    return render(request, 'front/about.html')