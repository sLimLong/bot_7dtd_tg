import subprocess
from aiogram import types, Dispatcher
from aiogram.filters import Command

# ✅ Список Telegram ID, которым разрешено обновление
ALLOWED_ADMINS = {
    297211090  # sLim
    # Добавь ID сюда
}

# 🔄 Команда /update — только для разрешённых ID
async def update_bot(message: types.Message):
    user_id = message.from_user.id

    if user_id not in ALLOWED_ADMINS:
        return await message.reply("⛔ У вас нет прав на обновление бота.")

    await message.reply("🔄 Обновление из GitHub и перезапуск через systemd...")

    try:
        # Обновление из GitHub
        subprocess.run(["git", "pull"], cwd="root/bot_7dtd_tg", check=True)

        # Перезапуск systemd-сервиса
        subprocess.run(["systemctl", "restart", "bot_7dtd_tg.service"], check=True)

        await message.reply("✅ Бот обновлён и перезапущен через systemd.")
    except subprocess.CalledProcessError as e:
        await message.reply(f"❌ Ошибка при обновлении: {e}")
    except Exception as e:
        await message.reply(f"❌ Непредвиденная ошибка: {e}")

# 📌 Регистрация
def register_admin(dp: Dispatcher):
    dp.message.register(update_bot, Command("update"))
