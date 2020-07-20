from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .pagination import DefaultPaginationBase


class BaseGenericViewSet(viewsets.GenericViewSet):

    model = None
    pagination_class = DefaultPaginationBase
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)

    def get_serializer_class(self):
        return self.serializer_dict.get(self.action, None)
