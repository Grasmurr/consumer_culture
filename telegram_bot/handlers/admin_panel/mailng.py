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


@dp.message(AdminStates.main, F.text == "Отправить рассылку")
async def choose_event_for_mailing(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Небо — 2023", "Неделя дизайна — 2022", "Назад")
    await state.set_state(AdminStates.choose_event_for_mailing)
    await message.answer('Выберите, для сотрудников какого мероприятия вы хотите сделать рассылку', reply_markup=markup)


@dp.message(AdminStates.choose_event_for_mailing, F.text == "Назад")
async def back_from_choose_event_for_mailing(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.choose_event_for_mailing, F.text == "Назад")
async def start_mailing(message: Message, state: FSMContext):
    buttons = chat_backends.create_keyboard_buttons('Текст', 'Фото', 'Файл', 'Назад')
    await message.answer('Хорошо! Выберите в каком формате вы хотите отправить рассылку:', reply_markup=buttons)
    await state.set_state(AdminStates.begin_mailing)


@dp.message(AdminStates.begin_mailing, F.text == 'Назад')
async def back_to_admin_menu(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.begin_mailing)
async def back_to_admin_menu(message: Message, state: FSMContext):
    type_to_mail = message.text
    if type_to_mail not in ['Текст', 'Фото', 'Файл']:
        buttons = chat_backends.create_keyboard_buttons('Текст', 'Фото', 'Файл', 'Назад')
        await message.answer('Кажется, вы выбрали что-то не из кнопок. Пожалуйста, воспользуйтесь кнопкой ниже:',
                             reply_markup=buttons)
        return
    buttons = chat_backends.create_keyboard_buttons('Назад')
    if type_to_mail == 'Текст':
        await state.set_state(AdminStates.mailing_with_text)
        await message.answer('Хорошо! Отправьте текст, который вы собираетесь отправить представителям:',
                             reply_markup=buttons)
    elif type_to_mail == 'Фото':
        await state.set_state(AdminStates.mailing_with_photo)
        await message.answer('Хорошо! Отправьте фото, которое вы собираетесь отправить представителям (с подписью):',
                             reply_markup=buttons)
    else:
        await state.set_state(AdminStates.mailing_with_file)
        await message.answer('Хорошо! Отправьте файл, который вы собираетесь отправить представителям (с подписью):',
                             reply_markup=buttons)


@dp.message(AdminStates.mailing_with_photo, F.text == 'Назад')
async def back_to_start_mailing(message: Message, state: FSMContext):
    await start_mailing(message, state)


@dp.message(AdminStates.mailing_with_text, F.text == 'Назад')
async def back_to_start_mailing(message: Message, state: FSMContext):
    await start_mailing(message, state)


@dp.message(AdminStates.mailing_with_file, F.text == 'Назад')
async def back_to_start_mailing(message: Message, state: FSMContext):
    await start_mailing(message, state)


@dp.message(AdminStates.mailing_with_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    caption = message.caption
    await state.update_data(mailing_type='Фото', photo_id=photo_id, caption=caption)
    buttons = chat_backends.create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите разослать такое фото с такой подписью?', reply_markup=buttons)
    await message.answer_photo(photo=photo_id, caption=caption)


@dp.message(AdminStates.mailing_with_file, F.document)
async def handle_photo(message: Message, state: FSMContext):
    file_id = message.document.file_id
    caption = message.caption
    await state.update_data(mailing_type='Файл', file_id=file_id, caption=caption)
    buttons = chat_backends.create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите разослать такой файл с такой подписью?', reply_markup=buttons)
    await message.answer_document(document=file_id, caption=caption)


@dp.message(AdminStates.mailing_with_text, F.text == 'Подтвердить')
async def handle_text(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.mailing_with_text)
async def handle_text(message: Message, state: FSMContext):
    ans = message.text
    await state.update_data(mailing_type='Текст', text_to_mail=ans)
    buttons = chat_backends.create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите разослать такой текст?', reply_markup=buttons)
    await message.answer(ans)


@dp.message(AdminStates.mailing_with_file, F.text == 'Подтвердить')
async def start_file_mailing(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.mailing_with_photo, F.text == 'Подтвердить')
async def start_photo_mailing(message: Message, state: FSMContext):
    await admin_menu(message, state)
