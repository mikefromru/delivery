import asyncio
from aiogram import Router
from aiogram.filters import Command 
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram import Bot


menu = Router()

@menu.message(Command('start'))
async def cmd_start(message: Message):
    await message.reply('Start command')


@menu.message(Command('description'))
async def cmd_description(message: Message):
    await message.reply('Description command')
