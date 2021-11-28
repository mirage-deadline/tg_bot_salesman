import telebot
from data import config
from keybords.default import buttons
from states.food import States
from telebot import types
from utils import state_actions as SA
from utils.set_bot_commands import set_default_commands


bot = telebot.TeleBot(config.TOKEN)
set_default_commands(bot)
order = {}


@bot.message_handler(func= lambda message: any([message.text == '/buy_pizza', message.text == 'Заказать пиццу']))
def greeting(message: types.Message):
    """
    Обработка первого хэндлера и выдача ФСМ для дальнейшей обработки
    """
    SA.create_base_state(message.from_user.id)
    bot.send_message(message.chat.id, text='Какую пиццу Вы хотите? Большую или маленькую?', reply_markup= buttons.size_keyboard())
    SA.add_state(message.from_user.id, States.DIALOG_START, 'pizza')


@bot.message_handler(func=lambda message: SA.get_state(message.from_user.id) == States.CHOOSE_SIZE.value)
def get_ans(message: types.Message):
    """
    Проверяем валидность полученного сообщения по размеру пиццы и в случае корректности направляем на хэндлер выбора оплаты
    """
    if message.text.lower() in ['большую', 'маленькую']:
        SA.add_state(message.from_user.id, States.CHOOSE_SIZE, 'size')        
        bot.send_message(message.chat.id, 'Как будете платить? Возможна оплата картой и наличкой.', reply_markup=buttons.pay_keybord())
        order[f'{message.from_user.id}_size'] = message.text.lower()
    elif message.text == '/cancel':
        bot.send_message(message.chat.id, text='Вы вышли в главное меню', reply_markup=None)
        SA.add_state(message.from_user.id, States.CHOOSE_SIZE, 'cancel')
    else: 
        bot.send_message(message.chat.id, text='Попробуйте ввести из выбранного. Вернуться в главное меню можно по команде /cancel')
        return    


@bot.message_handler(func=lambda message: SA.get_state(message.from_user.id) == States.CHOOSE_PAYMENT.value)
def payment(message: types.Message):
    """
    Проверка правильности созданного заказа
    """
    msg_id = message.from_user.id
    if message.text.lower() in ['картой', 'наличкой']:
        SA.add_state(msg_id, States.CHOOSE_PAYMENT, 'payment')        
        order[f'{message.from_user.id}_pay_method'] = message.text.lower()
        bot.send_message(message.chat.id, text= 'Вы хотите {} пиццу, оплата - {}?'.format(order[f'{msg_id}_size'], order[f'{msg_id}_pay_method']), reply_markup=buttons.confirm_keybord())
    elif message.text == '/cancel':
        bot.send_message(message.chat.id, text='Вы вышли в главное меню')
        SA.add_state(message.from_user.id, States.CHOOSE_PAYMENT, 'cancel')
    else: 
        bot.send_message(message.chat.id, text='Возможна оплата картой и наличкой. Вернуться в главное меню можно по команде /cancel')
        return
    

@bot.message_handler(func=lambda message: SA.get_state(message.from_user.id) == States.MAKE_SURE.value)
def confirm_order(message: types.Message):
    """
    Дальнейшие действия по отправке и внесению заказа куда-либо могут быть реалзованы после текущего состояния обработки заказа
    """
    if message.text.lower() == 'да':
        SA.add_state(message.from_user.id, States.MAKE_SURE, 'cancel')
        bot.send_message(message.chat.id, text='Спасибо за заказ', reply_markup=buttons.bot_info())
    elif message.text.lower() == '/cancel' or 'нет' or 'В главное меню':
        bot.send_message(message.chat.id, text='Выход в главное меню. Вы можете собрать заказ с самого начала!', reply_markup=buttons.bot_info())
        SA.add_state(message.from_user.id, States.MAKE_SURE, 'cancel')
    else: 
        bot.send_message(message.chat.id, text='Проверьте правильность ввоода\
            Возможна оплата картой и наличкой. Вернуться в главное меню можно по команде /cancel')
        return

@bot.message_handler(func= lambda message: any([message.text == '/help', message.text == 'Возможности бота']))
def greetings(message: types.Message):
    bot.send_message(message.chat.id, 'В данном боте Вы можете заказать самую лучшую пиццу, просто нажимаете /buy_pizza и выбираете')


@bot.message_handler(commands=['start'])
def say_hello(message: types.Message):
    bot.send_message(message.chat.id, 'Бот для заказа пиццы. Для подробностей нажимайте /help')
    

bot.infinity_polling()