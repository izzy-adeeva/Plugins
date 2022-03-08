import asyncio
import html
import os
import re
import random
import sys

from math import ceil
from re import compile

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

from ramext.sql.gvar_sql import gvarstat
from . import *
from ramext.config import Config

ram_row = Config.BUTTONS_IN_HELP
emoji = Config.EMOJI_IN_HELP
ram_pic = Config.PMPERMIT_PIC or "https://telegra.ph/file/e62dcb31e02594af0fab4.png"
cstm_pmp = Config.CUSTOM_PMPERMIT
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Config.LOGGER_ID
mssge = (
    str(cstm_pmp)
    if cstm_pmp
    else "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
)

USER_BOT_WARN_ZERO = "Enough Of Your Flooding In My Master's PM!! \n\n**🚫 Blocked and Reported**"

RAM_BOT = (
    "**🔥 RAM-UBOT Extended🔥**\n\nThis is to inform you that "
    "{} is currently unavailable.\nThis is an automated message.\n\n"
    "{}\n\n**Please Choose Why You Are Here!!**"
)

alive_txt = """{}\n
<b> 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 </b>
<b>Telethon ≈</b>  <i>{}</i>
<b>RAM-UBOT ≈</b>  <i>{}</i>
<b>Uptime ≈</b>  <i>{}</i>
<b>Sudo ≈</b>  <i>{}</i>
"""

def button(page, modules):
    Row = ram_row
    Column = 3

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::2], modules[1::2])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline(f"{emoji} " + pair + f" {emoji}", data=f"Information[{page}]({pair})")
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
               f"◀️ Back {emoji}", data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
               f"• ❌ •", data="close"
            ),
            custom.Button.inline(
               f"{emoji} Next ▶️", data=f"page({0 if page == (max_pages - 1) else page + 1})"
            ),
        ]
    )
    return [max_pages, buttons]


    modules = CMD_HELP
