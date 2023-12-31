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

from telegram_bot.assets.configs import config


@dp.message(F.text == '/admin', F.from_user.id == config.ADMIN_ID)
async def admin_menu(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Посмотреть статистику",
                                                   "Отправить рассылку",
                                                   "Сформировать отчет",
                                                   "Управление мероприятиями",
                                                   "В панель сотрудника")
    await state.set_state(AdminStates.main)
    await message.answer('Добро пожаловать в админ-панель!', reply_markup=markup)

# TODO: придумать какие группы можно сформировать для рассылки
@dp.message(AdminStates.main, F.text == 'Назад')
async def back_from_main_menu(message: Message, state: FSMContext):
    await main_menu.promouter_menu(message, state)