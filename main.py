import asyncio
import logging
import sys
import redis
from os import getenv
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

TOKEN = "1123060936:AAEH-cHbw3LAo4GFwCGZWvH-tSps1fXeOFQ"

#  instantiate a redis connection

REDIS_CLOUD_HOST = 'redis-16278.c321.us-east-1-2.ec2.cloud.redislabs.com'
REDIS_CLOUD_PORT = 16278
REDIS_CLOUD_PASSWORD = 'm8eVuVcmR7nrXGq07IIhiTyOxa526w6N'

redis_connection = redis.StrictRedis(
    host=REDIS_CLOUD_HOST,
    port=REDIS_CLOUD_PORT,
    password=REDIS_CLOUD_PASSWORD,
    decode_responses=True,
) 


form_router = Router()

# ask user to login or input user name and password as a new user using buttons
# if user is new, ask for user name and password
# if user is old, ask for user name and password
# if user is old and password is wrong, ask for user name and password
# if user is old and password is correct, show the menu

class Form(StatesGroup):
    Register = State()  # ask for user name and password


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    user_id = message.chat.id

    # check if user is already registered in redis welcome and if not ask user to register using registor button

    if not redis_connection.exists(user_id):
        await message.answer(
            "Hi there! Please register first",
            reply_markup=ReplyKeyboardMarkup(keyboard=
                [
                    [KeyboardButton(text="Register")],
                ],
                resize_keyboard=True,
            ),
        )
        await state.set_state(Form.Register)
        # register user Id in redis
        # redis_connection.set(user_id, "welcome")
    else:
        await message.answer(
            "Hi there! What do you want to do?",
            reply_markup=ReplyKeyboardMarkup(keyboard=
                [
                    [KeyboardButton(text="Book a ride")],
                    [KeyboardButton(text="Show history")],
                    
                ],
                resize_keyboard=True,
            ),
        )

       
async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())