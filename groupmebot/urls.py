
from django.conf.urls import include, url
from django.contrib import admin
from bot.views import SignUpView

urlpatterns = [
    url(r'^$', SignUpView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^bot/', include("bot.urls", namespace='bot')),

]
