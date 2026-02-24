from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()
router.message.filter(F.chat.type == "private")

@router.message(Command("help"))
async def bot_help(message: Message):
    await message.answer("Yordam bo‘limi")
