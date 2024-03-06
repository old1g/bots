from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import config as c

bot = Bot(token='6501484371:AAFokE9KfDjAZgUdlUnSxxfBuV6pYreTvuY', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(content_types=['text'])
async def start(message: types.Message):
    if message.text == '/start':
        await bot.send_message(message.chat.id, 'Здравствуйте, я бот', 
                               reply_markup=InlineKeyboardMarkup(row_width=1).
                               add(InlineKeyboardButton(text='Информация обо мне',
                                                        callback_data='info'),
                                   InlineKeyboardButton(text='Помощь', callback_data='help'),
                                   InlineKeyboardButton(text='Какое аниме мне посмотреть?',
                                                        callback_data='anime_list')))    


@dp.callback_query_handler(lambda call: True, state='*')
async def callback_inline(call, state: FSMContext):
    id_user = call.from_user.id
    if 'help' in call.data:
        await bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id, text='Помощь',
                                    reply_markup=InlineKeyboardMarkup().
                                     add(InlineKeyboardButton(text='Вернуться в главное меню', 
                                                              callback_data='menu')))
    
    elif 'anime_list' in call.data:
        list_anime = '\n'.join(['<a href="https://animego.org/anime/monolog-farmacevta-2422">1) Монолог фармацевта</a>',
                                          '<a href="https://animego.org/anime/provozhayuschaya-v-posledniy-put-friren-2430">2) Провожающая в последний путь Фрирен</a>',
                                          '<a href="https://animego.org/anime/ohotnik-h-ohotnik-2-280">3) Охотник х Охотник 2</a>',
                                          '<a href="https://animego.org/anime/krutoy-uchitel-onidzuka-556">4) Крутой учитель Онидзука</a>',
                                          '<a href="https://animego.org/anime/bleach-sennen-kessen-hen-2129">5) Блич: Тысячелетняя кровавая война</a>'])
        await bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id, 
                                    text='Посмотри вот такие аниме:\n'+list_anime, 
                                    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')), 
                                                              parse_mode=types.ParseMode.HTML)
        
    elif 'info' in call.data:
        await bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id, text=f"Твое имя пользователя: {call.message.chat.username}\nТвой айди: {call.message.chat.id}", 
                                    reply_markup=InlineKeyboardMarkup().
                                     add(InlineKeyboardButton(text='Вернуться в главное меню', 
                                                              callback_data='menu')))
    
    else:
        await call.message.edit_text('Здравствуйте, я бот')
        await call.message.edit_reply_markup(InlineKeyboardMarkup(row_width=1).
                               add(InlineKeyboardButton(text='Информация обо мне',
                                                        callback_data='info'),
                                   InlineKeyboardButton(text='Помощь', callback_data='help'),
                                   InlineKeyboardButton(text='Какое аниме мне посмотреть?',
                                                        callback_data='anime_list')))
        

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)