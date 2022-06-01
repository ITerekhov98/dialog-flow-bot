import logging

import telegram


class LogsHandler(logging.Handler):

    def __init__(self, tg_bot_token, chat_id, bot_name):
        super().__init__()
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=tg_bot_token)
        self.bot_name = bot_name

    def emit(self, record):
        log_entry = f'Exception in {self.bot_name}: \n{self.format(record)}'
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)

