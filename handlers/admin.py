import subprocess
import os
from aiogram import types, Dispatcher
from aiogram.filters import Command

# ✅ Список Telegram ID, которым разрешено обновление
ALLOWED_ADMINS = {
    297211090  # sLim
}

REPO_PATH = "/root/bot_7dtd_tg"
SERVICE_NAME = "bot_7dtd_tg.service"

# 🔄 Команда /update — только для разрешённых ID
async def update_bot(message: types.Message):
    user_id = message.from_user.id

    if user_id not in ALLOWED_ADMINS:
        return await message.reply("⛔ У вас нет прав на обновление бота.")

    if not os.path.isdir(REPO_PATH):
        return await message.reply(f"❌ Путь не найден: {REPO_PATH}")

    await message.reply("🔄 Сохраняю изменения и обновляю из GitHub...")

    try:
        # Авто-стэш локальных изменений
        subprocess.run(["git", "stash", "push", "-m", "Auto stash before update"], cwd=REPO_PATH, check=True)

        # Обновление из GitHub
        subprocess.run(["git", "pull"], cwd=REPO_PATH, check=True)

        # Возврат изменений
        subprocess.run(["git", "stash", "pop"], cwd=REPO_PATH, check=True)

        # Перезапуск systemd-сервиса
        subprocess.run(["systemctl", "restart", SERVICE_NAME], check=True)

        await message.reply("✅ Бот обновлён и перезапущен.")
    except subprocess.CalledProcessError as e:
        await message.reply(f"❌ Ошибка при обновлении:\n```\n{e}\n```", parse_mode="Markdown")
    except Exception as e:
        await message.reply(f"❌ Непредвиденная ошибка:\n```\n{e}\n```", parse_mode="Markdown")

# 📌 Регистрация
def register_admin(dp: Dispatcher):
    dp.message.register(update_bot, Command("update"))
