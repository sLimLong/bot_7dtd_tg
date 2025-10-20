import json
import time
from aiogram import types, Dispatcher
from aiogram.filters import Command
from pathlib import Path

STATS_FILE = Path("data/user_stats.json")
COOLDOWN_FILE = Path("data/stats_cooldown.json")
COOLDOWN_SECONDS = 1800  # 30 минут

def load_json(path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def show_stats(event: types.Message):
    user_id = str(event.from_user.id)
    now = time.time()

    cooldowns = load_json(COOLDOWN_FILE)
    last_time = cooldowns.get(user_id, 0)

    if now - last_time < COOLDOWN_SECONDS:
        remaining = int(COOLDOWN_SECONDS - (now - last_time))
        return await event.reply(f"⏳ Подождите {remaining // 60} мин. перед следующим запросом статистики.")

    stats = load_json(STATS_FILE)
    if not stats:
        return await event.reply("Статистика пуста.")

    # Сортировка по количеству сообщений
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]["count"] if isinstance(x[1], dict) else x[1], reverse=True)

    text = "📊 <b>Топ 20 активных пользователей:</b>\n"
    for i, (uid, data) in enumerate(sorted_stats[:20], 1):
        if isinstance(data, int):
            display = f"ID {uid}"
            count = data
        else:
            name = data.get("name", f"ID {uid}")
            username = data.get("username", "")
            display = f"@{username}" if username else name
            count = data.get("count", 0)

        # Экранируем HTML
        safe_display = display.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
        text += f"{i}. {safe_display} — <b>{count}</b> сообщений\n"

    cooldowns[user_id] = now
    save_json(COOLDOWN_FILE, cooldowns)

    await event.reply(text, parse_mode="HTML")

def register_stats(dp: Dispatcher):
    dp.message.register(show_stats, Command("stats"))
