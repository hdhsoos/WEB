from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import randint

TOKEN = '1246543622:AAGV4wEzLqINoUKufPCU_KaMfAcfwg1KUgk'


def start(update, context):
    update.message.reply_text(
        "Показываю клавиатуру",
        reply_markup=markup
    )


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Время истекло!', reply_markup=markup)


def dice(update, context):
    update.message.reply_text("Показываю клавиатуру", reply_markup=markup_two)


def timer(update, context):
    update.message.reply_text("Показываю клавиатуру", reply_markup=markup_third)


def mes(update, context):
    args = update.message.text
    if args == 'кинуть один шестигранный кубик':
        a = str(randint(1, 7))
        update.message.reply_text(a)
    elif args == 'кинуть 2 шестигранных кубика одновременно':
        a = str(randint(1, 7)) + ' ' + str(randint(1, 7))
        update.message.reply_text(a)
    elif args == 'кинуть 20-гранный кубик':
        a = str(randint(1, 21))
        update.message.reply_text(a)
    elif args == 'вернуться назад':
        update.message.reply_text("Показываю клавиатуру", reply_markup=markup)
    elif args == 'close':
        if 'job' not in context.chat_data:
            update.message.reply_text('Нет активного таймера')
            return
        job = context.chat_data['job']
        job.schedule_removal()
        del context.chat_data['job']
        update.message.reply_text('Таймер сброшен', reply_markup=markup)
    elif args.split()[1] in ['минут', 'секунд', 'минута', 'секунда']:
        due = int(update.message.text.split()[0])
        if due != 30:
            due *= 60
        chat_id = update.message.chat_id
        try:
            if 'job' in context.chat_data:
                old_job = context.chat_data['job']
                old_job.schedule_removal()
            new_job = context.job_queue.run_once(task, due, context=chat_id)
            context.chat_data['job'] = new_job
            update.message.reply_text(f'Засёк {due}', reply_markup=markup_fourth)
        except (IndexError, ValueError):
            update.message.reply_text('Использование: /set <секунд>')


def close_keyboard(update, context):
    update.message.reply_text("Ok", reply_markup=ReplyKeyboardRemove())


reply_keyboard1 = [['/dice', '/timer']]
markup = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=False, resize_keyboard=True)
reply_keyboard2 = [['кинуть один шестигранный кубик',
                    'кинуть 2 шестигранных кубика одновременно'],
                   ['кинуть 20-гранный кубик', 'вернуться назад']]
markup_two = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=False, resize_keyboard=True)
reply_keyboard3 = [['30 секунд', '1 минута'],
                   ['5 минут', 'вернуться назад']]
markup_third = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=False, resize_keyboard=True)
reply_keyboard4 = [['close']]
markup_fourth = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=False, resize_keyboard=True)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(MessageHandler(Filters.text, mes))
    dp.add_handler(CommandHandler("close_keyboard", close_keyboard))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
