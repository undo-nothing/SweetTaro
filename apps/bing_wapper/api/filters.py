from django_filters import rest_framework as filters

from apps.bing_wapper.models import BingWapper


class BingWapperFilter(filters.FilterSet):

    filename_icontains = filters.CharFilter(field_name="filename", lookup_expr='icontains')
    title_icontains = filters.CharFilter(field_name="title", lookup_expr='icontains')
    date_gte = filters.DateFilter(field_name="date", lookup_expr='get')
    date_lte = filters.DateFilter(field_name="date", lookup_expr='lte')
    year = filters.NumberFilter(field_name='date', method='filter_date_year')
    month = filters.NumberFilter(field_name='date', method='filter_date_month')
    day = filters.NumberFilter(field_name='date', method='filter_date_day')
    default = filters.CharFilter(field_name='default', method='filter_default')

    def filter_date_year(self, qs, name, value):
        return qs.filter(date__year=value)

    def filter_date_month(self, qs, name, value):
        return qs.filter(date__month=value)

    def filter_date_day(self, qs, name, value):
        return qs.filter(date__day=value)

    def filter_default(self, qs, name, value):
        if not qs.exists():
            if value == 'latest':
                qs = BingWapper.objects.order_by('-date')[:1]

        return qs

    class Meta:
        model = BingWapper
        fields = ['filename', 'filename_icontains',
                  'title', 'title_icontains',
                  'date', 'author',
                  'year', 'month', 'day'
                  ]
