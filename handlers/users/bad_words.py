from aiogram import types

from filters.badwords_filter import BadWords
from loader import dp, db


@dp.message_handler(BadWords())
async def cath_bad_words2(message: types.Message):
    idd = message.from_user.full_name
    if db.check_user(message.from_user.id):
        db.add_user(id=message.from_user.id, name=idd)
    else:
        db.update_value(message.from_user.id, idd)
    user = db.select_user(id=message.from_user.id)
    await message.answer(text=f'{idd} за метлой следи! \n'
                              f'Ты сматерился уже {user[2]} раз!')
