from collections import OrderedDict

from django.contrib.auth.models import Permission
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.api import serializers
from apps.api.viewset import ApiGenericViewSet


class PermissionViewSet(ApiGenericViewSet,
                        mixins.ListModelMixin,
                        # mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        # mixins.UpdateModelMixin,
                        # mixins.DestroyModelMixin
                        ):
    """
    PermissionViewSet
    """
    model = Permission
    queryset = Permission.objects.all()

    serializer_dict = {
        'list': serializers.PermissionSerializer,
        'retrieve': serializers.PermissionSerializer,
        'create': serializers.PermissionCreateSerializer,
        'update': serializers.PermissionUpdateSerializer,
        'partial_update': serializers.PermissionUpdateSerializer,
    }

    @action(methods=['get'], detail=False)
    def tree(self, request, *args, **kwargs):
        perms = Permission.objects.select_related('content_type').order_by('id')
        nodes = OrderedDict()
        for perm in perms:
            ct = perm.content_type.id
            if ct not in nodes:
                nodes[ct] = {
                    'id': 'ct_%s' % ct,
                    'label': perm.content_type.model,
                    'children': []
                }
            node = {'id': perm.id, 'label': perm.codename}
            children = nodes[ct].get('children')
            children.append(node)
        return Response(list(nodes.values()))
