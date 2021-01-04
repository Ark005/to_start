from django.urls import path
from cart.views import add_to_cart, remove_from_cart, CartView, decreaseCart
from . views import home, ProductDetail, Home, postFriend, \
checkNickName,indexView, show_subcategory, get_subcategory, postProduct, get_products, new_indexView

app_name= 'mainapp'

urlpatterns = [
    # выводит категорию
    path('', home, name='home'),


    path('p', Home.as_view(), name='home'),
    # детали продукта
    # старая вьюха
    # path('product/<slug>/', indexView, name='product'),
    # новая вьюха
    path('product/<slug>/', new_indexView, name='product'),
    
    # возвращает результат по ajax
    path('post_product', postProduct, name='postproduct'),
    path('subproduct/', show_subcategory, name='subproduct'),

    # возвращает субкатегорию
    path('get_subcategory/<category>/', get_subcategory, name='get_subcategory'),
    # возвращает категорию
    # path('get_category/<category>/', get_category, name='get_category'),

    path('get_subcategory/<category>/get_products/<subcategory>', get_products, name='get_products'),

    path('cart/', CartView, name='cart-home'),
    path('cart/<slug>', add_to_cart, name='cart'),
    path('decrease-cart/<slug>', decreaseCart, name='decrease-cart'),
    path('remove/<slug>', remove_from_cart, name='remove-cart'),
]


