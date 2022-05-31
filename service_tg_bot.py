import telegram


def report_about_error(token, chat_id, log_entry):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=log_entry)