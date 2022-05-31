import logging

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext

from dialog_flow_lib import fetch_intent_response


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger('tg_bot')


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
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
