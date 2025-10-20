from collections import defaultdict
from datetime import datetime, timedelta

# Хранилище активности
user_trust = defaultdict(lambda: {
    "last_violation": None,
    "messages": 0,
    "joined": datetime.now()
})

TRUST_WINDOW_DAYS = 7  # сколько дней без нарушений считается "доверенным"

def register_message(user_id: int):
    user_trust[user_id]["messages"] += 1

def register_violation(user_id: int):
    user_trust[user_id]["last_violation"] = datetime.now()

def is_trusted(user_id: int):
    data = user_trust[user_id]
    if not data["last_violation"]:
        return True
    return datetime.now() - data["last_violation"] > timedelta(days=TRUST_WINDOW_DAYS)

def get_trusted_users():
    return [uid for uid in user_trust if is_trusted(uid)]
