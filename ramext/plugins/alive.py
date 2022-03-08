import datetime
import random
import time

from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from ramext.sql.gvar_sql import gvarstat
from . import *

#-------------------------------------------------------------------------------

ALIVE_TEMP = """
<b><i>RAM-UBOT Extended</b></i>
<i><b>- owner -</i></b> : 『 <a href='tg://user?id={}'>{}</a> 』
╭──────────────
┣─ <b>Telethon ~</b> <i>{}</i>
┣─ <b>RAM-UBOT ~</b> <i>{}</i>
┣─ <b>Sudo ~</b> <i>{}</i>
┣─ <b>Uptime ~</b> <i>{}</i>
┣─ <b>Ping ~</b> <i>{}</i>
╰──────────────
<b><a href='https://t.me/ramsupportt'>[ RAM-UBOT Extended ]</a></b>
"""
#-------------------------------------------------------------------------------

@ram_cmd(pattern="alive$")
async def up(event):
    cid = await client_id(event)
    ramtod, RAM_USER, ram_mention = cid[0], cid[1], cid[2]
    start = datetime.datetime.now()
    zzy = await eor(event, "`Building Alive....`")
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
    ram_pic = PIC
    end = datetime.datetime.now()
    ling = (end - start).microseconds / 1000
    omk = ALIVE_TEMP.format(ramtod, RAM_USER, telethon_ver, ram_version, is_sudo, uptime, ling)
    await event.client.send_file(event.chat_id, file=ram_pic, caption=omk, parse_mode="HTML")
    await zzy.delete()


msg = """{}\n
<b>RAM-UBOT Extended </b>
<b>Telethon ≈</b>  <i>{}</i>
<b>RAM-UBOT ≈</b>  <i>{}</i>
<b>Uptime ≈</b>  <i>{}</i>
<b>Sudo ≈</b>  <i>{}</i>
"""
botname = Config.BOT_USERNAME

@ram_cmd(pattern="ram$")
async def ram_a(event):
    cid = await client_id(event)
    ramtod, RAM_USER, ram_mention = cid[0], cid[1], cid[2]
    uptime = await get_time((time.time() - StartTime))
    am = gvarstat("ALIVE_MSG") or "<b>RAM-UBOT is ONLINE</b>"
    try:
        zzy = await event.client.inline_query(botname, "alive")
        await zzy[0].click(event.chat_id)
        if event.sender_id == ramtod:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg.format(am, telethon_ver, ram_version, uptime, abuse_m, is_sudo), parse_mode="HTML")


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "ram", None, "Shows Inline Alive Menu with more details."
).add_warning(
  "✅ Harmless Module"
).add()
