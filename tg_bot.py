import logging
import time

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext

from dialog_flow_lib import fetch_intent_response
from service_tg_bot import report_about_error

logger = logging.getLogger('tg_bot')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot_token = tg_bot_token

    def emit(self, record):
        log_entry = f'Exception in Tg_bot: \n{self.format(record)}'
        report_about_error(self.tg_bot_token, self.chat_id, log_entry)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def reply_using_dialog_flow(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = fetch_intent_response(
        update.message.from_user.id,
        user_message,
    )
    update.message.reply_text(response.query_result.fulfillment_text)


def main() -> None:
    env = Env()
    updater = Updater(env.str('TG_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        reply_using_dialog_flow
        )
    )
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(
        env.str('TG_BOT_TOKEN'),
        env.str('SERVICE_TG_CHAT_ID')
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
