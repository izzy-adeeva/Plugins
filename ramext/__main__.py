import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from ramext import LOGS, bot, tbot
from ramext.clients.session import RAM, RAM2, RAM3, RAM4, RAM5
from ramext.config import Config
from ramext.utils import load_module
from ramext.version import version as ramver
ii = Config.HANDLER

RAM_PIC = "https://telegra.ph/file/e62dcb31e02594af0fab4.png"


# let's get the bot ready
async def h1(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()


# Multi-Client helper
async def ram_client(client):
    client.me = await client.get_me()
    client.uid = telethon.utils.get_peer_id(client.me)


# Multi-Client Starter
def rams():
    failed = 0
    if Config.SESSION_2:
        LOGS.info("SESSION_2 detected! Starting 2nd Client.")
        try:
            RAM2.start()
            RAM2.loop.run_until_complete(ram_client(RAM2))
        except:
            LOGS.info("SESSION_2 failed. Please Check Your String session.")
            failed += 1

    if Config.SESSION_3:
        LOGS.info("SESSION_3 detected! Starting 3rd Client.")
        try:
            RAM3.start()
            RAM3.loop.run_until_complete(ram_client(RAM3))
        except:
            LOGS.info("SESSION_3 failed. Please Check Your String session.")
            failed += 1

    if Config.SESSION_4:
        LOGS.info("SESSION_4 detected! Starting 4th Client.")
        try:
            RAM4.start()
            RAM4.loop.run_until_complete(ram_client(RAM4))
        except:
            LOGS.info("SESSION_4 failed. Please Check Your String session.")
            failed += 1

    if Config.SESSION_5:
        LOGS.info("SESSION_5 detected! Starting 5th Client.")
        try:
            RAM5.start()
            RAM5.loop.run_until_complete(ram_client(RAM5))
        except:
            LOGS.info("SESSION_5 failed. Please Check Your String session.")
            failed += 1

    if not Config.SESSION_2:
        failed += 1
    if not Config.SESSION_3:
        failed += 1
    if not Config.SESSION_4:
        failed += 1
    if not Config.SESSION_5:
        failed += 1
    return failed


# iraa starter...
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if Config.BOT_USERNAME is not None:
            LOGS.info("Checking Telegram Bot Username...")
            bot.tgbot = tbot
            LOGS.info("Checking Completed. Proceeding to next step...")
            LOGS.info("- Starting RAM-UBOT Extended -")
            bot.loop.run_until_complete(h1(Config.BOT_USERNAME))
            failed_client = rams()
            global total
            total = 5 - failed_client
            LOGS.info("- RAM-UBOT Extended Startup Completed -")
            LOGS.info(f"» Total Clients = {total} «")
        else:
            bot.start()
            failed_client = rams()
            total = 5 - failed_client
            LOGS.info(f"» Total Clients = {total} «")
    except Exception as e:
        LOGS.error(f"BOT_TOKEN - {str(e)}")
        sys.exit()


# imports plugins...
path = "ramext/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))


# let the party begin...
LOGS.info("Starting Bot Mode !")
tbot.start()
LOGS.info(" RAM-UBOT Extended is Online ")
LOGS.info("Shut up and Enjoy your bot.")
LOGS.info(f"» Total Clients = {total} «")

# that's life...
async def ram_on():
    try:
        x = await bot.get_me()
        xid = telethon.utils.get_peer_id(x)
        send_to = Config.LOGGER_ID if Config.LOGGER_ID != 0 else xid
        await bot.send_file(
            send_to,
            RAM_PIC,
            caption=f"#RAM-UBOT Extended \n\n<b><i>Version :</b></i> <code>{ramver}</code> \n<b><i>Clients :</b></i> <code>{total}</code> \n\n<b><u><a href='https://t.me/ramsupportt'>RAM-UBOT Extended</a></u></b>",
            parse_mode="HTML",
        )
    except Exception as e:
        LOGS.info(str(e))
# Join ramubot Channel after deploying 🤐😅
    try:
        await bot(JoinChannelRequest("ramsupportt"))
    except BaseException:
        pass
    try:
        if RAM2:
            await RAM2(JoinChannelRequest("ramsupportt"))
    except BaseException:
        pass
    try:
        if RAM3:
            await RAM3(JoinChannelRequest("ramsupportt"))
    except BaseException:
        pass
    try:
        if RAM4:
            await RAM4(JoinChannelRequest("ramsupportt"))
    except BaseException:
        pass
    try:
        if RAM5:
            await RAM5(JoinChannelRequest("ramsupportt"))
    except BaseException:
        pass
# Why not come here and chat??
    try:
        await bot(ImportChatInviteRequest('ramsupportt'))
    except BaseException:
        pass
    try:
        if RAM2:
            await RAM2(ImportChatInviteRequest('ramsupportt'))
    except BaseException:
        pass
    try:
        if RAM3:
            await RAM3(ImportChatInviteRequest('ramsupportt'))
    except BaseException:
        pass
    try:
        if RAM4:
            await RAM4(ImportChatInviteRequest('ramsupportt'))
    except BaseException:
        pass
    try:
        if RAM5:
            await RAM5(ImportChatInviteRequest('ramsupportt'))
    except BaseException:
        pass



bot.loop.create_task(ram_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()

# iraa
