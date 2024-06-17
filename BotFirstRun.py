# Импортируем библиотеки
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import os

# ипортируем из другого файла хэндлеры, который в папке app
from app.handlers import router

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Объект бота
TOKEN = os.getenv('TOKEN') # выгружаем из .env токен
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(router) # Теперь диспетчер знает, в каком файле находится роутер обработчик хэндлеров
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO) # Включаем логирование, чтобы не пропустить важные сообщения (на продакшене нужно выключить, если много юзеров)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')