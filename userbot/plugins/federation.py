import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *

logs_id = Config.FBAN_LOG_GROUP
fbot = "@MissRose_bot"


@ram_cmd(pattern="newfed ([\s\S]*)")
async def _(event):
    hell_input = event.pattern_match.group(1)
    chat = "@MissRose_Bot"
    TOD = await eor(event, "`Making new fed...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=609517172)
            )
            await event.client.send_message(chat, f"/newfed {hell_input}")
            response = await response
        except YouBlockedUserError:
            await eod(TOD, "`Please unblock` @MissRose_Bot `and try again`")
            return
        if response.text.startswith("You already have a federation"):
            await eod(
                TOD,
                f"You already have a federation. Do {ii}renamefed to rename your current fed.",
            )
        else:
            await TOD.edit(f"{response.message.message}")


@ram_cmd(pattern="renamefed ([\s\S]*)")
async def _(event):
    hell_input = event.pattern_match.group(1)
    chat = "@MissRose_Bot"
    TOD = await eor(event, "`Trying to rename your fed...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=609517172)
            )
            await event.client.send_message(chat, f"/renamefed {hell_input}")
            response = await response
        except YouBlockedUserError:
            await eod(TOD, "Please Unblock @MissRose_Bot")
            return
        else:
            await TOD.edit(response.message)


@ram_cmd(pattern="fstat ([\s\S]*)")
async def _(event):
    TOD = await eor(event, "`Collecting fstat....`")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        lavde = str(previous_message.sender_id)
        user = f"[user](tg://user?id={lavde})"
    else:
        lavde = event.pattern_match.group(1)
    if lavde == "":
        await TOD.edit("`Need username/id to check fstat`")
        return
    else:
        async with event.client.conversation(fbot) as conv:
            try:
                await conv.send_message("/fedstat " + lavde)
                await asyncio.sleep(4)
                response = await conv.get_response()
                await asyncio.sleep(2)
                await event.client.send_message(event.chat_id, response)
                await event.delete()
            except YouBlockedUserError:
                await TOD.edit("`Please Unblock` @MissRose_Bot")


@ram_cmd(pattern="fedinfo ([\s\S]*)")
async def _(event):
    TOD = await eor(event, "`Fetching fed info.... please wait`")
    lavde = event.pattern_match.group(1)
    async with event.client.conversation(fbot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedinfo " + lavde)
            massive = await conv.get_response()
            await TOD.edit(massive.text + "\n\n**ʟɛɢɛռɖaʀʏ_ᴀғ_ɦɛʟʟɮօt**")
        except YouBlockedUserError:
            await TOD.edit("`Please Unblock` @MissRose_Bot")


CmdHelp("federation").add_command(
    "newfed", "<newfed name>", "Makes a federation of Rose bot"
).add_command("renamefed", "<new name>", "Renames the fed of Rose Bot").add_command(
    "fstat", "<username/id>", "Gets the fban stats of the user from rose bot federation"
).add_command(
    "fedinfo", "<fed id>", "Gives details of the given fed id"
).add_info(
    "Rose Bot Federation."
).add_warning(
    "✅ Harmless Module."
).add()
