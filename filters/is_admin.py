from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from Cakeshop_Euphoria_Bot.config import ADMINS

class IsAdmin(BoundFilter):

    async def check(self, message: Message):
        return message.from_user.id in ADMINS