import asyncio
import os
import re
import sys

from telethon import TelegramClient
from ramext.sql.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)

import logging

logging.basicConfig(
    format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)


package_patern = re.compile(r"([\w-]+)(?:=|<|>|!)")
github_patern = re.compile(r"(?:https?)?(?:www.)?(?:github.com/)?([\w\-.]+/[\w\-.]+)/?")
github_raw_pattern = re.compile(
    r"(?:https?)?(?:raw.)?(?:githubusercontent.com/)?([\w\-.]+/[\w\-.]+)/?"
)
trees_pattern = "https://api.github.com/repos/{}/git/trees/master"
raw_pattern = "https://raw.githubusercontent.com/{}/master/{}"

LOGS = logging.getLogger(__name__)


async def restart_script(client: TelegramClient, zzy):
    """Restart the current script."""
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [zzy.chat_id, zzy.id])
    except Exception as e:
        LOGS.error(e)
    executable = sys.executable.replace(" ", "\\ ")
    args = [executable, "-m", "ramext"]
    os.execle(executable, *args, os.environ)
    os._exit(143)


