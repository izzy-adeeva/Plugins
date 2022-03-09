import asyncio
import io
import math
import os
import random
import textwrap
import urllib.request

from os import remove
from PIL import Image, ImageDraw, ImageFont
from telethon import events
from telethon.errors import PackShortNameOccupiedError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeSticker, InputStickerSetID, MessageMediaPhoto, InputMessagesFilterDocument
from telethon.utils import get_input_document

from ramext.sql.gvar_sql import addgvar, gvarstat, delgvar
from . import *

KANGING_STR = [
    "simsalabim, jadi apa.. prok prok prok..",
    "dua tiga anak kalong, stiker ini saya colong",
    "pinjem bentar, tar dibalikin..."
]

ramubot = gvarstat("STICKER_PACKNAME")



@ram_cmd(pattern="kang(?:\s|$)([\s\S]*)")
async def kang(event):
    user = await event.client.get_me()
    karin, RAM_USER, ram_mention = await client_id(event)
    izzy = f"@{user.username}" if user.username else user.first_name
    izzy_ = user.username if user.username else karin
    message = await event.get_reply_message()
    queen = gvarstat("STICKER_PACKNAME")
    photo = None
    emojibypass = False
    is_anim = False
    is_vid = False
    emoji = None
    if message and message.media:
        if message.photo:
            zyy = await eor(event, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await event.client.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            zyy = await eor(event, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await event.client.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            zyy = await eor(event, f"`{random.choice(KANGING_STR)}`")
            await event.client.download_file(message.media.document, "AnimatedSticker.tgs")

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            emojibypass = True
            is_anim = True
            photo = 1
        elif "video" in message.media.document.mime_type.split("/"):
            if message.media.document.mime_type == "video/webm":
                zyy = await eor(event, f"`{random.choice(KANGING_STR)}`")
                VS = await args.client.download_media(message.media.document, "VideoSticker.webm")
                attributes = message.media.document.attributes
                for attribute in attributes:
                    if isinstance(attribute, DocumentAttributeSticker):
                        emoji = attribute.alt
                        emojibypass = True
            elif message.media.document.mime_type == "video/mp4":
                zyy = await eor(event, "bismillah, video... **[ Converting ]**")
                VS = await VSticker(event, message)
                await eor(zyy, f"`{random.choice(KANGING_STR)}`")
            is_vid = True
            photo = 1
        else:
            await eod(event, "`File tidak disupport!`")
            return
    else:
        await eod(event, "`Gagal mengambil stiker...`")
        return

    if photo:
        splat = event.text.split()
        if not emojibypass:
            emoji = "😎"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                pack = int(splat[1])
            else:
                emoji = splat[1]

        packname = f"Ram-ubot_{izzy_}_{pack}"
        packnick = (
            f"{queen} Vol.{pack}"
            if queen
            else f"{izzy}'s RAM-UBOT Vol.{pack}"
        )
        cmd = "/newpack"
        file = io.BytesIO()

        if not is_anim and not is_vid:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        elif is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"
        elif is_vid:
            packname += "_vid"
            packnick += " (Video)"
            cmd = "/newvideo"

        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")

        if (
            "  Pengguna <strong>RAM-UBOT</strong> Membuat <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with event.client.conversation("@Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while ("50" in x.text) or ("120" in x.text):
                    pack += 1
                    packname = f"ram-ubot{izzy_}_{pack}"
                    packnick = (
                        f"{queen} Vol.{pack}"
                        if queen
                        else f"{izzy}'s RAM-UBOT Vol.{pack}"
                    )
                    cmd = "/newpack"

                    if is_anim:
                        packname += "_anim"
                        packnick += " (Animated)"
                        cmd = "/newanimated"
                    elif is_vid:
                        packname += "_vid"
                        packnick += " (Video)"
                        cmd = "/newvideo"
                    await zyy.edit(f"`Switching to Pack {str(pack)} due to insufficient space`")
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Invalid set selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        elif is_vid:
                            await conv.send_file("VideoSticker.webm")
                            remove("VideoSticker.webm")
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await zyy.edit(f"**Menambahkan stiker di pack yang lain !**\nPack stiker baru dibuat!\nLink [here](t.me/addstickers/{packname})")
                        return
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                elif is_vid:
                    await conv.send_file("VideoSticker.webm")
                    remove("VideoSticker.webm")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "File tidak didukung." in rsp.text:
                    return await zyy.edit("`gagal menambahkan stiker, chat` @Stickers `dan tambahkan secara manual.`")
                await conv.send_message(emoji)
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
        else:
            await zyy.edit("`Membuat Pack baru....`")
            async with event.client.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                if is_vid:
                    await conv.send_file("VideoSticker.webm")
                    remove("VideoSticker.webm")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "File tidak didukung." in rsp.text:
                    return await zyy.edit("`gagal menambahkan stiker, chat` @Stickers `dan tambahkan secara manual`")
                await conv.send_message(emoji)
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)

        await eod(zyy, f"** Stiker berhasil di ambil [kanged](t.me/addstickers/{packname}) berhasil ditambahkan ke pack **")
        await tbot.send_message(Config.LOGGER_ID,
                                "#KANG #STICKER \n\n**Stiker telah ditambahkan. Click link dibawah!**",
                                buttons=[[Button.url("Pack Stiker", f"t.me/addstickers/{packname}")]],
                            )


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


@ram_cmd(pattern="stkrinfo$")
async def get_pack_info(event):
    if not event.is_reply:
        await eod(event, "`Balas ke stiker!!!`")
        return
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await eod(event, "`Balas ke stiker untuk mendapatkan info`")
        return
    try:
        stickerset_attr = rep_msg.document.attributes[1]
        zyy = await eor(event, "`Mengambil data, mohon memnunggu..`")
    except BaseException:
        await eod(event, "`Stiker tidak ditemukan, harap balas pesan ke stiker.`")
        return

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        await zyy.edit("`Stiker tidak ditemukan, harap balas pesan ke stiker.`")
        return

    get_stickerset = await event.client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    OUTPUT = (
        f"🔹 **Sticker Title :** `{get_stickerset.set.title}\n`"
        f"🔸 **Sticker Short Name :** `{get_stickerset.set.short_name}`\n"
        f"🔹 **Official :** `{get_stickerset.set.official}`\n"
        f"🔸 **Archived :** `{get_stickerset.set.archived}`\n"
        f"🔹 **Stickers In Pack :** `{len(get_stickerset.packs)}`\n"
        f"🔸 **Emojis In Pack :**\n{' '.join(pack_emojis)}"
    )

    await zyy.edit(OUTPUT)


@ram_cmd(pattern="delst(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        await eod(event, "`Balas ke pesan stiker.`")
        return
    reply_message = await event.get_reply_message()
    chat = "@Stickers"
    reply_message.sender
    zyy = await eor(event, "Menghapus stiker...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=429000)
            )
            await conv.send_message("/delsticker")
            await conv.get_response()
            await asyncio.sleep(1)
            await event.client.forward_messages(chat, reply_message)
            response = await conv.get_response()
        except YouBlockedUserError:
            await zyy.edit("Mohon unblock @Stickers dan coba lagi")
            return
        await zyy.edit(response.text)


@ram_cmd(pattern="editst(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        await eod(event, "`Blas ke pesan stiker.`")
        return
    reply_message = await event.get_reply_message()
    ram_ = event.pattern_match.group(1)
    chat = "@Stickers"
    zyy = await eor(event, "Menganti emoji stiker...`")
    if ram_ == "":
        await zyy.edit("**Error, terjadi kesalahan**")
    else:
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=429000)
                )
                await conv.send_message(f"/editsticker")
                await conv.get_response()
                await asyncio.sleep(2)
                await event.client.forward_messages(chat, reply_message)
                await conv.get_response()
                await asyncio.sleep(2)
                await conv.send_message(f"{ram_}")
                response = await conv.get_response()
            except YouBlockedUserError:
                await zyy.edit("Mohon unblock @Stickers dan coba lagi")
                return
            await zyy.edit(f"{response.text}")


@ram_cmd(pattern="pkang(?:\s|$)([\s\S]*)")
async def _(event):
    ram_ = await eor(event, "`Menyiapkan Pack...`")
    rply = await event.get_reply_message()
    karin, RAM_USER, ram_mention = await client_id(event)
    zyy = event.text[7:]
    bot_ = Config.BOT_USERNAME
    bot_un = bot_.replace("@", "")
    user = await event.client.get_me()
    izzy = f"@{user.username}" if user.username else user.first_name
    izzy_ = user.username if user.username else karin
    if not rply:
        return await eod(ram_, "`Balas pesan stiker untuk mengambil Pack.`")
    if zyy == "":
        pname = f"{izzy}'s Ram Pack"
    else:
        pname = zyy
    if rply and rply.media and rply.media.document.mime_type == "image/webp":
        ram_id = rply.media.document.attributes[1].stickerset.id
        ram_hash = rply.media.document.attributes[1].stickerset.access_hash
        got_stcr = await event.client(
            functions.messages.GetStickerSetRequest(
                stickerset=types.InputStickerSetID(id=ram_id, access_hash=ram_hash)
            )
        )
        stcrs = []
        for sti in got_stcr.documents:
            inp = get_input_document(sti)
            stcrs.append(
                types.InputStickerSetItem(
                    document=inp,
                    emoji=(sti.attributes[1]).alt,
                )
            )
        x = gvarstat("PKANG")
        if x is None:
            y = addgvar("PKANG", "0")
            pack = int(y) + 1
        else:
            pack = int(x) + 1
        await ram_.edit("`Mengambil Pack...`")
        try:
            create_st = await tbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=karin,
                    title=pname,
                    short_name=f"ram_{izzy_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", str(pack))
        except PackShortNameOccupiedError:
            await asyncio.sleep(1)
            await ram_.edit("`Nama Pack telah ada... membuat pack stiker baru`")
            pack = int(pack) + 1
            create_st = await tbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=karin,
                    title=pname,
                    short_name=f"ram_{izzy_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", str(pack))
        await eod(ram_, f"** Pack stiker berhasil diambil [kanged](t.me/addstickers/{create_st.set.short_name}) **")
        await tbot.send_message(Config.LOGGER_ID,
                                "#PKANG #STICKER \n\n**stiker pack berhasil diambil. Link...!**",
                                buttons=[[Button.url("Pack Stiker", f"t.me/addstickers/{create_st.set.short_name}")]],
                            )
    else:
        await ram_.edit("File tidak disupport. balas ke pesan stiker.")


