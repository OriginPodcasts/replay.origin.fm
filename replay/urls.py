from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.defaults import page_not_found, server_error


urlpatterns = (
    path('admin/', admin.site.urls),
    path('', include('replay.front.urls')),
    path('', include('replay.feeds.urls')),
    path('', include('replay.legal.urls'))
)

if settings.DEBUG:
    from django.views.static import serve as static_serve

    urlpatterns += (
        re_path(
            r'^media/(?P<path>.*)$',
            static_serve,
            {
                'document_root': settings.MEDIA_ROOT
            }
        ),
        path(
            '404/',
            page_not_found,
            {
                'exception': Exception()
            }
        ),
        path(
            '500/',
            server_error
        )
    )
