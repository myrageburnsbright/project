from django.contrib import admin

# Register your models here.
from goods.models import Categories, Product

#admin.site.register(Categories)


#admin.site.register(Product)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_products')
    #list_display = ('name', 'slug', 'products')
    prepopulated_fields = {'slug': ('name',)}
    def get_products(self, obj):
        # Если нужно показать список названий продуктов через запятую:
        return ", ".join([p.name for p in obj.products.all()])
    get_products.short_description = 'Продукты'

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
