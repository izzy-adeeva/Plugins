import json

import requests

from . import *

PLACE = TZ = os.environ.get("TZ", "Asia/Jakarta")

@ram_cmd(pattern="adzan$")
async def get_adzan(adzan):
    if not adzan.pattern_match.group(1):
        LOCATION = PLACE
        if not LOCATION:
            await adzan.edit("`Harap Menentukan Kota Atau Negara.`")
            return
    else:
        LOCATION = adzan.pattern_match.group(1)

   
    url = f"https://api.pray.zone/v2/times/today.json?city={LOCATION}"
    request = requests.get(url)
    if request.status_code == 500:
        return await adzan.edit(f"**Tidak Dapat Menemukan Kota** `{LOCATION}`")

    parsed = json.loads(request.text)

    city = parsed["results"]["location"]["city"]
    country = parsed["results"]["location"]["country"]
    timezone = parsed["results"]["location"]["timezone"]
    date = parsed["results"]["datetime"][0]["date"]["gregorian"]

    imsak = parsed["results"]["datetime"][0]["times"]["Imsak"]
    subuh = parsed["results"]["datetime"][0]["times"]["Fajr"]
    zuhur = parsed["results"]["datetime"][0]["times"]["Dhuhr"]
    ashar = parsed["results"]["datetime"][0]["times"]["Asr"]
    maghrib = parsed["results"]["datetime"][0]["times"]["Maghrib"]
    isya = parsed["results"]["datetime"][0]["times"]["Isha"]

    result = (
        f"**Jadwal Sholat**:\n"
        f"📅 `{date} | {timezone}`\n"
        f"🌏 `{city} | {country}`\n\n"
        f"**Imsak :** `{imsak}`\n"
        f"**Subuh :** `{subuh}`\n"
        f"**Zuhur :** `{zuhur}`\n"
        f"**Ashar :** `{ashar}`\n"
        f"**Maghrib :** `{maghrib}`\n"
        f"**Isya :** `{isya}`\n"
    )

    await adzan.edit(result)

    CmdHelp("adzan").add_command(
  'adzan', "Untuk ifo jadwal Sholat"
).add_info(
  "Jadwal Sholat"
).add_warning(
  "✅ Harmless Module."
).add()
