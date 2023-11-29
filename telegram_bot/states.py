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

    enter_event_name = State()
    confirm_event_name = State()
    upload_list_of_participants = State()
    confirm_list_uploaded = State()
    enter_dateframe_for_preparing = State()
    enter_start_event_date = State()


class StaffStates(StatesGroup):
    main = State()
