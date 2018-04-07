from flask import Flask
import telebot
import requests
import datetime
import os

config = []
config['API_TOKEN'] = os.environ.get('API_TOKEN', None)
config['WEBHOOK_URL_BASE'] = os.environ.get('WEBHOOK_URL_BASE', None)
config['WEBHOOK_URL_PATH'] = "/%s/".format(config['API_TOKEN'])

bot = telebot.TeleBot(config['API_TOKEN'])


# bot.remove_webhook()
# bot.set_webhook(url=config['WEBHOOK_URL_BASE'] + config['WEBHOOK_URL_PATH'])

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
