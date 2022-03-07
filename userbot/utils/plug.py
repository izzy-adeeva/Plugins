import importlib
import logging
import os
import sys
from pathlib import Path

from userbot import *
from userbot.clients import *
from userbot.config import *
from userbot.helpers import *
from userbot.utils import *

# ENV
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from userbot.config import Config
else:
    if os.path.exists("Config.py"):
        from Config import Development as Config


# load plugins
def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import userbot.utils

        path = Path(f"userbot/plugins/{shortname}.py")
        name = "userbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("RamBot - Successfully imported " + shortname)
    else:
        import userbot.utils

        path = Path(f"userbot/plugins/{shortname}.py")
        name = "userbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = TOD
        mod.ramm = TOD
        mod.TOD2 = TOD2
        mod.TOD3 = TOD3
        mod.TOD4 = TOD4
        mod.TOD5 = TOD5
        mod.TOD = TOD
        mod.RamBot = RamBot
        mod.tbot = RamBot
        mod.tgbot = bot.tgbot
        mod.command = command
        mod.CmdHelp = CmdHelp
        mod.client_id = client_id
        mod.logger = logging.getLogger(shortname)
        # support for uniborg
        sys.modules["uniborg.util"] = userbot.utils
        mod.Config = Config
        mod.borg = bot
        mod.userbot = bot
        mod.edit_or_reply = edit_or_reply
        mod.eor = edit_or_reply
        mod.delete_hell = delete_hell
        mod.eod = delete_hell
        mod.Var = Config
        mod.admin_cmd = admin_cmd
        mod.ram_cmd = ram_cmd
        mod.sudo_cmd = sudo_cmd
        # support for other userbots
        sys.modules["userbot.utils"] = userbot.utils
        sys.modules["userbot"] = userbot
        # support for paperplaneextended
        sys.modules["userbot.events"] = userbot
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["userbot.plugins." + shortname] = mod
        LOGS.info("⚡ RAM-UBOT Extended ⚡ - Successfully Imported " + shortname)


# remove plugins
def remove_plugin(shortname):
    try:
        try:
            for i in LOAD_PLUG[shortname]:
                bot.remove_event_handler(i)
            del LOAD_PLUG[shortname]

        except BaseException:
            name = f"userbot.plugins.{shortname}"

            for i in reversed(range(len(bot._event_builders))):
                ev, cb = bot._event_builders[i]
                if cb.__module__ == name:
                    del bot._event_builders[i]
    except BaseException:
        raise ValueError


# userbot
