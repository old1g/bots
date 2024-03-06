#написать нормальное добаление ссылки в бд и достать данные пользователя из бд
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import config as c
from texta import start_text
from class_db import work_db


# Инициализация бота и диспетчера
bot = Bot(token=c.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
db = work_db(c.host, c.port, c.user, c.password, c.database)


class anketa(StatesGroup):
	name = State()
	gender = State()
	age = State()
	city = State()

class chat(StatesGroup):
	link = State()


def creat_table(): #Данную функцию будем запускать при каждом запуске кода, параметры функция не принимает
	#Для начала конектимся к базе данных:
	connection = db.connect_db()
	if connection: 
		creat_table_request = 'CREATE TABLE IF NOT EXISTS `ankets`(id int AUTO_INCREMENT, id_user int, username varchar(24), name varchar(10), gender varchar(10), age int, city varchar(15), PRIMARY KEY (id));'
		status = db.create_table(connection, creat_table_request) #Предаём необходимые данные (Конект и сам запрос)
		#Проверяем статус создания базы данных:
		if status: #Если вернуло True значит всё хорошо (выведем в консоль что запрос выполнен)
			print('Таблица успешно создана')
			#Закрываем конект
			if db.connect_close(connection):
				print('Конект закрыт!')
			else: #Если нам вернуло False, значит произошла ошибка, в вспомогательном классе мы прописали вывод ошибки
				print('Ошибка указана выше')
		else: #Если вернуло False, значит не удалось создать таблицу, ошибку мы так же вывели в классе
			print('Ошибка указана выше')
	else: #Если мы не смогли подключиться к базе данных, то опять же ошибка была выведена в классе
		print('Ошибка указана выше')


def creat_table2(): #Данную функцию будем запускать при каждом запуске кода, параметры функция не принимает
	#Для начала конектимся к базе данных:
	connection = db.connect_db()
	if connection: 
		creat_table_request = 'CREATE TABLE IF NOT EXISTS `chat`(id int AUTO_INCREMENT, link varchar(128), PRIMARY KEY (id));'
		status = db.create_table(connection, creat_table_request) #Предаём необходимые данные (Конект и сам запрос)
		#Проверяем статус создания базы данных:
		if status: #Если вернуло True значит всё хорошо (выведем в консоль что запрос выполнен)
			print('Таблица успешно создана')
			#Закрываем конект
			if db.connect_close(connection):
				print('Конект закрыт!')
			else: #Если нам вернуло False, значит произошла ошибка, в вспомогательном классе мы прописали вывод ошибки
				print('Ошибка указана выше')
		else: #Если вернуло False, значит не удалось создать таблицу, ошибку мы так же вывели в классе
			print('Ошибка указана выше')
	else: #Если мы не смогли подключиться к базе данных, то опять же ошибка была выведена в классе
		print('Ошибка указана выше')


def insert_table2(id_,link_): #Данная функция принимает имя таблицы в которую надо записать данные (Сразу скажу т.к. мы записывать будет в ankets распишем получение данных)
	#Для начала конектимся к базе данных:
	connection = db.connect_db()
	if connection: #Если класс вернул конект, а не False
		#Напишем сам запрос
		insert_table_request = 'INSERT INTO chat (id, link) VALUES (%s,%s);' #И так в этом запросе мы создаём запись данных
		with connection.cursor() as cursor:
			cursor.execute(insert_table_request, id_, link_) #Записываем данные полученные в функцию
		connection.commit() #Сохраняем изменения
		print('Данные записаны!')
		if db.connect_close(connection):
			print('Конект закрыт!')
		else: #Если нам вернуло False, значит произошла ошибка, в вспомогательном классе мы прописали вывод ошибки
			print('Ошибка указана выше')
	else: #Если мы не смогли подключиться к базе данных, то опять же ошибка была выведена в классе
		print('Ошибка указана выше')



@dp.message_handler(content_types=['text']) #Обрабатываем каждое сообщение от пользователей, добавляем content_types для обработки текста, в будущих уроках будет фото и видео
async def text(message: types.Message): #Асинхронная функция с название "text" которая принимает в переменную message, текст пользователя отправевшего сообщение
	if message.text == '/start':
		await bot.send_message(message.chat.id, start_text, reply_markup=
						 InlineKeyboardMarkup().
						 add(InlineKeyboardButton(text="Начать анкетирование", callback_data="start_survey")))
	
	elif message.text == '/new_link':
		await bot.send_message(message.chat.id, 'Введите ссылку на чат:')
		await chat.link.set()

@dp.message_handler(state=anketa.name)
async def anketa_name(message: types.Message, state: FSMContext): #Как видите у нас добавился FSMContext, он нам нужен как раз для обработки машины состояния
	#Записываем имя в кеш
	await state.update_data(name=message.text)
	#Далее просим ввести пол, с выбором пола из кнопок
	await bot.send_message(message.chat.id, 'Введите свой пол:')
	await anketa.gender.set()

@dp.message_handler(state=anketa.gender)
async def anketa_name(message: types.Message, state: FSMContext):
	#Записываем пол в кеш
	await state.update_data(gender=message.text)
	#Далее просим ввести свой возраст
	await bot.send_message(message.chat.id, 'Введите свой возраст:')
	await anketa.age.set()

@dp.message_handler(state=anketa.age)
async def anketa_name(message: types.Message, state: FSMContext):
	#Получим все данные записанные в кеш
	await state.update_data(age=message.text)
	await bot.send_message(message.chat.id, 'Введите свой город: ')
	await anketa.city.set()

@dp.message_handler(state=anketa.city)
async def anketa_name(message: types.Message, state: FSMContext):
	#Получим все данные записанные в кеш
	await state.update_data(city=message.text)
	data = await state.get_data()
	name = data['name']
	gender = data['gender']
	age = data['age']
	city = data['city']
	#Выведем анкету пользователю
	await bot.send_message(message.chat.id, f"Ваше имя: {name}\nВаш пол: {gender}\nВаш возраст: {age}\nВаш город: {city}", 
						reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="Отправить анкету", callback_data="submit_survey"), InlineKeyboardButton(text="Заполнить заново", callback_data="restart_survey")))


