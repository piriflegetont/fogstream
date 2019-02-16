from . import views
from testApp.models import Message
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.send_form, name='send_form'),
    url(r'^send$', views.send_message, name='send_message'),
]
