from aiogram import types, Dispatcher
from filters.profanity_filter import ProfanityFilter

async def delete_profanity(message: types.Message):
    await message.delete()

def register_base(dp: Dispatcher):
    dp.message.register(delete_profanity, ProfanityFilter())
