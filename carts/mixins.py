from multiprocessing import context
from django.urls import reverse
from carts.models import Cart
from django.template.loader import render_to_string
from carts.utils import get_user_carts
class CartMixin():
    def get_cart(self, request, product = None, cart_id = None):
        if request.user.is_authenticated:
            query_kwargs = {"user" : request.user}
        else:
            query_kwargs = {"session_key" : request.session.session_key}
        
        if product:
            query_kwargs['product'] = product
        else:
            query_kwargs['id'] = cart_id
        return Cart.objects.filter(**query_kwargs).first()
    
    def render_cart(self, request):
        
        referer = request.META.get('HTTP_REFERER')
        if reverse('orders:create_order') in referer:
            context["order"] = True
    
        user_carts= get_user_carts(request)
        context = {"carts" : user_carts}
        
        return render_to_string(
        "carts/includes/included_cart.html", context=context, request=request
    )
            