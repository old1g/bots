import pymysql
from pymysql import cursors
from config import host, port, user, password, database #Импортируем модуль pymysql который установили в первом уроке

class work_db:
	def __init__(self, host, port, user, password, database): #Функция для иницилизирования переменных в класс, запускать её не надо
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.database = database

	def connect_db(self): #Функция для конекта к базе данных
		try:
			connection = pymysql.connect(
				host = self.host,
				port = self.port,
				user = self.user,
				password = self.password,
				database = self.database,
				cursorclass = pymysql.cursors.DictCursor # type: ignore
			)
			return connection #Если конект прошёл успешно, возвращаем переменную connection, для дальнейшей работы
		except Exception as eror:
			print(eror) #Если произошла ошибка, выводим её в консоль
			return False #Если произошла ошибка, возвращаем False

	def connect_close(self, connection): #Передаём переменную connection если в коде подключились, после каждого подключения к базе данных и выполнения какого-либо когда, нужно закрывать подключение
		try:
			connection.close() #Закрываем подключение к базе данных
			return True #Если успешно закрыли подключение к базе, возвращаем True
		except Exception as eror:
			print(eror) #Если произошла ошибка, выводим её в консоль
			return False #Если произошла ошибка, возвращаем False

	def create_table(self, connection, creat): #Функция для создания таблице в базе данных, в creat будем передавать текст запроса
		try:
			with connection.cursor() as cursor:
				cursor.execute(creat)
			connection.commit()
			return True
		except Exception as eror:
			print(eror) #Если произошла ошибка, выводим её в консоль
			return False #Если произошла ошибка, возвращаем False

	def edit_table(self, connection, zapros, values):
		try:
			with connection.cursor() as cursor:
				cursor.execute(zapros, values)
			connection.commit()
			return True
		except Exception as eror:
			print(eror) #Если произошла ошибка, выводим её в консоль
			return False #Если произошла ошибка, возвращаем False

	def info_table(self, connection, info, values): #Функция для получения данных из таблицы, в info будем передавать текст запроса
		try:
			with connection.cursor() as cursor:
				cursor.execute(info, values)
			return cursor.fetchall() #Возвращаем всё что нашли
		except Exception as eror:
			print(str(eror)+'\n\n') #Если произошла ошибка, выводим её в консоль
			return False #Если произошла ошибка, возвращаем False

	def insert_table(self, connection, zapros, values):
		try:
			with connection.cursor() as cursor:
				a = cursor.execute(zapros, values)
			connection.commit()
			return a
		except Exception as eror:
			print(eror) #Если произошла ошибка, выводим её в консоль
			return False #Если произошла ошибка, возвращаем False

	def delete_from_table(self, connection, delete_, values): #Функция для редактирования данных в таблице, в delete_ будем передавать текст запроса
		try:
			with connection.cursor() as cursor:
				cursor.execute(delete_, values)
			connection.commit()
			return True
		except Exception as eror:
			print(eror) #Если произошла ошибка, выводим её в консоль
			return False #Если произошла ошибка, возвращаем False