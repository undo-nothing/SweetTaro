from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class DefaultPaginationBase(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    page_query_param = "page"
    another_page_size_query_param = 'limit'
    max_page_size = 200

    def paginate_queryset(self, queryset, request, view=None):
        if not request.query_params.get(self.page_size_query_param):
            if request.query_params.get(self.another_page_size_query_param):
                self.page_size_query_param = self.another_page_size_query_param
        return super(DefaultPaginationBase, self).paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))
