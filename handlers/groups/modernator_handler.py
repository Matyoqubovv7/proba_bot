from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

router.message.filter(F.chat.type.in_({"group", "supergroup"}), F.new_chat_members)

@router.message(F.new_chat_members)
async def welcome_handler(message: Message):
    for i in message.new_chat_members:
        await message.reply(f"Salom @{i.username}! guruhga xush kelibsiz")


@router.message(F.left_chat_member)
async def left_member_handler(message: Message):
    await message.delete()
    await.message.answer(f"@{message.left_chat_member.username} bizni yosh tark etdi")


@router.message(F.text.regexp("reklama","dnx"))
async def haqoratli_suzlar(message: Message):
    await message.delete()
    await.message.answer(f"@{message.from_user.username} haqoratli suzlarni ishlatma!")
