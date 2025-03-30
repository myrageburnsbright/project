from django.shortcuts import render
from goods.models import Product, Categories
# Create your views here.
def catalog(request):

    goods = Product.objects.all()
    
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