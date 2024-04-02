from sqlalchemy import create_engine, MetaData, Table, String, Integer, \
    Column, Text, DateTime, Boolean, ForeignKey
from datetime import datetime

from Config_data.config import Config, load_config

# строки доступа к базе при необходимости логина, пароля, хоста
# from Config_data import Config, load_config
config: Config = load_config()


def engine():
    # engine = create_engine(f'mysql+pymysql://root:{config.db.db_password}@localhost/{config.db.database}', echo=True)
    #   объявляем переменную {config.db.db_password}
    #   Создаём базу данных с именем
    engine = create_engine('sqlite:///LESSON.db')
    #   Подключаемся к базе
    #engine.connect()
    metadata = MetaData()
    # Создаём структуру/модель базы банных. Column-колонка
    users = Table(
        'users',  # название таблицы
        metadata,
        # Integer-целые числа, unique=True - параметр ID должен быть уникальный
        # параметр ID является "primary_key=True" - главным ключом
        Column('Id', Integer(), unique=True, primary_key=True),
        #   Text()-ячейка текстовая, "default=False"-не может быть пустой
        Column('User_id', Integer(), unique=True, nullable=False),
        Column('First_name', String(100), nullable=False),
        #   String(100) - тоже, что и текст - ограничение на поле=100 символов
        Column('Age', Boolean(), default=True),
        Column('Phone', Boolean(), default=True),
        Column('City', Boolean(), default=True),
        #   в каждой строке проставляется время заполнения NOW-текущее время
        Column('Greate_user', DateTime(), default=datetime.now()),
    )
    #   команда на создание таблицы с заданными параметрами
    metadata.create_all(engine)
    return engine

