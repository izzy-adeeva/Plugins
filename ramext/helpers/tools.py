import functools
import re

from telethon import events

from ramext import bot
from ramext.config import Config


# forward check
def forwards():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if event.fwd_from:
                await func(event)
            else:
                pass

        return wrapper

    return decorator



def iadmin():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            myid = await bot.get_me()
            myperm = await bot.get_permissions(event.chat_id, myid)
            if myperm.is_admin:
                await func(event)
            if myperm.is_creator:
                await func(event)
            else:
                await event.edit(
                    "I'm not admin."
                )

        return wrapper

    return decorator



def if_bot():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            reply_msg = await event.get_reply_message()
            reply_msg.sender
            if not reply_msg.sender.bot:
                await func(event)
            else:
                await event.edit("That's a Bot..")

        return wrapper

    return decorator


# set the pm limit
def pm_limit():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if event.is_group:
                await func(event)
            else:
                await event.edit("This Command Only Works In Groups...")

        return wrapper

    return decorator


# checks for groups
def no_grp():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if event.is_group:
                pass
            else:
                await func(event)

        return wrapper

    return decorator


# iraa
