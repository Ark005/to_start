"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from products.views import (
    indexView,
    postFriend, 
    checkNickName,
)

urlpatterns = [
 	path('', include('products.urls', namespace='mainapp')),
 	path('', include('checkout.urls', namespace='checkout')),
    path('product_detail.html',indexView),
    path('http://127.0.0.1:8000/product/br/',indexView),
    path('post/ajax/friend', postFriend, name = "post_friend"),
    path('get/ajax/validate/nickname', checkNickName, name = "validate_nickname"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('index11.html',indexView),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



