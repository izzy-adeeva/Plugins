import asyncio
import datetime
import time

from . import *

ping_txt = """<b>--- PONG ---</b>

    Speed :</i> <code>{}</code>
    Uptime :</i> <code>{}</code>
    Owner:</i> {}"""


@ram_cmd(pattern="ping$")
async def pong(zzy):
    start = datetime.datetime.now()
    event = await eor(zzy, "`·.·PINGING·.·´")
    cid = await client_id(event)
    ramtod, RAM_USER = cid[0], cid[1]
    ram_mention = f"<a href='tg://user?id={ramtod}'>{RAM_USER}</a>"
    uptime = await get_time((time.time() - StartTime))
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(ping_txt.format(ms, uptime, ram_mention), parse_mode="HTML")


CmdHelp("ping").add_command(
  "ping", None, "Checks the ping speed of your RAM-UBOT"
).add_warning(
  "✅ Harmless Module"
).add()