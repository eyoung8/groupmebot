from django import forms
from .models import Bot

class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = [
            "name",
            "bot_id",
            "group_id",
        ]