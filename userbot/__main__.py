import glob
import sys
from pathlib import Path

import telethon.utils
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from userbot import LOGS, bot, tbot
from userbot.clients.session import TOD2, TOD3, TOD4, TOD5
from userbot.config import Config
from userbot.utils import load_module
from userbot.version import __tod__ as todversion

ii = Config.HANDLER

RAM_PIC = "https://telegra.ph/file/e62dcb31e02594af0fab4.png"


async def ramm(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()


async def ram_client(client):
    client.me = await client.get_me()
    client.uid = telethon.utils.get_peer_id(client.me)


def rams():
    failed = 0
    if Config.SESSION_2:
        LOGS.info("SESSION_2 detected! Starting 2nd Client.")
        try:
            TOD2.start()
            TOD2.loop.run_until_complete(ram_client(TOD2))
        except:
            LOGS.info("SESSION_2 failed. Please Check Your String session.")
            failed += 1

    if Config.SESSION_3:
        LOGS.info("SESSION_3 detected! Starting 3rd Client.")
        try:
            TOD3.start()
            TOD3.loop.run_until_complete(ram_client(TOD3))
        except:
            LOGS.info("SESSION_3 failed. Please Check Your String session.")
            failed += 1

    if Config.SESSION_4:
        LOGS.info("SESSION_4 detected! Starting 4th Client.")
        try:
            TOD4.start()
            TOD4.loop.run_until_complete(ram_client(TOD4))
        except:
            LOGS.info("SESSION_4 failed. Please Check Your String session.")
            failed += 1

    if Config.SESSION_5:
        LOGS.info("SESSION_5 detected! Starting 5th Client.")
        try:
            TOD5.start()
            TOD5.loop.run_until_complete(ram_client(TOD5))
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


if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if Config.BOT_USERNAME is not None:
            LOGS.info("Checking Telegram Bot Username...")
            bot.tgbot = tbot
            LOGS.info("Checking Completed. Proceeding to next step...")
            LOGS.info("Starting RAM-EXTENDED UBOT")
            bot.loop.run_until_complete(ramm(Config.BOT_USERNAME))
            failed_client = rams()
            global total
            total = 5 - failed_client
            LOGS.info("RAM-EXTENDED UBOT")
            LOGS.info(f"» Total Clients = {total} «")
        else:
            bot.start()
            failed_client = rams()
            total = 5 - failed_client
            LOGS.info(f"» Total Clients = {total} «")
    except Exception as e:
        LOGS.error(f"BOT_TOKEN - {str(e)}")
        sys.exit()


path = "userbot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))


LOGS.info("Starting Bot Mode !")
tbot.start()
LOGS.info("RAM-EXTENDED UBOT is working")
LOGS.info("SHUT UP AND ENJOY YOUR BOT!.")
LOGS.info(f"» Total Clients = {total} «")


async def ram_on():
    try:
        x = await bot.get_me()
        xid = telethon.utils.get_peer_id(x)
        send_to = Config.LOGGER_ID if Config.LOGGER_ID != 0 else xid
        await bot.send_file(
            send_to,
            RAM_PIC,
            caption=f"#START \n\n<b><i>Version :</b></i> <code>{todversion}</code> \n<b><i>Clients :</b></i> <code>{total}</code> \n\n<b><i>»» <u><a href='https://t.me/Its_HellBot'>RAM_UBOT Extended</a></u> ««</i></b>",
            parse_mode="HTML",
        )
    except Exception as e:
        LOGS.info(str(e))

    try:
        await bot(JoinChannelRequest("@ramsupportt"))
    except BaseException:
        pass
    try:
        if TOD2:
            await TOD2(JoinChannelRequest("@ramsupportt"))
    except BaseException:
        pass
    try:
        if TOD3:
            await TOD3(JoinChannelRequest("@ramsupportt"))
    except BaseException:
        pass
    try:
        if TOD4:
            await TOD4(JoinChannelRequest("@ramsupportt"))
    except BaseException:
        pass

    try:
        if TOD5:
            await TOD5(JoinChannelRequest("@ramsupportt"))
    except BaseException:
        pass
    try:
        await bot(ImportChatInviteRequest("@ramsupportt"))
    except BaseException:
        pass
    try:
        if TOD2:
            await TOD2(ImportChatInviteRequest("@ramsupportt"))
    except BaseException:
        pass
    try:
        if TOD3:
            await TOD3(ImportChatInviteRequest("@ramsupportt"))
    except BaseException:
        pass
    try:
        if TOD4:
            await TOD4(ImportChatInviteRequest("@ramsupportt"))
    except BaseException:
        pass
    try:
        if TOD5:
            await TOD5(ImportChatInviteRequest("@ramsupportt"))
    except BaseException:
        pass


bot.loop.create_task(ram_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()

# userbot
