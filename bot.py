import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import base, stats, admin
from middlewares.activity_tracker import ActivityTrackerMiddleware
from middlewares.group_antispam import GroupAntiSpamMiddleware  # 👈 добавлено

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    # 🧠 Подключаем middlewares
    dp.message.middleware(ActivityTrackerMiddleware())
    dp.message.middleware(GroupAntiSpamMiddleware(cooldown_seconds=3, notify=True))  # 👈 защита от спама

    # 📦 Регистрируем хендлеры
    base.register_base(dp)
    stats.register_stats(dp)
    admin.register_admin(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
