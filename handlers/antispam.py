import asyncio
from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ContentType
from collections import defaultdict

# Память
recent_texts = defaultdict(list)
recent_times = defaultdict(list)
recent_gifs = defaultdict(list)
recent_stickers = defaultdict(list)

# Параметры антиспама:

SPAM_WINDOW = 5  # ⏱️ Временное окно (в секундах), в течение которого отслеживаются повторные действия пользователя.
TEXT_REPEAT_THRESHOLD = 3  # 🔁 Повтор одного и того же текста
TEXT_FLOOD_THRESHOLD = 5   # 💬 Любых текстов подряд
MIN_MESSAGE_LENGTH = 1     # 🧹 Игнорировать слишком короткие сообщения

GIF_REPEAT_THRESHOLD = 2   # 🎞️ Одинаковых гифок
GIF_TOTAL_THRESHOLD = 4    # 🎞️ Любых гифок подряд

STICKER_REPEAT_THRESHOLD = 2  # 🧊 Одинаковых стикеров
STICKER_TOTAL_THRESHOLD = 4   # 🧊 Любых стикеров подряд

def register_antispam(dp: Dispatcher):
    # 🔁 Повтор текста
    @dp.message(F.text)
    async def block_text_spam(message: Message):
        user_id = message.from_user.id
        text = message.text.strip().lower()
        now = asyncio.get_event_loop().time()

        if len(text) < MIN_MESSAGE_LENGTH:
            return

        recent_texts[user_id] = [
            (t, ts) for t, ts in recent_texts[user_id] if now - ts < SPAM_WINDOW
        ]
        recent_texts[user_id].append((text, now))

        repeats = sum(1 for t, _ in recent_texts[user_id] if t == text)
        if repeats >= TEXT_REPEAT_THRESHOLD:
            await message.delete()
            await message.answer(f"🔁 {message.from_user.full_name}, не повторяй одно и то же!")

        # ⏱️ Быстрый флуд разными текстами
        recent_times[user_id] = [
            ts for ts in recent_times[user_id] if now - ts < SPAM_WINDOW
        ]
        recent_times[user_id].append(now)

        if len(recent_times[user_id]) >= TEXT_FLOOD_THRESHOLD:
            await message.delete()
            await message.answer(f"⏱️ {message.from_user.full_name}, слишком много сообщений подряд!")

    # 🎞️ Гиф-спам
    @dp.message(F.content_type == ContentType.ANIMATION)
    async def block_gif_spam(message: Message):
        user_id = message.from_user.id
        gif_id = message.animation.file_unique_id
        now = asyncio.get_event_loop().time()

        recent_gifs[user_id] = [
            (gid, ts) for gid, ts in recent_gifs[user_id] if now - ts < SPAM_WINDOW
        ]
        recent_gifs[user_id].append((gif_id, now))

        total = len(recent_gifs[user_id])
        same = sum(1 for gid, _ in recent_gifs[user_id] if gid == gif_id)

        if same >= GIF_REPEAT_THRESHOLD:
            await message.delete()
            await message.answer(f"🚫 {message.from_user.full_name}, не повторяй одну и ту же гифку!")
        elif total >= GIF_TOTAL_THRESHOLD:
            await message.delete()
            await message.answer(f"⚠️ {message.from_user.full_name}, слишком много гифок подряд!")

    # 🧊 Стикер-спам
    @dp.message(F.content_type == ContentType.STICKER)
    async def block_sticker_spam(message: Message):
        user_id = message.from_user.id
        sticker_id = message.sticker.file_unique_id
        now = asyncio.get_event_loop().time()

        recent_stickers[user_id] = [
            (sid, ts) for sid, ts in recent_stickers[user_id] if now - ts < SPAM_WINDOW
        ]
        recent_stickers[user_id].append((sticker_id, now))

        total = len(recent_stickers[user_id])
        same = sum(1 for sid, _ in recent_stickers[user_id] if sid == sticker_id)

        if same >= STICKER_REPEAT_THRESHOLD:
            await message.delete()
            await message.answer(f"🚫 {message.from_user.full_name}, не повторяй один и тот же стикер!")
        elif total >= STICKER_TOTAL_THRESHOLD:
            await message.delete()
            await message.answer(f"⚠️ {message.from_user.full_name}, слишком много стикеров подряд!")
