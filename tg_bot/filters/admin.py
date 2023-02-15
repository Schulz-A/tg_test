from aiogram.dispatcher.filters import BoundFilter

from tg_bot.config import Config


class AdminFilter(BoundFilter):
    async def check(self, *args) -> bool:
        config: Config =