from django.contrib import admin

from .models import Bot, BotResponse, MultipleResponse
# Register your models here.

class BotAdmin(admin.ModelAdmin):
    list_display = ["name", "timestamp", "updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["name"]
    class Meta:
        model = Bot

class BotResponseAdmin(admin.ModelAdmin):
    list_display = ["command", "response", "timestamp", "updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["command"]
    class Meta:
        model = BotResponse

class MultipleResponseAdmin(admin.ModelAdmin):
    list_display = ["command", "response", "timestamp", "updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["command"]
    class Meta:
        model = MultipleResponse

admin.site.register(Bot, BotAdmin)
admin.site.register(BotResponse, BotResponseAdmin)
admin.site.register(MultipleResponse, MultipleResponseAdmin)