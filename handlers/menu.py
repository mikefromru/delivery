from aiogram import Router
from aiogram.filters import Command 
from aiogram.types import Message


menu = Router()


desc_message = '''
<b>Это компания Delivery Ok!</b>
Мы доставляем грузы по всем странам СНГ. На рынке более 10 лет!
Оформите груз и мы позаботимся о его целостности и доставим в указанный срок!
'''

@menu.message(Command('start'))
async def cmd_start(message: Message):
    await message.reply('Start command')


@menu.message(Command('description'))
async def cmd_description(message: Message):
    await message.reply(desc_message)
