import sys

from telethon import TelegramClient
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession

from ramext.config import Config


if Config.STRING_SESSION:
    session = StringSession(str(Config.STRING_SESSION))
else:
    session = "ramubot"

try:
    RAM = TelegramClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
except Exception as e:
    print(f"STRING_SESSION - {e}")
    sys.exit()


if Config.SESSION_2:
    session2 = StringSession(str(Config.SESSION_2))
    RAM2 = TelegramClient(
        session=session2,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
else:
    RAM2 = None


if Config.SESSION_3:
    session3 = StringSession(str(Config.SESSION_3))
    RAM3 = TelegramClient(
        session=session3,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
else:
    RAM3 = None


if Config.SESSION_4:
    session4 = StringSession(str(Config.SESSION_4))
    RAM4 = TelegramClient(
        session=session4,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
else:
    RAM4 = None


if Config.SESSION_5:
    session5 = StringSession(str(Config.SESSION_5))
    RAM5 = TelegramClient(
        session=session5,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
else:
    RAM5 = None


rambot = TelegramClient(
    session="RAM-TBot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
).start(bot_token=Config.BOT_TOKEN)
