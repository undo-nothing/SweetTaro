from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from apps.api.viewset import ApiGenericViewSet
from apps.bing_wapper.models import BingWapper
from apps.bing_wapper.api import serializers
from apps.bing_wapper.api.filters import BingWapperFilter
from apps.api.mixins import ExportModelMixin
from apps.bing_wapper.task import check_bingwapper_data_task


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
    permission_classes = (IsAuthenticatedOrReadOnly, )

    serializer_dict = {
        'list': serializers.BingWapperSerializer,
        'metadata': serializers.BingWapperSerializer,
        'retrieve': serializers.BingWapperSerializer,
        'create': serializers.BingWapperCreateSerializer,
        'update': serializers.BingWapperUpdateSerializer,
        'partial_update': serializers.BingWapperUpdateSerializer,
        'export': serializers.BingWapperSerializer,
    }

    @action(methods=['get'], detail=False, permission_classes=(IsAuthenticated, ))
    def check_bingwapper(self, request, async_task=True, recorder=None):
        check_bingwapper_data_task.delay()
        return Response({'code': 0, 'message': 'success'})
