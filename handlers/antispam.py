import asyncio
from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ContentType
from collections import defaultdict

# Память для повторяющихся сообщений
recent_texts = defaultdict(list)
recent_gifs = defaultdict(list)

SPAM_WINDOW = 10  # секунд
TEXT_REPEAT_THRESHOLD = 3
GIF_SPAM_THRESHOLD = 3

def register_antispam(dp: Dispatcher):
    # 🔁 Блокировка повторяющегося текста
    @dp.message(F.text)
    async def block_repeated_text(message: Message):
        user_id = message.from_user.id
        text = message.text.strip().lower()
        now = asyncio.get_event_loop().time()

        recent_texts[user_id] = [
            (t, ts) for t, ts in recent_texts[user_id] if now - ts < SPAM_WINDOW
        ]
        recent_texts[user_id].append((text, now))

        repeats = sum(1 for t, _ in recent_texts[user_id] if t == text)
        if repeats >= TEXT_REPEAT_THRESHOLD:
            await message.delete()
            await message.answer(f"⚠️ {message.from_user.full_name}, хватит спамить одинаковым текстом!")

    # 🚫 Блокировка гиф-спама
    @dp.message(F.content_type == ContentType.ANIMATION)
    async def block_gif_spam(message: Message):
        user_id = message.from_user.id
        gif_id = message.animation.file_unique_id
        now = asyncio.get_event_loop().time()

        recent_gifs[user_id] = [
            (gid, ts) for gid, ts in recent_gifs[user_id] if now - ts < SPAM_WINDOW
        ]
        recent_gifs[user_id].append((gif_id, now))

        # Проверка: слишком много гифок подряд или одна и та же гифка
        total_gifs = len(recent_gifs[user_id])
        same_gif_count = sum(1 for gid, _ in recent_gifs[user_id] if gid == gif_id)

        if total_gifs >= GIF_SPAM_THRESHOLD or same_gif_count >= 2:
            await message.delete()
            await message.answer(f"🚫 {message.from_user.full_name}, не спамь гифками!")

