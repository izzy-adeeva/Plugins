import asyncio
import io
import os
from pathlib import Path

from . import *


@ram_cmd(pattern="cmds$")
async def kk(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    zy = await client_id(event)
    rampedo, RAM_USER, ram_mention = zy[0], zy[1], zy[2]
    cmd = "ls userbot/plugins"
    thumb = ram_logo
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    _o = o.split("\n")
    o = "\n".join(_o)
    OUTPUT = f"List of Plugins in bot :- \n\n{o}\n\n<><><><><><><><><><><><><><><><><><><><><><><><>\nHELP:- If you want to know the commands for a plugin, do :- \n.plinfo <plugin name> without the < > brackets. \nJoin {hell_grp} for help."
    if len(OUTPUT) > 69:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "cmd_list.text"
            hell_file = await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                thumb=thumb,
                reply_to=reply_to_id,
            )
            await edit_or_reply(
                hell_file,
                f"Output Too Large. This is the file for the list of plugins in bot.\n\n**BY :-** {RAM_USER}",
            )
            await event.delete()


@ram_cmd(pattern="send ([\s\S]*)")
async def send(event):
    zy = await client_id(event)
    rampedo, RAM_USER, ram_mention = zy[0], zy[1], zy[2]
    message_id = event.message.id
    thumb = ram_logo
    input_str = event.pattern_match.group(1)
    omk = f"**• Plugin name ≈** `{input_str}`\n**• Uploaded by ≈** {ram_mention}\n\n **RAM_UBOT Extended({chnl_link})** "
    the_plugin_file = "./userbot/plugins/{}.py".format(input_str)
    if os.path.exists(the_plugin_file):
        lauda = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            thumb=thumb,
            caption=omk,
            force_document=True,
            allow_cache=False,
            reply_to=message_id,
        )
        await event.delete()
    else:
        await eod(event, "File not found...")


@ram_cmd(pattern="install(?:\s|$)([\s\S]*)")
async def install(event):
    zy = await client_id(event)
    rampedo, RAM_USER, ram_mention = zy[0], zy[1], zy[2]
    b = 1
    owo = event.text[9:]
    TOD = await eor(event, "__Installing.__")
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = (
                await event.client.download_media(  # pylint:disable=E0602
                    await event.get_reply_message(),
                    "./userbot/plugins/",  # pylint:disable=E0602
                )
            )
            if owo != "-f":
                op = open(downloaded_file_name, "r")
                rd = op.read()
                op.close()
                try:
                    for harm in HARMFUL:
                        if harm in rd:
                            os.remove(downloaded_file_name)
                            return await TOD.edit(
                                f"**⚠️ WARNING !!** \n\n__Replied plugin file contains some harmful codes. Please consider checking the file. If you still want to install then use__ `{ii}install -f`. \n\n**Codes Detected :** \n• {harm}"
                            )
                except BaseException:
                    pass
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                if shortname in CMD_LIST:
                    string = "**Commands found in** `{}`\n".format(
                        (os.path.basename(downloaded_file_name))
                    )
                    for i in CMD_LIST[shortname]:
                        string += "  •  `" + i
                        string += "`\n"
                        if b == 1:
                            a = "__Installing..__"
                            b = 2
                        else:
                            a = "__Installing...__"
                            b = 1
                        await TOD.edit(a)
                    return await TOD.edit(
                        f"✅ **Installed module** :- `{shortname}` \n BY :- {ram_mention}\n\n{string}\n\n         **RAM-UBOT Extended({chnl_link})** ",
                        link_preview=False,
                    )
                return await TOD.edit(
                    f"Installed module `{os.path.basename(downloaded_file_name)}`"
                )
            else:
                os.remove(downloaded_file_name)
                return await eod(
                    TOD,
                    f"**Failed to Install** \n`Error`\nModule already installed or unknown format",
                )
        except Exception as e:
            await eod(TOD, f"**Failed to Install** \n`Error`\n{str(e)}")
            return os.remove(downloaded_file_name)


@ram_cmd(pattern="uninstall ([\s\S]*)")
async def uninstall(event):
    shortname = event.text[11:]
    if ".py" in shortname:
        shortname = shortname.replace(".py", "")
    TOD = await eor(event, f"__Trying to uninstall plugin__ `{shortname}` ...")
    dir_path = f"./userbot/plugins/{shortname}.py"
    try:
        remove_plugin(shortname)
        os.remove(dir_path)
        await eod(TOD, f"**Uninstalled plugin** `{shortname}` **successfully.**")
    except OSError as e:
        await eod(TOD, f"**Error !!** \n\n`{dir_path}` : __{e.strerror}__")


@ram_cmd(pattern="unload ([\s\S]*)")
async def unload(event):
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await event.edit(f"Successfully unloaded `{shortname}`")
    except Exception as e:
        await event.edit(
            "Successfully unloaded {shortname}\n{}".format(shortname, str(e))
        )


@ram_cmd(pattern="load ([\s\S]*)")
async def load(event):
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await event.edit(f"Successfully loaded `{shortname}`")
    except Exception as e:
        await event.edit(
            f"Sorry, could not load {shortname} because of the following error.\n{str(e)}"
        )


CmdHelp("core").add_command(
    "install",
    "<reply to a .py file>",
    "Installs the replied python file if suitable to RAM-UBOT Extended's codes.`\n**🚩 Flags :** `-f",
).add_command(
    "uninstall",
    "<plugin name>",
    "Uninstalls the given plugin from RAM-UBOT Extended. To get that again do .restart",
    "uninstall alive",
).add_command(
    "load", "<plugin name>", "Loades the unloaded plugin to your userbot", "load alive"
).add_command(
    "unload", "<plugin name>", "Unloads the plugin from your userbot", "unload alive"
).add_command(
    "send",
    "<file name>",
    "Sends the given file from your userbot server, if any.",
    "send alive",
).add_command(
    "cmds", None, "Gives out the list of modules in RAM-UBOT."
).add_warning(
    "❌ Install External Plugin On Your Own Risk. We won't help if anything goes wrong after installing a plugin."
).add()
