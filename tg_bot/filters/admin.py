from aiogram.dispatcher.filters import BoundFilter

from tg_bot.config import Config


class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin=None):
        self.is_admin = is_admin

    async def check(self, *args) -> bool | None:
        if self.is_admin is None:
            return
        if not self.is_admin:
            return False
        config: Config = args[0].bot.get("config")
        user_id = args[0].from_user.id
        return user_id in config.tg_bot.admin_ids
