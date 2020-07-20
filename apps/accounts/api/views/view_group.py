from rest_framework import mixins
from django.contrib.auth.models import Group

from apps.api.viewset import ApiGenericViewSet
from apps.accounts.api import serializers


class GroupViewSet(ApiGenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    """
    GroupViewSet
    """
    model = Group
    queryset = Group.objects.all()

    serializer_dict = {
        'list': serializers.GroupSerializer,
        'retrieve': serializers.GroupSerializer,
        'create': serializers.GroupCreateSerializer,
        'update': serializers.GroupUpdateSerializer,
        'partial_update': serializers.GroupUpdateSerializer,
    }

    def get_queryset(self):
        qs = super(GroupViewSet, self).get_queryset().order_by('id')
        return qs
