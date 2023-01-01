#!/usr/bin/python3

import requests
import json
import traceback
import datetime
import sys
import os
import math
import decimal
dec = decimal.Decimal

API_KEY = os.getenv('APIKEY')
API_PREFIX = 'https://api.telegram.org/bot' + API_KEY + '/'

guides_group = -1001786539369
hosts_group = -1001658680990
test_group = -795223636
oncall = 174125991

if len(sys.argv) > 2 and sys.argv[2] == 'get':
  r = requests.get(API_PREFIX + 'getUpdates')
  print(json.dumps(r.json()))
  sys.exit(0)

weekdays = {
 0: 'Mon',
 1: 'Tue',
 2: 'Wed',
 3: 'Thu',
 4: 'Fri',
 5: 'Sat',
 6: 'Sun'
} 

day = datetime.datetime.utcnow()

while weekdays[day.weekday()] != 'Sun':
  day = day + datetime.timedelta(days=1)

def position(now=None): 
   if now is None: 
      now = datetime.datetime.now()

   diff = now - datetime.datetime(2001, 1, 1)
   days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
   lunations = dec("0.20439731") + (days * dec("0.03386319269"))

   return lunations % dec(1)

def phase(pos): 
   index = (pos * dec(29))
   index = math.floor(index)

   dates = {
      0: "New Moon", 
      5: "6th", 
      13: "Full Moon",
      19: "20st" 
   }
   return dates.get(int(index) & 31, '')

options = []

for _ in range(7):
  day = day + datetime.timedelta(days=1)
  options.append(
    day.strftime('%A %d/%b') + 
    ' ' + 
    phase(position(day))) 

options.append('Show results')

def sendWeeklyPoll(group, question):
  r = requests.get(API_PREFIX + 'sendPoll', json = {
    'chat_id': group, 
    'question': question,
    'options': options,
    'is_anonymous': False,
    'allows_multiple_answers': True
  })
  r.raise_for_status()

def hello_pubsub(event):
  try:
    sendWeeklyPoll(guides_group, 'Planning next week! Please choose dates you can guide!')
    res = 'Success!'
  except:
    res =  f'Failure! {traceback.format_exc()}'

  requests.get(API_PREFIX + 'sendMessage', json = {'chat_id': oncall, 'text': res})
  return 'OK'

