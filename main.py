import telebot
from telebot import types
from telebot.handler_backends import MemoryHandlerBackend
from data import config
from states.food import States
from transitions import Machine
from keybords.default import buttons
from utils.set_bot_commands import set_default_commands


bot = telebot.TeleBot(config.TOKEN)
set_default_commands(bot)
transitions = [
    ['pizza', States.DIALOG_START, States.CHOOSE_SIZE],
    ['size', States.CHOOSE_SIZE, States.CHOOSE_PAYMENT],
    ['get_back', States.CHOOSE_PAYMENT, States.CHOOSE_SIZE],
    ['payment', States.CHOOSE_PAYMENT, States.MAKE_SURE],
    ['answer_y', States.MAKE_SURE, States.DONE_ORDER],
    ['answer_n', States.DONE_ORDER, States.CHOOSE_SIZE],
    ['cancel', '*', States.DIALOG_START]]
m = Machine(states=States, transitions=transitions, initial=States.DIALOG_START)
order = {}


@bot.message_handler(func= lambda message: any([message.text == '/buy_pizza', message.text == 'Заказать пиццу']))
def greeting(message):
    bot.send_message(message.chat.id, text='Какую пиццу Вы хотите? Большую или маленькую?', reply_markup= buttons.size_keyboard())
    m.pizza()

@bot.message_handler(func=lambda message: m.state.value == States.CHOOSE_SIZE.value)
def get_ans(message):

    if message.text.lower() in ['большую', 'маленькую']:
        m.size()
        bot.send_message(message.chat.id, 'Как будете платить? Возможна оплата картой и наличкой.', reply_markup=buttons.pay_keybord())
        order['size'] = message.text.lower()
    elif message.text == '/cancel':
        bot.send_message(message.chat.id, text='Вы вышли в главное меню', reply_markup=None)
        m.cancel()
    else: 
        bot.send_message(message.chat.id, text='Попробуйте ввести из выбранного. Вернуться в главное меню можно по команде /cancel')
        return    


@bot.message_handler(func=lambda message: m.state == States.CHOOSE_PAYMENT)
def payment(message):
    
    if message.text.lower() in ['картой', 'наличкой']:
        m.payment()
        order['pay_method'] = message.text.lower()
        bot.send_message(message.chat.id, text= 'Вы хотите {} пиццу, оплата - {}?'.format(order['size'], order['pay_method']), reply_markup=buttons.confirm_keybord())
    elif message.text == '/cancel':
        bot.send_message(message.chat.id, text='Вы вышли в главное меню')
        m.cancel()
    else: 
        bot.send_message(message.chat.id, text='Возможна оплата картой и наличкой. Вернуться в главное меню можно по команде /cancel')
        return
    

@bot.message_handler(func=lambda message: m.state == States.MAKE_SURE)
def confirm_order(message):
    if message.text.lower() == 'да':
        m.cancel()
        bot.send_message(message.chat.id, text='Спасибо за заказ', reply_markup=buttons.bot_info())
    elif message.text.lower() == '/cancel' or 'нет' or 'В главное меню':
        bot.send_message(message.chat.id, text='Выход в главное меню. Вы можете собрать заказ с самого начала!', reply_markup=buttons.bot_info())
        m.cancel()
    else: 
        bot.send_message(message.chat.id, text='Проверьте правильность ввоода\
            Возможна оплата картой и наличкой. Вернуться в главное меню можно по команде /cancel')
        return

@bot.message_handler(func= lambda message: any([message.text == '/help', message.text == 'Возможности бота']))
def greetings(message):
    bot.send_message(message.chat.id, 'В данном боте Вы можете заказать самую лучшую пиццу, просто нажимаете /buy_pizza и выбираете')
    

bot.infinity_polling()