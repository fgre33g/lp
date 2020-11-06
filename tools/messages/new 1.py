import random
import threading
import time

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_token = "8b42238a2cba473982dfffff8b0530c19903f56165b797ec888e16501a82483e0365164cd4aedcb3febec"
# Сюда вставляешь свой токен. (Я юзал от кейта. Получить можно тут https://vkhost.github.io )

contest_trigger_list = ('розыгрыш', 'конкурс')  # Листик слов триггеров для уведомления о розыгрыше:
# Прим. contest_trigger_list = ('розыгрыш', 'конкурс')

contest_white_list = (1, 2, 3)  # Вайтлист айди для триггеров на конкурс:
# Прим. contest_white_list = (1, 2, 3)

start_my_contest_trigger = (
    "пкнварапр"  # Вводишь в кавычках команду, с которой начинается свой розыгрыш.
)
trigger_word = (
    "Удоли"  # Триггер слово в кавычках, с маленькой буквы для удаления сообщений.
)

layout_swap_trigger = (
    "врарварвар"  # Триггер слово в кавычках, с маленькой буквы для смены раскладки на последнем сообщении.
)

chat_everyone_trigger = (
    "Ало"  # Триггер для оповещения всех в беседе.
)

mention_answer_list = (
    "@all",  # Триггер для автоответчика в кавычках;
    [18167],  # [1, 2, 3] - Заполняете в скобках id стикеров для ответа;
    False,  # Установите True, чтобы использовать упоминание как дополнительный триггер (наприм. @durov)
    10  # Минимальное время (в секундах) между старой и новой "реакцией" на сообщение
)

mention_answer_list1 = (
    "Паша",  # Триггер для автоответчика в кавычках;
    [18167],  # [1, 2, 3] - Заполняете в скобках id стикеров для ответа;
    False,  # Установите True, чтобы использовать упоминание как дополнительный триггер (наприм. @durov)
    10  # Минимальное время (в секундах) между старой и новой "реакцией" на сообщение
)


vk_session = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

past_safe = None
to_delete_count = None
to_delete = []
started_contest = {}
contest_peer_id = {}
contest_msg_id = {}
contest_instruction_row = {}
contest_instruction = {}
setup_timer = {}
contest_list = {}
contest_member_list = {}
user_get_self = vk.users.get(fields='domain')[0]
my_id = user_get_self["id"]
my_domain = user_get_self["domain"]
global_delay = False


def msg_delete():
    for n in vk.messages.getHistory(peer_id=event.peer_id).get("items"):
        if n["from_id"] == my_id and len(to_delete) < to_delete_count:
            to_delete.append(n["id"])
    to_delete.append(event.message_id)
    try:
        vk.messages.delete(message_ids=str(to_delete), delete_for_all=1)
    except vk_api.exceptions.ApiError:
        vk.messages.delete(message_ids=str(to_delete), delete_for_all=0)
    to_delete.clear()


def msg_replace_delete():
    for n in vk.messages.getHistory(peer_id=event.peer_id).get("items"):
        if n["from_id"] == my_id and len(to_delete) < to_delete_count:
            to_delete.append(n["id"])
    to_delete.append(event.message_id)
    for h in to_delete[::-1]:
        if h != event.message_id:
            try:
                vk.messages.edit(peer_id=event.peer_id, message_id=h, message="ᅠ")
            except vk_api.exceptions.Captcha:
                break
            except vk_api.exceptions.ApiError:
                pass
    try:
        vk.messages.delete(message_ids=str(to_delete), delete_for_all=1)
    except vk_api.exceptions.ApiError:
        vk.messages.delete(message_ids=str(to_delete), delete_for_all=0)
    to_delete.clear()


def contest_member(cm_id):
    for p, _ in enumerate(contest_member_list.get(cm_id)):
        n = vk.users.get(user_ids=contest_member_list.get(cm_id)[p])[0].get(
            "first_name"
        )
        o = f"[id{contest_member_list.get(cm_id)[p]}|{n}]"
        if o not in contest_list.get(cm_id):
            contest_list[cm_id].append(o)
    return contest_list[cm_id]


def contest_validator():
    return event.peer_id == contest_peer_id.get(event.text.lower())


def contest_cleaner(cc_id):
    global setup_timer, contest_peer_id, started_contest, contest_list, contest_member_list, contest_msg_id, contest_instruction
    started_contest.pop(cc_id)
    contest_msg_id.pop(cc_id)
    contest_member_list.pop(cc_id)
    contest_list.pop(cc_id)
    setup_timer.pop(cc_id)
    contest_instruction.pop(cc_id)
    contest_peer_id = {key: val for key, val in contest_peer_id.items() if val != cc_id}


