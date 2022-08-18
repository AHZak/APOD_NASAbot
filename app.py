from flask import Flask, jsonify, request
from functions import fetch_id, fetch_text, fetch_type, is_valid_date, log_it, make_post, send_animation, send_message, send_photo, send_sticker
from config import FILES, MSG, PATH, SECRET_TKN


app = Flask(__name__)

#application entry point
application = app

@app.route(PATH, methods=['GET', 'POST'])
def response():
    if request.method == 'POST':
        ###[START] Authentication: making sure if request comes from Telegram

        #secret_token is being sent with setwebhook as a query which telegram includes in it's update header

        if request.headers.get('X-Telegram-Bot-Api-Secret-Token'):
            if request.headers['X-Telegram-Bot-Api-Secret-Token'] != SECRET_TKN:
                return jsonify('unauthorized'), 401
        else:
            return jsonify('missing header'), 403

        ###[END] Authentication: making sure if request comes from Telegram


        ###[START] logging incoming update from Telegram

        #appending log file

        log_it(request.json, type='upd')

        ###[END] logging incoming update from Telegram


        ###[START] Processing incoming request

        #incoming update is logged into a text file

        #1: defining the type of incoming update
        #2.1: if it was a text:
            #1: chacking if it is a predefined text
            #2: checking if it is a valid date format
            #3: informing the user about available options
        #2.2: if it was not a text:
            #1 Sending predefined text or media by it's Telegram file_id
 
        type = fetch_type(request.json)

        if (type == "text"):
            chat_id = fetch_id(request.json)
            text    = fetch_text(request.json)

            if (text == "/start"):
                log_it(send_message(chat_id, MSG["START"]).json(), type='res')
            elif (text == "/today"):
                res = make_post(chat_id)

                if not res or res['status'] == 400: #400, 403, 404, ...
                    log_it(send_message(chat_id,MSG["UNKNOWN"]).json(), type='res')
                elif res['status'] == 200:
                    if res['data'][0]['ok'] and res['data'][1]['ok']:
                        log_it(res['data'], type='res')
                    else:
                        log_it(res['data'], type='err')
                else: #429
                    log_it(send_message(chat_id, MSG["LIMIT"]).json(), type='res')
            elif (text == "/random"):
                res = make_post(chat_id, count='1')

                if not res or res['status'] == 400: #400, 403, 404, ...
                    log_it(send_message(chat_id,MSG["UNKNOWN"]).json(), type='res')
                elif res['status'] == 200:
                    if res['data'][0]['ok'] and res['data'][1]['ok']:
                        log_it(res['data'], type='res')
                    else:
                        log_it(res['data'], type='err')
                else: #429
                    log_it(send_message(chat_id, MSG["LIMIT"]).json(), type='res')
            elif (text == "About 🦖"):
                log_it(send_message(chat_id, MSG["ABOUT"]).json(), type='res')
            elif (text == "Archive 🗄"):
                log_it(send_message(chat_id, MSG["ARCHIVE"], kb=False).json(), type='res')
            else:
                if is_valid_date(text):
                    res = make_post(chat_id, date=text)

                    if not res: #403, 404, ...
                        log_it(send_message(chat_id, MSG["UNKNOWN"]).json(), type='res')
                    elif res['status'] == 200:
                        if res['data'][0]['ok'] and res['data'][1]['ok']:
                            log_it(res['data'], type='res')
                        else:
                            log_it(res['data'], type='err')
                    elif res['status'] == 429:
                        log_it(send_message(chat_id, MSG["LIMIT"]).json(), type='res')
                    else: #400
                        log_it(send_message(chat_id, MSG["OR_DATE"], kb=False).json(), type='res')
                else:
                    log_it(send_message(chat_id, MSG["OPTIONS"]).json(), type='res')
        elif(type == "photo"):
            log_it(send_photo(fetch_id(request.json), FILES["PHOTO"]).json(), type='res')
        elif(type == "sticker"):
            log_it(send_sticker(fetch_id(request.json), FILES["STICKER"]).json(), type='res')
        elif(type == "animation"):
            log_it(send_animation(fetch_id(request.json), FILES["GIF"]).json(), type='res')
        elif(type == "audio"):
            log_it(send_message(fetch_id(request.json), MSG["FOR_AUDIO"]).json(), type='res')
        elif(type == "video"):
            log_it(send_message(fetch_id(request.json), MSG["FOR_VIDEO"]).json(), type='res')
        elif(type == "voice" or type == "video_note"):
            log_it(send_message(fetch_id(request.json), MSG["FOR_MISC"]).json(), type='res')
        elif(type == "forward"):
            log_it(send_message(fetch_id(request.json), MSG["FOR_FRW"]).json(), type='res')
        else:
            None #to be expanded
        ###[END] Processing incoming request

        return jsonify(200), 200
    else:
        return jsonify('Request denied'), 400 #on incoming GET requests