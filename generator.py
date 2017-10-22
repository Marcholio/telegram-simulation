# -*- coding: utf-8 -*-

import json, random, re
from itertools import groupby
from operator import itemgetter
from time import time

class Generator:
  def __init__(self):
    print 'Initializing generator'
    start = time()
    random.seed(time())

    # Read data from file
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
    self.pairs = {}
    for i in range(1,len(data)):
      fromUser = data[i-1]['from']['username']
      toUser = data[i]['from']['username']
      difference = data[i-1]['date'] - data[i]['date']
      if fromUser in self.pairs:
        self.pairs[fromUser].append((toUser, difference))
      else:
        self.pairs[fromUser] = [(toUser, difference)]

    # Create list of self.users from self.pairs identified
    self.users = list(set(map(lambda x: x.split('-')[0], self.pairs)))

    # Parse self.words from messages
    self.words = {}
    for msg in data:
      user = msg['from']['username']
      text = str(msg['text'].encode('utf-8', 'ignore')).split(' ')
      text.append(None)
      if user in self.words:
        self.words[user] += text
      else:
        self.words[user] = text

    # Remove special characters and make self.words lower case
    for u in self.users:
      for i in range(len(self.words[u])):
        if self.words[u][i] is not None and 'http' not in self.words[u][i]:
          self.words[u][i] = re.sub('[^A-ZÅÄÖa-zåäö0-9:]+', '', self.words[u][i])

          # self.words to lower case, ignore emojis
          if len(self.words[u][i]) > 0 and self.words[u][i][0].isalnum():
            self.words[u][i] = self.words[u][i].lower()

      # Filter out empty self.words
      self.words[u] = filter(lambda x: x is None or len(x) > 0, self.words[u])

    # Construct self.markov chain
    self.markov = {}
    for u in self.users:
      self.markov[u] = {}
      for i in range(len(self.words[u])-1):
        word = self.words[u][i]
        if word in self.markov[u]:
          self.markov[u][word].append(self.words[u][i+1])
        else:
          self.markov[u][word] = [self.words[u][i+1]]
          
    # Select random user to start the conversation
    self.user = random.choice(self.users)
    self.diff = 0
    self.timestamp = int(time())

          
    print 'Generator initialied (%.2f s)' % float(time() - start)

  '''
  Generates self.markov-chain sentence for given user
  '''
  def generate_sentence(self, user):
    # Select a word to start with
    w = random.choice(self.words[user])
    while w is None:
      w = random.choice(self.words[user])
    msg = ''

    # Add self.words to sentence until end is met
    while w is not None:
      msg += ' ' + w
      w = random.choice(self.markov[user][w])
    return msg.strip()
  
  '''
  Returns new message with text, difference in seconds to previous message and user
  '''
  def getMessage(self):
    msg = self.generate_sentence(self.user).decode('utf-8', 'ignore')
    diff = self.diff
    user = self.user
    (self.user, self.diff) = random.choice(self.pairs[user])
    return msg, diff, user
