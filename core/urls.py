from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', admin.site.urls),
    url(r'', include('testApp.urls')),
]


