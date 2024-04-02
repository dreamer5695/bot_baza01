# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from Config_data.config import Config, load_config
from Handlers.events import start_bot, stop_bot
from Handlers import other_handlers, admin_handlers
# блок для обработки сообщений по времени
import aioschedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Handlers.events import send_message
from datetime import datetime

# инициализация логирования
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуск бота
async def main() -> None:
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    # выводим в консоль информацию и начале запуска
    logger.info('starting lesson')

    # Загружаем конфиг переменную config
    config: Config = load_config()  # в () можно прописать путь до файла .env если меняем место расположения

    # Инициализируем бота и диспетчера
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # сообщение по расписании
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # ОПИСАНИЕ:отработай функцию send_message по тригеру cron(раз в день) в какое время , с какого времени начинать,
    scheduler.add_job(send_message, trigger='cron', hour=11, minute=23, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.start()

    # Зарегистрируем роутеры
    dp.include_router(admin_handlers.router)    # Код читается сверху вниз. Админский код должен быть первым
    dp.include_router(other_handlers.router)
    dp.include_router(admin_handlers.start_dialog)
    setup_dialogs(dp)

    # Пропускать накопленные апдейты (пропуск, накопившихся за время, не работы бота сообщений) и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

