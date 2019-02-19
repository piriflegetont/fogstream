from . import views
from . import ajax
from django.conf.urls import url
from django.conf import settings
handler404 = 'testApp.views.e_handler404'
handler500 = 'testApp.views.e_handler500'

api = [
    url(r'^login$', ajax.e_login, name='login'),
    url(r'^logout$', ajax.e_logout, name='logout'),
    url(r'^register$', ajax.e_register, name='register'),
    url(r'^send$', ajax.send_message, name='send_message'),
]

urlpatterns = [
    url(r'^$', views.send_form, name='send_form'),
    url(r'^auth$', views.auth, name='auth'),
] + api

if settings.DEBUG:
    urlpatterns = [
        url(r'^404$', views.e_handler404),
        url(r'^500$', views.e_handler500)
    ] + urlpatterns + api
