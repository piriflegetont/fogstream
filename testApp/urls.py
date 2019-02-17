from . import views
from django.conf.urls import url
from django.conf import settings
handler404 = 'testApp.views.e_handler404'
handler500 = 'testApp.views.e_handler500'

urlpatterns = [
    url(r'^$', views.send_form, name='send_form'),
    url(r'^auth$', views.auth, name='auth'),
    url(r'^send$', views.send_message, name='send_message'),
]

if settings.DEBUG:
    urlpatterns = [
        url(r'^404$', views.e_handler404),
        url(r'^500$', views.e_handler500)
    ] + urlpatterns
