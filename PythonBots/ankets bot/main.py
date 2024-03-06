from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from class_db import work_db #Импорируем класс для работы с базой данных из файла class_db.py
import test as bb #Импортируем файл test.py в переменную bb (мне так удобнее работать с ним)
import config as c #Импортируем файл config.py в переменную с (опять же мне так удобнее)



#Создаём класс бота и дистпетчера
bot = Bot(token=c.token, parse_mode=types.ParseMode.HTML) #Берём токен бота из файла config.py который импортировали ранее в переменную c
dp = Dispatcher(bot, storage=MemoryStorage())
db_work = work_db(c.host, c.port, c.user, c.password, c.database) #Создаём экземпляр класса для работы с базой данных, передав все нужные параметры из конфига


class anketa(StatesGroup):
	name = State()
	floor = State()
	age = State()


class new_values(StatesGroup):
	new_value = State()


class delete_strok_table(StatesGroup):
	id_strok = State()


def creat_table(): #Данную функцию будем запускать при каждом запуске кода, параметры функция не принимает
	#Для начала конектимся к базе данных:
	connection = db_work.connect_db()
	if connection: #Если класс вернул конект, а не False
		#Напишем сам запрос
		creat_table_request = 'CREATE TABLE IF NOT EXISTS `ankets`(id int AUTO_INCREMENT, name varchar(32), floor varchar(10), age int, PRIMARY KEY (id));' #И так мы написали запрос, но для чего он нам?
		#Он нам для того что-бы создать таблицу для анкет где будут следующие данные: id - это будет id анкеты (число), оно будет прописываться само (из-за AUTO_INCREMENT)
		#name типа сроки длинной не более 32 символов, floor типа строки не более 10 символов и age типа числа без ограничения
		#Первичный ключ (PRIMARY KEY) — особенное поле в таблице, которое позволяет однозначно идентифицировать каждую запись в ней
		#Запрос написан, давайте его выполним:
		status = db_work.create_table(connection, creat_table_request) #Предаём необходимые данные (Конект и сам запрос)
		#Проверяем статус создания базы данных:
		if status: #Если вернуло True значит всё хорошо (выведем в консоль что запрос выполнен)
			print('Таблица успешно создана')
			#Закрываем конект
			if db_work.connect_close(connection):
				print('Конект закрыт!')
			else: #Если нам вернуло False, значит произошла ошибка, в вспомогательном классе мы прописали вывод ошибки
				print('Ошибка указана выше')
		else: #Если вернуло False, значит не удалось создать таблицу, ошибку мы так же вывели в классе
			print('Ошибка указана выше')
	else: #Если мы не смогли подключиться к базе данных, то опять же ошибка была выведена в классе
		print('Ошибка указана выше')


def creat_table2(): #Данную функцию будем запускать при каждом запуске кода, параметры функция не принимает
	#Для начала конектимся к базе данных:
	connection = db_work.connect_db()
	if connection: #Если класс вернул конект, а не False
		#Напишем сам запрос
		creat_table_request = 'CREATE TABLE IF NOT EXISTS `users`(id int AUTO_INCREMENT, name varchar(32), password varchar(20), age int, PRIMARY KEY (id));' #И так мы написали запрос, но для чего он нам?
		#Он нам для того что-бы создать таблицу для анкет где будут следующие данные: id - это будет id анкеты (число), оно будет прописываться само (из-за AUTO_INCREMENT)
		#name типа сроки длинной не более 32 символов, password типа строки не более 20 символов и age типа числа без ограничения
		#Первичный ключ (PRIMARY KEY) — особенное поле в таблице, которое позволяет однозначно идентифицировать каждую запись в ней
		#Запрос написан, давайте его выполним:
		status = db_work.create_table(connection, creat_table_request) #Предаём необходимые данные (Конект и сам запрос)
		#Проверяем статус создания базы данных:
		if status: #Если вернуло True значит всё хорошо (выведем в консоль что запрос выполнен)
			print('Таблица успешно создана')
			#Закрываем конект
			if db_work.connect_close(connection):
				print('Конект закрыт!')
			else: #Если нам вернуло False, значит произошла ошибка, в вспомогательном классе мы прописали вывод ошибки
				print('Ошибка указана выше')
		else: #Если вернуло False, значит не удалось создать таблицу, ошибку мы так же вывели в классе
			print('Ошибка указана выше')
	else: #Если мы не смогли подключиться к базе данных, то опять же ошибка была выведена в классе
		print('Ошибка указана выше')


