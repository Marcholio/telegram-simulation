# -*- coding: utf-8 -*-

import json, sys
from telegram import Bot
from telegram.ext import CommandHandler, Updater

class TelegramBot:
  def __init__(self, token):
    self.updater = Updater(token=token)
    self.bot = Bot(token)
    startHandler = CommandHandler('start', self.start)
    stopHandler = CommandHandler('stop', self.stop)
    pingHandler = CommandHandler('ping', self.ping)
    self.updater.dispatcher.add_handler(startHandler)
    self.updater.dispatcher.add_handler(stopHandler)
    self.updater.start_polling()
    self.chatId = None
    
  def start(self, bot, update):
    self.chatId = update.message.chat.id
    
  def stop(self, usr, msg):
    self.updater.stop()
    raise SystemExit
    
  def ping(self, bot, update):
    self.sendMessage('jöpjöp')
    
  def sendMessage(self, msg):
    if self.chatId is not None:
      self.bot.send_message(chat_id=self.chatId, text=msg)