import telebot
from config import currency, TOKEN
from extentions import Schitalka, ConvertionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = "Чтобы начать, введите данные через ПРОБЕЛ: \n -имя валюты которую хотите купить маленькими буквами \n -за какую валюту преобретаете маленькими буквами \n -количество покупаемой валюты цифрами \nУвидеть список всех доступных валют можно по команде /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in currency.keys():
        text = '\n'.join((text, i, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        dannye = message.text.split(' ')
        if len(dannye) != 3:
            raise ConvertionException('Неверное количество параметров, должно быть 3 параметра.')
        quote, base, amount = dannye
        total_base = Schitalka.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e} Введите снова.')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду, что-то не так с системой.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

