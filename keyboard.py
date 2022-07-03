from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from config import support
#слито в @smoke_software

start_btn_1 = KeyboardButton('☘️ Клик', callback_data='Click')
start_btn_2 = KeyboardButton('📝 О боте', callback_data='info')
start_btn_3 = KeyboardButton('⚙️ Поддержка', callback_data='help')
start_btn_4 = KeyboardButton('👤 Кабинет', callback_data='cadinet')
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(start_btn_1)
start_keyboard.add(start_btn_4)
start_keyboard.add(start_btn_3, start_btn_2)

admin_kb = KeyboardButton('✉️ Рассылка', callback_data='ksks')
admin_kb1 = KeyboardButton('🔍 Поиск пользователя', callback_data='psps')
admin_kb2 = KeyboardButton('❌ Выйти из админки', callback_data='psps')
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(admin_kb)
admin_keyboard.add(admin_kb1)
admin_keyboard.add(admin_kb2)

withdraw = InlineKeyboardButton('🖱️ Вывести', callback_data='withdrawl1')
withdrawl = InlineKeyboardMarkup().add(withdraw)

exit = InlineKeyboardButton('❌ Закрыть', callback_data='exi1t')
infouser = InlineKeyboardMarkup().add(exit)

check_pay = InlineKeyboardButton('🔍 Проверить оплату', callback_data='paych')
check_pay_kb = InlineKeyboardMarkup().add(check_pay)

#слито в @smoke_software
buttonk = InlineKeyboardButton(text="🖱️ Поддержка", url=f"{support}")
ppp = InlineKeyboardMarkup().add(buttonk)
