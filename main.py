from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import json, os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

USERS_FILE = "users.json"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    users = load_users()
    if message.from_user.id not in users:
        users.append(message.from_user.id)
        save_users(users)
    await message.answer("Вы подписаны на обновления.")

@dp.channel_post_handler()
async def forward_channel(message: types.Message):
    users = load_users()
    for uid in users:
        try:
            await message.forward(uid)
        except:
            pass

executor.start_polling(dp)
