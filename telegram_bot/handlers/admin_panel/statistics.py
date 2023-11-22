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

@dp.message(AdminStates.main, F.text == "Посмотреть статистику")
async def choose_event_for_stat(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Небо — 2023", "Неделя дизайна — 2022", "Назад")
    await state.set_state(AdminStates.choose_event_for_stat)
    await message.answer('Выберите мероприятие, для которого вы хотите посмотреть статистику', reply_markup=markup)

@dp.message(AdminStates.choose_event_for_stat, F.text == "Назад")
async def back_from_choose_event_for_stat(message: Message, state: FSMContext):
    await admin_menu(message, state)

@dp.message(AdminStates.choose_event_for_stat)
async def show_stat(message: Message, state: FSMContext):
    event = message.text
    markup = chat_backends.create_keyboard_buttons("Направить напоминания","Получить статистику по другому мероприятию", "Вернуться в меню")
    await message.answer(f'Статистика по мероприятию «{event}»/n/n'
                         f'Программная дирекция:/n'
                         f'Анастасия Быковская — 1/2 фотографий/n'
                         f'Татьяна Тенькова — 2/2 фотографий/n/n'
                         f'Техническая дирекция:/n'
                         f'Александр Соломин — 0/6 фотографий/n/n'
                         f'Вы можете направить напоминания сотрудникам, загрузившим не все фотографии', reply_markup=markup)
    await state.set_state(AdminStates.stat_ends)

@dp.message(AdminStates.choose_event_for_stat, F.text == "Направить напоминания")
async def send_mailing_from_stat(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Получить статистику по другому мероприятию", "Вернуться в меню")
    await message.answer(f'Рассылка отправлена!', reply_markup=markup)

@dp.message(AdminStates.choose_event_for_stat, F.text == "Получить статистику по другому мероприятию")
async def choose_another_event_for_stat(message: Message, state: FSMContext):
    await choose_event_for_stat(message, state)

@dp.message(AdminStates.choose_event_for_stat, F.text == "Вернуться в меню")
async def back_to_admin_menu_from_show_stat(message: Message, state: FSMContext):
    await admin_menu(message, state)

