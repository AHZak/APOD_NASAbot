from datetime import datetime, timedelta
import pytz

### TELEGRAM API
TG_API_KEY  = "YOUR_BOT_API"
SECRET_TKN  = "SECRET_PHRASE" #passed with setwebhook request
HTTPS       = "HTTPS_URL_TO_APPLICATION" #HTTPS url to application
PATH        = "/CUSTOM_PATH" #custom path, can be even a "/"
TG_BASE_URL = "https://api.telegram.org/bot"
TG_REQ_URL  = TG_BASE_URL + TG_API_KEY


### NASA API
NASA_API_KEY    = "YOUR_NASA_API_KEY"
APOD_URL        = "https://api.nasa.gov/planetary/apod"


### BOT
MSG = {
    "START"     : "Welcome to APOD bot!\nIt gives you access to NASA's Astronomy Picture of the Day archive in your comfort on Telegram.\nYou can\n• pass a date(like 2020-2-22)\n• use /today for the most recent picture\n• or let the bot surprise you by /random !\n\nThis is an open-source project.\nSee About for more information.\n\nWith 💛 by Amir",
    "ABOUT"     : "I was wondering if it would be more convenient to access NASA's APOD archive from a Telegram bot, so I made it happen :)\nThis is an open-source project. You can find the source code on <a href='https://github.com/AHZak/APOD_NASAbot'>Github</a>\nTo report bugs and for suggestions, please contact me via\npro@zakariazadeh.com\n\n∆ by <a href='https://zakariazadeh.com'>Amir Zakaria</a>",
    'ARCHIVE'   : "An archinve holding more than 27 years of daily APOD pictures!\nSimply send me a date from Jun 16, 1995 in the following format:\n2022-2-22",
    "UNKNOWN"   : "I don't know what's happening 🤔\nI'll inform Amir",
    'OPTIONS'   : "You can send me /today" + ", " + "/random or a date in the following format:\n2020-2-22",
    "LIMIT"     : "Server is meltig! please try in another time :D",
    "OR_DATE"   : "Date must be between Jun 16, 1995 and " + (datetime.now(pytz.timezone("EST")) - timedelta(days=1)).strftime("%b %d %Y"),
    "FOR_AUDIO" : "Let me send this song to Mars...",
    "FOR_VIDEO" : "I'll show this video to ISS astronauts ;)",
    "FOR_MISC"  : "I wish I could understand :)",
    "FOR_FRW"   : "You don't like to talk to me directly? :)"
}

#file_id of predefined media
FILES = {
    "PHOTO"     : "PHOTO_FILE_ID",
    "STICKER"   : "STICKER_FILE_ID",
    "GIF"       : "GIF_FILE_ID"
}