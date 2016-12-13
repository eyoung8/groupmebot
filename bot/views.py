from django.core.exceptions import ObjectDoesNotExist
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
    logger.info("entering new_command")
    logger.info(type(text))
    response = ' '.join(text[1:])
    logger.info(response)
    command = text[0]
    logger.info(command)
    if not command[0]=="/":
        logger.info("incorrectly formatted new command")
        send_response(bot.bot_id, "command must begin with /")
    else:
        logger.info("correctly formatted new command")
        br = BotResponse(command=command, response=response, bot=bot)
        br.save()
        logger.info("new BotResponse saved")
        send_response(bot.bot_id, "command {} successfully created".format(command))
        logger.info("response sent to group")

def new_rand_command(bot, text):
    logger.info("entering new_rand_command")
    response = ' '.join(text[1:])
    logger.info(response)
    command = text[0]
    logger.info(command)

    br = MultipleResponse(command=command, response=response, bot=bot)
    br.save()
    logger.info("new BotResponse saved")
    send_response(bot.bot_id, "random command {} successfully created".format(command))
    logger.info("response sent to group")

def rand(bot, text):
    logger.info("entering rand")
    command = text[0]
    logger.info("Determined command: " + command)
    qs = MultipleResponse.objects.filter(bot__id__iexact=bot.bot_id).filter(command__iexact=command).order_by('?')
    logger.info("Got queryset")
    response = qs[0].response
    logger.info("Got response: " + response)
    send_response(bot.bot_id, responses)
    logger.info("Response sent")

def bot_help(bot, host):
    logger.info("in help")
    help_url ="".join(["https://", host, bot.get_absolute_url()])
    logger.info("got help_url= " + help_url)
    send_response(bot.bot_id, help_url)
 
def delete_bot_response(bot, text):
    logger.info("entering delete bot response")
    command = text[0]
    logger.info("command found: " + command)
    deleted = False
    try:
        bot_response = BotResponse.objects.get(command=command, bot=bot)
        logger.info("BotResponse object found")
        bot_response.delete()
        deleted = True
        logger.info("BotResponse object deleted")
        send_response(bot.bot_id,"Command {} successfully deleted".format(command))
        logger.info("Messaged chat")
    except:
        logger.info("delete exception")
        send_response(bot.bot_id, "Command not found or issue deleting command")
    return deleted

def edit_bot(bot, text):
    logger.info("entering edit")
    deleted = delete_bot_response(bot, text)
    if deleted:
        new_command(bot, text)

def handle_command(bot, command, text, host):
    if command == "/new":
        logger.info("command=" + command)
        new_command(bot, text)
    elif command == "/help":
        logger.info("command=" + command)
        bot_help(bot, host)
    elif command == "/delete":
        logger.info("command=" + command)
        delete_bot_response(bot, text)
    elif command == "/edit":
        logger.info("command=" + command)
        edit_bot(bot,text)
    elif command == "/random":
        logger.info("command=" + command)
        rand(bot, text)
    elif command == "/newrand":
        logger.info("command=" + command)
        new_rand_command(bot, text)
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
                     ("/delete", "Deletes an existing command in the format '/delete /{existing_command}'"),]
        context = {"bot_name"  : bot.name,
                   "responses" : responses,
                   "built_ins" : built_ins,
                    }
        return render(request, "bot_detail.html", context)

    except:
        return HttpResponse("Bot does not exist")





