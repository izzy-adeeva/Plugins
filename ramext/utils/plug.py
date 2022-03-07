import asyncio
import datetime
import importlib
import inspect
import logging
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from time import gmtime, strftime

from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from ramext import *
from ramext.clients import *
from ramext.helpers import *
from ramext.config import *
from ramext.utils import *


# ENV
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from ramext.config import Config
else:
    if os.path.exists("Config.py"):
        from Config import Development as Config


# load plugins
def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import ramext.utils

        path = Path(f"ramext/plugins/{shortname}.py")
        name = "ramext.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("ramext - Successfully imported " + shortname)
    else:
        import ramext.utils

        path = Path(f"ramext/plugins/{shortname}.py")
        name = "ramext.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = RAM
        mod.H1 = RAM
        mod.RAM2 = RAM2
        mod.RAM3 = RAM3
        mod.RAM4 = RAM4
        mod.RAM5 = RAM5
        mod.RAM = RAM
        mod.ramext = ramext
        mod.tbot = ramext
        mod.tgbot = bot.tgbot
        mod.command = command
        mod.CmdHelp = CmdHelp
        mod.client_id = client_id
        mod.logger = logging.getLogger(shortname)
        # support for uniborg
        sys.modules["uniborg.util"] = ramext.utils
        mod.Config = Config
        mod.borg = bot
        mod.ramext = bot
        mod.edit_or_reply = edit_or_reply
        mod.eor = edit_or_reply
        mod.del_ram = del_ram
        mod.eod = del_ram
        mod.Var = Config
        mod.admin_cmd = admin_cmd
        mod.ram_cmd = ram_cmd
        mod.sudo_cmd = sudo_cmd
        # support for other userbots
        sys.modules["ramext.utils"] = ramext.utils
        sys.modules["ramext"] = ramext
        # support for paperplaneextended
        sys.modules["ramext.events"] = ramext
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["ramext.plugins." + shortname] = mod
        LOGS.info(">RAM-UBOT EXTENDED - Successfully Imported " + shortname)


# remove plugins
def remove_plugin(shortname):
    try:
        try:
            for i in LOAD_PLUG[shortname]:
                bot.remove_event_handler(i)
            del LOAD_PLUG[shortname]

        except BaseException:
            name = f"ramext.plugins.{shortname}"

            for i in reversed(range(len(bot._event_builders))):
                ev, cb = bot._event_builders[i]
                if cb.__module__ == name:
                    del bot._event_builders[i]
    except BaseException:
        raise ValueError

# iraa
