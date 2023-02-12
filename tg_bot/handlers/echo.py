from aiogram import types


async def bot_echo(message: types.Message):
    text = [
        "Echo without state.",
        "Message:",
        message.text
    ]
    await message.answer("\n".join(text))