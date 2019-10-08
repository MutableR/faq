#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.


import logging
from bot_informer.db import DBHelper

import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from bot_informer.config import TG_TOKEN
from bot_informer.mwt import MWT
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

db = DBHelper()

FAQ, ANSWER  =  range(2)

def start(update, context):
    update.message.reply_text(
        "Hello {}".format(update.message.from_user.first_name)
    )

def faq(update, context):
    if db.get_owmers() in get_admin_ids():
        faq = db.get_items()
    return faq, ANSWER
def add_data(update, context):
    if update.effective_user.id in get_admin_ids(context.bot, update.message.chat_id):
        update.message.reply_text(
            "Pls give me question\n"
        )
        item_text = update.message.text
        owner = update.message.from_user
        db.add_item(item_text,owner)
        return

@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

def main():
    #create db
    db.setup()
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    updater = Updater(token=TG_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with entry points
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start',start), CommandHandler('faq', faq)])

    dp.add_handler(conv_handler)

    #log all errors
    dp.add_error_handler()

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()