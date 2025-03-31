from django.shortcuts import render, get_list_or_404
from goods.models import Product, Categories
from django.core.paginator import Paginator
# Create your views here.
def catalog(request, category_slug, page = 1):

    if category_slug == 'all':
        goods = Product.objects.all()
    else:
        goods = get_list_or_404(Product.objects.all().filter(category__slug=category_slug))
    paginator = Paginator(goods, 3)
    current_page = paginator.page(page)

    context = {
        'title': "Home - Catalog",
        'goods' : current_page,
        'slug_url' : category_slug,      
    }
    
    return render(request, 'goods/catalog.html', context=context)

def product(request, product_slug):
    product = Product.objects.get(slug = product_slug)
    
    context = {
        'product' : product
    }

    return render(request, 'goods/product.html', context=context)