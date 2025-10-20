#!/bin/bash

cd /home/slim/bots/bot_7dtd
source ~/.bashrc

echo "🚀 Запуск Telegram-бота..."
nohup python3 bot.py > logs.txt 2>&1 &
