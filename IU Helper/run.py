import asyncio, os, logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from App.handlers import router

# Загружаем токены из системы
load_dotenv()

# Создаем экземпляры бота и деспетчера
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

# Основная функия
async def main():
   dp.include_router(router=router)
   # await bot(DeleteWebhook(drop_pending_updates=True))
   await dp.start_polling(bot)
   
# Запускаем бота
if __name__ == '__main__':
   logging.basicConfig(level=logging.INFO) # Включаем логгирование
   try:
      asyncio.run(main())
   except KeyboardInterrupt:
      print('Бот остановлен')