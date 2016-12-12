from django.core.exceptions import ValidationError
from django.db import models
import logging
logger = logging.getLogger('testlogger')

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
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, unique=False, blank=False, null=False)

    def save(self, *args, **kwargs):
        logger.info("Entering BotResponse save")
        qs = BotResponse.objects.filter(command__iexact=self.command).filter(bot__id__iexact=self.bot.id)
        logger.info("Got queryset")
        if qs.exists():
            logger.info("Raising validation error")
            raise ValidationError
        else:
            logger.info("Saving")
            super(BotResponse, self).save(*args, **kwargs)
            logger.info("BotResponse saved")

    class Meta:
        ordering = ["-timestamp", "-updated"]
    def __str__(self):
        return "command: {} , response: {}".format(self.command,self.response)
