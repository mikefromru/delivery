import logging
from aiogram import Router, html, F
from aiogram.filters import Command 
from aiogram.types import Message
from typing import Any, Dict
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


complaint_router = Router()

class FormComplaint(StatesGroup):

    number = State()
    email = State()
    description = State()
    money = State()
    photo = State()


@complaint_router.message(Command('complaint'))
async def cmd_complaint(message: Message, state: FSMContext) -> None:
    await state.set_state(FormComplaint.number)
    await message.answer(text='Введите номер накладной',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Отменить'),
                ]
            ],
            resize_keyboard=True,
        ),

    )


@complaint_router.message(Command("cancel"))
@complaint_router.message(F.text.casefold() == 'отменить')
async def complaint_cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        'Отмена.',
        reply_markup=ReplyKeyboardRemove(),
    )


@complaint_router.message(FormComplaint.number)
async def complaint_process_number(message: Message, state: FSMContext) -> None:
    await state.update_data(number=message.text)
    await state.set_state(FormComplaint.email)
    await message.answer('Напишите ваш E-mail. Мы отправим ответ')


@complaint_router.message(FormComplaint.email)
async def complaint_process_email(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(FormComplaint.description)
    await message.answer('Опишите ситуацию')


@complaint_router.message(FormComplaint.description)
async def complaint_process_description_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FormComplaint.money)
    await message.answer('Требуемая сумма')


@complaint_router.message(FormComplaint.money)
async def complaint_process_money(message: Message, state: FSMContext) -> None:
    data = await state.update_data(money=message.text)
    await state.set_state(FormComplaint.photo)
    await message.answer('Фото/сканы')


@complaint_router.message(FormComplaint.photo)
async def complaint_process_photo(message: Message, state: FSMContext) -> None:
    data = await state.update_data(photo=message.text)
    await state.clear()
    await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    number = data.get('number')
    email = data.get('email')
    description = data.get('description')
    money = data.get('money')
    photo = data.get('photo')

    text = f'Номер накладной: {html.bold(number)}\n'
    text += f'Email: {html.bold(email)}\n'
    text += f'Описание претензии: {html.bold(description)}\n'
    text += f'Требуемая сумма: {html.bold(money)}\n'
    text += f'Фото/сканы: {html.bold(photo)}\n'

    await message.answer(text=text)
    await message.answer(text='Ваша жалоба будет рассмотрена в ближайшее время!')