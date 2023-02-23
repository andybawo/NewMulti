# function Q helps search for two products
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def search(request):
    find = request.GET.get('find', '')
    products = Product.objects.filter(Q(title__icontains=find) | Q(description__icontains=find))

    return render(request, 'store/search.html', {
        'find':find,
        'products':products
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, slug):
    # to create a basic 404 error page
    product = get_object_or_404(Product, slug=slug,)
    return render(request, 'store/product_detail.html', {
        'product': product
    })