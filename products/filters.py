from . models import Product, Category
import django_filters
from django_filters.filters import RangeFilter


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains',label='поиск по названию')
    #price = RangeFilter()


    class Meta:
        model = Product
        fields = ['name']

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains',label='поиск по названию')
    class Meta:
        verbose_name = 'коробка'
    #price = RangeFilter()
   


    class Meta:
        model = Category
        fields = ['name']
      
