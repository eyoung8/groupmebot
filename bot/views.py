from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Bot, BotResponse, MultipleResponse
from .util import handle_command, send_response
from .forms import BotForm
import logging
import json

logger = logging.getLogger('testlogger')
# Create your views here.


@csrf_exempt
def get_message(request):
    host = request.get_host()
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        group_id = body["group_id"]
        logger.info(group_id)
        try:
            bot = Bot.objects.get(group_id=group_id)
            text = body["text"]
            logger.info("text = {}".format(text))
            if text and text[0] == "/":
                split_text = text.split()
                command = split_text[0].lower()
                logger.info("command = {}".format(command))
                handle_command(bot, command, split_text[1:], host)
        except:
            logger.info("get_message exception")        
    return HttpResponse("don't come here")

def bot_detail(request, group_id):
    try:
        bot = Bot.objects.get(group_id=group_id)
        responses = BotResponse.objects.filter(bot__group_id__iexact=group_id)
        random_commands = MultipleResponse.objects.filter(bot__group_id__iexact=group_id).order_by('command').values('command').distinct()
        built_ins = [("/new" ,   "Create a new command\nex: '/new /command response'"),
                     ("/help",   "Gives a url to the bot's help page"),
                     ("/edit",   "Edits an existing command\nex: '/edit /command new_response'"),
                     ("/delete", "Deletes an existing command\nex: '/delete /command'"),
                     ("/newrand","Creates a new command with multiple possible responses\nex: /newrand command response\nex2: /newrand command response2"),
                     ("/random", "Calls a random /newrand command\nex: '/random newrand_command'"),
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

def guide(request):
    return render(request, "bot_guide.html", {})

def groupme_upload(request):
    return render(request, "groupme_upload_guide.html", {})





