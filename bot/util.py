import requests
import logging
logger = logging.getLogger('testlogger')

def send_response(bot_id, text):
    logger.info("bot_id: " + bot_id)
    logger.info("text: " + text)
    payload = {"bot_id": bot_id, "text": text}
    logger.info(payload)
    r = requests.post('https://api.groupme.com/v3/bots/post', data=payload)
    logger.info("done")