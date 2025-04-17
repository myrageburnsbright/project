from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from orders.forms import CreateOrderForm
from django.db import transaction
from carts.models import Cart
from orders.models import Order, OrderItem
from django.forms import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('orders:create_order')
    
    def get_initial(self):
        initial = super().get_initial()
        initial = {
            'first_name' : self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
            'requires_delivery': "1",        
        }
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)
                if cart_items.exists():
                    order = Order.objects.create(
                        user = user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                    )
                    total_price = 0
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price= cart_item.product.sell_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f"Недостаточное количество товара {name} на складе\
                                                    в наличии - {product.quantity}")
                        
                        item = OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )

                        total_price += item.products_price()
                        product.quantity -= quantity
                        product.save()
                    order.total_price = total_price
                    order.save()
                    cart_items.delete()

                    messages.success(self.request, "Заказ оформлен!")
                    return redirect(reverse('user:profile'))
        except ValidationError as e:
            messages.success(self.request, str(e))
        
        return self.render_to_response(self.get_context_data(form=form))
            
    def form_invalid(self, form):
        messages.error(self.request, "Заполните все обязательные поля и проверте!")
        super().form_invalid(form)
        return redirect('orders:create_order')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "Оформление заказа"
        context["order"] = True 
        #print(context['form']['requires_delivery'].value, "DEDEFEFE")

        return context
    
@login_required
def create_order(request):
    if request.method == "POST":
        form = CreateOrderForm(data = request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)
                    if cart_items.exists():
                        order = Order.objects.create(
                            user = user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price= cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f"Недостаточное количество товара {name} на складе\
                                                      в наличии - {product.quantity}")
                            
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )

                            product.quantity -= quantity
                            product.save()

                        cart_items.delete()

                        messages.success(request, "Заказ оформлен!")
                        return redirect(reverse('user:profile'))
            except ValidationError as e:
                messages.success(request, str(e))
    else:
        initial = {
            'first_name' : request.user.first_name,
            'last_name': request.user.last_name
        }
        form = CreateOrderForm(initial=initial)
    
    context = {
         'title':'Order',
         'form': form,
         'order':True,
    }
    return render(request, 'orders/create_order.html', context=context)

