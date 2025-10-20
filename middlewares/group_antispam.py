# middlewares/group_antispam.py
from aiogram import BaseMiddleware
from aiogram.types import Message
from datetime import datetime, timedelta

class GroupAntiSpamMiddleware(BaseMiddleware):
    def __init__(self, cooldown_seconds: int = 3, notify: bool = True):
        super().__init__()
        self.cooldown = timedelta(seconds=cooldown_seconds)
        self.user_last_message_time = {}
        self.notify = notify

    async def __call__(self, handler, event: Message, data):
        if event.chat.type not in ("group", "supergroup"):
            return await handler(event, data)

        user_id = event.from_user.id
        now = datetime.now()

        last_time = self.user_last_message_time.get(user_id)
        if last_time and now - last_time < self.cooldown:
            try:
                await event.delete()
                if self.notify:
                    await event.chat.send_message(
                        f"⚠️ @{event.from_user.username or event.from_user.full_name} — не спамьте, пожалуйста."
                    )
            except Exception:
                pass
            return

        self.user_last_message_time[user_id] = now
        return await handler(event, data)
