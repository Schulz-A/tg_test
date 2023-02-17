from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from tg_bot.misc.states import Test


async def test_command(message: types.Message):
    await message.answer("Введите ваше имя")

    await Test.Q1.set()


async def answer_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Введите email")

    await Test.Q2.set()


async def answer_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите номер телефона")

    await Test.Q3.set()


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
    dp.register_message_handler(answer_name, state=Test.Q1)
    dp.register_message_handler(answer_email, state=Test.Q2)
    dp.register_message_handler(answer_number, state=Test.Q3)
