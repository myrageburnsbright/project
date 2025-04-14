from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse 
from django.shortcuts import redirect
from django.template.loader import render_to_string
from goods.models import Product
from carts.models import Cart
from carts.utils import get_user_carts

# Create your views here.
def cart_add(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)
        
    user_carts = get_user_carts(request)
    
    cart_item_html = render_to_string(
        "carts/includes/included_cart.html", {"carts" : user_carts}, request=request
    )

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_item_html,
    }
    return JsonResponse(response_data)
def cart_change(request):
    card_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")
    cart = Cart.objects.get(id=card_id)
    cart.quantity = quantity
    cart.save()

    user_carts = get_user_carts(request)

    context = {"carts": user_carts}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get('HTTP_REFERER')
    if reverse('orders:create_order') in referer:
        context["order"] = True
    cart_item_html = render_to_string(
        "carts/includes/included_cart.html", context=context, request=request
    )

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_item_html,
    }
    return JsonResponse(response_data)

def cart_remove(request):
    card_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=card_id)
    quantity = cart.quantity
    cart.delete()

    user_carts = get_user_carts(request)

    context = {"carts": user_carts}
 
    # if referer page is create_order add key orders: True to context
    referer = request.META.get('HTTP_REFERER')
    if reverse('orders:create_order') in referer:
         context["order"] = True

    cart_item_html = render_to_string(
        "carts/includes/included_cart.html", context=context, request=request
    )

    response_data = {
        "message": "Товар удален",
        "cart_items_html": cart_item_html,
        "quantity_deleted": quantity
    }
    return JsonResponse(response_data)