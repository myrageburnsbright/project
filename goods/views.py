from django.shortcuts import render, get_list_or_404
from goods.models import Product, Categories
from django.core.paginator import Paginator
from .utils import q_search
from goods.utils import q_search
# Create your views here.
def catalog(request, category_slug = None) :
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Product.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Product.objects.all().filter(category__slug=category_slug)
    
    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)
    goods = get_list_or_404(goods)
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