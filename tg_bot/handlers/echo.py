from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.utils.markdown import hcode

from tg_bot.misc.rate_limit_decor import rate_limit


@rate_limit(5, key="start")
async def start_command(message: types.Message):
    text = [
        "Echo without state.",
        "Message:",
        message.text
    ]
    await message.answer("Enter whatever:")


async def bot_echo_all(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    state_name = await state.get_state()
    text = [
        f"Echo in state {hcode(state_name)}",
        "Message:",
        message.text
    ]
    await message.answer("ok")


def register_echo(dp: Dispatcher):
    dp.register_message_handler(start_command, CommandStart())
    # dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