def contest_updater(cu_id):
    global setup_timer, started_contest
    while True:
        time.sleep(60)
        setup_timer.update({cu_id: int(setup_timer.get(cu_id)) - 1})
        try:
            vk.messages.edit(
                peer_id=cu_id,
                message_id=contest_msg_id.get(cu_id),
                message="Ого! Запущено начало розыгрыша. \nДля принятия участия введите: "
                        + contest_instruction_row.get(cu_id)
                        + "\n\n До окончания розыгрыша: "
                        + str(setup_timer.get(cu_id))
                        + " мин.\n\nУчастники в розыгрыше: "
                        + ", ".join(contest_member(cu_id)),
            )
        except vk_api.exceptions.ApiError:
            contest_cleaner(cu_id)
            break
        if setup_timer.get(cu_id) == 0:
            if not contest_member(cu_id):
                try:
                    vk.messages.send(
                        peer_id=cu_id,
                        random_id=0,
                        message="В розыгрыше нет победителя, в связи с отсутствием участников!",
                        reply_to=contest_msg_id.get(cu_id),
                    )
                    contest_cleaner(cu_id)
                except vk_api.exceptions.ApiError:
                    contest_cleaner(cu_id)
                break
            else:
                try:
                    vk.messages.send(
                        peer_id=cu_id,
                        random_id=0,
                        message="В розыгрыше побеждает "
                                + random.choice(contest_member(cu_id))
                                + "\nПоздравляем!",
                        reply_to=contest_msg_id.get(cu_id),
                    )
                    contest_cleaner(cu_id)
                except vk_api.exceptions.ApiError:
                    contest_cleaner(cu_id)
                break


def layout_swapper(message):
    eng_chars = "~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
    rus_chars = "ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
    trans_table = dict(zip(eng_chars + rus_chars, rus_chars + eng_chars))
    swapped_message = ""
    for c in message:
        try:
            swapped_message += trans_table.get(c)
        except TypeError:
            swapped_message += c
    return swapped_message


def empty_mentions():
    user_id_list = [
        str(user_data["member_id"]) for user_data in vk.messages.getConversationMembers(
            peer_id=event.peer_id
        ).get("items")
    ]
    user_id_list.remove(
        str(my_id)
    )
    empty_mentions_string = ' '.join(
        [
            f"@{f'club{user_id[1:]}' if user_id.startswith('-') else f'id{user_id}'} (&#8300;)" for user_id in user_id_list
        ]
    )
    return f"{chat_everyone_trigger} {empty_mentions_string}"


def mention_checker(message):
    if not global_delay:
        if mention_answer_list[2]:
            if (
                    f" {message.lower()} ".find(f" [id{my_id}|@{my_domain}] ") != -1
                    or f" {message.lower()} ".find(f" [id{my_id}|@{my_domain}], ") != -1
            ):
                return True
        if (
                message.lower().find(f" {mention_answer_list[0]}") != -1
                or message.lower().startswith(mention_answer_list[0])
        ):
            return True
    else:
        return False


def answer_delay():
    global global_delay
    global_delay = True
    time.sleep(mention_answer_list[3])
    global_delay = False
   

def mention_checker(message):
    if not global_delay:
        if mention_answer_list1[2]:
            if (
                    f" {message.lower()} ".find(f" [id{my_id}|@{my_domain}] ") != -1
                    or f" {message.lower()} ".find(f" [id{my_id}|@{my_domain}], ") != -1
            ):
                return True
        if (
                message.lower().find(f" {mention_answer_list1[0]}") != -1
                or message.lower().startswith(mention_answer_list1[0])
        ):
            return True
    else:
        return False


def answer_delay():
    global global_delay
    global_delay = True
    time.sleep(mention_answer_list1[3])
    global_delay = False
