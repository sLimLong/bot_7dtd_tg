@echo off
echo 🔧 Запускаем обработку локализаций...

REM Проверка наличия Python
py --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Python не найден. Установи его отсюда: https://www.python.org/downloads/
    pause
    exit /b
)

REM Запуск скрипта
py bot.py

IF ERRORLEVEL 1 (
    echo ❌ Ошибка при запуске bot.py
) ELSE (
    echo ✅ Скрипт успешно завершён
)

pause