def insert_table(name_, floor_, age_): #Данная функция принимает имя таблицы в которую надо записать данные (Сразу скажу т.к. мы записывать будет в ankets распишем получение данных)
	#Для начала конектимся к базе данных:
	connection = db_work.connect_db()
	if connection: #Если класс вернул конект, а не False
		#Напишем сам запрос
		insert_table_request = 'INSERT INTO ankets (name, floor, age) VALUES (%s, %s, %s);' #И так в этом запросе мы создаём запись данных
		with connection.cursor() as cursor:
			cursor.execute(insert_table_request, (name_, floor_, age_)) #Записываем данные полученные в функцию
		connection.commit() #Сохраняем изменения
		print('Данные записаны!')
		if db_work.connect_close(connection):
			print('Конект закрыт!')
		else: #Если нам вернуло False, значит произошла ошибка, в вспомогательном классе мы прописали вывод ошибки
			print('Ошибка указана выше')
	else: #Если мы не смогли подключиться к базе данных, то опять же ошибка была выведена в классе
		print('Ошибка указана выше')


def delete_from_table(self, connection, delete_, values): #Функция для редактирования данных в таблице, в delete_ будем передавать текст запроса
		try:
			with connection.cursor() as cursor:
				cursor.execute(delete_, values)
			connection.commit()
			return True
		except Exception as eror:
			print(eror) #Если произошла ошибка, выводим её в консоль
			return False #Если произошла ошибка, возвращаем False


@dp.message_handler(content_types=['text']) #Обрабатываем каждое сообщение от пользователей, добавляем content_types для обработки текста, в будущих уроках будет фото и видео
async def text(message: types.Message): #Асинхронная функция с название "text" которая принимает в переменную message, текст пользователя отправевшего сообщение
	if message.text == '/start':
		await bot.send_message(message.chat.id, 'Привет, заполни анкету, или посмотри информацйию о мне', reply_markup=bb.mark_menu) #Обрабатываем команду /start и выводим клавиатуру из файлы test.py
	elif message.text == 'Информация':
		await bot.send_message(message.chat.id, f'Сюда пишем какую либо информацию, например я хочу вывести ID пользователя\nТвой ID: <code>{message.chat.id}</code>', parse_mode = "HTML")
	elif message.text == 'Заполнить анкету':
		await bot.send_message(message.chat.id, '<b>Введите своё имя:</b>', parse_mode = "HTML")
		await anketa.name.set()
	elif message.text == '/info_table':
		info_request = 'SELECT * FROM ankets WHERE id = %s'
		values = (1,)
		connection = db_work.connect_db() #Конектимся к базе данных
		if connection: #Если конект успешный
			info = db_work.info_table(connection, info_request, values)
			if info: #Если получили данные по id = 1
				await bot.send_message(message.chat.id, f'Полученные данные:\nID: {info["id"]}\nИмя: {info["name"]}\nПол: {info["floor"]}\nВозраст: {info["age"]}')
			else: #Если не смогли получить данные
				await bot.send_message(message.chat.id, 'Не удалось получить данные')
		else: #Если конект не удался
			await bot.send_message(message.chat.id, 'Не удалось подключиться к базе данных')
	elif message.text == '/new_value':
		await bot.send_message(message.chat.id, 'Введите ID для изменения возраста:')
		await new_values.new_value.set()
	elif message.text == '/delete_strok_table':
		await bot.send_message(message.chat.id, 'Введите ID для удаления:')
		await delete_strok_table.id_strok.set()


@dp.message_handler(state=new_values.new_value)
async def anketa_name(message: types.Message, state: FSMContext): #Как видите у нас добавился FSMContext, он нам нужен как раз для обработки машины состояния
	#Записываем ID в кеш
	await state.update_data(id_value=message.text)
	#Выводим инлайн кнопки с числами
	#Пока напишу прямо тут, в следующих уроках будем создавать функции
	await bot.send_message(message.chat.id, 'Выберите новое значение:', reply_markup=InlineKeyboardMarkup(row_width=3).add(
		InlineKeyboardButton(text='1', callback_data='new_value_1'),InlineKeyboardButton(text='2', callback_data='new_value_2'), InlineKeyboardButton(text='3', callback_data='new_value_3'),
		InlineKeyboardButton(text='25', callback_data='new_value_25')))
	#Этого достаточно


@dp.message_handler(state=anketa.name)
async def anketa_name(message: types.Message, state: FSMContext): #Как видите у нас добавился FSMContext, он нам нужен как раз для обработки машины состояния
	#Записываем имя в кеш
	await state.update_data(name=message.text)
	#Далее просим ввести пол, с выбором пола из кнопок
	await bot.send_message(message.chat.id, '<b>Выберите свой пол:</b>', reply_markup=bb.menu_floor, parse_mode="HTML") #добавляем вывод кнопок с выбором пола
	await anketa.floor.set()


@dp.message_handler(state=anketa.floor)
async def anketa_name(message: types.Message, state: FSMContext):
	#Записываем пол в кеш
	await state.update_data(floor=message.text)
	#Далее просим ввести свой возраст
	await bot.send_message(message.chat.id, '<b>Введите свой возраст:</b>', reply_markup=ReplyKeyboardRemove(), parse_mode = "HTML") #убираем текстовую клавиатуру
	await anketa.age.set()


