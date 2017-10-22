# -*- coding: utf-8 -*-

import json, random, re
from itertools import groupby
from operator import itemgetter
from time import time, strftime, localtime

random.seed(time())

data = []
with open('Data.jsonl') as d:
  for line in d:
    try:
      j = json.loads(line)
      # Filter out other than text messages and some noice from history :D
      if 'text' in j and len(j['text']) < 2000:
        data.append(j)
    except:
      pass

'''
Calculate probabilities for certain user to be the next to
send message to chat given sender of the last message.
'''
pairs = {}
for i in range(1,len(data)):
  fromUser = data[i-1]['from']['username']
  toUser = data[i]['from']['username']
  difference = data[i-1]['date'] - data[i]['date']
  if fromUser in pairs:
    pairs[fromUser].append((toUser, difference))
  else:
    pairs[fromUser] = [(toUser, difference)]

# Create list of users from pairs identified
users = list(set(map(lambda x: x.split('-')[0], pairs)))

# Total count of messages after filtering
totalMsgCount = len(pairs)

# Parse words from messages
words = {}
for msg in data:
  user = msg['from']['username']
  text = str(msg['text'].encode('utf-8', 'ignore')).split(' ')
  text.append(None)
  if user in words:
    words[user] += text
  else:
    words[user] = text

# Remove special characters and make words lower case
for u in users:
  for i in range(len(words[u])):
    if words[u][i] is not None and 'http' not in words[u][i]:
      words[u][i] = re.sub('[^A-ZÅÄÖa-zåäö0-9:]+', '', words[u][i])
      
      # Words to lower case, ignore emojis
      if len(words[u][i]) > 0 and words[u][i][0].isalnum():
        words[u][i] = words[u][i].lower()
        
  # Filter out empty words
  words[u] = filter(lambda x: x is None or len(x) > 0, words[u])

# Construct markov chain
markov = {}
for u in users:
  markov[u] = {}
  for i in range(len(words[u])-1):
    word = words[u][i]
    if word in markov[u]:
      markov[u][word].append(words[u][i+1])
    else:
      markov[u][word] = [words[u][i+1]]

'''
Generates markov-chain sentence for given user
'''
def generate_sentence(user):
  # Select a word to start with
  w = random.choice(words[user])
  while w is None:
    w = random.choice(words[user])
  msg = ''
  
  # Add words to sentence until end is met
  while w is not None:
    msg += ' ' + w
    w = random.choice(markov[user][w])
  return msg.strip()

# Select random user to start the conversation
user = random.choice(users)
diff = 0
timestamp = int(time())

for i in range(25):
  timestamp += diff
  print '%s - %10s: %s' % (strftime('%Y-%m-%d %H:%M:%S', localtime(timestamp)), user, generate_sentence(u).decode('utf-8', 'ignore'))
  (user, diff) = random.choice(pairs[user])