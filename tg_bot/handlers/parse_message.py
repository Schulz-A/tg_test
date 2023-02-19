from aiogram import types, Dispatcher

from tg_bot.filters.triggers_filter import TriggerFilter


triggers = [
    "mojo",
    "mojoform",
    "moj",
    "моджо",
    "моджоформ"
]


async def text_parse(message: types.Message):
    mess = message.text
    if not mess:
        mess = message.caption
    edited_mess = " ".join((x for x in mess.split() if x.lower() not in triggers))

    text = [
        "New Task!\n",
        f"from: {message.chat.title}\n",
        f"user: {message.from_user.full_name}\n",
        "<b>Task:</b>\n",
        f"{edited_mess}"
    ]
    if "text" in message:
        await message.bot.send_message(chat_id=message.chat.id, text="\n".join(text))
    else:
        photo = message.photo.pop(-1).file_id
        await message.bot.send_photo(317939471, photo=photo, caption="\n".join(text))


def register_parse_message(dp: Dispatcher):
    dp.register_message_handler(text_parse, TriggerFilter(triggers), content_types=["photo", "text"])
