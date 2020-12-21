from django.contrib import admin

from products.models import Category, Product, Friend

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Friend)