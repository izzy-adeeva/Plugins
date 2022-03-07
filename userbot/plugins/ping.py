import datetime
import time

from . import *

ping_txt = """<b><i>PONG</b></i>

    ⚘  <i>SPEED:</i> <code>{}</code>
    ⚘  <i>UPTIME:</i> <code>{}</code>
    ⚘  <i>OWNER:</i> {}"""


@ram_cmd(pattern="ping$")
async def pong(TOD):
    start = datetime.datetime.now()
    event = await eor(TOD, "`... PING ...´")
    cid = await client_id(event)
    rampedo, RAM_USER = cid[0], cid[1]
    ram_mention = f"<a href='tg://user?id={rampedo}'>{RAM_USER}</a>"
    uptime = await get_time((time.time() - StartTime))
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(ping_txt.format(ms, uptime, ram_mention), parse_mode="HTML")


CmdHelp("ping").add_command(
    "ping", None, "Checks the ping speed of your RAM-UBOT Extended"
).add_warning("✅ Harmless Module").add()
