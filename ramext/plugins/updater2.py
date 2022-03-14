import asyncio
from email.mime import base
import os
import sys
import base64
from asyncio.exceptions import CancelledError

import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError


from ramext.config import Config
from . import *
from ramext.utils.extras import edit_delete, edit_or_reply
from ramext.sql.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ramext.sql.gvar_sql import delgvar

import logging

logging.basicConfig(
    format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

LOGS = logging.getLogger(__name__)
# -- Constants -- #

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = "master"

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "Heroku app tidak ditemukan"
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting heroku aplication"
IS_SELECTED_DIFFERENT_BRANCH = (
    "Branch kostumisasi {branch_name} "
    "digunakan:\n"
    "Update tidak bisa dilanjutkan."
    "Silahkan gunakan branch official untuk melanjutkan."
)


# -- Constants End -- #

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("`Changelog terlalu banyak, silahkan liat file output.`")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communisade()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    zzy = await event.edit(
        "`Berhasil diupdate!\n" "Me-restart bot... Harap bersabar!`"
    )
    await event.client.reload(zzy)

async def restart_script(client: TelegramClient, zzy):
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

async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is None:
        return await event.edit("`Masukan vars`  **HEROKU_API_KEY**  `...`")
    heroku = heroku3.from_key(HEROKU_API_KEY)
    heroku_app = None
    heroku_aplications = heroku.apps()
    if HEROKU_APP_NAME is None:
        await event.edit(
            "`Masukan vars` **HEROKU_APP_NAME** "
            " untuk dapat melanjutkan proses deploy...`"
        )
        repo.__del__()
        return
    for app in heroku_aplications:
        if app.name == HEROKU_APP_NAME:
            heroku_app = app
            break
    if heroku_app is None:
        await event.edit(
            f"{txt}\n" "`Heroku app/key tidak valid.`"
        )
        return repo.__del__()
    zzy = await event.edit(
        "`RAM-UBOT sedang di deploy, proses akan berlangsung 4-5 menit.`"
    )
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
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace(
        "https://", "https://api:" + HEROKU_API_KEY + "@"
    )
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**Error log:**\n`{error}`")
        return repo.__del__()
    build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build_status.status == "failed":
        return await edit_delete(
            event, "`Deploy GAGAL!\n" "silahkan check logs deploy...`"
        )
    try:
        remote.push("master:main", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**Error logs:**\n`{error}`")
        return repo.__del__()
    await event.edit("`Deploy GAGAL, mencoba ulang update`")
    delgvar("ipaddress")
    try:
        await event.client.disconnect()
        if HEROKU_APP is not None:
            HEROKU_APP.restart()
    except CancelledError:
        pass


@ram_cmd(pattern="update(| now)?$", ) 
async def upstream(event):
    "To check if the bot is up to date and update if specified"
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, "`Memeriksa pembaharuan, Tunggu sebentar....`")
    off_repo = "https://github.com/izzy-adeeva/Plugins"
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await edit_or_reply(
            event, "`Harap masukan vars yg dibutuhkan untuk update`"
        )
    try:
        txt = "`Update GAGAL"
        txt += "Logs`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} tidak ditemukan`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`GAGAL! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Direktori/folder {error} "
                "bukan git yang valid.\n"
                "silahkan coba untuk memperbaiki dengan update now "
                ".update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Anda menggunakan branch non-official ({ac_br}). "
            "Update tidak dapat dilanjutkan "
            "Branch kustom tidak dapat dukungan`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if changelog == "" and not force_update:
        await event.edit(
            "\n`RAM-UBOT`  **telah diperbaharui**  `dengan branch`  "
            f"**{UPSTREAM_REPO_BRANCH}** belum ada pembaharuan yang tersedia\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond(
            f"ketik`{ii}update deploy` untuk update"
        )

    if force_update:
        await event.edit(
            "`Update paksa, tunggu sebentar...`"
        )
    if conf == "now":
        await event.edit("`memproses update....`")
        await update(event, repo, ups_rem, ac_br)
    return


@ram_cmd(
    pattern="update deploy$",
)
async def upstream(event):
    event = await edit_or_reply(event, "`Pulling repo....`")
    off_repo = "https://github.com/hitokizzy/RAM-UBOT_EXTENDED"
    os.chdir("/bin")
    try:
        txt = "`Update GAGAL "
        txt += "logs`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directori {error} tidak ditemukan`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`GAGAL! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("`Proses Deploy RAM, harap bersabar....`")
    await deploy(event, repo, ups_rem, ac_br, txt)


    
CmdHelp("update").add_command(
  "update", None, "Memeriksa pembaharuan RAM-UBOT."
).add_command(
  "update now", None, "Soft-Update RAM-UBOT.."
).add_command(
  "update build", None, "Hard-Update Your RAM-UBOT.."
).add_info(
  "RAM-UBOT Updater."
).add_warning(
  "✅ Harmless Module."
).add()
