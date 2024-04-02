from Config_data.config import Secrets
from aiogram import Bot
from Lexicon.lexicon_ru import LEXICON_STATE, LEXICON_TIME


#   функции сообщения админу о запуске и остановке бота
async def start_bot(bot: Bot):
    await bot.send_message(Secrets.admin_id, LEXICON_STATE['start'])


async def stop_bot(bot: Bot):
    await bot.send_message(Secrets.admin_id, LEXICON_STATE['stop'])


#   функция сообщений по времени
async def send_message(bot: Bot):
    await bot.send_message(Secrets.channel_id, LEXICON_TIME['mes'])



