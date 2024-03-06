from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, BotCommand, WebAppInfo
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
import config as c
import test as bb
import asyncio
import pymysql
from class_db import work_db
from module_sms import main_sms
from datetime import datetime
import pytz


bot = Bot(token=c.token_bot, parse_mode=types.ParseMode.HTML) #Берём токен бота из файла config.py который импортировали ранее в переменную c
dp = Dispatcher(bot, storage=MemoryStorage())
db_work = work_db(c.host, c.port, c.user, c.password, c.database) #Создаём экземпляр класса для работы с базой данных, передав все нужные параметры из конфига
work_sms = main_sms(c.token_sms) #Создаём экземпляр класса для работы с сервисом смс


def time_Moscow():
	# Устанавливаем часовой пояс Москвы
	moscow_tz = pytz.timezone('Europe/Moscow')
	# Получаем текущее время в часовом поясе Москвы
	moscow_time = datetime.now(moscow_tz)
	# Форматируем время в часы:минуты:секунды
	formatted_time = moscow_time.strftime('%H:%M:%S')
	return str(formatted_time) #Возвращаем строку с временем


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
	id_user = message.from_user.id #Записываем id пользователя (Ранее писали message.chat.id)
	if message.text == '/start':
		await bot.send_message(id_user, 'Хай, вы попали в смс бота для работы с сайтом 365sms.ru', reply_markup=bb.mark_menu) #При команде старт отправляем приветственное сообщение и рассказываем о себе, и выводим клавиатуру
	elif message.text == 'Получить баланс':
		balanse_sms = work_sms.get_balanse() #Запрашиваем баланс с сайта по api
		time_msk = time_Moscow() #Получаем время мск
		try:
			await bot.send_message(id_user, f'<b>[{time_msk}]</b> Текущий баланс: {float(balanse_sms):.2f}₽', reply_markup=InlineKeyboardMarkup(row_width=1).add(
    		InlineKeyboardButton(text='Обновить', callback_data='new_balance'))) #Пока выводим то что получили от сайта
		except:
			if 'BAD_KEY' in balanse_sms:
				await bot.send_message(id_user, 'Не правильный токен для запроса, проверьте и обновите его!') #Если указали не верный токен
			elif 'ERROR_SQL' in balanse_sms:
				await bot.send_message(id_user, 'Ошибка на стороне сайта поопробуйте позже!') #Если на сайте произошла ошибка
			else:
				await bot.send_message(id_user, 'Ваш запрос был составлен не правильно!') #Если мы не правильно составили запрос (в уроке такого не будет)
	elif message.text == 'Получить номер':
		number = work_sms.new_number(servis='qw', strana=0)
		#Будем получать номер для вк без оператора и регистрироваться через бота (Страну возьмём индонезию потому что дёшево ID: 6)
		#Обработаем ошибки:
		if number == 'NO_NUMBERS': #Если пришёл ответ что нет номеров
			await bot.send_message(id_user, 'Нет номеров с заданными параметрами, попробуйте позже, или поменяйте оператора, страну', reply_markup=bb.mark_menu)
		elif number == 'NO_BALANCE': #Если на балансе не хватает денег на номер телефона
			await bot.send_message(id_user, 'Закончились деньги на аккаунте', reply_markup=bb.mark_menu)
		elif number == 'WRONG_SERVICE': #Если не правильно указали "servis"
			await bot.send_message(id_user, 'Неверный идентификатор сервиса', reply_markup=bb.mark_menu)
		else: #Если номер упешно получен
			#В ответе будет такой формат: ACCESS_NUMBER:ID:NUMBER - Пример: ACCESS_NUMBER:234242:79123456789
    		#Делим ответ на список:
			info_number = number.split(':')
			#Итоговый список будет выглядеть так: ['ACCESS_NUMBER', 'ID', 'NUMBER'] - Пример: ['ACCESS_NUMBER', '234242', '79123456789']
    		#Индексы списка начинаються с 0
    		#т.е с индексом 0 - 'ACCESS_NUMBER', c индексом 1 - 'ID', c индексом 2 - 'NUMBER'
    		#Отправляем данные пользователю:
			await bot.send_message(id_user, f'ID номера: {info_number[1]}\nНомер: <code>{info_number[2]}</code>', reply_markup=InlineKeyboardMarkup(row_width=1).add(
				InlineKeyboardButton(text='Изменить статус', callback_data=f'new_status_{info_number[1]}'))) #Передаём id номера в callback_data


