import requests
import logging
from .models import Bot, BotResponse, MultipleResponse

logger = logging.getLogger('testlogger')

def log_enter_exit(func):
    def wrapper():
        logger.info('entering')
        func()
        logger.info('exited')
    return wrapper

#@log_enter_exit
def send_response(bot_id, text):
    payload = {"bot_id": bot_id, "text": text}
    r = requests.post('https://api.groupme.com/v3/bots/post', data=payload)

#@log_enter_exit
def new_bot_response(bot, command, response):
    br = BotResponse(command=command, response=response, bot=bot)
    br.save()

#@log_enter_exit
def delete_bot_response(bot, command):
    try:
        bot_response = BotResponse.objects.get(command=command, bot=bot)
        bot_response.delete()
        deleted = True
    except:
        deleted = False
    return deleted
   
#@log_enter_exit
def new_multiple_response(bot, command, response):
    mr = MultipleResponse(command=command, response=response, bot=bot)
    mr.save()

#@log_enter_exit
def new_command(bot, text):
    response = ' '.join(text[1:])
    command = text[0]
    if not command[0]=="/":
        send_response(bot.bot_id, "command must begin with /")
    else:
        new_bot_response(bot, command, response)
        send_response(bot.bot_id, "command {} successfully created".format(command))

#@log_enter_exit
def command(bot, command):
    try:
        bot_response = BotResponse.objects.get(bot=bot, command=command).response
        send_response(bot.bot_id, bot_response)
    except:
        pass

#@log_enter_exit
def new_random_command(bot, text):
    response = ' '.join(text[1:])
    command = text[0]
    new_multiple_response(bot, command, response)
    send_response(bot.bot_id, "random command {} successfully created".format(command))

#@log_enter_exit
def random_command(bot, text):
    command = text[0]
    try:
        qs = MultipleResponse.objects.filter(bot=bot, command=command).order_by('?')
        if qs.count() > 0:
            response = qs[0].response
            send_response(bot.bot_id, response)
        else:
            send_response(bot.bot_id, "command {} not found".format(command))
    except:
        pass

#@log_enter_exit
def bot_help(bot, host):
    help_url ="".join(["https://", host, bot.get_absolute_url()])
    send_response(bot.bot_id, help_url)

#@log_enter_exit 
def delete_command(bot, text):
    command = text[0]
    deleted = delete_bot_response(bot, command)
    if deleted:
        msg = "Command {} successfully deleted".format(command)
    else:
        msg = "Command not found or issue deleting command"
    send_response(bot.bot_id, msg)

#@log_enter_exit
def edit_command(bot, text):
    command = text[0]
    response = ' '.join(text[1:])
    deleted = delete_bot_response(bot, command)
    if deleted:
        new_bot_response(bot, command, response)
        msg = "Command {} successfully edited".format(command)
    else:
        msg = "Command {} could not be found".format(command)
    send_response(bot.bot_id, msg)





