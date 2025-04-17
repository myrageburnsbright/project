from django.shortcuts import render, get_list_or_404
from django.http import Http404
from goods.models import Product, Categories
from django.core.paginator import Paginator
from .utils import q_search
from goods.utils import q_search
from django.views.generic import TemplateView, DetailView, ListView

# Create your views here.
class CatalogView(ListView):
    model = Product
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by =  3
    allow_empty = False
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')

        #page = self.request.GET.get('page', 1)
        on_sale = self.request.GET.get('on_sale', None)
        order_by = self.request.GET.get('order_by', None)
        query = self.request.GET.get('q', None)

        if category_slug == 'all':
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()
            
        if on_sale:
            goods = goods.filter(discount__gt=0)
        if order_by and order_by != "default":
            goods = goods.order_by(order_by)
        
        return goods
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Home - Catalog"
        context['slug_url'] = self.kwargs.get('category_slug')
        return context

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
        goods = Product.objects.filter(category__slug=category_slug)
        if not goods.exists():
             raise Http404()
        
    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)
    
    paginator = Paginator(goods, 3)
    current_page = paginator.page(page)

    context = {
        'title': "Home - Catalog",
        'goods' : current_page,
        'slug_url' : category_slug,      
    }
    
    return render(request, 'goods/catalog.html', context=context)

class ProductView(DetailView):
    template_name = 'goods/product.html'
    #slug_field = "slug"
    #slug_url_kwarg = "product_slug"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset = ...):
        #print(self.slug_url_kwarg)
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context
    

# def product(request, product_slug):
#     product = Product.objects.get(slug = product_slug)
    
#     context = {
#         'product' : product
#     }

#     return render(request, 'goods/product.html', context=context)