@ram_cmd(pattern="text(?:\s|$)([\s\S]*)")
async def sticklet(event):
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)

    sticktext = event.pattern_match.group(1)
    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = "\n".join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = await get_font_file(event.client, "@Ramfonts")

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2, (512 - height) / 2), sticktext, font=font, fill=(R, G, B)
    )

    image_stream = io.BytesIO()
    image_stream.name = "RAM.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)


    await event.client.send_message(
        event.chat_id,
        "{}".format(sticktext),
        file=image_stream,
        reply_to=event.message.reply_to_msg_id,
    )
    try:
        os.remove(FONT_FILE)
    except:
        pass


async def get_font_file(client, channel_id):
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
    )
    font_file_message = random.choice(font_file_message_s)

    return await client.download_media(font_file_message)


@ram_cmd(pattern="waifu(?:\s|$)([\s\S]*)")
async def waifu(event):
    text = event.pattern_match.group(1)
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            await eod(event, "Give some text... **PRO !!**")
            return
    animus = [1, 3, 7, 9, 13, 22, 34, 35, 36, 37, 43, 44, 45, 52, 53, 55]
    sticcers = await event.client.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    await sticcers[0].click(
        event.chat_id,
        reply_to=event.reply_to_msg_id,
        silent=True if event.is_reply else False,
        hide_via=True,
    )
    await event.delete()

CmdHelp("stickers").add_command(
  "kang", "<emoji> <number>", "menambahkan stiker ke pack. emoji default adalah 😎. \n  ✓(1 pack = 120 non-animated stickers)\n  ✓(1 pack = 50 animated stickers)"
).add_command(
  "stkrinfo", "<balas ke stiker>", "Mandapatkan info dari stiker pack"
).add_command(
  "delst", "<balas ke stiker>", "menghapus stiker dari pack."
).add_command(
  "editst", "<balas ke stiker> <emoji baru>", "mengganti emoji stiker."
).add_command(
  "text", "<kata-kata>", "membuat kata kata dalam bentuk stiker."
).add_command(
  "waifu", "<kata-kata>", "membuat anime mengetik pesan anda."
).add_command(
  "pkang", "<balas ke stiker> <nama pack>", "mengambil pack stiker, kostumisasi nama pack setelah command.", "pkang Stiker pack saya"
).add_info(
  "Everything about Sticker."
).add_warning(
  "✅ Harmless Module."
).add()
