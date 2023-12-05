import asyncio
from aiogram import Router
from aiogram.filters import Command 
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram import Bot


client = Router()

@client.message(Command('delivery'))
async def cmd_start(message: Message):
    await message.reply('Delivery func')

