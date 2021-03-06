import requests
import logging
from .models import Bot, BotResponse, MultipleResponse

logger = logging.getLogger('testlogger')

def log_enter_exit(func):
    def wrapper(*args, **kwargs):
        logger.info('entering ' + func.__name__)
        val = func(*args, **kwargs)
        logger.info(func.__name__ + ' exited')
        return val
    return wrapper

@log_enter_exit
def send_response(bot_id, text):
    payload = {"bot_id": bot_id, "text": text}
    r = requests.post('https://api.groupme.com/v3/bots/post', data=payload)

@log_enter_exit
def new_bot_response(bot, command, response):
    br = BotResponse(command=command, response=response, bot=bot)
    br.save()

@log_enter_exit
def delete_bot_response(bot, command):
    try:
        logger.info("in try")
        bot_response = BotResponse.objects.get(command=command, bot=bot)
        logger.info("got bot response")
        bot_response.delete()
        logger.info("bot response deleted")
        deleted = True
        logger.info("deleted set to true")
    except:
        logger.info("in except block")
        deleted = False
        logger.info("deleted set to false")
    logger.info("deleted=" + str(deleted))
    return deleted
   
@log_enter_exit
def new_multiple_response(bot, command, response):
    mr = MultipleResponse(command=command, response=response, bot=bot)
    mr.save()

@log_enter_exit
def new_command(bot, text):
    response = ' '.join(text[1:])
    command = text[0].lower()
    if not command[0]=="/":
        send_response(bot.bot_id, "command must begin with /")
    else:
        new_bot_response(bot, command, response)
        send_response(bot.bot_id, "command {} successfully created".format(command))

@log_enter_exit
def send_command_response(bot, command):
    try:
        bot_response = BotResponse.objects.get(bot=bot, command=command).response
        logger.info("response = {}".format(bot_response))
        send_response(bot.bot_id, bot_response)
    except:
        pass

@log_enter_exit
def new_random_command(bot, text):
    response = ' '.join(text[1:])
    command = text[0].lower()
    new_multiple_response(bot, command, response)
    send_response(bot.bot_id, "random command {} successfully created".format(command))

@log_enter_exit
def random_command(bot, text):
    command = text[0].lower()
    try:
        qs = MultipleResponse.objects.filter(bot=bot, command=command).order_by('?')
        if qs.count() > 0:
            response = qs[0].response
            send_response(bot.bot_id, response)
        else:
            send_response(bot.bot_id, "command {} not found".format(command))
    except:
        pass

@log_enter_exit
def bot_help(bot, host):
    help_url ="".join(["https://", host, bot.get_absolute_url()])
    send_response(bot.bot_id, help_url)

@log_enter_exit 
def delete_command(bot, text):
    command = text[0]
    deleted = delete_bot_response(bot, command)
    logger.info("deleted results=" + str(deleted))
    if deleted:
        msg = "Command {} successfully deleted".format(command)
    else:
        msg = "Command not found or issue deleting command"
    send_response(bot.bot_id, msg)

@log_enter_exit
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

@log_enter_exit
def handle_command(bot, command, text, host):
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
            send_command_response(bot, command)



