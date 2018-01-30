#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MAIN_MENU, COMMIT_MENU, COMMIT_MENU2, COMMIT_MENU3, TRACKING = range(5)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    reply_keyboard = [['Розпочнем', 'Вихід']]

    update.message.reply_text(
        'Привіт! Я бот сервісу "Пильнуй своїх".'
        'Я допоможу тобі налаштувати супроводження.'
        'Коли ми завершимо, я надсилатиму повідомлення про твої пересування, а також затримки у дорозі тому, на кого ти можешь покластися.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MAIN_MENU


def main_menu_phone(bot, update, user_data):
    update.message.reply_text('Введи номер телефона отримувача:',
                              reply_markup=ReplyKeyboardRemove())

    return COMMIT_MENU


def main_menu_done(bot, update, user_data):
    update.message.reply_text('До зустрічи!')

    return ConversationHandler.END


def commit_phone(bot, update, user_data):
    logger.info("phone: %s", update.message.text)
    text = update.message.text
    user_data['phone'] = text
    reply_keyboard = [['Вірно', 'Коригувати']]
    update.message.reply_text('Номер, який ти ввів: ' + text,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return COMMIT_MENU2

def confirm_tracking(bot, update, user_data):
    logger.info("phone: %s", update.message.text)
    text = update.message.text
    reply_keyboard = [['Поїхали']]
    update.message.reply_text('Чудово! Заходь до мене в чат та натискай "Поїхали", щоб розпочати подорож у '
                              'віртуальному сопроводженні. Щоб припинити супроводження натисни "Я у безпеці". У разі '
                              'потреби натискай "Допоможі мені"',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return COMMIT_MENU3


def start_tracking(bot, update, user_data):
    reply_keyboard = [['Допоможі мені!', 'Я в безпеці']]
    update.message.reply_text('Ввімкнений режім супроводу. Телефон отримувача: ' + user_data['phone'],
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return TRACKING


def sos(bot, update, user_data):
    reply_keyboard = [['Допоможі мені!', 'Я в безпеці']]
    update.message.reply_text('Допомога скоро прийде!',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return TRACKING


def home(bot, update, user_data):
    reply_keyboard = [['Розпочнем', 'Вихід']]
    update.message.reply_text('Радий допомогти!',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MAIN_MENU


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("461142496:AAFaDMdZmwwfdZgdmECXuBQ8fGEcFt8ZpiY")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN_MENU: [RegexHandler('^Розпочнем$',
                                     main_menu_phone,
                                     pass_user_data=True),
                        ],

            COMMIT_MENU: [
                MessageHandler(Filters.text,
                               commit_phone,
                               pass_user_data=True),
            ],
            COMMIT_MENU2: [
                RegexHandler('^Вірно$',
                             confirm_tracking,
                             pass_user_data=True),
                RegexHandler('^Коригувати$',
                             main_menu_phone,
                             pass_user_data=True),
            ],
            COMMIT_MENU3: [
                RegexHandler('^Поїхали$',
                             start_tracking,
                             pass_user_data=True),
            ],
            TRACKING: [
                RegexHandler('^Допоможі мені!$',
                             sos,
                             pass_user_data=True),
                RegexHandler('^Я в безпеці$',
                             home,
                             pass_user_data=True),
            ]
        },

        fallbacks=[RegexHandler('^Вихід$', main_menu_done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
