# VK и TG боты для техподдержки с интеграцией DialogFlow

![Иллюстрация к проекту]([https://github.com/ITerekhov98/chat_bots_lesson_3/Анимация.gif](https://github.com/ITerekhov98/chat_bots_lesson_3/%D0%90%D0%BD%D0%B8%D0%BC%D0%B0%D1%86%D0%B8%D1%8F.gif))

### Ссылки на работающих ботов:
- [VK](https://vk.com/club213637331)
- [Telegram](https://t.me/sam_isdat_bot)


Чат-боты, реализованные в этом репозитории используют сервис распознавания языка от Google - [DialogFlow](https://cloud.google.com/dialogflow). Они охватывают большинство шаблонных запросов от пользователей, на такие темы как:
- Приветствие
- Вопросы по бану
- Вопросы от действующих партнёров
- Что делать если забыл пароль
- Удаление аккаунта
- Устройство на работу

### Установка и запуск:
Скачайте репозиторий с кодом, создайте  файл `.env` и наполните его необходимыми данными, в формате `KEY=VALUE`. Ожидаются следующие параметры:
- `TG_BOT_TOKEN` - токен вашего бота в тг
- `GOOGLE_APPLICATION_CREDENTIALS` - путь к json-файлу, содержащему необходимую информацию для доступа к вашему проекту DialogFlow. Подробнее можно посмотреть [здесь](https://cloud.google.com/docs/authentication/getting-started)
- `GOOGLE_PROJECT_ID` - ID вашего проекта в DialogFlow. Как создать посмотрите [здесь](https://cloud.google.com/dialogflow/es/docs/quick/setup)
- `VK_API_TOKEN` - Токен, выданный VK API, для доступа бота к сообщениям. Получить его можно открыв *Ваша группа -> Настройки -> Работа с API*
- `SERVICE_TG_CHAT_ID` - ID телеграм чата в который будут отправляться репорты о возможных ошибках

Далее из терминала запускайте скрипты:
```
python vk_bot.py & python tg_bot.py
```
