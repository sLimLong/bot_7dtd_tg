#!/bin/bash

cd /bot_7dtd_tg

echo "🚀 Перезапуск Telegram-бота..."
pkill -f bot.py
sleep 2
nohup python3 bot.py > logs.txt 2>&1 &
