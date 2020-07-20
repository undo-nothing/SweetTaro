
from django.urls import include, path

from . import views

# will exec register() in apps.api.url
bing_wapper_register_list = [
    (r'bingwappers', views.BingWapperViewSet, 'bingwapper'),
]

urlpatterns = [
    # path('', include(router.urls)),
]
