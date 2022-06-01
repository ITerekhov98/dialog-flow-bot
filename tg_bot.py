import logging
import time

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext

from dialog_flow_lib import fetch_intent_response
from log_hadler import LogsHandler


logger = logging.getLogger('tg_bot')


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def reply_using_dialog_flow(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = fetch_intent_response(
        update.message.from_user.id,
        user_message,
    )
    update.message.reply_text(response.query_result.fulfillment_text)


def main() -> None:
    env = Env()
    env.read_env()
    updater = Updater(env.str('TG_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        reply_using_dialog_flow
        )
    )
    logger.setLevel(logging.WARNING)
    logger.addHandler(LogsHandler(
        env.str('TG_BOT_TOKEN'),
        env.str('SERVICE_TG_CHAT_ID'),
        'TG_bot',
        )
    )
    while True:
        try:
            updater.start_polling()
            updater.idle()
        except Exception as err:
            logger.exception(err)
            time.sleep(120)


if __name__ == '__main__':
    main()
