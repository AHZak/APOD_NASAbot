from datetime import datetime
from urllib.parse import urlparse
import requests
from config import APOD_URL, NASA_API_KEY, TG_REQ_URL


#
##
### [START] Telegram
##
#

# every incoming update has a type based of it's content and origin
def fetch_type(update):
    if update.get('message'):
        if update['message'].get('forward_from') or update['message'].get('forward_sender_name'):
            return 'forward'
        elif update['message'].get('text'):
            return 'text'
        elif update['message'].get('photo'):
            return 'photo'
        elif update['message'].get('animation'):
            return 'animation'
        elif update['message'].get('sticker'):
            return 'sticker'
        elif update['message'].get('voice'):
            return 'voice'
        elif update['message'].get('audio'):
            return 'audio'
        elif update['message'].get('video_note'):
            return 'video_note'
        elif update['message'].get('video'):
            return 'video'   
        else:
            return False
    else:
        return False

#every coming update from the user has a user id, we use it to respond
def fetch_id(update):
    return update['message']['chat']['id']

#returning text of incoming update of type text
def fetch_text(update):
    return update['message']['text']

#making request: sendMessage
def send_message(chat_id, text, kb=True):
    URL = TG_REQ_URL + '/sendMessage'
    PARAMS = {
        'chat_id'                   : chat_id,
        'text'                      : text,
        'parse_mode'                : 'HTML',
        'disable_web_page_preview'  : True,
        'reply_markup'              : kb_bldr() if kb else {"remove_keyboard" : True}
    }
    return requests.post(url=URL, json= PARAMS)

#making request: sendSticker
def send_sticker(chat_id, sticker):
    URL = TG_REQ_URL + '/sendSticker'
    PARAMS = {
        'chat_id'   : chat_id,
        'sticker'   : sticker
    }
    return requests.post(url=URL, json= PARAMS)

#making request: sendPhoto
def send_photo(chat_id, photo, caption=''):
    URL = TG_REQ_URL + '/sendPhoto'
    PARAMS = {
        'chat_id'   : chat_id,
        'photo'     : photo,
        'caption'   : caption
    }
    return requests.post(url=URL, json= PARAMS)

#making request: sendAnimation
def send_animation(chat_id, animation):
    URL = TG_REQ_URL + '/sendAnimation'
    PARAMS = {
        'chat_id'   : chat_id,
        'animation' : animation
    }
    return requests.post(url=URL, json= PARAMS)

#keyboard array as declared in bot documentation
def kb_bldr():
    return {"keyboard" : [['/today','Archive 🗄'],['/random','About 🦖']], 'resize_keyboard' : True}

#
##
### [END] Telegram
##
#


#
##
### [START] APOD
##
#

def apod(date='', count=''):
    PARAMS = {
        'api_key'   : NASA_API_KEY,
        'date'      : date,
        'count'     : count
    }
    res = requests.get(url= APOD_URL, params= PARAMS)
    if res.status_code == 200:
        return {'status' : 200, 'data' : res.json()}
    elif res.status_code == 429:
        return {'status' : 429, 'data' : res.json()}
    elif res.status_code == 400:
        return {'status' : 400, 'data' : res.json()}
    else: #e.g. 403, 404, ...
        log_it(res.json(), type='err')
        return None

#some apods contain copyright
def is_public(res):
    if res.get('copyright'):
        return False
    return True

#
##
### [END] APOD
##
#


#
##
### [START] LOG
##
#

def log_it(content, type=''):
    if type == "upd":
        f = open("log.txt", "a", encoding="utf-8")
        f.write("[" + str(datetime.now()) + "][UPD]: " + str(content))
        f.write("\n")
        f.close()
    elif type == "res":
        f = open("log.txt", "a", encoding="utf-8")
        f.write("[" + str(datetime.now()) + "][RES]: " + str(content))
        f.write("\n")
        f.close()
    elif type == "err":
        f = open("log.txt", "a", encoding="utf-8")
        f.write("[" + str(datetime.now()) + "][ERR]: " + str(content))
        f.write("\n")
        f.close()
    else:
        f = open("log.txt", "a", encoding="utf-8")
        f.write("[" + str(datetime.now()) + "]: " + str(content))
        f.write("\n")
        f.close()

