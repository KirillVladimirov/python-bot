from flask import Flask, request, abort
import telebot
import logging
import os

app = Flask(__name__)
app.config['IS_HEROKU'] = os.environ.get('IS_HEROKU', None)
# bot = telebot.TeleBot(app.config['API_TOKEN'])


@app.route('/')
def hello_world():
    if app.config['IS_HEROKU']:
        return 'Hello, Heroku!'
    else:
        return 'Hello, World!'


# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

#
# bot = telebot.TeleBot(app.config['api_token'])
#
# app = Flask(__name__)
# app.config['webhook_url_path'] = "/%s/".format(app.config['api_token'])
#
# # Remove webhook, it fails sometimes the set if there is a previous webhook
# bot.remove_webhook()
#
# # Set webhook
# bot.set_webhook(url=app.config['webhook_url_base'] + app.config['webhook_url_path'])
#
#
# # Empty webserver index, return nothing, just http 200
# @app.route('/', methods=['GET', 'HEAD'])
# def index():
#     return ''
#
#
# # Process webhook calls
# @app.route(app.config['webhook_url_path'], methods=['POST'])
# def webhook():
#     if request.headers.get('content-type') == 'application/json':
#         json_string = request.get_data().decode('utf-8')
#         update = telebot.types.Update.de_json(json_string)
#         bot.process_new_updates([update])
#         return ''
#     else:
#         abort(403)
#
#
# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.reply_to(message,
#                  ("Hi there, I am EchoBot.\n"
#                   "I am here to echo your kind words back to you."))
#
#
# # Handle all other messages
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_message(message):
#     bot.reply_to(message, message.text)