for event in longpoll.listen():
    if (
            event.type == VkEventType.MESSAGE_NEW
            and event.text.lower().startswith(trigger_word)
            and event.from_me
            and len(event.text.split()) == 1
    ):
        if len(event.text) > len(trigger_word):
            if event.text[len(trigger_word):] == "1":
                to_delete_count = 2
                msg_delete()
            else:
                if event.text[len(trigger_word):].isdigit():
                    to_delete_count = int(event.text[len(trigger_word):]) + 1
                    msg_delete()
        else:
            to_delete_count = 2
            msg_delete()
    if (
            event.type == VkEventType.MESSAGE_NEW
            and event.text.lower().startswith(trigger_word + "-")
            and event.from_me
            and len(event.text.split()) == 1
    ):
        if len(event.text) > (len(trigger_word) + 1):
            if event.text[(len(trigger_word) + 1):] == "1":
                to_delete_count = 2
                msg_replace_delete()
            else:
                if event.text[(len(trigger_word) + 1):].isdigit():
                    to_delete_count = int(event.text[(len(trigger_word) + 1):]) + 1
                    msg_replace_delete()
        else:
            to_delete_count = 2
            msg_replace_delete()
    if (
            event.type == VkEventType.MESSAGE_NEW
            and event.from_chat
            and any(
        contest_trigger_word in event.text.lower()
        for contest_trigger_word in contest_trigger_list
    )
    ):
        if (
                type(contest_white_list) is tuple
                and event.user_id in contest_white_list
        ) or (
                type(contest_white_list) is int
                and event.user_id == contest_white_list
        ):
            vk.messages.send(
                peer_id=my_id,
                random_id=0,
                message=f"Потенциальное начало конкурса/розыгрыша в"
                        f" {vk.messages.getChatPreview(peer_id=event.peer_id).get('preview')['title']}"
                        f"\n\n{vk.users.get(user_ids=my_id)[0].get('first_name')}"
                        f" не пропусти его, котик ♥",
                forward_messages=event.message_id,
            )
    if (
            event.type == VkEventType.MESSAGE_NEW
            and event.text.lower().startswith(start_my_contest_trigger)
            and event.from_me
            and event.from_chat
            and (
            not started_contest.get(event.peer_id)
            or started_contest.get(event.peer_id) is None
    )
    ):
        if (
                len(event.text.split()) > 2
                and event.text.split()[1].isdigit()
                and event.text.split()[1] != "0"
        ):
            setup_timer.update({event.peer_id: int(event.text.split()[1])})
            vk.messages.delete(message_ids=event.message_id, delete_for_all=1)
            try:
                contest_instruction.update(
                    {
                        event.peer_id: " ".join(
                            event.text.split()[2: len(event.text.split())]
                        ).lower()
                    }
                )
                contest_instruction_row.update(
                    {
                        event.peer_id: " ".join(
                            event.text.split(" ")[2: len(event.text.split())]
                        )
                    }
                )
                vk.messages.send(
                    peer_id=event.peer_id,
                    random_id=0,
                    message=f"Ого! Запущено начало розыгрыша."
                            f"\nДля принятия участия введите:"
                            f" {contest_instruction_row.get(event.peer_id)}"
                            f" \n\n До окончания розыгрыша:"
                            f" {setup_timer.get(event.peer_id)}"
                            f" мин.\n\nУчастники в розыгрыше:",
                )
            except IndexError:
                contest_cleaner(event.peer_id)
    if (
            event.type == VkEventType.MESSAGE_NEW
            and event.from_me
            and event.text.startswith("Ого!")
            and started_contest.get(event.peer_id) is None
    ):
        contest_peer_id.update({contest_instruction.get(event.peer_id): event.peer_id})
        contest_msg_id.update({event.peer_id: event.message_id})
        contest_member_list.update({event.peer_id: []})
        contest_list.update({event.peer_id: []})
        started_contest.update({event.peer_id: True})
        threading.Thread(target=contest_updater, args=(event.peer_id,)).start()
    if (
            event.type == VkEventType.MESSAGE_NEW
            and event.from_chat
            and contest_validator()
    ):
        if event.user_id not in contest_member_list.get(event.peer_id):
            contest_member_list.get(event.peer_id).append(event.user_id)
            try:
                vk.messages.edit(
                    peer_id=event.peer_id,
                    message_id=contest_msg_id.get(event.peer_id),
                    message=f"Ого! Запущено начало розыгрыша."
                            f" \nДля принятия участия введите:"
                            f" {contest_instruction_row.get(event.peer_id)}"
                            f" \n\n До окончания розыгрыша:"
                            f" {setup_timer.get(event.peer_id)}"
                            f" мин.\n\nУчастники в розыгрыше:"
                            f" {', '.join(contest_member(event.peer_id))}",
                )
            except vk_api.exceptions.ApiError:
                contest_cleaner(event.peer_id)
    if (
            event.type == VkEventType.MESSAGE_NEW
            and event.from_me
            and event.text.lower() == layout_swap_trigger
    ):
        for a, n in enumerate(vk.messages.getHistory(peer_id=event.peer_id).get("items")):
            if n["from_id"] == my_id:
                if a != 0:
                    vk.messages.edit(
                        peer_id=event.peer_id,
                        message_id=n["id"],
                        message=layout_swapper(n["text"])
                    )
                    break
                else:
                    vk.messages.delete(
                        message_ids=n["id"],
                        delete_for_all=1
                    )
    if (
            event.type == VkEventType.MESSAGE_NEW
            and event.from_me
            and event.from_chat
            and event.text.lower() == chat_everyone_trigger
    ):
        vk.messages.delete(
            message_ids=event.message_id,
            delete_for_all=1
        )
        vk.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=empty_mentions()
        )
    if (
            event.type == VkEventType.MESSAGE_NEW
            and event.from_chat
            and mention_checker(event.text)
    ):
        vk.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            sticker_id=random.choice(mention_answer_list[1])
        )
        threading.Thread(target=answer_delay, args=()).start()
