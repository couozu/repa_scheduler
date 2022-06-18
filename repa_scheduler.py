#!/usr/local/bin/python3

import requests
import json

with open('repa_scheduler_api_key') as f:
    API_KEY = f.read().strip()

API_PREFIX = 'https://api.telegram.org/bot' + API_KEY + '/'

guides_group = -1001786539369

r = requests.get(API_PREFIX + 'sendMessage', json = {
'chat_id': guides_group, 'text': 'test'})

print('here')

print(json.dumps(r.json()))

print('here')

print(r.request.headers)
print(r.request.url)
print(r.request.body)

print(r.json())
