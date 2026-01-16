import telebot, os
import generator, board

TOKEN = 'INSERT_TOKEN_HERE'
bot = telebot.TeleBot(TOKEN)

chats = {}
styles = []

for file in os.listdir('styles'):
    if file.endswith('.py'):
        styles.append(file)

def default(message):
    if not message.chat.id in chats:
        chats[message.chat.id] = styles[0].removesuffix('.py')

# Хендлер для команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот. Напиши /help, чтобы узнать, что я умею, или /info, чтобы узнать обо мне побольше.")
    default(message)

@bot.message_handler(commands=['info'])
def send_welcome(message):
    info = """Привет! Я бот, который был создан для задания на онлайн курсе Kodland.
    Моя задумка была в преобразовании текста различными шрифтами.
    
    Этого бота было интересно создавать, придумывая структуру проекта."""
    bot.reply_to(message, info)
    default(message)

# Хендлер для команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    Я умею преобразовывать текст красивым шрифтом.
    Введи текст, и я его преобразую!
    Введи /style чтобы выбрать стиль текста.

    (Преобразовать русские символы нельзя.)
    """
    bot.reply_to(message, help_text)

# Хендлер для выбора стиля
@bot.message_handler(commands=['style'])
def fancy_text(message):
    default(message)
    current = styles.index(chats[message.chat.id]+".py")+1
    total = len(styles)
    preview = generator.generate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', chats[message.chat.id])
    bot.send_message(chat_id=message.chat.id, text=preview, reply_markup=board.board(current, total, chats[message.chat.id]))

@bot.callback_query_handler(func=lambda response: True)
def callback(response):
    current = styles.index(chats[response.message.chat.id]+".py")
    total = len(styles)-1
    if response.data == 'prev':
        if 0 <= current-1 <= total:
            chats[response.message.chat.id] = styles[current-1].removesuffix('.py')
            preview = generator.generate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', chats[response.message.chat.id])
            bot.delete_message(chat_id=response.message.chat.id, message_id=response.message.message_id)
            bot.send_message(chat_id=response.message.chat.id, text=preview, reply_markup=board.board(current-1+1, total+1, chats[response.message.chat.id]))
        else:
            bot.answer_callback_query(response.id, text="Вы в начале списка")
    
    elif response.data == 'next':
        if 0 <= current+1 <= total:
            chats[response.message.chat.id] = styles[current+1].removesuffix('.py')
            preview = generator.generate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', chats[response.message.chat.id])
            bot.delete_message(chat_id=response.message.chat.id, message_id=response.message.message_id)
            bot.send_message(chat_id=response.message.chat.id, text=preview, reply_markup=board.board(current+1+1, total+1, chats[response.message.chat.id]))
        else:
            bot.answer_callback_query(response.id, text="Вы достигли конца списка")

    elif response.data == 'pick':
        bot.delete_message(chat_id=response.message.chat.id, message_id=response.message.message_id)

# Хендлер для преобразования текста
@bot.message_handler(func=lambda message: True)
def fancy_text(message):
    default(message)
    fancy = generator.generate(message.text, chats[message.chat.id])
    bot.send_message(message.chat.id, fancy)

bot.polling(none_stop=True)