@dp.callback_query_handler(lambda call: True, state='*')
async def callback_inline(call, state: FSMContext):
	id_user = call.from_user.id
	if call.data == 'new_balance':
		time_msk = time_Moscow() #Получаем время мск
		balanse_sms = work_sms.get_balanse() #Запрашиваем баланс с сайта по api
		await bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id, text=f'{call.message.html_text}\n<b>[{time_msk}]</b> Текущий баланс: {float(balanse_sms):.2f}₽', reply_markup=InlineKeyboardMarkup(row_width=1).add(
    		InlineKeyboardButton(text='Обновить', callback_data='new_balance')))
	elif 'new_status_' in call.data: #В call.data содержиться callback_data
		id_number = int(call.data.replace('new_status_', '')) #С момощью этого кода мы получим число типа int, удалив из call.data не нужное нам
		#Грубыми словами с помощью replace мы заменяем new_status_ на ничего
    	#Отправим клавиатуру с дальнейшими статусами, перед этим проверив текущий статус номера
		status_number = work_sms.get_status(idi=id_number)
		#Давайте в зависимости от статуса выведем клавиатуру:
		if status_number == 'STATUS_WAIT_CODE': #Данный статус будет после получения номера он означает "Ожидание смс"
			int_status = 0 #Поставим 0 будет означать что номер только что получен
			await call.answer('Текущий статус: Ожидает смс', show_alert=True) #Выводим табличку с текущим статусом (show_alert позваляет вывести табличку с кнопко "ОК")
		elif status_number == 'STATUS_CANCEL': #Данный статус будет после отмены номера он означает "Активация отменена"
			int_status = 1 #Поставим 1 будет означать что номер больше не активен (отменён)
			await call.answer('Текущий статус: Активация отменена', show_alert=True) #Выводим табличку с текущим статусом (show_alert позваляет вывести табличку с кнопко "ОК")
		else: #Т.к. больше статусов которые может вернуть сайт нет, будем обабатывать успешное получение смс
		#Делим полученное сообение на список с помощью split
			kode_aktivate = status_number.split(':') #Получили список ["STATUS_OK", "CODE"]
			int_status = 2 #Поставим 2 будет означать что смс получен
			await call.answer(f'Текущий статус: Смс получено\nКод: <code>{kode_aktivate[1]}</code>', show_alert=True)
		#Сделаем стандартную клавиатуру с дефолтной нопкой:
		klawa = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Узнать статус', callback_data=f'new_status_{id_number}'))
		if int_status == 0:
			klawa.add(InlineKeyboardButton(text='Отменить активацию', callback_data=f'cancel_akt_{id_number}'))
		elif int_status == 1:
			klawa.add(InlineKeyboardButton(text='Получить новый номер', callback_data='new_number'))
		else:
			klawa.add(InlineKeyboardButton(text='Подтвердить SMS-код и завершить активацию', callback_data=f'true_aktiv_{id_number}'),
    			InlineKeyboardButton(text='Запросить еще одну смс', callback_data=f'dop_sms_{id_number}'))
		try: #Если смогли отредактировать сообщение
			await bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id, text=call.message.html_text, reply_markup=klawa)
		except: #Если произошла любая ошибка
			pass
	elif 'dop_sms_' in call.data:
		id_number = call.data.replace('dop_sms_', '')
		await call.answer('Новый статус установлен', show_alert=True)
		work_sms.new_status(idi=id_number, status=3) #Устанавливаем статус 3 - нужна повторная смс
		klawa = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Узнать статус', callback_data=f'new_status_{id_number}'),
    		InlineKeyboardButton(text='Подтвердить SMS-код и завершить активацию', callback_data=f'true_aktiv_{id_number}'))
		await bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id, text=call.message.html_text, reply_markup=klawa)
	elif 'true_aktiv_' in call.data:
		id_number = call.data.replace('true_aktiv_', '')
		await call.answer('Новый статус установлен', show_alert=True)
		work_sms.new_status(idi=id_number, status=6) #Устанавливаем статус 6 - Подтвердить SMS-код и завершить активацию
		klawa = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Получить новый номер', callback_data='new_number'))
		await bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id, text=f'{call.message.html_text}\nАктивация завершена', reply_markup=klawa)
	elif 'cancel_akt_' in call.data:
		id_number = call.data.replace('cancel_akt_', '')
		status_number = work_sms.new_status(idi=id_number, status=8) #Устанавливаем статус 8 - Отменить активацию
		await call.answer('Активация отменена', show_alert=True)
		await bot.send_message(id_user, 'Хай, вы попали в смс бота для работы с сайтом 365sms.ru', reply_markup=bb.mark_menu)
	elif call.data == 'new_number':
		await bot.delete_message(id_user, call.message.message_id) #Удаляем сообщение
		#Будем получать номер для вк без оператора и регистрироваться через бота (Страну возьмём индонезию потому что дёшево ID: 6)
		number = work_sms.new_number(servis='qw', strana=0)
		#Обработаем ошибки:
		if number == 'NO_NUMBERS': #Если пришёл ответ что нет номеров
			await bot.send_message(id_user, 'Нет номеров с заданными параметрами, попробуйте позже, или поменяйте оператора, страну', reply_markup=bb.mark_menu)
		elif number == 'NO_BALANCE': #Если на балансе не хватает денег на номер телефона
			await bot.send_message(id_user, 'Закончились деньги на аккаунте', reply_markup=bb.mark_menu)
		elif number == 'WRONG_SERVICE': #Если не правильно указали "servis"
			await bot.send_message(id_user, 'Неверный идентификатор сервиса', reply_markup=bb.mark_menu)
		else: #Если номер упешно получен
			#В ответе будет такой формат: ACCESS_NUMBER:ID:NUMBER - Пример: ACCESS_NUMBER:234242:79123456789
    		#Делим ответ на список:
			info_number = number.split(':')
			#Итоговый список будет выглядеть так: ['ACCESS_NUMBER', 'ID', 'NUMBER'] - Пример: ['ACCESS_NUMBER', '234242', '79123456789']
    		#Индексы списка начинаються с 0
    		#т.е с индексом 0 - 'ACCESS_NUMBER', c индексом 1 - 'ID', c индексом 2 - 'NUMBER'
    		#Отправляем данные пользователю:
			await bot.send_message(id_user, f'ID номера: {info_number[1]}\nНомер: <code>{info_number[2]}</code>', reply_markup=InlineKeyboardMarkup(row_width=1).add(
    			InlineKeyboardButton(text='Изменить статус', callback_data=f'new_status_{info_number[1]}'))) #Передаём id номера в callback_data

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)