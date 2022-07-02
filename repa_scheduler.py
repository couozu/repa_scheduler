#!/usr/local/bin/python3

import requests
import json
import traceback
import datetime
import sys

with open('repa_scheduler_api_key') as f:
    API_KEY = f.read().strip()

API_PREFIX = 'https://api.telegram.org/bot' + API_KEY + '/'

guides_group = -1001786539369
hosts_group = -1001658680990
test_group = -795223636
oncall = 174125991

'''
r = requests.get(API_PREFIX + 'getUpdates')
print(json.dumps(r.json()))
sys.exit(0)
'''

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

options = []

for _ in range(7):
  day = day + datetime.timedelta(days=1)
  options.append(day.strftime('%A %d/%b')) 

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

try:
  sendWeeklyPoll(hosts_group, 'Planning next week! Please choose dates you can host!')
  sendWeeklyPoll(guides_group, 'Planning next week! Please choose the dates you can guide!')
  res = 'Success!'
except:
  res =  f'Failure! {traceback.format_exc()}'

requests.get(API_PREFIX + 'sendMessage', json = {'chat_id': oncall, 'text': res})

