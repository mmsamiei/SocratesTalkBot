import time
import json
import requests
import urllib

TOKEN = "341714084:AAEdbGYDWqEyy-R__QMRTP8DEgxZ2mSNw_k"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def forward_message(chat_id, from_chat_id, message_id):
    url = URL + "forwardMessage?chat_id={}&from_chat_id={}&message_id={}".format(chat_id, from_chat_id, message_id)
    get_url(url)

def forward_all(updates):
    for update in updates["result"]:
        from_chat_id = update["message"]["chat"]["id"]
        message_id = update["message"]["message_id"]
        #send_message(text, chat)
        #send_message(text, 143266172)#mmsamiei
        forward_message(143266172,from_chat_id,message_id)

def main():
    last_update_id = None
    while True:
        print ("start to get updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            forward_all(updates)
        time.sleep(0.5)

if __name__== '__main__':
    main()
