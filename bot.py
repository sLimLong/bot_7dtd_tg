import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import base, stats
from middlewares.activity_tracker import ActivityTrackerMiddleware

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.message.middleware(ActivityTrackerMiddleware())

    base.register_base(dp)
    stats.register_stats(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
