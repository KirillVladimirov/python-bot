from flask import Flask, request, abort
import telebot
import logging
import os

app = Flask(__name__)
app.config['IS_HEROKU'] = os.environ.get('IS_HEROKU', None) == 'True'
app.config['API_TOKEN'] = os.environ.get('API_TOKEN', None)
app.config['WEBHOOK_URL_BASE'] = os.environ.get('WEBHOOK_URL_BASE', None)
app.config['WEBHOOK_URL_PATH'] = "/%s/".format(app.config['API_TOKEN'])

bot = telebot.TeleBot(app.config['API_TOKEN'])

app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@app.route("/токен бота", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(app.config['WEBHOOK_URL_BASE'] + app.config['WEBHOOK_URL_PATH'])
    return "!", 200
