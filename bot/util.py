import requests

def send_response(bot, text):
    payload = {"bot_id": bot.bot_id, "text": text}
    r = requests.post('https://api.groupme.com/v3/bots/post', data=post_body)