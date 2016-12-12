from django.http import HttpResponse
from django.shortcuts import render
from .models import Bot, BotResponse
from .util import send_response
from django.views.decorators.csrf import csrf_exempt
import logging
import json

logger = logging.getLogger('testlogger')
# Create your views here.

def new_command(bot, text):
    pass

def help(bot):
    pass

def handle_command(bot, command, text):
    if command == "/new":
        new_command(bot, text)
    elif command == "/help":
        bot_help(bot)
    else:
        try:
            logger.info(command)
            bot_response = BotResponse.objects.get(bot=bot, command=command).response
            logger.info(bot_response)
            send_response(bot, bot_response)
        except:
            pass

@csrf_exempt
def get_message(request):
    logger.info("in")

    if request.method == "POST":
        logger.info("in2")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        group_id = body["group_id"]
        logger.info(group_id)
        try:
            logger.info("try1")
            bot = Bot.objects.get(group_id=group_id)
            logger.info("try2")
            text = body["text"]
            logger.info("try3")
            logger.info(bot.name)
            if text and text[0] == "/":
                logger.info("found command")
                split_text = text.split()
                command = split_text[0]
                handle_command(bot, command, split_text[1:])
        except:
            logger.info("except")
            pass
    return HttpResponse("don't come here")