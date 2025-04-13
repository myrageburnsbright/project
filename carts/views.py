from django.shortcuts import render
from goods.models import Product
from carts.models import Cart
from django.shortcuts import redirect

# Create your views here.
def cart_add(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    
    return redirect(request.META['HTTP_REFERER'])

def cart_change(request, product_slug):
    return render()

def cart_remove(request, product_slug):
    pass