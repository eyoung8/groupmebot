
from django.conf.urls import include, url
from django.contrib import admin
from bot.views import SignUpView, create_bot_instructions

urlpatterns = [
    url(r'^$', SignUpView.as_view(), name='sign_up'),
    url(r'^create_bot_instructions/$', create_bot_instructions, name='create_bot_instructions'),
    url(r'^admin/', admin.site.urls),
    url(r'^bot/', include("bot.urls", namespace='bot')),

]
