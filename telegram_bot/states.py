from aiogram.fsm.state import StatesGroup, State


class MainMenuStates(StatesGroup):
    registration = State()


class AdminStates(StatesGroup):
    main = State()

    choose_event_for_stat = State()
    stat_ends = State()

    choose_event_for_mailing = State()
    begin_mailing = State()
    mailing_with_text = State()
    mailing_with_photo = State()
    mailing_with_file = State()

    manage_event = State()


class StaffStates(StatesGroup):
    main = State()
