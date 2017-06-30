import time
import json
import requests
import urllib

TOKEN = "321327563:AAHFSm4SQ96HorBGI8V3Ok9BzGRLtkqaIp4"
mmsamiei_id = "143266172"
badri_id = "92811076"
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

def get_poem():
    url = "http://emrani.net/hafez/api/hafez/fal"
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


def do_all(updates):
    for update in updates["result"]:


        if("message" in update):

            if("reply_to_message" in update["message"]):
                who_reply =(str) (update["message"]["from"]["id"])
                if( who_reply == mmsamiei_id):
                    print("mmsamiei Replys!")
                    from_chat_id = update["message"]["chat"]["id"]
                    message_id = update["message"]["message_id"]
                    if("forward_from" in update["message"]["reply_to_message"]):
                        who_replied_id = update["message"]["reply_to_message"]["forward_from"]["id"]
                        forward_message(who_replied_id,from_chat_id,message_id)
                    return

            if("text" in update["message"]):
            ##    Text processing ##
                text = update["message"]["text"]


                if( text =="فال حافظ"):
                    poem = get_poem()
                    poem_text=(poem["poem"])
                    from_chat_id = update["message"]["chat"]["id"]
                    send_message(poem_text, from_chat_id)
                    from_chat_id = update["message"]["chat"]["id"]
                    message_id = update["message"]["message_id"]
                    forward_message(143266172,from_chat_id,message_id)


                else:
                    from_chat_id = update["message"]["chat"]["id"]
                    message_id = update["message"]["message_id"]
                    forward_message(143266172,from_chat_id,message_id)
                    forward_message(badri_id,from_chat_id,message_id)
            else:
                    from_chat_id = update["message"]["chat"]["id"]
                    message_id = update["message"]["message_id"]
                    forward_message(143266172,from_chat_id,message_id)
                    forward_message(badri_id,from_chat_id,message_id)




def main():
    last_update_id = None
    while True:
        print ("start to get updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            #forward_all(updates)
            do_all(updates)
        time.sleep(0.5)

if __name__== '__main__':
    main()
