from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import AdminStates

from telegram_bot.repository import api_methods
from telegram_bot.handlers import main_menu
from telegram_bot.handlers.admin_panel.main_admin_panel import admin_menu

from telegram_bot.assets.configs import config


@dp.message(AdminStates.main, F.text == "Управление мероприятиями")
async def manage_event(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Создать мероприятие",
                                                   "Отредактировать мероприятие",
                                                   "Удалить мероприятие",
                                                   "Назад")
    await state.set_state(AdminStates.manage_event)
    await message.answer('Выберите, что вы хотите сделать', reply_markup=markup)

@dp.message(AdminStates.manage_event, F.text == "Назад")
async def back_from_manage_event(message: Message, state: FSMContext):
    await admin_menu(message, state)