#!/usr/bin/env python3.7

from requests import get, post
from os import path
import time
import json
import re


filename = 'settings.json'
if path.exists(filename):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
else:
    print("no settings.json file with telegram bot_token and chat_id")
    exit(1)


telegram_url = f"https://api.telegram.org/bot{settings['bot_token']}/sendPhoto"

def send_to_telegram(comic):
    global settings
    global telegram_url
    params = {"chat_id": settings['chat_id'], "photo": comic['comic_url'], "caption": comic['comic_num']}
    res = post(url = telegram_url, data = params)
    return res

def get_latest():
    res = get("https://questionablecontent.net/")
    if res.status_code == 200:
        comic = re.search(r'https?://www.questionablecontent.net/comics/(\d+)\.\w{3,4}', res.text)
        comic_url = comic.group(0)
        comic_num = comic.group(1)
        return dict(comic_num = comic_num, comic_url = comic_url)
    else:
        print("no comic found") # need to log this
        return None


latest_comic_num = None

while True:
    comic = get_latest()
    if comic:
        if not latest_comic_num:
            latest_comic_num = comic['comic_num']

        if int(comic['comic_num']) > int(latest_comic_num):
            send_to_telegram(comic)
            latest_comic_num = comic['comic_num']
            print(latest_comic_num)

    time.sleep(5*60)