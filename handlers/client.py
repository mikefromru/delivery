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

import fpdf

client = Router()

class Form(StatesGroup):

    description = State()
    weight = State()
    size = State()
    from_address = State()
    to_address = State()
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
    await state.set_state(Form.from_address)
    await message.answer('type the from address')


@client.message(Form.from_address)
async def process_name(message: Message, state: FSMContext) -> None:
    data = await state.update_data(from_address=message.text)
    await state.set_state(Form.to_address)
    await message.answer('type the to address')


@client.message(Form.to_address)
async def process_name(message: Message, state: FSMContext) -> None:
    data = await state.update_data(to_address=message.text)
    await state.set_state(Form.method_pay)
    await message.answer('type the method pay')


@client.message(Form.method_pay)
async def process_name(message: Message, state: FSMContext) -> None:
    data = await state.update_data(method_pay=message.text)
    await state.clear()
    await show_summary(message=message, data=data)

        
async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    description = data.get('description')
    weight = data.get('weight')
    size = data.get('size')
    from_address = data.get('from_address')
    to_address = data.get('to_address')
    method_pay = data.get('method_pay')

    text = f'Description is {html.bold(description)}\n'
    text += f'Weight is {html.bold(weight)}\n'
    text += f'Size is {html.bold(size)}\n'
    text += f'Delivery from {html.bold(from_address)}\n'
    text += f'Delivery to {html.bold(to_address)}\n'
    text += f'Method to pay is {html.bold(method_pay)}'

    await message.answer(text=text)
    write_pdf(description, weight, size, from_address, to_address, method_pay)

def write_pdf(description, weight, size, from_address, to_address, method_pay):
    import os
    pdf = fpdf.FPDF(format='letter') #pdf format
    pdf.add_page() #create new page
    path = os.path.abspath('handlers/OpenSans-Bold.ttf')
    # pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('OpenSans', '', path, uni=True)
    pdf.set_font('OpenSans', size=12) # font and textsize
    pdf.cell(200, 10, txt='Документ', ln=1, align='T')
    pdf.cell(200, 10, txt=f'Описание груза - {description}', ln=2, align='L')
    pdf.cell(200, 10, txt=f'Вес груза - {weight}', ln=2, align='L')
    pdf.cell(200, 10, txt=f'Габариты груза - {size}', ln=2, align='L')
    pdf.cell(200, 10, txt=f'Точный адрес отправки - {from_address}', ln=2, align='L')
    pdf.cell(200, 10, txt=f'Точный адрес получения - {to_address}', ln=2, align='L')
    pdf.cell(200, 10, txt=f'Способ оплаты - {method_pay}', ln=3, align='L')
    pdf.output('Накладная.pdf')


# def write_pdf(description, weight, size, from_address, to_address):
#     pdf = fpdf.FPDF(format='letter') #pdf format
#     pdf.add_page() #create new page
#     pdf.set_font("Arial", size=12) # font and textsize
#     pdf.cell(200, 10, txt='Накладная', ln=1, align='R')
#     pdf.cell(200, 10, txt=f'Описание груза\n{description}', ln=2, align='L')
#     pdf.cell(200, 10, txt=f'Вес груза - {weight}', ln=2, align='L')
#     pdf.cell(200, 10, txt=f'Габариты груза - {size}', ln=2, align='L')
#     pdf.cell(200, 10, txt=f'Адрес отправки - {from_address}', ln=2, align='L')
#     pdf.cell(200, 10, txt=f'Адрес получателя - {to_address}', ln=3, align='L')
#     pdf.output('nacladnay.pdf')
