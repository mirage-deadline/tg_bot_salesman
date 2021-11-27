from telebot import types


def size_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = types.KeyboardButton('Маленькую'), types.KeyboardButton('Большую')
    markup.add(*buttons)
    return markup


def pay_keybord():
    markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    buttons = types.KeyboardButton('Картой'), types.KeyboardButton('Наличкой')
    markup.add(*buttons)
    return markup

def confirm_keybord():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    buttons = types.KeyboardButton('Да'), types.KeyboardButton('Нет'), types.KeyboardButton('В главное меню')
    markup.add(*buttons)
    return markup

def bot_info():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = types.KeyboardButton('Заказать пиццу'), types.KeyboardButton('Возможности бота')
    markup.add(*buttons)
    return markup