if Config.BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(InlineQuery)
    async def inline_handler(event):
        cids = await client_id(event, event.query.user_id)
        ramtod, RAM_USER, ram_mention = cids[0], cids[1], cids[2]
        builder = event.builder
        result = None
        query = event.text
        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        if event.query.user_id in auth and query == "RAM-UBOT_help":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            a = gvarstat("HELP_PIC")
            if a:
                help_pic = a.split("")[0]
            else:
                help_pic = "https://telegra.ph/file/e62dcb31e02594af0fab4.png"
            help_msg = f"**{ram_mention}**\n\n __No.of Plugins__ : `{len(CMD_HELP)}` \n __Commands__ : `{len(apn)}`\n __Page__ : 1/{veriler[0]}"
            if help_pic == "DISABLE":
                result = builder.article(
                    f"Hey! Only use {ii}help please",
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic.endswith((".jpg", ".png")):
                result = builder.photo(
                    help_pic,
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic:
                result = builder.document(
                    help_pic,
                    text=help_msg,
                    title="RAM-UBOT Alive",
                    buttons=veriler[1],
                    link_preview=False,
                )
        elif event.query.user_id in auth and query == "alive":
            uptime = await get_time((time.time() - StartTime))
            alv_msg = gvarstat("ALIVE_MSG") or "<b>RAM-UBOT IS ONLINE</b>"
            he_ll = alive_txt.format(alv_msg, telethon_ver, ram_version, uptime, abuse_m, is_sudo)
            alv_btn = [
                [Button.url(f"{RAM_USER}", f"tg://openmessage?user_id={ramtod}")],
                [Button.url("My Channel", f"https://t.me/{my_channel}"), 
                Button.url("My Group", f"https://t.me/{my_group}")],
            ]
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
            ALV_PIC = PIC
            if ALV_PIC and ALV_PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    ALV_PIC,
                    text=he_ll,
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            elif ALV_PIC:
                result = builder.document(
                    ALV_PIC,
                    text=he_ll,
                    title="RAM-UBOT Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            else:
                result = builder.article(
                    text=he_ll,
                    title="RAM-UBOT Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )

        elif event.query.user_id in auth and query == "pm_warn":
            hel_l = RAM_BOT.format(ram_mention, mssge)
            result = builder.photo(
                file=ram_pic,
                text=hel_l,
                buttons=[
                    [
                        custom.Button.inline(" Request ", data="req"),
                        custom.Button.inline(" Chat ", data="chat"),
                    ],
                    [custom.Button.inline(" Spam ", data="heheboi")],
                    [custom.Button.inline("Curious ", data="pmclick")],
                ],
            )

        elif event.query.user_id in auth and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"** RAM-UBOT Extended **",
                buttons=[
                    [Button.url("📑 Repo 📑", "https://github.com/hitokizzy/RAM-UBOT")],
                    [Button.url("🚀 Deploy 🚀", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fhitokizzy%2FRAM-UBOT&template=https%3A%2F%2Fgithub.com%2Fhitokizzy%2FRAM-UBOT")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[‏‏‎ ‎]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "RAM-UBOT_EXTENDED",
                text="""**Hey! This is [RAM-UBOT](https://t.me/ramsupport) \nYou can know more about me from the links given below 👇**""",
                buttons=[
                    [
                        custom.Button.url("🔥 CHANNEL 🔥", "https://t.me/ramsupportt"),
                        custom.Button.url(
                            " GROUP ", "https://t.me/GeezSupport"
                        ),
                    ],
                    [
                        custom.Button.url(
                            " REPO ", "https://github.com/hitokizzy/RAM-UBOT_Extended"),
                        custom.Button.url
                    (
                            " TUTORIAL ", "https://xnxx.com"
                    )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pmclick")))
    async def on_pm_click(event):

        x = await H1.get_me()
        ram_mention = f"[{x.first_name}]({x.id})"

        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for Other Users..."
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"🔰 This is RAM-UBOT PM Security for {ram_mention} to keep away unwanted retards from spamming PM..."
            )

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):


        x = await H1.get_me()
        ram_mention = f"[{x.first_name}]({x.id})"

        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"✅ **Request Registered** \n\n{ram_mention} will now decide to look for your request or not.\n😐 Till then wait patiently and don't spam!!"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**👀 Hey {ram_mention} !!** \n\n⚜️ You Got A Request From [{first_name}](tg://user?id={ok}) In PM!!"
            await event.client.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"chat")))
    async def on_pm_click(event):

        x = await H1.get_me()
        ram_mention = f"[{x.first_name}]({x.id})"

        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        event.query.user_id
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Ahh!! You here to do chit-chat!!\n\nPlease wait for {ram_mention} to come. Till then keep patience and don't spam."
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**👀 Hey {ram_mention} !!** \n\n⚜️ You Got A PM from  [{first_name}](tg://user?id={ok})  for random chats!!"
            await event.client.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):

        x = await H1.get_me()
        ram_mention = f"[{x.first_name}]({x.id})"
        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"🥴 **Nikal lawde\nPehli fursat me nikal**"
            )
            await event.client(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            first_name = html.escape(target.user.first_name)
            await event.client.send_message(
                LOG_GP,
                f"**Blocked**  [{first_name}](tg://user?id={ok}) \n\nReason:- Spam",
            )


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
        cids = await client_id(event, event.query.user_id)
        ramtod, RAM_USER, ram_mention = cids[0], cids[1], cids[2]
        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        if event.query.user_id in auth:
            current_page_number=0
            simp = button(current_page_number, CMD_HELP)
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            await event.edit(
                f"🔰 **{ram_mention}**\n\n __No.of Plugins__ : `{len(CMD_HELP)}` \n __Commands__ : `{len(apn)}`\n__Page__ : 1/{veriler[0]}",
                buttons=simp[1],
                link_preview=False,
            )
        else:
            reply_pop_up_alert = "Make you own © RAM-UBOT ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        cids = await client_id(event, event.query.user_id)
        ramtod, RAM_USER, ram_mention = cids[0], cids[1], cids[2]
        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        if event.query.user_id in auth:
            veriler = custom.Button.inline(f"{emoji} Re-Open Menu {emoji}", data="reopen")
            await event.edit(f"**⚜️ RAM-UBOT Menu closed⚜️**\n\n**Bot Of :**  {ram_mention}\n\n        [©️ RAM-UBOT ™️]({chnl_link})", buttons=veriler, link_preview=False)
        else:
            reply_pop_up_alert = "Make Your own © RAM-UBOT ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
   

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        cids = await client_id(event, event.query.user_id)
        ramtod, RAM_USER, ram_mention = cids[0], cids[1], cids[2]
        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id in auth:
            await event.edit(
                f"🔰 **{ram_mention}**\n\n __No.of Plugins__ : `{len(CMD_HELP)}`\n __Commands__ : `{len(apn)}`\n __Page__ : {page + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer(
                "Make your own © RAM-UBOT ™",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)"))
    )
    async def Information(event):
        cids = await client_id(event, event.query.user_id)
        ramtod, RAM_USER, ram_mention = cids[0], cids[1], cids[2]
        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline(
                    "⚡ " + cmd[0] + " ⚡", data=f"commands[{commands}[{page}]]({cmd[0]})"
                )
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer(
                "No Description is written for this plugin", cache_time=0, alert=True
            )

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"{emoji} Main Menu {emoji}", data=f"page({page})")])
        if event.query.user_id in auth:
            await event.edit(
                f"**📗 File :**  `{commands}`\n**🔢 Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer(
                "Make your own © RAM-UBOT ™",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)"))
    )
    async def commands(event):
        cids = await client_id(event, event.query.user_id)
        ramtod, RAM_USER, ram_mention = cids[0], cids[1], cids[2]
        auth = await clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5)
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**📗 File :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**ℹ️ Info :**  {CMD_HELP_BOT[cmd]['info']['info']}\n"
        sextraa = CMD_HELP_BOT[cmd]["extra"]
        if sextraa:
            a = sorted(sextraa.keys())
            for b in a:
                c = b
                d = sextraa[c]["content"]
                result += f"**{c} :**  `{d}`\n"
        result += "\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']}`\n"
        else:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**💬 Explanation :**  `{command['usage']}`\n\n"
        else:
            result += f"**💬 Explanation :**  `{command['usage']}`\n"
            result += f"**⌨️ For Example :**  `{HANDLER[:1]}{command['example']}`\n\n"
        if event.query.user_id in auth:
            await event.edit(
                result,
                buttons=[
                    custom.Button.inline(f"{emoji} Return {emoji}", data=f"Information[{page}]({cmd})")
                ],
                link_preview=False,
            )
        else:
            return await event.answer(
                "Make your own © RAM-UBOT ™",
                cache_time=0,
                alert=True,
            )


# iraa
