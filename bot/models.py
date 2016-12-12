from django.db import models

# Create your models here.

class Bot(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    bot_id = models.CharField(max_length=100, unique=True, blank=False)
    group_id = models.CharField(max_length=100, unique=True, blank=False)
    updated   = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def __str__(self):
        return self.name

class BotResponse(models.Model):
    command = models.CharField(max_length=100, unique=False, blank=False)
    response = models.CharField(max_length=1000, unique=False, blank=False)
    updated   = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        ordering = ["-timestamp", "-updated"]
        unique_together = ('command', 'bot',)
    def __str__(self):
        return "command: {} , response: {}".format(self.command,self.response)
