from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Bot, BotResponse, MultipleResponse
from .util import send_response, new_command, new_random_command, random_command, bot_help, delete_command, edit_command, command
import logging
import json

logger = logging.getLogger('testlogger')
# Create your views here.

def handle_command1(bot, command, text, host):
    command_dict = {"/new"     : new_command(bot, text),
                    "/edit"    : edit_command(bot, text),
                    "/delete"  : delete_command(bot, text),
                    "/newrand" : new_random_command(bot, text),
                    "/random"  : random_command(bot, text),
                    "/help"    : bot_help(bot, host),
                    }
    try:
        command_dict[command]
    except:
        command(bot, command)



def handle_command(bot, command, text, host):
    if command == "/new":
        logger.info("command=" + command)
        new_command(bot, text)
    elif command == "/help":
        logger.info("command=" + command)
        bot_help(bot, host)
    elif command == "/delete":
        logger.info("command=" + command)
        delete_command(bot, text)
    elif command == "/edit":
        logger.info("command=" + command)
        edit_command(bot,text)
    elif command == "/random":
        logger.info("command=" + command)
        random_command(bot, text)
    elif command == "/newrand":
        logger.info("command=" + command)
        new_random_command(bot, text)
    else:
        try:
            logger.info(command)
            bot_response = BotResponse.objects.get(bot=bot, command=command).response
            logger.info(bot_response)
            send_response(bot.bot_id, bot_response)
        except:
            logger.info("handle_command exception")
            

@csrf_exempt
def get_message(request):
    logger.info("in")
    host = request.get_host()
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
                handle_command(bot, command, split_text[1:], host)
        except:
            logger.info("get_message exception")        
    return HttpResponse("don't come here")

def bot_detail(request, group_id):
    try:
        bot = Bot.objects.get(group_id=group_id)
        responses = BotResponse.objects.filter(bot__group_id__iexact=group_id)
        built_ins = [("/new" ,   "Create a new command by sending '/new /{new_command} {new command response}'"),
                     ("/help",   "Gives a url to the bot's help page"),
                     ("/edit",   "Edits an existing command in the format '/edit /{existing_command} {new command response}'"),
                     ("/delete", "Deletes an existing command in the format '/delete /{existing_command}'"),
                     ("/newrand","Creates a new command in the same format of /new but /newrand commands have multiple responses that are randomly selected"),
                     ("/random", "Calls a random /newrand command in the format '/random {newrand_command}'"),
                     ]
        context = {"bot_name"  : bot.name,
                   "responses" : responses,
                   "built_ins" : built_ins,
                    }
        return render(request, "bot_detail.html", context)
    except:
        return HttpResponse("Bot does not exist")

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "bot_home.html", {})


