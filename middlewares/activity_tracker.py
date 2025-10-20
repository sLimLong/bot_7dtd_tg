import json
from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from pathlib import Path

STATS_FILE = Path("data/user_stats.json")

class ActivityTrackerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message, data: dict):
        if not event.from_user or not event.text:
            return await handler(event, data)

        STATS_FILE.parent.mkdir(exist_ok=True)
        stats = {}
        if STATS_FILE.exists():
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                stats = json.load(f)

        user_id = str(event.from_user.id)
        full_name = event.from_user.full_name
        username = event.from_user.username or ""

        stats[user_id] = {
            "count": stats.get(user_id, {}).get("count", 0) + 1,
            "name": full_name,
            "username": username
        }

        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        return await handler(event, data)
