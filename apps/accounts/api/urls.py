from django.urls import include, path

from . import views


# will exec register() in apps.api.url
accounts_register_list = [
    (r'users', views.UserViewSet, 'user'),
    (r'groups', views.GroupViewSet, 'group'),
    (r'permissions', views.PermissionViewSet, 'permission'),
]

urlpatterns = [
    # path('', include(router.urls)),
]
