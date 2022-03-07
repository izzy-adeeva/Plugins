import datetime
import time

from ramext import *
from ramext.clients import *
from ramext.config import Config
from ramext.helpers import *
from ramext.utils import *
from ramext.random_strings import *
from ramext.version import version
from ramext.sql.gvar_sql import gvarstat
from telethon import version

ram_logo = "https://telegra.ph/file/e62dcb31e02594af0fab4.png"
anu = "./ramext/resources/pics/anu.jpg"
anu2 = "./ramext/resources/pics/anu2.jpeg"
anu3 = "./ramext/resources/pics/anu3.jpg"
anu4 = "./ramext/resources/pics/anu4.jpeg"
ii = Config.HANDLER
sdh = Config.SUDO_HANDLER
ram_version = version
telethon_ver = version.__version__

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
    abuse_m ="Disabled"


my_channel = Config.MY_CHANNEL or "ramsupport"
my_group = Config.MY_GROUP or "GeezSupport"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

chnl_link = "https://t.me/ramsupport"
ram_channel = f"[RAM-UBOT]({chnl_link})"
grp_link = "https://t.me/GeezSupport"
ram_grp = f"[GEEZ]({grp_link})"

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

# iraa
