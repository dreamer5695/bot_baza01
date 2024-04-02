from __future__ import annotations

from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TgBot:
    token: str


@dataclass
class Admin:
    Admin: str


@dataclass
class Secrets:
    admin_id: int = 934354271
    channel_id: int = -1002044182502


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    admin: Admin


#   Вариант базы данных на sqlite.
# def load_config(path: str | None = None) -> Config:     #path - путь до файла
#     env: Env = Env()
#     env.read_env(path)
#
#     return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))

#   Вариант базы данных на MySQL
def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  db=DatabaseConfig(database=env('DATABASE'),
                                    db_host=env('DB_HOST'),
                                    db_user=env('DB_USER'),
                                    db_password=env('DB_PASSWORD')),
                  admin=Admin(Admin=env('ADMIN'))
                  )

