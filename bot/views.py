from django.http import HttpResponse
from django.shortcuts import render
from .util import send_response
from django.views.decorators.csrf import csrf_exempt
import logging
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
    logger.info(request.POST)
    if request.POST:
        logger.info("in2")
        group_id = request.POST.get("group_id")
        try:
            bot = Bot.objects.get(group_id=group_id)
            text = request.POST.get("text")
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