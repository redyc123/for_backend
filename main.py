from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

import asyncio

from money import monyes

from user import User

from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user = User()
current_kb = [[
           types.KeyboardButton(text="/info_moneys"),
           types.KeyboardButton(text="/moneys_menu"),
           types.KeyboardButton(text="/check_history")
       ]]

@dp.message_handler(commands="check_history")
async def check_history(message: types.Message):
    user_id = str(message["from"]["id"])
    print(await user.read_table(user_id))
    text = list(await user.read_table(user_id))[5]
    user_name = message['from']["first_name"]
    await message.answer(f'история запросов пользователя {user_name}:\n{text}')

@dp.message_handler(commands=["change_bitcoin", "change_ethereum"])
async def change_money(message: types.Message):
    user_id = str(message["from"]["id"])
    text = await user.change_money(message["text"], user_id)
    await message.answer(f'{text}')

@dp.message_handler(commands="moneys_menu")
async def moneys_menu(message: types.Message):
    kb = [
       [
           types.KeyboardButton(text="/change_bitcoin"),
           types.KeyboardButton(text="/change_ethereum"),
           types.KeyboardButton(text="/back")
       ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("настройка отображаемых валют", reply_markup=keyboard)

@dp.message_handler(commands=["bitcoin", "ethereum"])
async def bitcoin_info(message: types.Message):
    user_id = str(message["from"]["id"])
    count = list(await user.read_table(user_id))[6]
    banned = list(await user.read_table(user_id))[3]
    user.ban_time = list(await user.read_table(user_id))[4]
    count += 1
    user.user_count = count
    ban = await user.ban(count=count, user_id=user_id)
    if ban == True or banned == 1:
        await message.answer(f"вы слишком много обращались к просмотру валют осталось ждать {int((600 - user.ban_time)/60)} минут до возвращения функционала")
        return
        
    print(ban)
    money = message["text"][1:]
    text = f'цена {money}:{monyes[money]}$'
    user.history = list(await user.read_table(user_id))[5] + text + "\n"
    await user.change_history(user.history, user_id)
    await message.answer(text)

@dp.message_handler(commands="back")
async def back(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=current_kb)
    await message.answer("вы вернулись назад", reply_markup=keyboard)

@dp.message_handler(commands="info_moneys")
async def main(message: types.Message):
    user_id = str(message["from"]["id"])
    user_buttons = list(await user.read_table(user_id))
    eth = types.KeyboardButton(text="/ethereum")
    btc = types.KeyboardButton(text="/bitcoin")
    back = types.KeyboardButton(text="/back")
    kb = [[btc, eth ,back]]
    if int(user_buttons[1]) == 1:
        if btc not in kb[0]:
            kb[0].append(btc)
    else:
        kb[0].remove(btc)
    if int(user_buttons[2]) == 1:
        if eth not in kb[0]:
            kb[0].append(eth)
    else:
        kb[0].remove(eth)
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("это список доступных валют", reply_markup=keyboard)

@dp.message_handler(commands="start")
async def main(message: types.Message):
    print(message)
    user_id = str(message["from"]["id"])
    try:
        user_in_db = await user.read_table(user_id)
        print(user_in_db)
    except:
        await user.add_user_db(user_id)
    kb = [
       [
           types.KeyboardButton(text="/info_moneys"),
           types.KeyboardButton(text="/moneys_menu"),
           types.KeyboardButton(text="/check_history")
       ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    user_name = message['from']["first_name"]
    await message.answer(f"Привет {user_name}, мой бот создан для просмотра цен криптовалют", reply_markup=keyboard)

@dp.message_handler()
async def messsage(message: types.Message):
    await message.answer("Выберете команду из пункта меню!")

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    executor.start_polling(dp, skip_updates=True)