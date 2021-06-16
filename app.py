import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter

# @Yuri_ChangeCurrencyBot

bot = telebot.TeleBot(TOKEN)


# handler start help
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n \
<имя валюты> \n \
<в какую валюту перевести> \n \
<количество переводимой валюты> \n увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


# handler values to take currency
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# conversion currency
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')
        quote, base, amount = values
        quote = quote.lower()
        base = base.lower()
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        def toFixed(numObj, digits=0):
            return f"{numObj:.{digits}f}"

        text = f'Цена {int(amount)} {quote} в {base} - {toFixed(total_base, 2)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
