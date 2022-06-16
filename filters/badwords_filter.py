from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from data.list_of_bad_wordds import bad_spisok


class BadWords(BoundFilter):
    async def check(self, msd: Message):
        for word in bad_spisok:
            if word in msd.text.lower():
                return True
