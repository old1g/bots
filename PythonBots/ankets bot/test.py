from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

mainy = [['Заполнить анкету'],['Информация']]

mark_menu = ReplyKeyboardMarkup(mainy, resize_keyboard=True)

main_floor = [['Мужской', 'Женский']]
menu_floor = ReplyKeyboardMarkup(main_floor, resize_keyboard=True)