from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class TriggerFilter(BoundFilter):
    def __init__(self, triggers: list):
        self.triggers = triggers

    async def check(self, message: types.Message) -> bool:
        mess = message.text
        if not mess:
            mess = message.caption
        return any((x.lower() in self.triggers for x in mess.split()))
