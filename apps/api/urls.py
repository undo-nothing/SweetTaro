from django.urls import include, path
from rest_framework.authtoken import views as authtoken_views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from apps.accounts.api.urls import accounts_register_list
from apps.bing_wapper.api.urls import bing_wapper_register_list

register_list = []
register_list += accounts_register_list
register_list += bing_wapper_register_list


router = DefaultRouter()
for argc in register_list:
    router.register(*argc)

api_docs_urls = [
    path('v1.0/', include(router.urls))
]

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='api-auth')),
    path('api-token-auth/', authtoken_views.obtain_auth_token),
    path('jwt-api-token-auth/', obtain_jwt_token),
    path('docs/', include_docs_urls(patterns=api_docs_urls, title="BioIclock API DOCS")),
]
