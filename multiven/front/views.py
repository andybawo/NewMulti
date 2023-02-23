from django.shortcuts import render
from store.models import Product


def frontpage(request):
    products = Product.objects.all()[0:12]
    return render(request, 'front/frontpage.html', {
        'products': products
    })

def about(request):
    return render(request, 'front/about.html')