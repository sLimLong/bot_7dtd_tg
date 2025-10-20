import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import base, stats, admin, antispam

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    base.register_base(dp)
    stats.register_stats(dp)
    admin.register_admin(dp)
    antispam.register_antispam(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
