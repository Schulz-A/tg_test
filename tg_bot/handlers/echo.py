from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.markdown import hcode


async def bot_echo(message: types.Message):
    text = [
        "Echo without state.",
        "Message:",
        message.text
    ]
    await message.answer("\n".join(text))


async def bot_echo_all(message: types.Message, state):
    state_name = await state.get_state()
    text = [
        f"Echo in state {hcode(state_name)}",
        "Message:",
        message.text
    ]
    await message.answer("\n".join(*text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo, CommandStart())
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
