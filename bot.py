import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

# ====== Настройки ======
BOT_TOKEN = os.getenv("BOT_TOKEN")       # Токен бота
ADMIN_ID = os.getenv("ADMIN_ID")         # Telegram ID администратора

if not BOT_TOKEN:
    raise ValueError("❌ Переменная BOT_TOKEN не задана!")

ADMIN_ID = int(ADMIN_ID) if ADMIN_ID and ADMIN_ID.isdigit() else None

GROUP_LINK = "https://t.me/+S8yADtnHIRhiOGNi"  # 🔗 Новая ссылка на группу ожидания

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ====== FSM для анкеты ======
class Form(StatesGroup):
    age = State()
    game_id = State()
    screenshot = State()

# ====== Веб сервер для Render ======
async def handle(request):
    return web.Response(text="Bot is running 🚀")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)
    port = int(os.getenv("PORT", 8000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Web server running on port {port}")

# ====== Хэндлеры бота ======
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Да"), KeyboardButton(text="❌ Нет")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "🍀 Привет! Хочешь оставить заявку на вступление в клан?",
        reply_markup=keyboard
    )

@dp.message(F.text == "✅ Да")
async def ask_age(message: types.Message, state: FSMContext):
    await state.set_state(Form.age)
    await message.answer(
        "✅ Отлично! Сколько тебе лет? 🔞",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dp.message(F.text == "❌ Нет")
async def cancel_form(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "😌 Хорошо. Возможно, твоя харизма ещё раскрывается. Успех любит время. ☘️",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dp.message(Form.age)
async def ask_game_id(message: types.Message, state: FSMContext):
    await state.update_data
