from aiogram.fsm.state import State, StatesGroup


class FSMSetServiceData(StatesGroup):
    input_service_name = State()
    input_login = State()
    input_password = State()
    exists_service = State()


class FSMGetServiceData(StatesGroup):
    get_service_data = State()


class FSMDelServiceData(StatesGroup):
    del_service_data = State()
