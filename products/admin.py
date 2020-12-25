from django.contrib import admin

from products.models import Category, Product, Friend,SubCategory

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Friend)
admin.site.register(SubCategory)