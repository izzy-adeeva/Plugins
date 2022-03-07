import datetime
import random
import time

from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from userbot.sql.gvar_sql import gvarstat

from . import *

# -------------------------------------------------------------------------------

ALIVE_TEMP = """
<b>RAM-UBOT Extended</b>
<b>OWNER</i> : <a href='tg://user?id={}'>{}</a> 

<b> Telethon ~</b> <i>{}</i>
<b> RAM-UBOT Extended ~</b> <i>{}</i>
<b> Sudo ~</b> <i>{}</i>
<b> Uptime ~</b> <i>{}</i>
<b> Ping ~</b> <i>{}</i>

<b><i><a href='https://t.me/ramsupport'>[ RAM_UBOT Extended ]</a></i></b>
"""
# -------------------------------------------------------------------------------


@ram_cmd(pattern="alive$")
async def up(event):
    cid = await client_id(event)
    rampedo, RAM_USER, ram_mention = cid[0], cid[1], cid[2]
    start = datetime.datetime.now()
    TOD = await eor(event, "`Building Alive....`")
    uptime = await get_time((time.time() - StartTime))
    a = gvarstat("ALIVE_PIC")
    if a is not None:
        b = a.split(" ")
        c = []
        if len(b) >= 1:
            for d in b:
                c.append(d)
        PIC = random.choice(c)
    else:
        PIC = "https://telegra.ph/file/e62dcb31e02594af0fab4.png"
    RAM_PIC = PIC
    end = datetime.datetime.now()
    ling = (end - start).microseconds / 1000
    omk = ALIVE_TEMP.format(rampedo, RAM_USER, tel_ver, ram_ver, is_sudo, uptime, ling)
    await event.client.send_file(
        event.chat_id, file=RAM_PIC, caption=omk, parse_mode="HTML"
    )
    await TOD.delete()


msg = """{}\n
<b><i>Bot Status</b></i>
<b>Telethon ≈</b>  <i>{}</i>
<b>RAM-UBOT Extended ≈</b>  <i>{}</i>
<b>Uptime ≈</b>  <i>{}</i>
<b>Sudo ≈</b>  <i>{}</i>
"""
botname = Config.BOT_USERNAME


@ram_cmd(pattern="TOD$")
async def hell_a(event):
    cid = await client_id(event)
    rampedo, RAM_USER, ram_mention = cid[0], cid[1], cid[2]
    uptime = await get_time((time.time() - StartTime))
    am = gvarstat("ALIVE_MSG") or "<b>RAM-UBOT Extended is online</b>"
    try:
        TOD = await event.client.inline_query(botname, "alive")
        await TOD[0].click(event.chat_id)
        if event.sender_id == rampedo:
            await event.delete()
    except (noin, dedbot):
        await eor(
            event,
            msg.format(am, tel_ver, ram_ver, uptime, abuse_m, is_sudo),
            parse_mode="HTML",
        )


CmdHelp("alive").add_command(
    "alive", None, "Shows the Default Alive Message"
).add_command("TOD", None, "Shows Inline Alive Menu with more details.").add_warning(
    "✅ Harmless Module"
).add()
