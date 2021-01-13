from . models import Product, Category
import django_filters
from django_filters.filters import RangeFilter


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains')
    #price = RangeFilter()


    class Meta:
        model = Product
        fields = ['name']

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains')
    #price = RangeFilter()
    labels = {
           'contains': ('содержит')
       }


    class Meta:
        model = Category
        fields = ['name']
        labels = {
           'name': ('название')
}