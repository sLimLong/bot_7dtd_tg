import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import base, stats, admin
from middlewares.activity_tracker import ActivityTrackerMiddleware
from middlewares.gif_emoji_antispam import GifEmojiAntiSpamMiddleware  # 👈 заменили

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    # 🧠 Подключаем middlewares
    dp.message.middleware(ActivityTrackerMiddleware())
    dp.message.middleware(GifEmojiAntiSpamMiddleware(
        gif_cooldown=10,
        emoji_limit=5,
        emoji_cooldown=10,
        notify=True
    ))

    # 📦 Регистрируем хендлеры
    base.register_base(dp)
    stats.register_stats(dp)
    admin.register_admin(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
