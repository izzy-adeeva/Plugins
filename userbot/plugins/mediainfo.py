import os

from . import *


@ram_cmd(pattern="mediainfo$")
async def mediainfo(event):
    HELL_MEDIA = None
    reply = await event.get_reply_message()
    logo = "https://telegra.ph/file/2c546060b20dfd7c1ff2d.jpg"
    if not reply:
        return await eod(event, "Reply to a media to fetch info...")
    if not reply.media:
        return await eod(event, "Reply to a media file to fetch info...")
    TOD = await eor(event, "`Fetching media info...`")
    HELL_MEDIA = reply.file.mime_type
    if not HELL_MEDIA:
        return await TOD.edit("Reply to a media file to fetch info...")
    elif HELL_MEDIA.startswith(("text")):
        return await TOD.edit("Reply to a media file to fetch info ...")
    hel_ = await mediadata(reply)
    file_path = await reply.download_media(Config.TMP_DOWNLOAD_DIRECTORY)
    out, err, ret, pid = await runcmd(f"mediainfo '{file_path}'")
    if not out:
        out = "Unknown Format !!"
    paster = f"""
<TOD2>📃 MEDIA INFO 📃</TOD2>
<code>
{hel_}
</code>
<TOD2>🧐 MORE DETAILS 🧐</TOD2>
<code>
{out} 
</code>
<img src='{logo}'/>"""
    paste = await telegraph_paste(f"{HELL_MEDIA}", paster)
    await TOD.edit(
        f"📌 Fetched  Media Info Successfully !! \n\n**Check Here :** [{HELL_MEDIA}]({paste})"
    )
    os.remove(file_path)


CmdHelp("mediainfo").add_command(
    "mediainfo",
    "<reply to a media>",
    "Fetches the detailed information of replied media.",
).add_info("Everything About That Media.").add_warning("✅ Harmless Module.").add()