@dp.message_handler(state=anketa.age)
async def anketa_name(message: types.Message, state: FSMContext):
	#Получим все данные записанные в кеш
	data = await state.get_data()
	#Сортируем их по переменным
	name = data['name'] #В ковычках пишем name, потому что сами записывали в такую переменную, там может быть любая другая
	floor = data['floor'] #В ковычках пишем floor, потому что сами записывали в такую переменную, там может быть любая другая
	age = message.text #записываем ввод пользователя в переменную age
	await state.finish() #Завершаем работу с машиной состояний
	#Выведем анкету пользователю
	await bot.send_message(message.chat.id, f'Ваша анкета:\nID: <code>{message.chat.id}</code>\nИмя: {name}\nПол: {floor}\nВозраст: {age}\n\nСпасибо за уделение времени', reply_markup=bb.mark_menu, parse_mode="HTML") #Отправляем анкету, благодарим, и выдаём ему текстовоем меню
	#Отправим анкету администратору по его ID из config.py
	#Так же выведем ID пользователя и его юзернейм
	await bot.send_message(c.admin, f'Пользователь: <code>{message.chat.id}</code>\n@{message.from_user.username} заполнил анкету\nЕго данные:\n\nИмя: {name}\nПол: {floor}\nВозраст: {age}', parse_mode="HTML")
	insert_table(name, floor, age) #Передаём необходимые данные


@dp.callback_query_handler(lambda call: True, state='*') #Обрабатываем нажатия всех инлайн кнопок, даже когда активно ожидание ввода от пользователя
async def callback_inline(call, state: FSMContext): #В переменную call принимаем данные о нажатой кнопке
	try: #Обрабатываем ошибки, если всё успешно то мы получим переменную id_value на всю функцию
		data = await state.get_data()
		id_value = data['id_value']
		await state.finish()
	except Exception as eror: #Если будут ошибки мы их пришлём пользователю
		await bot.send_message(call.message.chat.id, f'Произошла ошибка: {eror}')
		return #Останавливаем выполнение функции
	#Приступим к обработке нажатия кнопок, т.к. у нас записано новое чило в callback_data, но начало одно и тоже
	#Нам нужно проверять есть ли в нажатой кнопке начало:
	if 'new_value_' in call.data: #В call.data содержиться callback_data
		new_value = int(call.data.replace('new_value_', '')) #С момощью этого кода мы получим число типа int, удалив из call.data не нужное нам
		#Грубыми словами с помощью replace мы заменяем new_value_ на ничего
		#Теперь давайте заменим значение в таблице по ID которое вписали изначально
		#Конектимся к базе данных:
		connection = db_work.connect_db()
		if connection: #Если конект успешен
			#Возпользуемся функцией edit_table из вспомогательного класса:
			new_value_request = 'UPDATE ankets SET age = %s WHERE id = %s'
			values = (new_value, int(id_value))
			status = db_work.edit_table(connection, new_value_request, values)
			if status: #Если успешно обновили данные
				await bot.send_message(call.message.chat.id, f'Данные для строки с ID: {id_value}\nУспешно обновлены на: {new_value}')
			else: #Если произошла ошибка
				await bot.send_message(call.message.chat.id, 'Произошла ошибка, она отобразилась в консоли!')
		else: #Если не удалось подключиться к базе данных
			await bot.send_message(call.message.chat.id, 'Не удалось подключиться к базе данных!')


@dp.message_handler(state=delete_strok_table.id_strok)
async def anketa_name(message: types.Message, state: FSMContext):
	await state.finish() #Завершаем работу с машиной состояний
	id_strok = message.text
	connection = db_work.connect_db()
	if connection: #Если класс вернул конект, а не False
		#Напишем сам запрос
		delete_table = 'DELETE FROM ankets WHERE id = %s'
		values = (id_strok,)
		status = db_work.delete_from_table(connection, delete_table, values)
		if status: #Если успешно обновили данные
			await bot.send_message(message.chat.id, f'Данные строки с ID: {id_strok} - Удалены!')
		else: #Если произошла ошибка
			await bot.send_message(message.chat.id, 'Произошла ошибка, она отобразилась в консоли!')
	else:
		await bot.send_message(message.chat.id, 'Не удалось подключиться к базе данных!')



if __name__ == "__main__": #Если скрипт запущен с этого файла, запускаем executor
	creat_table() #Запускаем функцию создания таблицы ankets
	creat_table2() #Запускаем функцию создания таблицы users
	executor.start_polling(dp, skip_updates=True) #skip_updates=True - нужен для того чтобы не обрабатывать сообщения которые были присланы пользователем в тот момент когда бот был выключен