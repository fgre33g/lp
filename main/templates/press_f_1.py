from tools.messages import messages
from tools.requests import vk_info
import vk_api
from vk_api.longpoll import VkLongPoll
import time
import asyncio
import json

async def pressf(delay, peer_id, command):
    await asyncio.sleep(delay)
    if "!н ф 1" in command:
        msg_1 = f"""
        🌕🌕🌗🌑🌑🌑🌑🌑🌓
        🌕🌕🌗🌑🌑🌑🌑🌑🌕
        🌕🌕🌗🌑🌓🌕🌕🌕🌕
        🌕🌕🌗🌑🌓🌕🌕🌕🌕
        🌕🌕🌗🌑🌑🌑🌑🌓🌕
        🌕🌕🌗🌑🌑🌑🌑🌕🌕
        🌕🌕🌗🌑🌓🌕🌕🌕🌕
        🌕🌕🌗🌑🌓🌕🌕🌕🌕
        🌕🌕🌗🌑🌓🌕🌕🌕🌕

        """.replace('    ', '')

        msg_2 = f"""
        🌓🌕🌕🌗🌑🌑🌑🌑🌑
        🌕🌕🌕🌗🌑🌑🌑🌑🌑
        🌕🌕🌕🌗🌑🌓🌕🌕🌕
        🌕🌕🌕🌗🌑🌓🌕🌕🌕
        🌕🌕🌕🌗🌑🌑🌑🌑🌓
        🌕🌕🌕🌗🌑🌑🌑🌑🌕
        🌕🌕🌕🌗🌑🌓🌕🌕🌕
        🌕🌕🌕🌗🌑🌓🌕🌕🌕
        🌕🌕🌕🌗🌑🌓🌕🌕🌕

        """.replace('    ', '')

        msg_3 = f"""
        🌑🌓🌕🌕🌗🌑🌑🌑🌑
        🌑🌕🌕🌕🌗🌑🌑🌑🌑
        🌕🌕🌕🌕🌗🌑🌓🌕🌕
        🌕🌕🌕🌕🌗🌑🌓🌕🌕
        🌓🌕🌕🌕🌗🌑🌑🌑🌑
        🌕🌕🌕🌕🌗🌑🌑🌑🌑
        🌕🌕🌕🌕🌗🌑🌓🌕🌕
        🌕🌕🌕🌕🌗🌑🌓🌕🌕
        🌕🌕🌕🌕🌗🌑🌓🌕🌕

        """.replace('    ', '')

        msg_4 = f"""
        🌑🌑🌓🌕🌕🌗🌑🌑🌑
        🌑🌑🌕🌕🌕🌗🌑🌑🌑
        🌕🌕🌕🌕🌕🌗🌑🌓🌕
        🌕🌕🌕🌕🌕🌗🌑🌓🌕
        🌑🌓🌕🌕🌕🌗🌑🌑🌑
        🌑🌕🌕🌕🌕🌗🌑🌑🌑
        🌕🌕🌕🌕🌕🌗🌑🌓🌕
        🌕🌕🌕🌕🌕🌗🌑🌓🌕
        🌕🌕🌕🌕🌕🌗🌑🌓🌕

        """.replace('    ', '')

        msg_5 = f"""
        🌑🌑🌑🌓🌕🌕🌗🌑🌑
        🌑🌑🌑🌕🌕🌕🌗🌑🌑
        🌕🌕🌕🌕🌕🌕🌗🌑🌓
        🌕🌕🌕🌕🌕🌕🌗🌑🌓
        🌑🌑🌓🌕🌕🌕🌗🌑🌑
        🌑🌑🌕🌕🌕🌕🌗🌑🌑
        🌕🌕🌕🌕🌕🌕🌗🌑🌓
        🌕🌕🌕🌕🌕🌕🌗🌑🌓
        🌕🌕🌕🌕🌕🌕🌗🌑🌓

        """.replace('    ', '')

        msg_6 = f"""
        🌑🌑🌑🌑🌓🌕🌕🌗🌑
        🌑🌑🌑🌑🌕🌕🌕🌗🌑
        🌓🌕🌕🌕🌕🌕🌕🌗🌑
        🌓🌕🌕🌕🌕🌕🌕🌗🌑
        🌑🌑🌑🌓🌕🌕🌕🌗🌑
        🌑🌑🌑🌕🌕🌕🌕🌗🌑
        🌓🌕🌕🌕🌕🌕🌕🌗🌑
        🌓🌕🌕🌕🌕🌕🌕🌗🌑
        🌓🌕🌕🌕🌕🌕🌕🌗🌑

        """.replace('    ', '')

        msg_7 = f"""
        🌑🌑🌑🌑🌑🌓🌕🌕🌗
        🌑🌑🌑🌑🌑🌕🌕🌕🌗
        🌑🌓🌕🌕🌕🌕🌕🌕🌗
        🌑🌓🌕🌕🌕🌕🌕🌕🌗
        🌑🌑🌑🌑🌓🌕🌕🌕🌗
        🌑🌑🌑🌑🌕🌕🌕🌕🌗
        🌑🌓🌕🌕🌕🌕🌕🌕🌗
        🌑🌓🌕🌕🌕🌕🌕🌕🌗
        🌑🌓🌕🌕🌕🌕🌕🌕🌗

        """.replace('    ', '')

        msg_8 = f"""
        🌗🌑🌑🌑🌑🌑🌓🌕🌕
        🌗🌑🌑🌑🌑🌑🌕🌕🌕
        🌗🌑🌓🌕🌕🌕🌕🌕🌕
        🌗🌑🌓🌕🌕🌕🌕🌕🌕
        🌗🌑🌑🌑🌑🌓🌕🌕🌕
        🌗🌑🌑🌑🌑🌕🌕🌕🌕
        🌗🌑🌓🌕🌕🌕🌕🌕🌕
        🌗🌑🌓🌕🌕🌕🌕🌕🌕
        🌗🌑🌓🌕🌕🌕🌕🌕🌕

        """.replace('    ', '')

        msg_9 = f"""
        🌕🌗🌑🌑🌑🌑🌑🌓🌕
        🌕🌗🌑🌑🌑🌑🌑🌕🌕
        🌕🌗🌑🌓🌕🌕🌕🌕🌕
        🌕🌗🌑🌓🌕🌕🌕🌕🌕
        🌕🌗🌑🌑🌑🌑🌓🌕🌕
        🌕🌗🌑🌑🌑🌑🌕🌕🌕
        🌕🌗🌑🌓🌕🌕🌕🌕🌕
        🌕🌗🌑🌓🌕🌕🌕🌕🌕
        🌕🌗🌑🌓🌕🌕🌕🌕🌕

        """.replace('    ', '')

        messages.write_msg(peer_id, msg_1)
        msg_id = vk_info.info_msg_id(peer_id)
        time.sleep(1)
        messages.edit_msg(peer_id, msg_2, msg_id)
        time.sleep(1)
        messages.edit_msg(peer_id, msg_3, msg_id)
        time.sleep(1)
        messages.edit_msg(peer_id, msg_4, msg_id)
        time.sleep(1)
        messages.edit_msg(peer_id, msg_5, msg_id)
        time.sleep(1)
        messages.edit_msg(peer_id, msg_6, msg_id)
        time.sleep(1)
        messages.edit_msg(peer_id, msg_7, msg_id)
        time.sleep(1)
        messages.edit_msg(peer_id, msg_8, msg_id)
        time.sleep(1)
        messages.edit_msg(peer_id, msg_9, msg_id)

with open("main/database/database_token.json", "r", encoding="utf-8") as file:
   data = json.loads(file.read())
token = data['token']

# Авторизуемся как сообщество
vk = vk_api.VkApi(app_id=6146827, token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk, wait = 0)
