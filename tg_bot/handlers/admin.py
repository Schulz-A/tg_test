from aiogram import types, Dispatcher


async def admin_start(message: types.Message, middleware_data):
    await message.bot.send_message(chat_id=message.chat.id, text=f"Hi {middleware_data}")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], is_admin=True)