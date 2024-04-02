from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
# CommandStart-простейшая функция реагирования на команду start
# StateFilter - состояния
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram.fsm.state import default_state, State, StatesGroup
from Filters.filters import IsAdmin
from Keyboards.Keyboards import create_key, create_inline_key
from Lexicon.lexicon_ru import LEXICON_ADMIN, LEXICON_INLINE
# импорт для работы с базой данных
from config_bd.user_bd import SQL

from aiogram import html

router: Router = Router()
router.message.filter(IsAdmin())  # обработка ниже пойдёт только если выполнено условие фильтра
keyboard_start = create_key(2, **LEXICON_ADMIN)


class StartD(StatesGroup):  # описание состояний
    start = State()
    update = State()


@router.message(CommandStart())
async def process_start_command(message: Message):
    s = SQL()
    s.INSERT(message.from_user.id, message.from_user.first_name)
    await message.answer("ТЫ админ,вот тебе руль", reply_markup=keyboard_start)


@router.message(F.text == 'В ДИАЛОГ')
async def dialog_start(message: Message, dialog_manager: DialogManager):
    # Описываем, в какое состояние перейти при выполнении условия.
    # RESET_STACK-при при нажатии 'В ДИАЛОГ', текущее состояние сбросится и перейдёт в новое
    await dialog_manager.start(state=StartD.start, mode=StartMode.RESET_STACK)


async def update_name(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    s = SQL()
    s.UPDATE('NEW_NAME', callback.from_user.id)
    result = s.SELECT('NEW_NAME')
    s.DELETE('NEW_NAME')
    #await callback.message.answer(str(result[1]))
    await callback.message.answer(str(result[1]))
    await dialog_manager.switch_to(state=StartD.update)

# Диалог->окна->виджиты - порядок построения
start_dialog = Dialog(
    Window(
        Const('Ты вошел в Диалог'),  # Const-не изменяемый текст
        Group(
            Button(Const('Изменить ИМЯ'), id='name', on_click=update_name),
            width=1     # количество кнопок
        ),
        state=StartD.start  # Указываем состояние, в которое надо переходить. Регистрируется в классах.
    ),
    Window(
        Const('Ты поменял имя!'),
        state=StartD.update
    )
)


# @router.message()
# async def process_start_command(message: Message):
#     await message.answer("нужны правильные команды")

