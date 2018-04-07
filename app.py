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

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=app.config['WEBHOOK_URL_BASE'] + app.config['WEBHOOK_URL_PATH'])


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(app.config['webhook_url_path'], methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)
