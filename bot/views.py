from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Bot, BotResponse, MultipleResponse
from .util import send_response, new_command, new_random_command, random_command, bot_help, delete_command, edit_command, send_command_response
from .forms import BotForm
import logging
import json

logger = logging.getLogger('testlogger')
# Create your views here.

def handle_command1(bot, command, text, host):
    if command=="/help":
        bot_help(bot, host)
    else:
        command_dict = {"/new"     : new_command,
                        "/edit"    : edit_command,
                        "/delete"  : delete_command,
                        "/newrand" : new_random_command,
                        "/random"  : random_command,   
                        }
        try:
            cmd = command_dict[command]
            cmd(bot, text)
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
                handle_command1(bot, command, split_text[1:], host)
        except:
            logger.info("get_message exception")        
    return HttpResponse("don't come here")

def bot_detail(request, group_id):
    try:
        bot = Bot.objects.get(group_id=group_id)
        responses = BotResponse.objects.filter(bot__group_id__iexact=group_id)
        random_commands = MultipleResponse.objects.filter(bot__group_id__iexact=group_id)
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
                   "random_commands": random_commands,
                    }
        return render(request, "bot_detail.html", context)
    except:
        return HttpResponse("Bot does not exist")

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        bot_form = BotForm()
        context = {
            "bot_form" : bot_form
        }
        return render(request, "bot_home.html", context)

    def post(self, request, *args, **kwargs):
        bot_form = BotForm(request.POST, request.FILES)
        if bot_form.is_valid():
            bot_form.save()
            bot_id = bot_form.cleaned_data.get("bot_id")
            bot_name = bot_form.cleaned_data.get("name")
            send_response(bot_id, "Hello, I'm {}, your new chat bot!".format(bot_name))
            send_response(bot_id, "For instructions on how to use me type '/help' into chat.")
            return HttpResponse("Bot created!")
        else:
            return HttpResponse("Bot not created!")

def create_bot_instructions(request):
    return render(request, "bot_create_instructions.html", {})
