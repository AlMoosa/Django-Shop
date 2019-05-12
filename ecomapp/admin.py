from django.contrib import admin
from .models import Category, Brand, Product, CartItem, Cart, Order
# Register your models here.


def make_payed(modeladmin, request, queryset):
    queryset.update(status='Оплачено')
make_payed.short_description = "Помітити як оплчені"


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payed]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)


