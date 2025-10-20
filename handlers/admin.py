import subprocess
import os
import asyncio
from aiogram import types, Dispatcher
from aiogram.filters import Command

ALLOWED_ADMINS = {
    297211090  # sLim
}

REPO_PATH = "/root/bot_7dtd_tg"
SERVICE_NAME = "bot_7dtd_tg.service"

async def update_bot(message: types.Message):
    user_id = message.from_user.id

    if user_id not in ALLOWED_ADMINS:
        return await message.reply("⛔ У вас нет прав на обновление бота.")

    if not os.path.isdir(REPO_PATH):
        return await message.reply(f"❌ Путь к репозиторию не найден: `{REPO_PATH}`", parse_mode="Markdown")

    await message.reply("🔄 Сохраняю изменения и обновляю из GitHub...")

    try:
        subprocess.run(["git", "stash", "push", "-m", "Auto stash before update"], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "pull"], cwd=REPO_PATH, check=True)

        try:
            subprocess.run(["git", "stash", "pop"], cwd=REPO_PATH, check=True)
        except subprocess.CalledProcessError:
            await message.reply(
                "⚠️ Обновление прошло, но возник конфликт при возврате локальных изменений.\n"
                "Изменения остались в stash. Проверь вручную:\n"
                "`git stash list`\n", parse_mode="Markdown"
            )

        await message.reply("✅ Обновление завершено. Перезапускаю бот через systemd...")

        # ⏳ Отложенный перезапуск, чтобы успеть отправить сообщение
        asyncio.create_task(delayed_restart())

    except subprocess.CalledProcessError as e:
        await message.reply(f"❌ Ошибка при выполнении команды:\n```\n{e}\n```", parse_mode="Markdown")
    except Exception as e:
        await message.reply(f"❌ Непредвиденная ошибка:\n```\n{e}\n```", parse_mode="Markdown")

async def delayed_restart():
    await asyncio.sleep(2)  # Дать время на отправку сообщения
    subprocess.run(["systemctl", "restart", SERVICE_NAME], check=True)

def register_admin(dp: Dispatcher):
    dp.message.register(update_bot, Command("update"))
