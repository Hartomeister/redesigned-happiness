from aiogram import Bot, Dispatcher, executor, types #слито в @smoke_software
from keyboard import *
import sqlite3
import datetime
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import random
from aiogram.types import CallbackQuery
from config import *


bot = Bot(bot_token, parse_mode='html')
dp = Dispatcher(bot,storage = MemoryStorage())


class admad(StatesGroup):
    ad = State()
class reuser(StatesGroup):
    userad = State()


def get_now_date():
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    return date

with sqlite3.connect("database.db") as conn:
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS Users
  (user_id INTEGER, balance TEXT, registration_date TEXT)
  """)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await bot.send_message(message.chat.id, "Добро пожаловать в кликер бот", reply_markup=start_keyboard)
	cursor.execute("select * from users where user_id = ?",(message.from_user.id,))
	usr = cursor.fetchone()
	if not usr:
	       user_id = (message.from_user.id)
	       user = [user_id, 0, get_now_date()]
	       cursor.execute(f'''INSERT INTO users(user_id, balance, registration_date) VALUES(?,?,?)''', user)
	       conn.commit()


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
	if message.from_user.id == admin_id:
		get_all_users = cursor.execute('SELECT Count(*) FROM users').fetchone()[0]
		get_all_today_users = cursor.execute(f"""SELECT Count(*) FROM users WHERE registration_date = '{get_now_date()}' """).fetchone()[0]
		await bot.send_message(message.chat.id, f"Админ панель:\n\nВсего пользователь: {get_all_users}\nНовые пользователи за сегодня: {get_all_today_users}", reply_markup=admin_keyboard)


@dp.message_handler(content_types=['text'])
async def get_message(message):
    if message.text == "☘️ Клик":
        cursor.execute(f'UPDATE users SET balance = balance + 0.1 WHERE user_id IS "{message.from_user.id}"')
        await bot.send_message(message.chat.id, text = "Вы кликнули и получили 0.1₽ на свой баланс!")
    if message.text == "⚙️ Поддержка":
        await bot.send_message(message.chat.id, text = "💻 Поддержка", reply_markup=ppp)
    if message.text == '❌ Выйти из админки':
        if message.chat.id == 5206676272:
        	await bot.send_message(message.chat.id,text = 'Главное меню',reply_markup=start_keyboard)
    if message.text == "📝 О боте":
    	get_all_users = cursor.execute('SELECT Count(*) FROM users').fetchone()[0]
    	get_all_today_users = cursor.execute(f"""SELECT Count(*) FROM users WHERE registration_date = '{get_now_date()}' """).fetchone()[0]
    	await bot.send_message(message.chat.id, text = f"<b>Статистика бота:</b>\n\n🖱️ Всего пользователь: {get_all_users}\n🖱️ Новых за сегодня: {get_all_today_users}\n🖱️ Выведено: \n🖱️ Старт боты произведён: 21.10.2021\n\n❗<i>Хотим сообщить вам, что данный проект является собственноручной разработкой и никак не имеет отношение к схожим проектам.</i>❗", parse_mode='html')
    if message.text == '✉️ Рассылка':
      if message.chat.id == 5206676272:
      	await admad.ad.set()
      	await bot.send_message(message.chat.id, text = "Введите текcт рассылки")
    if message.text == '🔍 Поиск пользователя':
      if message.chat.id == 5206676272:
      	await reuser.userad.set()
      	await bot.send_message(message.chat.id, text = "Введите id пользователя")
    if message.text == "👤 Кабинет":
        balance = cursor.execute(f"SELECT balance FROM users WHERE user_id = {message.from_user.id}").fetchone()[0]
        regist = cursor.execute(f"""SELECT registration_date  FROM users WHERE user_id = {message.from_user.id}""").fetchone()[0]
        await bot.send_message(message.chat.id, text = f"""🖱️ Кабинет:\n\n🖱️ Ваш id: <code>{message.from_user.id}</code>\n\n🖱️ Дата регистрации: {regist}\n\n🖱️ Логин: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>\n\n🖱️ Ваш баланс: {balance}\n\n🖱️ Всего зароботано: {balance}""", reply_markup=withdrawl)

@dp.callback_query_handler(lambda c: c.data)
async def anhs(call: CallbackQuery):
        if call.data == 'exi1t':
        	await call.message.delete()
        	await bot.send_message(call.message.chat.id,text = "❌ Закрыто!")
        if call.data == 'paych':
        	await bot.send_message(call.message.chat.id,text = "❌ Оплата не найдена")
        if call.data == 'withdrawl1':
            price = 50
            comment = random.randint(1000, 99999)
            await bot.send_message(call.message.chat.id,text = f"Для вывода нужно оплатить 50₽ на наш киви кошелек, для того чтобы проверить что вы не робот!\n\nНомер для перевода: <code>{phone}</code>\nКоментрий к переводу: <code>{comment}</code>\nСумма к переводу: {price}₽", reply_markup=check_pay_kb)



@dp.message_handler(state=admad.ad)
async def getcount(message: types.Message, state: FSMContext):
    ad = message.text
    await state.update_data(ad=ad)
    await state.finish()
    all_id = cursor.execute("SELECT user_id FROM users").fetchall()
    for id in all_id:
     for id in id:
      try:
       await bot.send_message(id,text = f"{ad}", parse_mode='html')
      except:
       pass  
    await bot.send_message(message.chat.id,text = 'Рассылка завершина')



@dp.message_handler(state=reuser.userad)
async def getcount(message: types.Message, state: FSMContext):
    userad = message.text
    await state.update_data(userad=userad)
    balance_2 = cursor.execute(f"SELECT balance FROM users WHERE user_id = {userad}").fetchone()[0]
    status_2 = cursor.execute(f"SELECT status FROM users WHERE user_id = {userad}").fetchone()[0]
    regist_2 = cursor.execute(f"""SELECT registration_date  FROM users WHERE user_id = {userad}""").fetchone()[0]
    await message.answer(f"""Информация о <a href="tg://user?id={message.text}">пользователе</a>:\n\n🖱️ ID: {message.text}\n🖱️ Имя: <a href="tg://user?id={message.text}">{message.from_user.first_name}</a>\n🖱️ Баланс: {balance_2}\n🖱️ Дата регистрации: {regist_2}\n🖱️ Статус: {status_2}""", reply_markup=infouser)

#слито в @smoke_software

if __name__ == '__main__':
    executor.start_polling(dp, fast=True, skip_updates=True)