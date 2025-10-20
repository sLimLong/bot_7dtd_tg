import subprocess
from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.enums.chat_member_status import ChatMemberStatus

# ✅ Проверка: является ли пользователь админом
async def is_admin(message: types.Message) -> bool:
    chat = message.chat
    user_id = message.from_user.id
    member = await message.bot.get_chat_member(chat.id, user_id)
    return member.status in {
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    }

# 🔄 Команда /update — только для админов
async def update_bot(message: types.Message):
    if not await is_admin(message):
        return await message.reply("⛔ Только администраторы могут выполнять обновление.")

    await message.reply("🔄 Обновление из GitHub и перезапуск...")

    try:
        # Обновление из GitHub
        subprocess.run(["git", "pull"], cwd="/bot_7dtd_tg", check=True)

        # Перезапуск через run_bot.sh
        subprocess.run(["bash", "run_bot.sh"], cwd="/bot_7dtd_tg", check=True)

        await message.reply("✅ Бот обновлён и перезапущен.")
    except subprocess.CalledProcessError as e:
        await message.reply(f"❌ Ошибка при обновлении: {e}")
    except Exception as e:
        await message.reply(f"❌ Непредвиденная ошибка: {e}")

# 📌 Регистрация
def register_admin(dp: Dispatcher):
    dp.message.register(update_bot, Command("update"))
