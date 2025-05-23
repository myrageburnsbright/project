
from django.db import models
from goods.models import Product
from users.models import User

class OrderitemQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_DEFAULT, verbose_name="Пользователь", default=None,blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    requires_delivery = models.BooleanField(default=False, verbose_name="Требуеться доставка")
    delivery_address= models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(default=True, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default="В обработке", verbose_name="Статус заказа")
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, verbose_name="Цена заказа")

    class Meta:
        db_table = 'order'
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)

    def __str__(self):
        return f"Заказ №{self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, verbose_name="Заказы")
    product = models.ForeignKey(Product, on_delete = models.SET_DEFAULT, verbose_name="Заказы☻", default=None,blank=True, null=True)
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")

    objects = OrderitemQueryset.as_manager()

    class Meta:
        db_table = 'order_item'
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("id",)
        
    def products_price(self):
        return round( self.price * self.quantity, 2)
    
    def __str__(self):
        return f"Товар {self.name} | заказ № {self.order.pk} "
    