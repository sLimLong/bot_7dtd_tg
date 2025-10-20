from aiogram import Dispatcher, types
from aiogram.filters import Command
from trust.tracker import is_trusted, get_trusted_users, user_trust

def register_trust(dp: Dispatcher):
    @dp.message(Command("respect"))
    async def show_trusted(message: types.Message):
        trusted = get_trusted_users()
        if not trusted:
            return await message.answer("😶 Пока нет доверенных пользователей.")
        
        lines = []
        for uid in trusted:
            data = user_trust[uid]
            days = (datetime.now() - data["joined"]).days
            lines.append(f"🛡️ ID: {uid} — {data['messages']} сообщений, {days} дней в чате")

        await message.answer("🎖️ Доверенные участники:\n\n" + "\n".join(lines))

    @dp.message(Command("truststats"))
    async def trust_stats(message: types.Message):
        uid = message.from_user.id
        data = user_trust[uid]
        last = data["last_violation"]
        status = "✅ Надёжный" if is_trusted(uid) else "⚠️ Недавние нарушения"
        last_text = f"Последнее нарушение: {last.strftime('%d.%m.%Y %H:%M')}" if last else "Нарушений не было"
        await message.answer(
            f"📊 Статистика доверия:\n"
            f"👤 {message.from_user.full_name}\n"
            f"💬 Сообщений: {data['messages']}\n"
            f"🕒 В чате: {(datetime.now() - data['joined']).days} дней\n"
            f"{last_text}\n"
            f"Статус: {status}"
        )
