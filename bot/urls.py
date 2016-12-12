from django.conf.urls import url
from django.contrib import admin

from .views import get_message

urlpatterns = [
    url(r'^receive/$', get_message),
]
