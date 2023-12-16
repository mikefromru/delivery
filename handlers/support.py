import logging
from aiogram import Router, html, F, Bot
from aiogram.filters import Command 
from aiogram.types import Message
from typing import Any, Dict
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramAPIError

import os


from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


support_router = Router()

@support_router.message(Command('support'))
async def cmd_manager(message: Message, bot: Bot) -> None:
    await bot.send_message(chat_id=os.getenv('MANAGER'), text='Вызов в чат!') # send to manager
    await message.answer(text='Задайте мне ваши вопросы',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Закончить'),
                ]
            ],
            resize_keyboard=True,
        ),

    )