# Telegram Password Storage Bot
Это Telegram бот, реализующий функционал персонального хранилища паролей. Вы можете использовать этот бот, чтобы хранить свои логины и пароли для разных сервисов в одном месте.

# Команды
Бот поддерживает следующие команды:
- /set - добавляет логин и пароль для сервиса.
- /get - получает логин и пароль по названию сервиса.
- /del - удаляет пароль для сервиса.
- /services - получает список всех сервисов в хранилище.

# Установка
Для запуска бота на своем компьютере, вам понадобится установить следующее программное обеспечение:
- Docker
- Docker Compose
После установки Docker и Docker Compose, выполните следующие действия:
1. Клонируйте репозиторий с кодом бота: git clone https://github.com/GlebDontsov/password-vault-bot.git
2. Создайте .env файл и заполните переменные окружения, указав данные для подключения к базе данных PostgreSQL и токен вашего Telegram-бота. Пример файла .env:
```
BOT_TOKEN=<YOUR_BOT_TOKEN>
CRYPTO_KEY=<YOUR_CRYPTO_TOKEN>
POSTGRES_DB=<YOUR_POSTGRES_DB>
POSTGRES_HOST=<YOUR_POSTGRES_HOST>
POSTGRES_USER=<YOUR_POSTGRES_USER>
POSTGRES_PASSWORD=<YOUR_POSTGRES_PASSWORD>
PG_DATA=/var/lib/pgsql/pgdata
```
3. Запустите контейнеры Docker-Compose: 
```
docker-compose up --build
```
4. Готово! Бот запущен и готов к использованию.

# Технологии
- Python 3.10
- aiogram 3.0.0b6
- PostgreSQL 14.7
- Docker 23.0.1
- Docker Compose 1.26.0
