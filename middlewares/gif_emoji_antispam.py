from aiogram import BaseMiddleware
from aiogram.types import Message
from datetime import datetime, timedelta
import regex  # pip install regex

class GifEmojiAntiSpamMiddleware(BaseMiddleware):
    def __init__(self, gif_cooldown: int = 10, emoji_limit: int = 5, emoji_cooldown: int = 10, notify: bool = True):
        super().__init__()
        self.gif_cooldown = timedelta(seconds=gif_cooldown)
        self.emoji_limit = emoji_limit
        self.emoji_cooldown = timedelta(seconds=emoji_cooldown)
        self.user_last_gif_time = {}
        self.user_last_emoji_spam = {}
        self.notify = notify

    def count_emojis(self, text: str) -> int:
        emoji_pattern = regex.compile(r'\p{Emoji}', flags=regex.UNICODE)
        return len(emoji_pattern.findall(text))

    async def __call__(self, handler, event: Message, data):
        if event.chat.type not in ("group", "supergroup"):
            return await handler(event, data)

        user_id = event.from_user.id
        now = datetime.now()

        # 🌀 Защита от гифок
        if event.animation:
            last_gif = self.user_last_gif_time.get(user_id)
            if last_gif and now - last_gif < self.gif_cooldown:
                try:
                    await event.delete()
                    if self.notify:
                        await event.chat.send_message(
                            f"⚠️ @{event.from_user.username or event.from_user.full_name} — не спамьте гифками."
                        )
                except Exception:
                    pass
                return
            self.user_last_gif_time[user_id] = now

        # 😊 Защита от смайлов
        if event.text:
            emoji_count = self.count_emojis(event.text)
            if emoji_count >= self.emoji_limit:
                last_emoji = self.user_last_emoji_spam.get(user_id)
                if last_emoji and now - last_emoji < self.emoji_cooldown:
                    try:
                        await event.delete()
                        if self.notify:
                            await event.chat.send_message(
                                f"⚠️ @{event.from_user.username or event.from_user.full_name} — слишком много смайлов. Не спамьте."
                            )
                    except Exception:
                        pass
                    return
                self.user_last_emoji_spam[user_id] = now

        return await handler(event, data)
