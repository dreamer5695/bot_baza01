from aiogram.types import KeyboardButton, InlineKeyboardButton, WebAppInfo, \
    ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from Lexicon.lexicon_ru import LEXICON_INLINE


def create_key(width: int, *args: str, **kwargs: str):  # Прописываем таблицу кнопок
    # Инициализация билдеров клавиатуры
    menu: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    # Инициализируем список кнопок
    buttons: list[KeyboardButton] = []

    # описываем условия входа
    if args:
        for button in args:
            buttons.append(KeyboardButton(text=button))

    if kwargs:
        for key, val in kwargs.items():  # items-перебираем именованные словари
            buttons.append(KeyboardButton(text=val))
    # символ * означает распаковку
    menu.row(*buttons, width=width)  # menu.row-Строка кнопок/ width-количество кнопок
    return menu.as_markup()


def create_inline_key(width: int, button1: str | None = None, *args: str, **kwargs: str):  # Прописываем таблицу кнопок
    # Инициализация билдеров клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Инициализируем список кнопок
    buttons: list[InlineKeyboardButton] = []

    # описываем условия входа
    if args:
        for button in args:
            # Если список, то
            buttons.append(InlineKeyboardButton(text=LEXICON_INLINE[button] if button in LEXICON_INLINE else button, callback_data=button))
            # если именованные аргументы (kwargs), то делаем по другому

    if kwargs:
        for key, button in kwargs.items():  # items-перебираем именованные словари
            buttons.append(InlineKeyboardButton(text=button, callback_data=key))

    # символ * означает распаковку, | - или
    kb_builder.row(*buttons, width=width)  # menu.row-Строка кнопок/ width-количество кнопок

#   Если этот аргумент есть(button=True) - если кнопка есть, тогда добавим(append)инлайн кнопку с текcтом.
    if button1:
# Пример для перехода из телеграм на страницу ресурса
        #kb = InlineKeyboardButton(text=button1, url='https://docs.aiogram.dev/en/v3.0.0/dispatcher/filters/magic_filters.html')
# Пример для открытия страницы ресурса в окне телеграмма
        kb = InlineKeyboardButton(text=button1, web_app=WebAppInfo(url='https://m.dzen.ru/'))
        kb_builder.row(kb)

    #   Возврат
    return kb_builder.as_markup()