@dp.message_handler(state=chat.link) #Обрабатываем нажатия всех инлайн кнопок, даже когда активно ожидание ввода от пользователя
async def new_link(message: types.Message, state: FSMContext):
		link_ = message.text
		connection = db.connect_db()
		if connection:
			new_link_req = 'UPDATE chat set link = %s WHERE id = 1'
			value = (link_)
			status = db.new_link(connection, new_link_req, value)
			if status:
				await bot.send_message(c.admin, f'Новая ссылка:\n{link_}')


@dp.callback_query_handler(lambda call: True, state = '*')
async def callback_inline(call, state: FSMContext):
	id_user = call.from_user.id
	username = call.from_user.username

	if 'start_survey' in call.data:
		await bot.send_message(chat_id=id_user, text = 'Введите своё имя:')
		await anketa.name.set()

	elif 'submit_survey' in call.data:
		await call.message.edit_text(call.message.text + "\nАнкета отправлена")
		await call.message.edit_reply_markup(reply_markup=None)
		data = await state.get_data()
		name = data['name']
		gender = data['gender']
		age = data['age']
		city = data['city']
		await state.finish()
		
		zapros = 'INSERT INTO ankets (id_user, username, name, gender, age, city) VALUES (%s,%s,%s,%s,%s,%s);' #И так в этом запросе мы создаём запись данных
		connection = db.connect_db()
		idi = int(db.insert_table(connection, zapros, id_user, username, name, gender, age, city))
		await bot.send_message(c.admin, text=f"Пришла новая анкета {idi}:\nID пользователя: {id_user}\nИмя пользователя: @{username}\nИмя: {name}\nПол: {gender}\nВозраст: {age}\nГород: {city}", 
							reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Принять анкету", callback_data="accept_survey_" + str(idi)), InlineKeyboardButton(text="Отклонить анкету", callback_data="reject_survey_" + str(idi))))
		
	elif 'reject_survey_' in call.data:
		idi = call.data
		idi = call.data.split('_')[2]
		print(idi)
		id_zapros = 'SELECT * FROM ankets WHERE id = %s'
		connection = db.connect_db()
		value = (idi,)
		if connection:
			ank = db.info_tabl(connection, id_zapros, value)
			if ank:
				id_us = ank['id_user']

		await bot.send_message(chat_id=id_us, text="Ваша анкета была отклонена")
		await call.message.edit_text(call.message.text + "\n❌ Анкета отклонена")
		await call.message.edit_reply_markup(reply_markup=None)
		await state.finish()
	
	elif 'accept_survey_' in call.data:
		idi = call.data.split('_')[2]
		zapros = 'SELECT * FROM chat WHERE id = %s'
		value = (1,)

		id_zapros = 'SELECT * FROM ankets WHERE id = %s'
		connection = db.connect_db()
		
		if connection:
			inf = db.info_tabl(connection, zapros, value)
			ank = db.info_tabl(connection, id_zapros, idi)
			if inf and ank:
				link = inf['link']
				id_us = ank['id_user']
		
		await bot.send_message(chat_id=id_us, text=f'Ваша анкета была одобрена!\nЗаходите в чат:\n{link}')
		await call.message.edit_text(call.message.text + "\n✅ Анкета одобрена")
		await call.message.edit_reply_markup(reply_markup=None)
		await state.finish()
		
	else:
		await call.message.edit_reply_markup(reply_markup=None)
		await bot.send_message(chat_id=id_user, text = 'Введите своё имя:')
		await anketa.name.set()
	


if __name__ == "__main__": #Если скрипт запущен с этого файла, запускаем executor
	creat_table()
	creat_table2()
	executor.start_polling(dp, skip_updates=True) #skip_updates=True - нужен для того чтобы не обрабатывать сообщения которые были присланы пользователем в тот момент когда бот был выключен
