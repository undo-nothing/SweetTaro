from rest_framework import mixins

from apps.api.viewset import ApiGenericViewSet
from apps.bing_wapper.models import BingWapper
from apps.bing_wapper.api import serializers
from apps.bing_wapper.api.filters import BingWapperFilter
from apps.api.mixins import ExportModelMixin


class BingWapperViewSet(ApiGenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        ExportModelMixin):
    """
    BingWapperList
    """
    model = BingWapper
    queryset = BingWapper.objects.all()
    ordering_fields = ('id', 'date')
    filter_class = BingWapperFilter

    serializer_dict = {
        'list': serializers.BingWapperSerializer,
        'metadata': serializers.BingWapperSerializer,
        'retrieve': serializers.BingWapperSerializer,
        'create': serializers.BingWapperCreateSerializer,
        'update': serializers.BingWapperUpdateSerializer,
        'partial_update': serializers.BingWapperUpdateSerializer,
        'export': serializers.BingWapperSerializer,
    }
