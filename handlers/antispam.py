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
# Все проверки (текст, гифки, стикеры) происходят в пределах этого окна.

TEXT_REPEAT_THRESHOLD = 3  # 🔁 Максимальное количество одинаковых текстов подряд, допустимое за SPAM_WINDOW.
# Если пользователь отправляет одно и то же сообщение ≥ 3 раз — оно считается спамом.

TEXT_FLOOD_THRESHOLD = 5  # 💬 Максимальное количество любых текстовых сообщений подряд за SPAM_WINDOW.
# Даже если тексты разные — если их ≥ 7 за 10 секунд, это считается флудом.

GIF_REPEAT_THRESHOLD = 2  # 🎞️ Максимальное количество одинаковых гифок подряд.
# Если одна и та же гифка отправляется ≥ 2 раз — она считается спамом.

GIF_TOTAL_THRESHOLD = 4  # 🎞️ Максимальное количество любых гифок подряд за SPAM_WINDOW.
# Даже если гифки разные — если их ≥ 4, это считается гиф-спамом.

STICKER_REPEAT_THRESHOLD = 2  # 🧊 Максимальное количество одинаковых стикеров подряд.
# Если один и тот же стикер отправляется ≥ 2 раз — он считается спамом.

STICKER_TOTAL_THRESHOLD = 4  # 🧊 Максимальное количество любых стикеров подряд за SPAM_WINDOW.
# Даже если стикеры разные — если их ≥ 4, это считается стикер-спамом.


def register_antispam(dp: Dispatcher):
    # 🔁 Повтор текста
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
            await message.answer(f"⚠️ {message.from_user.full_name}, не повторяй одно и то же!")

    # ⏱️ Быстрый флуд разными текстами
    @dp.message(F.text)
    async def block_fast_flood(message: Message):
        user_id = message.from_user.id
        now = asyncio.get_event_loop().time()

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
