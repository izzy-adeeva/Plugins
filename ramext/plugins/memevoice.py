from . import *
# Credits to @ramtod developer of ramubot.
# This is my first plugin that I made when I released first ramubot.
# Modified to work in groups with inline mode disabled.
# Added error msg if no voice is found.
# So please dont remove credit. 
# You can use it in your repo. But dont remove these lines...

@ram_cmd(pattern="mev(?:\s|$)([\s\S]*)")
async def _(event):
    zzy = event.text[5:]
    rply = await event.get_reply_message()
    if not zzy:
        if event.is_reply:
            rply.message
        else:
            return await eod(event, "`Sir please give some query to search and download it for you..!`")
    troll = await event.client.inline_query("TrollVoiceBot", f"{(deEmojify(zzy))}")
    if troll:
        await event.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await event.client.send_file(
                event.chat_id,
                hel_,
                caption="",
                reply_to=rply,
            )
        await hel_.delete()
    else:
        await eod(event, "**Error 404:**  Not Found")


@ram_cmd(pattern="meev(?:\s|$)([\s\S]*)")
async def _(event):
    zzy = event.text[6:]
    rply = await event.get_reply_message()
    if not zzy:
        if event.is_reply:
            rply.message
        else:
            return await eod(event, "`Sir please give some query to search and download it for you..!`")
    troll = await event.client.inline_query("Myinstantsbot", f"{(deEmojify(zzy))}")
    if troll:
        await event.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await event.client.send_file(
                event.chat_id,
                hel_,
                caption="",
                reply_to=rply,
            )
        await hel_.delete()
    else:
        await eod(event, "**Error 404:**  Not Found")


CmdHelp("memevoice").add_command(
    "mev", "<query>", "Searches the given meme and sends audio if found."
).add_command(
    "meev", "<query>", "Same as {ii}mev"
).add_info(
    "Audio Memes."
).add_warning(
    "✅ Harmless Module."
).add()
