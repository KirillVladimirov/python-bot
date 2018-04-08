# -*- coding: utf-8 -*-

import telebot
import time
import os
import logging
from aiohttp import web

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

config = dict()

config['API_TOKEN'] = os.environ.get('API_TOKEN', None)
config['WEBHOOK_URL_BASE'] = os.environ.get('WEBHOOK_URL_BASE', None)
config['WEBHOOK_URL_PATH'] = "/%s/".format(config['API_TOKEN'])
config['WEBHOOK_LISTEN'] = '0.0.0.0'
config['WEBHOOK_PORT'] = 8443

bot = telebot.TeleBot(config['API_TOKEN'])

info = bot.get_webhook_info()
if config['WEBHOOK_URL_BASE'] != info.url:
    bot.remove_webhook()
    time.sleep(5)
    bot.set_webhook(url=config['WEBHOOK_URL_BASE'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# Process webhook calls
async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)


async def root_handler(request):
    request_body_dict = await request.json()
    print('root_handler')
    print(request_body_dict)
    return web.Response(status=200)


app = web.Application()
app.router.add_get('/', root_handler)
app.router.add_post('/{token}/', handle)

# web.run_app(app, host=config['WEBHOOK_LISTEN'], port=config['WEBHOOK_PORT'])
