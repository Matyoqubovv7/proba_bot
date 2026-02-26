from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.db import save_registration


router = Router()
router.message.filter(F.chat.type == "private")


class RegistrationStates(StatesGroup):
    choosing_role = State()
    full_name = State()
    age = State()
    phone = State()
    extra = State()
    confirm = State()


def role_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="O'quvchi", callback_data="role_student"),
                InlineKeyboardButton(text="O'qituvchi", callback_data="role_teacher"),
            ]
        ]
    )


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="confirm_save"),
                InlineKeyboardButton(text="Bekor qilish ❌", callback_data="cancel_save"),
            ]
        ]
    )


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Iltimos, rolingizni tanlang:", reply_markup=role_keyboard())
    await state.set_state(RegistrationStates.choosing_role)


@router.callback_query(F.data.in_(["role_student", "role_teacher"]), RegistrationStates.choosing_role)
async def process_role(callback: CallbackQuery, state: FSMContext):
    role = "o'quvchi" if callback.data == "role_student" else "o'qituvchi"
    await state.update_data(role=role)
    await callback.message.edit_text(f"Siz: <b>{role}</b> sifatida ro'yxatdan o'tmoqdasiz.\n\nIsm-familiyangizni kiriting:")
    await state.set_state(RegistrationStates.full_name)
    await callback.answer()


@router.message(RegistrationStates.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer("Yoshingizni kiriting (faqat son):")
    await state.set_state(RegistrationStates.age)


@router.message(RegistrationStates.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Yoshni faqat son ko'rinishida kiriting, masalan: 18")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Telefon raqamingizni kiriting (masalan: +99890xxxxxxx):")
    await state.set_state(RegistrationStates.phone)


@router.message(RegistrationStates.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    data = await state.get_data()
    if data.get("role") == "o'quvchi":
        text = "Qaysi sinfda o'qiysiz? (masalan: 9A)"
    else:
        text = "Qaysi fanlardan dars berasiz?"
    await message.answer(text)
    await state.set_state(RegistrationStates.extra)


@router.message(RegistrationStates.extra)
async def process_extra(message: Message, state: FSMContext):
    await state.update_data(extra=message.text.strip())
    data = await state.get_data()

    summary = (
        "Quyidagi ma'lumotlar kiritildi:\n\n"
        f"Rol: <b>{data.get('role')}</b>\n"
        f"F.I.Sh: <b>{data.get('full_name')}</b>\n"
        f"Yosh: <b>{data.get('age')}</b>\n"
        f"Telefon: <b>{data.get('phone')}</b>\n"
    )

    if data.get("role") == "o'quvchi":
        summary += f"Sinf: <b>{data.get('extra')}</b>\n"
    else:
        summary += f"Fan(lar): <b>{data.get('extra')}</b>\n"

    summary += "\nMa'lumotlar to'g'rimi?"

    await message.answer(summary, reply_markup=confirm_keyboard())
    await state.set_state(RegistrationStates.confirm)


@router.callback_query(F.data == "confirm_save", RegistrationStates.confirm)
async def process_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    save_registration(
        telegram_id=callback.from_user.id,
        role=data.get("role", ""),
        full_name=data.get("full_name", ""),
        age=int(data.get("age", 0)),
        phone=data.get("phone", ""),
        extra=data.get("extra", ""),
    )

    await state.clear()
    await callback.message.edit_text("Ma'lumotlar bazaga muvaffaqiyatli saqlandi ✅")
    await callback.answer()


@router.callback_query(F.data == "cancel_save", RegistrationStates.confirm)
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Ro'yxatdan o'tish bekor qilindi.")
    await callback.answer()

