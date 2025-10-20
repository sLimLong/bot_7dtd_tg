import asyncio
from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ContentType
from collections import defaultdict
from trust.tracker import register_message, register_violation  # 👈 подключение трекера

# Память
recent_texts = defaultdict(list)
recent_times = defaultdict(list)
recent_gifs = defaultdict(list)

# Параметры
SPAM_WINDOW = 10  # секунд
TEXT_REPEAT_THRESHOLD = 3
TEXT_FLOOD_THRESHOLD = 7
GIF_REPEAT_THRESHOLD = 2
GIF_SPAM_THRESHOLD = 4

def register_antispam(dp: Dispatcher):
    # 🔁 Повтор текста + быстрый флуд
    @dp.message(F.text)
    async def block_text_spam(message: Message):
        user_id = message.from_user.id
        text = message.text.strip().lower()
        now = asyncio.get_event_loop().time()

        register_message(user_id)  # ✅ фиксируем активность

        # Повтор текста
        recent_texts[user_id] = [
            (t, ts) for t, ts in recent_texts[user_id] if now - ts < SPAM_WINDOW
        ]
        recent_texts[user_id].append((text, now))

        repeats = sum(1 for t, _ in recent_texts[user_id] if t == text)
        if repeats >= TEXT_REPEAT_THRESHOLD:
            register_violation(user_id)
            await message.delete()
            return await message.answer(f"🔁 {message.from_user.full_name}, не повторяй одно и то же!")

        # Быстрый флуд
        recent_times[user_id] = [
            ts for ts in recent_times[user_id] if now - ts < SPAM_WINDOW
        ]
        recent_times[user_id].append(now)

        if len(recent_times[user_id]) >= TEXT_FLOOD_THRESHOLD:
            register_violation(user_id)
            await message.delete()
            return await message.answer(f"⏱️ {message.from_user.full_name}, слишком много сообщений подряд!")

    # 🎞️ Гиф-спам
    @dp.message(F.content_type == ContentType.ANIMATION)
    async def block_gif_spam(message: Message):
        user_id = message.from_user.id
        gif_id = message.animation.file_unique_id
        now = asyncio.get_event_loop().time()

        register_message(user_id)

        recent_gifs[user_id] = [
            (gid, ts) for gid, ts in recent_gifs[user_id] if now - ts < SPAM_WINDOW
        ]
        recent_gifs[user_id].append((gif_id, now))

        total = len(recent_gifs[user_id])
        same = sum(1 for gid, _ in recent_gifs[user_id] if gid == gif_id)

        if same >= GIF_REPEAT_THRESHOLD:
            register_violation(user_id)
            await message.delete()
            return await message.answer(f"🚫 {message.from_user.full_name}, не повторяй одну и ту же гифку!")

        elif total >= GIF_SPAM_THRESHOLD:
            register_violation(user_id)
            await message.delete()
            return await message.answer(f"⚠️ {message.from_user.full_name}, слишком много гифок подряд!")
