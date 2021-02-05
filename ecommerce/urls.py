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
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from products.views import (
    indexView,
    postProduct, 
    checkNickName,
)

urlpatterns = [
 	path('', include('products.urls', namespace='mainapp')),
 	path('', include('checkout.urls', namespace='checkout')),
    path('post/ajax/product', postProduct, name = "post_product"),
    path('get/ajax/validate/nickname', checkNickName, name = "validate_nickname"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('about.html/', TemplateView.as_view(template_name="products/about.html")),
    path('requirements.html/', TemplateView.as_view(template_name="products/requirements.html")),
    path('technologies.html/', TemplateView.as_view(template_name="products/technologies.html")),
    path('layout.html/', TemplateView.as_view(template_name="products/layout.html")),
    path('delivery.html/', TemplateView.as_view(template_name="products/delivery.html")),
    path('photo.html/', TemplateView.as_view(template_name="products/photo.html")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



urlpatterns += staticfiles_urlpatterns()
