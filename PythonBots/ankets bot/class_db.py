import pymysql
from pymysql import cursors
from config import host, port, user, password, database

class work_db:
    def __init__(self, host, port, user, password, database): #Функция для иницилизирования переменных в класс, запускать её не надо
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connect_db(self):
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as eror:
            print(eror)
            return False

    def connect_close(self,connection):
        try:
            connection.close()
            return True
        except Exception as eror:
            print(eror)
            return False

    def create_table(self,connection,creat):
        try:
            with connection.cursor() as cursor:
                cursor.execute(creat)
            connection.commit()
            return True
        except Exception as eror:
            print(eror)
            return False

    def info_table(self,connection,info, values):
        try:
            with connection.cursor() as cursor:
                cursor.execute(info, values)
            return cursor.fetchall()[0]
        except Exception as eror:
            print(eror)
            return False

    def delete_from_table(self,connection,delete_, values):
        try:
            with connection.cursor() as cursor:
                cursor.execute(delete_, values)
            connection.commit()
            return True
        except Exception as eror:
            print(eror)
            return False
        
    def edit_table(self, connection, edit, values): #Функция для редактирования данных в таблице, в edit будем передавать текст запроса
        try:
            with connection.cursor() as cursor:
                cursor.execute(edit, values)
            connection.commit()
            return True
        except Exception as eror:
            print(eror) #Если произошла ошибка, выводим её в консоль
            return False #Если произошла ошибка, возвращаем False



