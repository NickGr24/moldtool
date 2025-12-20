@echo off
echo ========================================
echo   MoldTool - Исправление стилей
echo ========================================
echo.

echo [1/4] Очистка старых статических файлов...
if exist staticfiles (
    rmdir /s /q staticfiles
    echo Папка staticfiles удалена
) else (
    echo Папка staticfiles не найдена
)
echo.

echo [2/4] Сбор статических файлов...
python manage.py collectstatic --noinput
echo.

echo [3/4] Проверка структуры папок...
if exist static\css\main.css (
    echo [OK] static\css\main.css найден
) else (
    echo [ОШИБКА] static\css\main.css НЕ найден!
)

if exist static\js\main.js (
    echo [OK] static\js\main.js найден
) else (
    echo [ОШИБКА] static\js\main.js НЕ найден!
)

if exist static\images\logo.jpg (
    echo [OK] static\images\logo.jpg найден
) else (
    echo [ВНИМАНИЕ] static\images\logo.jpg НЕ найден
)
echo.

echo [4/4] Готово!
echo.
echo ========================================
echo   Рекомендации:
echo ========================================
echo 1. Перезапустите сервер Django
echo 2. Очистите кэш браузера (Ctrl+Shift+Delete)
echo 3. Откройте страницу в режиме инкогнито (Ctrl+Shift+N)
echo 4. Сделайте жёсткую перезагрузку (Ctrl+F5)
echo.
echo Если проблема осталась, откройте TROUBLESHOOTING.md
echo ========================================
echo.
pause


