from django.urls import path
from .views import (base_view,
                    category_view,
                    product_view,
                    cart_view,
                    add_to_cart_view,
                    remove_from_cart_view,
                    change_item_qty,
                    checkout_view,
                    order_create_view
                    )

urlpatterns = [
    path('', base_view, name='base'),
    path('category/<str:category_slug>/', category_view, name='category_detail'),
    path('product/<str:product_slug>/', product_view, name='product_detail'),
    path('remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('change_item_qty', change_item_qty, name='change_item_qty'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('order/', order_create_view, name='create_order')


]
