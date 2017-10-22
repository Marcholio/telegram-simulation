import json, sys
from telegram import Bot
from telegram.ext import CommandHandler, Updater

class TelegramBot:
  def __init__(self, token):
    self.updater = Updater(token=token)
    self.bot = Bot(token)
    startHandler = CommandHandler('start', self.start)
    stopHandler = CommandHandler('stop', self.stop)
    self.updater.dispatcher.add_handler(startHandler)
    self.updater.dispatcher.add_handler(stopHandler)
    self.updater.start_polling()
    self.chatId = 0
    
  def start(self, bot, update):
    self.chatId = update.message.chat.id
    
  def stop(self, usr, msg):
    self.updater.stop()
    raise SystemExit
    
  def sendMessage(self, msg):
    if self.chatId is not 0:
      self.bot.send_message(chat_id=self.chatId, text=msg)