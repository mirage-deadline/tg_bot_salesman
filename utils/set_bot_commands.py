from telebot import types


def set_default_commands(bot):
    bot.set_my_commands(
        [
            types.BotCommand('/start', 'Запустить бота'),
            types.BotCommand('/help', 'Показать функции бота'),
            types.BotCommand('/buy_pizza', 'Заказать пиццу')

        ]
    )