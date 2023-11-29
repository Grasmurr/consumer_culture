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
from telegram_bot.handlers.admin_panel.manage_event import manage_event

from telegram_bot.assets.configs import config
import datetime


@dp.message(AdminStates.manage_event, F.text == "Создать мероприятие")
async def enter_event_name(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Назад")
    await message.answer("Введите название мероприятия", reply_markup=markup)
    await state.set_state(AdminStates.enter_event_name)


@dp.message(AdminStates.enter_event_name, F.text == "Назад")
async def back_from_enter_event_name(message: Message, state: FSMContext):
    await manage_event(message, state)


@dp.message(AdminStates.enter_event_name)
async def confirm_event_name(message: Message, state: FSMContext):
    name_of_event = message.text
    markup = chat_backends.create_keyboard_buttons('Да', 'Назад')
    await message.answer(f'Вы хотите создать мероприятие «{name_of_event}». Продолжить?',
                         reply_markup=markup)
    await state.update_data(name=name_of_event)
    await state.set_state(AdminStates.confirm_event_name)


@dp.message(AdminStates.confirm_event_name, F.text == "Назад")
async def back_from_confirm_event_name(message: Message, state: FSMContext):
    await enter_event_name(message, state)


@dp.message(AdminStates.confirm_event_name, F.text == "Да")
async def upload_list_of_participants(message: Message, state: FSMContext):
    await state.get_data()
    markup = chat_backends.create_keyboard_buttons("Назад")
    await message.answer(f'Пожалуйста загрузите реестр исполнителей по мероприятию {data["name"]}/n/n'
                         f'- Формат xlsx/n'
                         f'- Столбцы: /n'
                         f'1) Должность согласно ТЗ/n'
                         f'2) ФИО/n'
                         f'3) Дата начала работы/n'
                         f'4) Необходимое количество фотографий "в работе"/n'
                         f'5) Необходимое количество фотографий "на площадке"'  # чтобы можно было также сообщать если
                         # фотографий недостаточно
                         , reply_markup=markup)
    await state.set_state(AdminStates.upload_list_of_participants)


@dp.message(AdminStates.upload_list_of_participants, F.text == "Назад")
async def back_from_upload_list_of_participants(message: Message, state: FSMContext):
    await confirm_event_name(message, state)


@dp.message(AdminStates.upload_list_of_participants, F.document)
async def confirm_list_uploaded(message: Message, state: FSMContext):
    file_id = message.document.file_id
    await state.update_data(mailing_type='Файл', file_id=file_id)
    markup = chat_backends.create_keyboard_buttons("Продолжить", "Назад")
    await message.answer('Если вы загрузили неправильный файл, нажмите кнопку "Назад" ниже./n/n'
                         'Для продолжение создания мероприятия нажмите "Продолжить".')
    await state.set_state(AdminStates.confirm_list_uploaded)


@dp.message(AdminStates.upload_list_of_participants)
async def wrong_upload_list_of_participants(message: Message, state: FSMContext):
    await message.answer("Кажется, вы прислали не файл или нажали не туда. Пожалуйста, "
                         "пришлите реестр исполнителей в формате xslx.")
    await upload_list_of_participants(message, state)


@dp.message(AdminStates.upload_list_of_participants, F.text == "Продолжить")
async def enter_dateframe_for_preparing(message: Message, state: FSMContext):
    await message.answer('Введите дату начала подготовки мероприятия '
                         '(минимальная дата, которую могут указывать исполнители).')
    await state.set_state(AdminStates.enter_dateframe_for_preparing)


@dp.message(AdminStates.upload_list_of_participants, F.text)
async def enter_start_event_date(message: Message, state: FSMContext):
    try:
        event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
        start_preparing_date = event_date.strftime('%Y-%m-%d')
        await state.update_data(start_preparing_date=start_preparing_date)
        await message.answer(f'Вы установили {start_preparing_date} в качестве самой '
                             f'ранней даты начала работы./n/n'
                             f'Теперь введите дату, начиная с которой работа будет '
                             f'квалифицироваться как работа на площадке')
        await state.set_state(AdminStates.enter_start_event_date)
    except ValueError:
        await message.answer('Пожалуйста, введите дату в формате YYYY-MM-DD. Например: 2023-10-29')


@dp.message(AdminStates.enter_start_event_date)
async def enter_start_event_date(message: Message, state: FSMContext):
    try:
        event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
        start_event_date = event_date.strftime('%Y-%m-%d')
        await state.update_data(start_event_date=start_event_date)
        await message.answer(f'Вы установили {start_event_date} в качестве '
                             f'даты начала работы на площадке. /n/n'
                             f'Теперь введите дату окончания мероприятия '
                             f'(если мероприятие длится один день, напишите ту же дату, что и в предыдущем пункте)')
        await state.set_state(AdminStates.enter_start_event_date)
    except ValueError:
        await message.answer('Пожалуйста, введите дату в формате YYYY-MM-DD. Например: 2023-10-29')
