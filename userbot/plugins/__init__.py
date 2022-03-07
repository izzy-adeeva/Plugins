import datetime
import time

from telethon import version

from userbot import *
from userbot.clients import *
from userbot.config import Config
from userbot.helpers import *
from userbot.random_strings import *
from userbot.sql.gvar_sql import gvarstat
from userbot.utils import *
from userbot.version import __tod__

ram_logo = "./userbot/resources/pics/userbot_logo.jpg"
todd = "./userbot/resources/pics/todd.jpg"
njirk = "./userbot/resources/pics/rest.jpeg"
wahk = "./userbot/resources/pics/wahk.jpg"
cot = "./userbot/resources/pics/chup_madarchod.jpeg"
ii = Config.HANDLER
shl = Config.SUDO_HANDLER
ram_ver = __tod__
tel_ver = version.__version__


async def get_user_id(ids):
    if str(ids).isdigit():
        userid = int(ids)
    else:
        userid = (await bot.get_entity(ids)).id
    return userid


sudos = Config.SUDO_USERS
if sudos:
    is_sudo = "True"
else:
    is_sudo = "False"

abus = Config.ABUSE
if abus == "ON":
    abuse_m = "Enabled"
else:
    abuse_m = "Disabled"


my_channel = Config.MY_CHANNEL or "ramsupport"
my_group = Config.MY_GROUP or "ramsupport"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

chnl_link = "https://t.me/ramsupport"
hell_channel = f"[RAM_UBOT Extended]({chnl_link})"
grp_link = "https://t.me/ramsupport"
hell_grp = f"[RAM-UBOT Extended Group]({grp_link})"

WELCOME_FORMAT = """**Use these fomats in your welcome note to make them attractive.**
  {mention} :  To mention the user
  {title} : To get chat name in message
  {count} : To get group members
  {first} : To use user first name
  {last} : To use user last name
  {fullname} : To use user full name
  {userid} : To use userid
  {username} : To use user username
  {my_first} : To use my first name
  {my_fullname} : To use my full name
  {my_last} : To use my last name
  {my_mention} : To mention myself
  {my_username} : To use my username
"""
# will add more soon

# userbot