#
##
### [END] LOG
##
#

#
##
### [START] Youtube
##
#

#building Youtube video thumbnail - there are different sizes available but not always 
def yt_thumb_bldr(url):
    pars_r = urlparse(url)
    pars_r = pars_r.path.strip('/').split('/')[1]
    res = requests.get("https://img.youtube.com/vi/" + pars_r + "/maxresdefault.jpg")
    if res.status_code == 200 or res.status_code == 304:
        return "https://img.youtube.com/vi/" + pars_r + "/maxresdefault.jpg"
    if requests.get("https://img.youtube.com/vi/" + pars_r + "/sddefault.jpg").status_code == 200:
        return "https://img.youtube.com/vi/" + pars_r + "/sddefault.jpg"
    if requests.get("https://img.youtube.com/vi/" + pars_r + "/hqdefault.jpg").status_code == 200:
        return "https://img.youtube.com/vi/" + pars_r + "/hqdefault.jpg"
    if requests.get("https://img.youtube.com/vi/" + pars_r + "/mqdefault.jpg").status_code == 200:
        return "https://img.youtube.com/vi/" + pars_r + "/mqdefault.jpg"
    return "https://img.youtube.com/vi/" + pars_r + "/default.jpg"

#building Youtube link based on apod's embedded video link structure
def yt_link_bldr(url):
    pars_r = urlparse(url)
    pars_r = pars_r.path.strip('/').split('/')[1]
    return "https://www.youtube.com/watch?v=" + pars_r

#
##
### [END] Youtube
##
#

#checking if a date is a date!
def is_valid_date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        None
    return False
    
#Telegram asks for replacing HTML tags when parse mode is HTML
def html_tag_rep(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text

#building a caption for post if it was a video
def photo_caption_bldr(res):
    if(not is_public(res)):
        caption = "<b>" + html_tag_rep(res['title']) + "</b>" + "\n\n" + html_tag_rep(res['explanation']) + "\n\n" + "<a href='" + res['hdurl'] + "'>Image(HD)</a>" + "\n\n" + "© Credit | " + html_tag_rep(res['copyright']) + "\n\n" + "[" + html_tag_rep(res['date']) + "]"
        return caption
    caption = "<b>" + html_tag_rep(res['title']) + "</b>" + "\n\n" + html_tag_rep(res['explanation']) + "\n\n" + "<a href='" + res['hdurl'] + "'>Image(HD)</a>" + "\n\n" +  "[" + html_tag_rep(res['date']) + "]"
    return caption

#building a caption for post if it was a video
def video_caption_bldr(res):
    if(not is_public(res)):
        caption = "<b>" + html_tag_rep(res['title']) + "</b>" + "\n\n" + html_tag_rep(res['explanation']) + "\n\n" + "<a href='" + yt_link_bldr(res['url']) + "'>Video on Youtube</a>" + "\n\n" + "© Credit | " + html_tag_rep(res['copyright']) + "\n\n" + "[" + html_tag_rep(res['date']) + "]"
        return caption
    caption = "<b>" + html_tag_rep(res['title']) + "</b>" + "\n\n" + html_tag_rep(res['explanation']) + "\n\n" + "<a href='" + yt_link_bldr(res['url']) + "'>Video on Youtube</a>" + "\n\n" +  "[" + html_tag_rep(res['date']) + "]"
    return caption


#sending picture and contents of the apod article to user
def make_post(chat_id, date='', count=''):
    res = apod(date,count)
    if not res: #403, 404, ...
        return None
    if res['status'] == 200:
        log_it(res, type='res')
        res = res['data']
        if count:
            res = res[0]
        if res['media_type'] == 'image':
            return {'status' : 200, 'data' : [send_photo(chat_id, res['url']).json(), send_message(chat_id, photo_caption_bldr(res)).json()]}
        elif res['media_type'] == 'video':
            return {'status' : 200, 'data' : [send_photo(chat_id, yt_thumb_bldr(res['url'])).json(), send_message(chat_id, video_caption_bldr(res)).json()]}
        else:
            return None #if media_type is missing
    elif res['status'] == 400:
        log_it(res, type='res')
        return res
    else: #429
        log_it(res, type='err')
        return res