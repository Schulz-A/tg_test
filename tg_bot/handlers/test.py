from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from tg_bot.handlers.echo import start_command
from tg_bot.misc.timeout_decor import timeout


@timeout(5, start_command)
async def test_command(message: types.Message, state: FSMContext):
    await state.set_state("start_state")
    await message.answer("Введите ваше имя")


@timeout(5, start_command)
async def answer_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state("name")

    await message.answer("Введите email")


@timeout(5, start_command)
async def answer_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state("email")
    await message.answer("Введите номер телефона")


async def answer_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    email = data.get("email")
    number = message.text
    text = [
        f"Привет! Ты ввел следующие данные:",
        f"Имя - {name}",
        f"Email - {email}",
        f"Телефон: - {number}"
    ]
    await message.answer("\n".join(text))

    await state.finish()


def register_test(dp: Dispatcher):
    dp.register_message_handler(test_command, Command("form"))
    dp.register_message_handler(answer_name, state="start_state")
    dp.register_message_handler(answer_email, state="name")
    dp.register_message_handler(answer_number, state="email")
