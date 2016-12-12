from django.http import HttpResponse
from django.shortcuts import render
from .util import send_response
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
            bot_response = BotResponse.objects.get(bot=bot, command=command).response
            send_response(bot, bot_response)
        except:
            pass

def get_message(request):
    if request.POST:
        group_id = request.POST.get("group_id")
        try:
            bot = Bot.objects.get(group_id=group_id)
            text = request.POST.get("text")
            if text and text[0] == "/":
                split_text = text.split()
                command = split_text[0]
                handle_command(bot, command, split_text[1:])
        except:
            pass
    return HttpResponse("don't come here")