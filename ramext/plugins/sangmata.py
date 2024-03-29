from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest

from . import *


@ram_cmd(pattern="sa(?:\s|$)([\s\S]*)")
async def _(ramevent):
    if not ramevent.reply_to_msg_id:
       await eod(ramevent, "`Please reply to a user to get his history`")
       return
    reply_message = await ramevent.get_reply_message() 
    chat = "Sangmatainfo_bot"
    victim = reply_message.sender.id
    if reply_message.sender.bot:
       await eod(ramevent, "Need actual users. Not Bots")
       return
    zzy = await eor(ramevent, "Checking...")
    async with ramevent.client.conversation(chat) as conv:
          try:     
              first = await conv.send_message(f"/search_id {victim}")
              response1 = await conv.get_response()
              response2 = await conv.get_response() 
              response3 = await conv.get_response()
          except YouBlockedUserError: 
              await eod(ramevent, "Please unblock @Sangmatainfo_bot")
              return
          if response1.text.startswith("Name History"):
              await zzy.edit(response1.text)
              await ramevent.client.delete_messages(conv.chat_id, [first.id, response1.id, response2.id, response3.id])
          elif response2.text.startswith("Name History"):
              await zzy.edit(response2.text)
              await ramevent.client.delete_messages(conv.chat_id, [first.id, response1.id, response2.id, response3.id])
          elif response3.text.startswith("Name History"):
              await zzy.edit(response3.text)
              await ramevent.client.delete_messages(conv.chat_id, [first.id, response1.id, response2.id, response3.id])
          else: 
              await zzy.edit("No Records Found !")


@ram_cmd(pattern="sg(?:\s|$)([\s\S]*)")
async def _(ramevent):
    if not ramevent.reply_to_msg_id:
       await eod(ramevent, "`Please Reply To A User To Get This Module Work`")
       return
    reply_message = await ramevent.get_reply_message() 
    chat = "Sangmatainfo_bot"
    victim = reply_message.sender.id
    if reply_message.sender.bot:
       await eod(ramevent, "Need actual users. Not Bots")
       return
    zzy = await eor(ramevent, "Checking...")
    async with ramevent.client.conversation(chat) as conv:
          try:     
              first = await conv.send_message(f"/search_id {victim}")
              response1 = await conv.get_response() 
              response2 = await conv.get_response()
              response3 = await conv.get_response()
          except YouBlockedUserError: 
              await eod(ramevent, "Please unblock @Sangmatainfo_bot")
              return
          if response1.text.startswith("Username History"):
              await zzy.edit(response1.text)
              await ramevent.client.delete_messages(conv.chat_id, [first.id, response1.id, response2.id, response3.id])
          elif response2.text.startswith("Username History"):
              await zzy.edit(response2.text)
              await ramevent.client.delete_messages(conv.chat_id, [first.id, response1.id, response2.id, response3.id])
          elif response3.text.startswith("Username History"):
              await zzy.edit(response3.text)
              await ramevent.client.delete_messages(conv.chat_id, [first.id, response1.id, response2.id, response3.id])
          else: 
              await zzy.edit("No Records Found !")


CmdHelp("sa").add_command(
  "history", "<reply to a user>", "Fetches the name history of replied user."
).add_command(
  "sg", "<reply to user>", "Fetches the Username History of replied users."
).add_info(
  "Telegram Name History"
).add_warning(
  "✅ Harmless Module."
).add()
