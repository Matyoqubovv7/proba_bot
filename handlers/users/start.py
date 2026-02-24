from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()
router.message.filter(F.chat.type == "private")

@router.message(CommandStart())
async def bot_start(message: Message):
    await message.answer("Salom 👋")
