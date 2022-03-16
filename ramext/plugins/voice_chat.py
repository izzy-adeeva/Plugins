from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.phone import CreateGroupCallRequest, DiscardGroupCallRequest, GetGroupCallRequest, InviteToGroupCallRequest
from . import *
async def getvc(event):
    chat_ = await event.client(GetFullChannelRequest(event.chat_id))
    _chat = await event.client(GetGroupCallRequest(chat_.full_chat.call))
    return _chat.call

def all_users(a, b):
    for c in range(0, len(a), b):
        yield a[c : c + b]


@ram_cmd(pattern="startvc$")
async def _(event):
    try:
        await event.client(CreateGroupCallRequest(event.chat_id))
        await eor(event, "**Memulai Voice Chat Group**")
    except Exception as e:
        await eod(event, f"`{str(e)}`")

@ram_cmd(pattern="endvc$")
async def _(event):
    try:
        await event.client(DiscardGroupCallRequest(await getvc(event)))
        await eor(event, "**Menghentikan voice chat group!**")
    except Exception as e:
        await eod(event, f"`{str(e)}`")

@ram_cmd(pattern="vcinvite$")
async def _(event):
    zzy = await eor(event, "` Mengundang ke voice chat....`")
    users = []
    i = 0
    async for j in event.client.iter_participants(event.chat_id):
        if not j.bot:
            users.append(j.id)
    hel_ = list(all_users(users, 6))
    for k in hel_:
        try:
            await event.client(InviteToGroupCallRequest(call=await getvc(event), users=k))
            i += 6
        except BaseException:
            pass
    await zzy.edit(f"**Mengundang {i} ke voice chat**")


CmdHelp("voice_chat").add_command(
  "startvc", None, "memulai voice chat."
).add_command(
  "endvc", None, "menghentikan voice chat."
).add_command(
  "vcinvite", None, "mengundang user ke voice chat."
).add_info(
  "Voice Chat Tools."
).add_warning(
  "✅ Harmless Module."
).add()
