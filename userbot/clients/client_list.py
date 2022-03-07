import telethon.utils
from telethon.tl.functions.users import GetFullUserRequest

from userbot.sql.gvar_sql import gvarstat


async def clients_list(Config, TOD, TOD2, TOD3, TOD4, TOD5):
    user_ids = []
    if gvarstat("SUDO_USERS"):
        a = gvarstat("SUDO_USERS").split(" ")
        for b in a:
            c = int(b)
            user_ids.append(c)
    main_id = await TOD.get_me()
    user_ids.append(main_id.id)

    try:
        if TOD2 is not None:
            id2 = await TOD2.get_me()
            user_ids.append(id2.id)
    except:
        pass

    try:
        if TOD3 is not None:
            id3 = await TOD3.get_me()
            user_ids.append(id3.id)
    except:
        pass

    try:
        if TOD4 is not None:
            id4 = await TOD4.get_me()
            user_ids.append(id4.id)
    except:
        pass

    try:
        if TOD5 is not None:
            id5 = await TOD5.get_me()
            user_ids.append(id5.id)
    except:
        pass

    return user_ids


async def client_id(event, botid=None):
    if botid is not None:
        uid = await event.client(GetFullUserRequest(botid))
        rampedo = uid.user.id
        RAM_USER = uid.user.first_name
        ram_mention = f"[{RAM_USER}](tg://user?id={rampedo})"
    else:
        client = await event.client.get_me()
        uid = telethon.utils.get_peer_id(client)
        rampedo = uid
        RAM_USER = client.first_name
        ram_mention = f"[{RAM_USER}](tg://user?id={rampedo})"
    return rampedo, RAM_USER, ram_mention
