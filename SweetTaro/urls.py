from django.urls import include, path
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.shortcuts import redirect


def index(request):
    return redirect('/v1.0/')


urlpatterns = [
    path('', index),
    path('v1.0/', include('apps.api.urls')),
    path('favicon.ico', serve, {'document_root': settings.BASE_DIR, 'path': 'static/favicon.ico'})
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
