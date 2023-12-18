import logging
from aiogram import Router, html, F, Bot
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
import os
import fpdf

order_router = Router()

class Form(StatesGroup):

    description = State()
    weight = State()
    size = State()
    from_address = State()
    to_address = State()
    method_pay = State()


@order_router.message(Command('delivery'))
async def cmd_delivery(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.description)
    await message.answer(text='Напишите описание груза',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Отменить составление накладной'),
                ]
            ],
            resize_keyboard=True,
        ),

    )


@order_router.message(Command("cancel"))
@order_router.message(F.text.casefold() == 'отменить составление накладной')
async def cancel_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    print('order.py')
    data = await state.get_data()
    
    text = 'Была отмена составления накладной\n' 
    text += f'Описание груза - {data.get("description")}\n'
    text += f'Вес - {data.get("weight")}\n'
    text += f'Габариты груза - {data.get("size")}\n'
    text += f'Место отправления - {data.get("from_address")}\n'
    text += f'Место назначения - {data.get("to_address")}\n'
    text += f'Способ оплаты - {data.get("method_pay")}\n'
    
    await state.clear()
    await bot.send_message(chat_id=os.getenv('MANAGER'), text=text) # send to manager
    await message.answer(
        'Отмена.',
        reply_markup=ReplyKeyboardRemove(),
    )


@order_router.message(Form.description)
async def process_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(Form.weight)
    await message.answer('Вес груза')


@order_router.message(Form.weight)
async def process_weight(message: Message, state: FSMContext) -> None:
    await state.update_data(weight=message.text)
    await state.set_state(Form.size)
    await message.answer('Габариты груза')


@order_router.message(Form.size)
async def process_size(message: Message, state: FSMContext) -> None:
    await state.update_data(size=message.text)
    await state.set_state(Form.from_address)
    await message.answer('Точный адрес отправки')


@order_router.message(Form.from_address)
async def process_from_address(message: Message, state: FSMContext) -> None:
    data = await state.update_data(from_address=message.text)
    await state.set_state(Form.to_address)
    await message.answer('Точный адрес получателя')


@order_router.message(Form.to_address)
async def process_to_address(message: Message, state: FSMContext) -> None:
    data = await state.update_data(to_address=message.text)
    await state.set_state(Form.method_pay)
    await message.answer('Способ оплаты')


@order_router.message(Form.method_pay)
async def process_method_pay(message: Message, state: FSMContext) -> None:
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
    await message.answer(text='Данные сохранены в PDF файл Накладная.pdf')
    write_pdf(description, weight, size, from_address, to_address, method_pay)

def write_pdf(description, weight, size, from_address, to_address, method_pay):
    import os
    pdf = fpdf.FPDF(format='letter') #pdf format
    pdf.add_page() #create new page
    path = os.path.abspath('handlers/OpenSans-Bold.ttf')
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
