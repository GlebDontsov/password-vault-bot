from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from services.services import encrypt_password, decrypt_password, delete_message
from keyboards.keyboards import keyboard_yes_no
from lexicon.lexicon_ru import LEXICON_RU
from states.states import FSMSetServiceData, FSMGetServiceData, FSMDelServiceData
from aiogram.fsm.context import FSMContext
from bot import db

router: Router = Router()
delay: int = 60


@router.message(CommandStart())
async def process_start_command(message: Message):
    if not db.existsUser(message.from_user.id):
        user_id = message.from_user.id
        db.addUser(user_id=user_id,
                   first_name=message.from_user.first_name,
                   last_name=message.from_user.last_name)
        db.createTableServiceData(user_id)
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands=['get']))
async def process_get_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['get_service_data'])
    await state.set_state(FSMGetServiceData.get_service_data)


@router.message(Command(commands=['del']))
async def process_set_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['del_service_data'])
    await state.set_state(FSMDelServiceData.del_service_data)


@router.message(Command(commands=['set']))
async def process_set_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['input_name_service'])
    await state.set_state(FSMSetServiceData.input_service_name)


@router.message(Command(commands=['services']))
async def process_services_command(message: Message):
    list_services = [item[0] for item in db.getServices(message.from_user.id)]
    if list_services:
        str_services = "\n".join(list_services)
        await message.answer(text=str_services)
    else:
        await message.answer(text=LEXICON_RU['empty_storage'])


@router.message(FSMGetServiceData.get_service_data)
async def process_get_service_date(message: Message, state: FSMContext):
    service_name = message.text
    if db.existsServiceData(user_id=message.from_user.id, service_name=service_name):
        service_data = db.getServiceData(user_id=message.from_user.id, service_name=service_name)
        sent_message = await message.answer(text=f'Сервис: {service_name}\n'
                                                 f'Логин: {service_data[0]}\n'
                                                 f'Пароль {decrypt_password(service_data[1])}')
        await delete_message(sent_message, delay)
    else:
        await message.answer(text=LEXICON_RU['info_not_exist'])
    await state.clear()


@router.message(FSMSetServiceData.input_service_name)
async def process_input_name_service(message: Message, state: FSMContext):
    data = {'service_name': message.text}
    await state.update_data(data)
    await message.answer(text=LEXICON_RU['input_login'])
    await state.set_state(FSMSetServiceData.input_login)


@router.message(FSMSetServiceData.input_login)
async def process_input_login(message: Message, state: FSMContext):
    data = await state.get_data()
    data['login'] = message.text
    await state.update_data(data)
    await message.answer(text=LEXICON_RU['input_password'])
    await state.set_state(FSMSetServiceData.input_password)


@router.message(FSMSetServiceData.input_password)
async def process_set_data(message: Message, state: FSMContext):
    data = await state.get_data()
    data['password'] = encrypt_password(message.text)
    await state.update_data(data)
    await message.delete()

    if not db.existsServiceData(user_id=message.from_user.id, service_name=data['service_name']):
        db.setServiceData(user_id=message.from_user.id,
                          service_name=data['service_name'],
                          login=data['login'],
                          password=data['password'])
        await message.answer(text=LEXICON_RU['done'])
        await state.clear()
    else:
        await message.answer(text=LEXICON_RU['exists_service'], reply_markup=keyboard_yes_no)
        await state.set_state(FSMSetServiceData.exists_service)


@router.message(FSMSetServiceData.exists_service)
async def process_confirmation_changes(message: Message, state: FSMContext):
    text = message.text.lower()
    if text not in ('да', 'нет'):
        return await message.answer(text=LEXICON_RU['repeat_answer'])
    if text == 'да':
        data = await state.get_data()
        db.updateServiceData(user_id=message.from_user.id,
                             login=data['login'],
                             password=data['password'],
                             service_name=data['service_name'])
        await message.answer(text=LEXICON_RU['data_changed'])
    await state.clear()


@router.message(FSMDelServiceData.del_service_data)
async def process_del_service_date(message: Message, state: FSMContext):
    db.delServiceData(user_id=message.from_user.id,
                      service_name=message.text)
    await message.answer(text=LEXICON_RU['data_deleted'])
    await state.clear()
