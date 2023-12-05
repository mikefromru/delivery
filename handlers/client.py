import asyncio
import logging
from aiogram import Router, html, F
from aiogram.filters import Command 
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
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


client = Router()

class Form(StatesGroup):

    description = State()
    weight = State()
    size = State()
    from_adress = State()
    to_adress = State()
    method_pay = State()


@client.message(Command('delivery'))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.description)
    await message.answer(text='Напишите описание груза?',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Cancel"),
                ]
            ],
            resize_keyboard=True, one_time_keyboard=False,
        ),

    )

@client.message(Command("cancel"))
@client.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@client.message(Form.description)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(Form.weight)
    await message.answer('ty[e the weight]')


@client.message(Form.weight)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(weight=message.text)
    await state.set_state(Form.size)
    await message.answer('type the size')


@client.message(Form.size)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(size=message.text)
    await state.set_state(Form.from_adress)
    await message.answer('type the from adress')


@client.message(Form.from_adress)
async def process_name(message: Message, state: FSMContext) -> None:
    data = await state.update_data(from_adress=message.text)
    await state.set_state(Form.to_adress)
    await message.answer('type the to adress')


@client.message(Form.to_adress)
async def process_name(message: Message, state: FSMContext) -> None:
    data = await state.update_data(to_adress=message.text)
    await state.set_state(Form.method_pay)
    await message.answer('type the method pay')


@client.message(Form.method_pay)
async def process_name(message: Message, state: FSMContext) -> None:
    data = await state.update_data(method_py=message.text)
    await state.clear()
    await show_summary(message=message, data=data)

        
async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    description = data.get('description')
    weight = data.get('weight')
    size = data.get('size')
    from_adress = data.get('from_adress')
    to_adress = data.get('to_adress')
    method_pay = data.get('method_pay')

    text = f'Description is {html.bold(description)}\n'
    text += f'Weight is {html.bold(weight)}\n'
    text += f'Size is {html.bold(size)}\n'
    text += f'Delivery from {html.bold(from_adress)}\n'
    text += f'Delivery to {html.bold(to_adress)}\n'
    text += f'Method to pay is {html.bold(method_pay)}'

    await message.answer(text=text)