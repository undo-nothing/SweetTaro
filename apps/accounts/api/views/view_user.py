
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.api.viewset import ApiGenericViewSet
from apps.accounts.api import serializers


User = get_user_model()


class UserViewSet(ApiGenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    """
    UserList
    """
    model = User
    queryset = User.objects.all()

    serializer_dict = {
        'list': serializers.UserSerializer,
        'retrieve': serializers.UserSerializer,
        'create': serializers.UserCreateSerializer,
        'update': serializers.UserUpdateSerializer,
        'partial_update': serializers.UserUpdateSerializer,
    }

    @action(methods=['get'], detail=True)
    def user_profile(self, request, *args, **kwargs):
        instance = self.get_object()
        info = {
            'nickname': 'test nickname',
            'userphoto': 'userphoto/%s.jpg' % instance.id,
        }
        return Response(info)
