import dp
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, \
    StateFilter  # CommandStart-простейшая функция реагирования на команду start
from aiogram.types import Message, ContentType, CallbackQuery

#   StateFilter - состояния
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from Keyboards.Keyboards import create_key, create_inline_key
from Lexicon.lexicon_ru import LEXICON_MENU, LEXICON_INLINE
# импорт для работы с базой данных
from config_bd.user_bd import SQL

from aiogram import html

router: Router = Router()
# в скобках указываем количество кнопок в ряду / вытаскиваем распакованное меню
keyboard_start = create_key(2, **LEXICON_MENU)
# доп.кнопку 'BACK' вне рядности описанной width прописываем в Keyboards.py
keyboard_inline = create_inline_key(2, 'Site', **LEXICON_INLINE)

# dict-словарь, int-цифры, str-строка
# создаём базу данных пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}


# создаём список состояний бота (шаги)
class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_phone = State()


@router.message(CommandStart())
async def process_start_comand(message: Message):
    # добавление в базу данных user_name и user_id
    s = SQL()
    s.INSERT(message.from_user.id, message.from_user.first_name)
    # Меню будет висеть до новой функции связанной с markup!!!
    await message.answer(f"Привет!", reply_markup=keyboard_start)


@router.message(F.text == 'HI')
async def hi(message: Message, bot: Bot):  # С начало сообщение "message", потом реакция бота
    # отправка сообщений конкретному пользователю user.id, группу, канала
    await message.answer(f'Привет, <b>{message.from_user.first_name}</b>')


# @router.message()
# async def echo(message: Message, bot: Bot):  # С начало сообщение "message", потом реакция бота
#     # отправка сообщений конкретному пользователю user.id, группу, канала
#     # Задание условий:
#     if message.text.count(' ') == 2:  # если пробелов в тексте >=1, то ответ.
#     # upper-текст верхнего регистра. capitalize-первая буква верхнего регистра.
#         await message.answer(text=message.text.upper())
#     if message.text.count(' ') >= 3:
#         await message.answer("много букафф")
# Можно указывать несколько условий ответа. Закрывается пустышкой(нет действий) или
# else:выполнением команды


@router.message(F.text == 'id')
async def myid(message: Message, bot: Bot):  # С начало сообщение "message", потом реакция бота
    # отправка сообщений конкретному пользователю user.id, группу, канала
    await message.answer(f'Ваш ID, <b>{message.from_user.id}</b>')


@router.message(F.text == 'Заполнить анкету')
async def anceta_start(message: Message, state: FSMContext):
    #   отправка сообщения в чат, где сработала команда
    await message.answer('Давайте заполним анкету!')
    await message.answer('Пожалуйста, напишите Ваше ФИО.')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


#   Первая функция(верхний абзац) запускает анкету и запрашивает имя.
#   Вторая функция(ниже) ловит ответ на запрос

@router.message(StateFilter(FSMFillForm.fill_name),
                F.text.isalpha())  # F.text.isalpha-фильтр. Сообщение только целый текст(одно слово)
async def anceta_name(message: Message, state: FSMContext):
    # Сохраняем введённое имя в хранилище
    await state.update_data(name=message.text)
    await message.answer('Спасибо. Теперь введите Ваш возраст.')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)


#   Если фильтр на текст не прошёл, возвращаем ответ
@router.message(StateFilter(FSMFillForm.fill_name))
async def anceta_name(message: Message, state: FSMContext):
    await message.answer('Некорректный ввод ФИО. Введите ФИО буквами.')
    # Устанавливаем состояние ожидания ввода телефона
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_age))
async def anceta_name(message: Message, state: FSMContext):
    # Сохраняем введённый возраст в хранилище
    await state.update_data(age=message.text)
    await message.answer('Спасибо. Теперь введите Ваш номер телефона.')
    # Устанавливаем состояние ожидания ввода телефона
    await state.set_state(FSMFillForm.fill_phone)


@router.message(StateFilter(FSMFillForm.fill_phone))
async def anceta_name(message: Message, state: FSMContext, bot: Bot):
    # Сохраняем введённый телефон в хранилище
    await state.update_data(phone=message.text)
    #   завершаем сбор данных
    user_dict[message.from_user.id] = await state.get_data()
    #   user_dict: dict[int, dict[str, str | int | bool]] = {}
    s = SQL()
    s.UPDATE(user_dict[message.from_user.id]["name"], user_dict[message.from_user.id]["age"],
             user_dict[message.from_user.id]["phone"])
    #   завершаем машину состояния и очистка состояния
    await state.clear()
    await message.answer('Спасибо. Ваши данные сохранены.')

    # отправляем пользователю сохранённые данные
    # if message.from_user.id in user_dict:  # проверяем наличие анкеты данного пользователя
    #     #   Ищем ключи описанные ранее (name, age, phone)
    #     await bot.send_message(934354271, text=f'Новый пользователь заполнил таблицу\n'
    #                                            f'Имя: {user_dict[message.from_user.id]["name"]}\n'
    #                                            f'Возраст: {user_dict[message.from_user.id]["age"]}\n'
    #                                            f'Телефон: {user_dict[message.from_user.id]["phone"]}\n'
    #                            )
    # else:
    #     await message.answer('Вы ещё не заполняли анкету.', reply_markup=keyboard_start)


#   Ловушка для неформализованного сообщения. При работе в канале или группе надо отключать
#   ибо бот читает ВСЕ сообщения и пытается ответить на ВСЁ
# @router.message()
# async def echo_message(message: Message):
#     await message.answer(" я не понимаю")

@router.message(F.text == 'help')
async def anceta_start(message: Message):
    #   отправка сообщения в чат, где сработала команда
    await message.answer('Привет', reply_markup=keyboard_inline)


@router.callback_query(F.text == '1')
async def anceta_start(callback: CallbackQuery):
    # отправка сообщения в чат, где сработала команда
    # await callback.answer('Подождите, я думаю...')  # выводит текст поверх чата, который исчезает через 2 секунды
    # await callback.message.edit_text('Нажали первую кнопку')   # выводит текст в чате и убирает клавиатуру
    try:
        await callback.message.edit_text('Нажали первую кнопку', reply_markup=keyboard_inline)
    except:
        await callback.answer('Первую кнопку уже нажимали')


@router.callback_query(F.text == '2')
async def anceta_start(callback: CallbackQuery):
    # отправка сообщения в чат, где сработала команда
    await callback.answer('Нажали вторую кнопку')  # выводит текст поверх чата, который исчезает через 2 секунды
    await callback.message.edit_text('Нажали вторую кнопку')  # выводит текст в чате и убирает клавиатуру
