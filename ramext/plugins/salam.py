import asyncio

from . import *
from ramext.utils.extras import edit_or_reply as karin



@ram_cmd(pattern="as$")
async def _(event):
    event = await karin(event, "as")
    await event.edit("yuuhuuuu")
    await asyncio.sleep(1)
    await event.edit("Assalamualaikum wr. wb.")


@ram_cmd(pattern="ws$")
async def _(event):
    "animation command"
    event = await karin(event, "ws")
    await event.edit("huuyyyy")
    await asyncio.sleep(1)
    await event.edit("Waalaikum salam wr. wb.")

CmdHelp("salam").add_command(
  'as', 'Kasih salam'
).add_command(
  'ws', 'jawab salam'
).add_info(
  "Biar sopan."
).add_warning(
  "⚠️ Some commands may cause flood error."
).add()