from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

TOKEN = '1246543622:AAGV4wEzLqINoUKufPCU_KaMfAcfwg1KUgk'


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?")

    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения от этого пользователя
    # должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


# Добавили словарь user_data в параметры.
def first_response(update, context):
    # Сохраняем ответ в словаре.
    context.user_data['locality'] = update.message.text
    update.message.reply_text(
        "Какая погода в городе {0}?".format(context.user_data['locality']))
    return 2


# Добавили словарь user_data в параметры.
def second_response(update, context):
    weather = update.message.text
    # Используем user_data в ответе.
    update.message.reply_text("Спасибо за участие в опросе! Привет, {0}!".
                              format(context.user_data['locality']))
    return ConversationHandler.END

def stop(update, context):
    update.message.reply_text('Хорошего дня.')
    return


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        # Без изменений
        entry_points=[CommandHandler('start', start)],

        states={
            # Добавили user_data для сохранения ответа.
            1: [MessageHandler(Filters.text, first_response, pass_user_data=True)],
            # ...и для его использования.
            2: [MessageHandler(Filters.text, second_response, pass_user_data=True)]
        },

        # Без изменений
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('stop', stop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
