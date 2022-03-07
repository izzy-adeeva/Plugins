import inspect
import re

from pathlib import Path
from telethon import events

from .session import RAM2, RAM3, RAM4, RAM5
from ramext import CMD_LIST, LOAD_PLUG, bot
from ramext.config import Config
from ramext.sql.gvar_sql import gvarstat


def ram_cmd(
    pattern: str = None,
    allow_sudo: bool = True,
    disable_edited: bool = False,
    forword=False,
    command: str = None,
    **args,
):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")

    if "disable_edited" in args:
        del args["disable_edited"]

    args["blacklist_chats"] = True
    black_list_chats = list(Config.BL_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats
    sudo_user = []
    if gvarstat("SUDO_USERS"):
        a = gvarstat("SUDO_USERS").split(" ")
        for c in a:
            a = int(c)
            sudo_user.append(a)

    if pattern is not None:
        global ram_reg
        global ram_sudo
        if (
            pattern.startswith(r"\#")
            or not pattern.startswith(r"\#")
            and pattern.startswith(r"^")
        ):
            ram_reg = ram_sudo = re.compile(pattern)
        else:
            ram_ = "\\" + Config.HANDLER
            sudo_ = "\\" + Config.SUDO_HANDLER
            ram_reg = re.compile(ram_ + pattern)
            ram_sudo = re.compile(sudo_ + pattern)
            if command is not None:
                cmd1 = ram_ + command
                cmd2 = sudo_ + command
            else:
                cmd1 = (
                    (ram_ + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
                cmd2 = (
                    (sudo_ + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd1)
            except BaseException:
                CMD_LIST.update({file_test: [cmd1]})


    def decorator(func):
        if not disable_edited:
            bot.add_event_handler(func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg))
        bot.add_event_handler(func, events.NewMessage(**args, outgoing=True, pattern=ram_reg))
        if allow_sudo:
            if not disable_edited:
                bot.add_event_handler(func, events.MessageEdited(**args, from_users=sudo_user, pattern=ram_sudo))
            bot.add_event_handler(func, events.NewMessage(**args, from_users=sudo_user, pattern=ram_sudo))
        if RAM2:
            if not disable_edited:
                RAM2.add_event_handler(func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg))
            RAM2.add_event_handler(func, events.NewMessage(**args, outgoing=True, pattern=ram_reg))
        if RAM3:
            if not disable_edited:
                RAM3.add_event_handler(func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg))
            RAM3.add_event_handler(func, events.NewMessage(**args, outgoing=True, pattern=ram_reg))
        if RAM4:
            if not disable_edited:
                RAM4.add_event_handler(func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg))
            RAM4.add_event_handler(func, events.NewMessage(**args, outgoing=True, pattern=ram_reg))
        if RAM5:
            if not disable_edited:
                RAM5.add_event_handler(func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg))
            RAM5.add_event_handler(func, events.NewMessage(**args, outgoing=True, pattern=ram_reg))
        try:
            LOAD_PLUG[file_test].append(func)
        except Exception:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator


def ram_handler(
    **args,
):
    def decorator(func):
        bot.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if RAM2:
            RAM2.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if RAM3:
            RAM3.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if RAM4:
            RAM4.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if RAM5:
            RAM5.add_event_handler(func, events.NewMessage(**args, incoming=True))
        return func

    return decorator
