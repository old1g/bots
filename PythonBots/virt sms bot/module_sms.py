import requests

class main_sms:
	def __init__(self, token):
		self.token = token #Токен будем передавать в класс
		self.link = 'https://365sms.ru/stubs/handler_api.php' #Ссылка для работы с api берём с сайта


	def get_balanse(self): #Функция для получения текущего баланса на сайте
		balans = requests.get(f'{self.link}?api_key={self.token}&action=getBalance') #Делаем get апрос для получения данных
		if 'ACCESS_BALANCE' in balans.text: #если мы успешно получили баланс то возращаем его
			spisok = balans.text.split(':') #Сплитуем(разделяем) текст по : который получили в ответе от сайта
			return spisok[1] #Возращаем баланс
		else:
			return balans.text #В ином случае возращаем весь текст который получили, для дальнейшей обработки


	def new_number(self, servis, strana, operator=None): #Функия для получения номера телефона
		if operator == None: #Если мы не передали оператор, то сайт нам выдаст рандомного оператора
			number = requests.get(f'{self.link}?api_key={self.token}&action=getNumber&service={servis}&country={strana}') #Делаем гет запрос без учёта оператора
		else: #В ином случае мы передаём в запрос ещё и оператора
			number = requests.get(f'{self.link}?api_key={self.token}&action=getNumber&service={servis}&operator={operator}&country={strana}')#Делаем гет запрос с учётом оператора
		return number.text #Возращаем всё что получили в ответ от сайта

	def new_status(self, idi, status): #Функция для изменения статуса номера
		stat = requests.get(f'{self.link}?api_key={self.token}&action=setStatus&status={status}&id={idi}') #Делаем гет запрос
		return stat.text #Возращаем всё что получили в ответ от сайта

	def get_status(self, idi): #Получаем статус номера по его id
		stat = requests.get(f'{self.link}?api_key={self.token}&action=getStatus&id={idi}') #Делаем гет запрос
		return stat.text #Возращаем всё что получили в ответ от сайта

	def get_all_price(self, strana, servis=None):
		if servis == None: #Если не передали сервис
			spisok = requests.get(f'{self.link}?api_key={self.token}&action=getPrices&country={strana}') #Делаем гет запрос без учёта сервиса
		else: #В ином случае при передаче сервиса
			spisok = requests.get(f'{self.link}?api_key={self.token}&action=getPrices&service={servis}&country={strana}') #Делаем гет запрос с учётом сервиса
		return spisok.json() #Возращаем всё что получили в ответ от сайта в формате json