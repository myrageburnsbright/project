from pyclbr import Class
from re import search
from django.contrib import admin
from orders.admin import OrderTabulareAdmin
from carts.admin import CartTabAdmin
from carts.models import Cart
from users.models import User

# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email"]
    search_fields = ["username", "first_name", "last_name", "email"]
    inlines = [CartTabAdmin, OrderTabulareAdmin, ]