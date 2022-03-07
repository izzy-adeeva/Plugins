import inspect
import re
from pathlib import Path

from telethon import events

from userbot import CMD_LIST, LOAD_PLUG, bot
from userbot.config import Config
from userbot.sql.gvar_sql import gvarstat

from .session import TOD2, TOD3, TOD4, TOD5


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
        global sudo_reg
        if (
            pattern.startswith(r"\#")
            or not pattern.startswith(r"\#")
            and pattern.startswith(r"^")
        ):
            ram_reg = sudo_reg = re.compile(pattern)
        else:
            ram_ = "\\" + Config.HANDLER
            sudo_ = "\\" + Config.SUDO_HANDLER
            ram_reg = re.compile(ram_ + pattern)
            sudo_reg = re.compile(sudo_ + pattern)
            if command is not None:
                cmd1 = ram_ + command
                cmd2 = sudo_ + command
            else:
                cmd1 = (
                    (ram_ + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
                cmd2 = (
                    (sudo_ + pattern)
                    .replace("$", "")
                    .replace("\\", "")
                    .replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd1)
            except BaseException:
                CMD_LIST.update({file_test: [cmd1]})

    def decorator(func):
        if not disable_edited:
            bot.add_event_handler(
                func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg)
            )
        bot.add_event_handler(
            func, events.NewMessage(**args, outgoing=True, pattern=ram_reg)
        )
        if allow_sudo:
            if not disable_edited:
                bot.add_event_handler(
                    func,
                    events.MessageEdited(
                        **args, from_users=sudo_user, pattern=sudo_reg
                    ),
                )
            bot.add_event_handler(
                func, events.NewMessage(**args, from_users=sudo_user, pattern=sudo_reg)
            )
        if TOD2:
            if not disable_edited:
                TOD2.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg)
                )
            TOD2.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=ram_reg)
            )
        if TOD3:
            if not disable_edited:
                TOD3.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg)
                )
            TOD3.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=ram_reg)
            )
        if TOD4:
            if not disable_edited:
                TOD4.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg)
                )
            TOD4.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=ram_reg)
            )
        if TOD5:
            if not disable_edited:
                TOD5.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=ram_reg)
                )
            TOD5.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=ram_reg)
            )
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
        if TOD2:
            TOD2.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if TOD3:
            TOD3.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if TOD4:
            TOD4.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if TOD5:
            TOD5.add_event_handler(func, events.NewMessage(**args, incoming=True))
        return func

    return decorator
