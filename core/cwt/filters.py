import django_filters

from .models import Test


class TestFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Test
        fields = ['title']
