from django.conf.urls import url
from django.contrib import admin

from .views import get_message, bot_detail

urlpatterns = [
    url(r'^receive/$', get_message),
    url(r'^(?P<group_id>[-\w]+)/$', bot_detail),

]
