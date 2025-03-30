from django.shortcuts import render, get_list_or_404
from goods.models import Product, Categories
# Create your views here.
def catalog(request, category_slug):

    if category_slug == 'all':
        goods = Product.objects.all()
    else:
        goods = get_list_or_404(Product.objects.all().filter(category__slug=category_slug))

    context = {
        'title': "Home - Catalog",
        'goods' : goods,
        
    }

    return render(request, 'goods/catalog.html', context=context)

def product(request, product_slug):
    product = Product.objects.get(slug = product_slug)
    
    context = {
        'product' : product
    }

    return render(request, 'goods/product.html', context=context)