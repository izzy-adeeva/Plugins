from telethon import events

from ramext.sql.autopost_sql import add_post, get_all_post, is_post, remove_post
from ramext.sql.gvar_sql import gvarstat, addgvar, delgvar

from . import *


@ram_cmd(pattern="autopost(?:\s|$)([\s\S]*)")
async def _(event):
    if event.is_private:
        return await eod(event, "AutoPost Can Only Be Used For Channels & Groups.")
    zzy = await eor(event, "Trying to start autoposting from here...")
    cid = await client_id(event)
    ramtod = cid[0]
    rr = event.text[10:]
    cli_ = ramtod
    checker = gvarstat(f"AUTOPOST_{str(cli_)}")
    if rr == "":
        return await eod(zzy, f"Give correct command for working of autopost. \n`{ii}autopost channel_id`")
    if str(rr).startswith("-100"):
        kk = str(rr).replace("-100", "")
    else:
        kk = rr
    if not kk.isdigit():
        return await eod(zzy, "**Please Give Channel ID !!**")
    if is_post(kk , event.chat_id):
        if checker and checker == "True":
            return await zzy.edit("This channel is already in this client's autopost database.")
        else:
            addgvar(f"AUTOPOST_{str(cli_)}", "True")
            return await zzy.edit(f"**📍 Started AutoPosting from** `{rr}` for `{cli_}`")
    add_post(kk, event.chat_id)
    addgvar(f"AUTOPOST_{str(cli_)}", "True")
    await zzy.edit(f"**📍 Started AutoPosting from** `{rr}` for `{cli_}`")


@ram_cmd(pattern="rmautopost(?:\s|$)([\s\S]*)")
async def _(event):
    if event.is_private:
        return await eod(event, "AutoPost Can Only Be Used For Channels.")
    zzy = await eor(event, "Removing autopost...")
    cid = await client_id(event)
    ramtod = cid[0]
    rr = event.text[12:]
    cli_ = ramtod
    checker = gvarstat(f"AUTOPOST_{str(cli_)}")
    if rr == "":
        return await eod(zzy, f"Give correct command for removing autopost. \n`{ii}autopost channel_id`")
    if str(rr).startswith("-100"):
        kk = str(rr).replace("-100", "")
    else:
        kk = rr
    if not kk.isdigit():
        return await eod(event, "**Please Give Channel ID !!**")
    if not is_post(kk, event.chat_id):
        return await eod(event, "I don't think this channel is in AutoPost Database.")
    if is_post(kk, event.chat_id):
        if checker and checker == "True":
            remove_post(kk, event.chat_id)
            delgvar(f"AUTOPOST_{str(cli_)}")
            return await eod(zzy, f"Removed `{rr}` from `{cli_}` autopost database.")
        else:
            return await eod(zzy, f"This channel is not in `{cli_}` autopost database.")


@ram_handler()
async def _(event):
    chat_id = str(event.chat_id).replace("-100", "")
    channels_set  = get_all_post(chat_id)
    if channels_set == []:
        return
    cid = await client_id(event)
    ramtod = cid[0]
    cli_ = ramtod
    checker = gvarstat(f"AUTOPOST_{str(cli_)}")
    if checker and checker == "True":
        for chat in channels_set:
            if event.media:
                await event.client.send_file(int(chat), event.media, caption=event.text)
            elif not event.media:
                await event.client.send_message(int(chat), event.message)


CmdHelp("autopost").add_command(
  "autopost", "<channel id>", "Auto Posts every new post from targeted channel to your channel.", "autopost <channelid> [in your channel]"
).add_command(
  "rmautopost", "<channel id>", "Stops AutoPost from targeted autoposting channel."
).add_info(
  "AutoPost From One Channel To Another."
).add_warning(
  "✅ Harmless Module."
).add()
