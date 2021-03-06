from . import *


@ram_cmd(pattern="gdl$")
async def g_download(event):
    zzy = await eor(event, "Accessing gdrive...")
    drive_link = event.text[5:]
    await zzy.edit(f"**Drive Link :** `{drive_link}`")
    file_id = await get_id(drive_link)
    await zzy.edit("Downloading requested file from G-Drive...")
    file_name = await download_file_from_google_drive(file_id)
    await zzy.edit(f"**File Downloaded !!**\n\n__Name :__ `{str(file_name)}`")

CmdHelp("gdrive").add_command(
  "gdl", "<gdrive link>", f"Downloads the file from gdirve to ramubot's local storage. Use {ii}upload <path> to upload it."
).add_info(
  "Google Drive Downloader"
).add_warning(
  "✅ Harmless Module."
).add()
