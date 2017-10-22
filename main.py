import json, logging
from time import time, sleep

from generator import Generator
from bot import TelegramBot

print 'TELEGRAM CHAT SIMULATOR'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

generator = Generator()

tokens = {}
with open('config.json') as c:
  j = json.load(c)
  tokens = j['tokens']

bots = {}

for u in generator.users:
  start = time()
  print 'Initializing %s bot' % u
  bots[u] = TelegramBot(tokens[u])
  print 'Bot initialized (%.2f s)' % float(time() - start)

for i in range(10):
  (msg, diff, user) = generator.getMessage()
  print 'Next message in %d seconds' % diff
  sleep(diff)
  b = bots[user]
  b.sendMessage(msg)