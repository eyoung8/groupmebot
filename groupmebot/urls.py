
from django.conf.urls import include, url
from django.contrib import admin
from bot.views import SignUpView, create_bot_instructions, guide, groupme_upload

urlpatterns = [
    url(r'^$', SignUpView.as_view(), name='sign_up'),
    url(r'^create_bot_instructions/$', create_bot_instructions, name='create_bot_instructions'),
    url(r'^guide/$', guide, name='guide'),
    url(r'^groupme_upload/$', groupme_upload, name='groupme_upload'),
    url(r'^admin/', admin.site.urls),
    url(r'^bot/', include("bot.urls", namespace='bot')),

]
