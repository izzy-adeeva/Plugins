

import os
from telethon.tl.types import ChatBannedRights

class Config(object):
    LOGGER = True
    ABUSE = os.environ.get("PROFANITY", "ON")
    ALIVE_MSG = os.environ.get("ALIVE_MSG", None)
    ALIVE_PIC = os.environ.get("ALIVE_PIC", None)
    ANTI_FLOOD_WARN_MODE = ChatBannedRights(until_date=None, view_messages=None, send_messages=True)
    API_HASH = os.environ.get("API_HASH", None)
    APP_ID = os.environ.get("APP_ID", None)
    AUTH_TOKEN_DATA = os.environ.get("AUTH_TOKEN_DATA", None)
    if AUTH_TOKEN_DATA != None:
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        t_file = open(TMP_DOWNLOAD_DIRECTORY+"auth_token.txt","w")
        t_file.write(AUTH_TOKEN_DATA)
        t_file.close()
    BAN_PIC = os.environ.get("BAN_PIC", None)
    BAN_TEXT = os.environ.get("BAN_TEXT", None)
    BIO_MSG = os.environ.get("BIO_MSG", "RAM-UBOT EXTENDED")
    BL_CHAT = set(int(x) for x in os.environ.get("BL_CHAT", "").split())
    BOT_HANDLER = os.environ.get("BOT_HANDLER", "\/")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
    BUTTONS_IN_HELP = int(os.environ.get("BUTTONS_IN_HELP", 7))
    CHATS_TO_MONITOR_FOR_ANTI_FLOOD = []
    CHROME_BIN = os.environ.get("CHROME_BIN", "/bin/.apt/usr/bin/google-chrome")
    CHROME_DRIVER = os.environ.get("CHROME_DRIVER", "/bin/.chromedriver/bin/chromedriver")
    CUSTOM_PMPERMIT = os.environ.get("CUSTOM_PMPERMIT", None)
    DB_URI = os.environ.get("DATABASE_URL", None)
    EMOJI_IN_HELP = os.environ.get("EMOJI_IN_HELP", "๑")
    FBAN_LOG_GROUP = os.environ.get("FBAN_LOG_GROUP", None)
    if FBAN_LOG_GROUP:
        FBAN_LOG_GROUP = int(FBAN_LOG_GROUP)
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    GBAN_LOG_GROUP = os.environ.get("GBAN_LOG_GROUP", None)
    if GBAN_LOG_GROUP:
        GBAN_LOG_GROUP = int(GBAN_LOG_GROUP)
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
    GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME", None)
    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)
    GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", "/bin/.apt/usr/bin/google-chrome")
    GROUP_REG_SED_EX_BOT_S = os.environ.get("GROUP_REG_SED_EX_BOT_S", r"(regex|moku|BananaButler_|rgx|l4mR)bot")
    HANDLER = os.environ.get("HANDLER", ".")
    HELP_PIC = os.environ.get("HELP_PIC", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    INSTANT_BLOCK = os.environ.get("INSTANT_BLOCK", None)
    LOCATION = os.environ.get("LOCATION", None)
    LOGGER_ID = os.environ.get("LOGGER_ID", None)
    if LOGGER_ID:
        LOGGER_ID = int(LOGGER_ID)
    MAX_ANTI_FLOOD_MESSAGES = 10
    MAX_MESSAGE_SIZE_LIMIT = 4095
    MAX_SPAM = int(os.environ.get("MAX_SPAM", 3))
    MY_CHANNEL = os.environ.get("YOUR_CHANNEL", "ramsupportt")
    MY_GROUP = os.environ.get("YOUR_GROUP", "GeezSupport")
    OCR_API = os.environ.get("OCR_API", None)
    PLUGIN_CHANNEL = os.environ.get("PLUGIN_CHANNEL", None)
    if PLUGIN_CHANNEL:
        PLUGIN_CHANNEL = int(PLUGIN_CHANNEL)
    PM_LOG_ID = os.environ.get("PM_LOG_ID", None)
    if PM_LOG_ID:
        PM_LOG_ID = int(PM_LOG_ID)
    PM_PERMIT = os.environ.get("PM_PERMIT", None)
    PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", "https://telegra.ph/file/e62dcb31e02594af0fab4.png")
    REMOVE_BG_API = os.environ.get("REMOVE_BG_API", None)
    SCREEN_SHOT_LAYER_ACCESS_KEY = os.environ.get("SCREEN_SHOT_LAYER_ACCESS_KEY", None)
    STICKER_PACKNAME = os.environ.get("STICKER_PACKNAME", "RAMSTIKERSPACK")
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    SESSION_2 = os.environ.get("SESSION_2", None)
    SESSION_3 = os.environ.get("SESSION_3", None)
    SESSION_4 = os.environ.get("SESSION_4", None)
    SESSION_5 = os.environ.get("SESSION_5", None)
    SUDO_HANDLER = os.environ.get("SUDO_HANDLER", ".")
    SUDO_USERS = []
    TAG_LOGGER = os.environ.get("TAG_LOGGER", None)
    if TAG_LOGGER: 
        TAG_LOGGER = int(TAG_LOGGER)
    TELEGRAPH_SHORT_NAME = os.environ.get("TELEGRAPH_SHORT_NAME", "ramubot")
    TEMP_DIR = os.environ.get("TEMP_DIR", None)
    TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")
    TZ = os.environ.get("TZ", "Asia/Kolkata")
    UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "https://github.com/hitokizzy/RAM-UBOT_EXTENDED")
    USE_EVAL = os.environ.get("USE_EVAL", None)
    WEATHER_API = os.environ.get("WEATHER_API", None)
    YOUR_NAME = os.environ.get("YOUR_NAME", None)
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)
    PING_PIC = (os.environ.get("PING_PIC"))
    PING_TEXT = os.environ.get("PING_TEXT")

class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
