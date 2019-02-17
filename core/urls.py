from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', admin.site.urls),
    url('accounts/login/', views.LoginView.as_view(), name='login'),
    url('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    url(r'', include('testApp.urls')),
]


