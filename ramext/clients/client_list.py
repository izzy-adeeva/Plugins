import telethon.utils

from telethon.tl.functions.users import GetFullUserRequest

from .session import RAM, RAM2, RAM3, RAM4, RAM5
from ramext.sql.gvar_sql import gvarstat


async def clients_list(Config, RAM, RAM2, RAM3, RAM4, RAM5):
    user_ids = []
    if gvarstat("SUDO_USERS"):
        a = gvarstat("SUDO_USERS").split(" ")
        for b in a:
            c = int(b)
            user_ids.append(c)
    main_id = await RAM.get_me()
    user_ids.append(main_id.id)

    try:
        if RAM2 is not None:
            id2 = await RAM2.get_me()
            user_ids.append(id2.id)
    except:
        pass

    try:
        if RAM3 is not None:
            id3 = await RAM3.get_me()
            user_ids.append(id3.id)
    except:
        pass

    try:
        if RAM4 is not None:
            id4 = await RAM4.get_me()
            user_ids.append(id4.id)
    except:
        pass

    try:
        if RAM5 is not None:
            id5 = await RAM5.get_me()
            user_ids.append(id5.id)
    except:
        pass

    return user_ids


async def client_id(event, botid=None):
    if botid is not None:
        uid = await event.client(GetFullUserRequest(botid))
        vcs = uid.user.id
        RAM_USER = uid.user.first_name
        ram_mention = f"[{RAM_USER}](tg://user?id={vcs})"
    else:
        client = await event.client.get_me()
        uid = telethon.utils.get_peer_id(client)
        vcs = uid
        RAM_USER = client.first_name
        ram_mention = f"[{RAM_USER}](tg://user?id={vcs})"
    return vcs, RAM_USER, ram_mention
