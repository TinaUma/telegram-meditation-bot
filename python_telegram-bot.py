import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# Загружаем переменные из файла .env
load_dotenv()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Словарь с медитациями для разных настроений
MEDITATIONS = {
    "1": {
        "mood": "тревожное",
        "description": "Медитация для снятия стресса (8 минут).",
        "audio_link": "https://www.youtube.com/watch?v=RjJhfbJJM2Q"
    },
    "2": {
        "mood": "грустное",
        "description": "Медитация для благодарности (6 минут).",
        "audio_link": "https://www.youtube.com/watch?v=6SE-HFqis4g"
    },
    "3": {
        "mood": "спокойное",
        "description": "Медитация для спокойствия (5 минут).",
        "audio_link": "https://www.youtube.com/watch?v=b-PoulK3Lls"
    }
}

# Константы для клавиатуры
INITIAL_KEYBOARD = [
    ["СТАРТ"]
]
MAIN_KEYBOARD = [
    ["СТАРТ", "Новая медитация"],
    ["Начать заново", "Завершить"]
]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("МЕНЮ", callback_data='show_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_keyboard = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True, one_time_keyboard=False)
    # Проверяем, откуда вызвана функция: из сообщения или callback
    if update.message:
        await update.message.reply_text(
            "Привет! Я бот для релаксации и медитаций. 🎶 Хочешь послушать персонализированную аудио-медитацию? Нажми СТАРТ или выбери МЕНЮ.",
            reply_markup=reply_keyboard
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "Привет! Я бот для релаксации и медитаций. 🎶 Хочешь послушать персонализированную аудио-медитацию? Нажми СТАРТ или выбери МЕНЮ.",
            reply_markup=reply_keyboard
        )

# Команда /meditate
async def meditate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_mood"] = True
    keyboard = [
        [InlineKeyboardButton("МЕНЮ", callback_data='show_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_keyboard = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True, one_time_keyboard=False)
    # Проверяем, откуда вызвана функция: из сообщения или callback
    if update.message:
        await update.message.reply_text(
            "Как ты себя чувствуешь? Выбери:\n1. Тревожно\n2. Грустно\n3. Спокойно\nНапиши номер (1, 2 или 3).",
            reply_markup=reply_keyboard
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "Как ты себя чувствуешь? Выбери:\n1. Тревожно\n2. Грустно\n3. Спокойно\nНапиши номер (1, 2 или 3).",
            reply_markup=reply_keyboard
        )

# Обработка первого сообщения или неизвестных команд
async def handle_first_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = ReplyKeyboardMarkup(INITIAL_KEYBOARD, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Привет! Кажется, мы ещё не начали. Нажми СТАРТ, чтобы запустить бота! 🎶",
        reply_markup=reply_keyboard
    )

# Обработка ответа пользователя (выбор настроения или кнопки)
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if context.user_data.get("awaiting_mood"):
        if text not in MEDITATIONS:
            reply_keyboard = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True, one_time_keyboard=False)
            await update.message.reply_text(
                "Пожалуйста, выбери 1, 2 или 3.\n1. Тревожно\n2. Грустно\n3. Спокойно",
                reply_markup=reply_keyboard
            )
            return

        meditation = MEDITATIONS[text]
        keyboard = [
            [InlineKeyboardButton("МЕНЮ", callback_data='show_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_keyboard = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text(
            f"Отлично! Для {meditation['mood']} настроения я подобрал медитацию:\n"
            f"{meditation['description']}\n"
            f"Слушай её здесь: {meditation['audio_link']}\n\n"
            f"Выбери действие ниже.",
            reply_markup=reply_keyboard
        )
        context.user_data["awaiting_mood"] = False
    elif text == "СТАРТ":
        await start(update, context)
    elif text == "Начать заново":
        await start(update, context)
    elif text == "Новая медитация":
        await meditate(update, context)
    elif text == "Завершить":
        reply_keyboard = ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True)  # Скрываем клавиатуру
        await update.message.reply_text("До свидания! Если захочешь вернуться, напиши /start. 🎶", reply_markup=reply_keyboard)

# Обработчик кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    logger.info(f"Обработка кнопки: {query.data}")  # Отладочный вывод
    await query.answer()

    if query.data == 'show_menu':
        keyboard = [
            [InlineKeyboardButton("Начать заново", callback_data='start')],
            [InlineKeyboardButton("Новая медитация", callback_data='meditate')],
            [InlineKeyboardButton("Завершить", callback_data='end')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Что ты хочешь сделать?", reply_markup=reply_markup)

    elif query.data == 'start':
        await start(update, context)

    elif query.data == 'meditate':
        await meditate(update, context)

    elif query.data == 'end':
        reply_keyboard = ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True)  # Скрываем клавиатуру
        await query.message.reply_text("До свидания! Если захочешь вернуться, напиши /start. 🎶", reply_markup=reply_keyboard)
        await query.message.delete()  # Удаляем сообщение с меню

# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка: {context.error}")
    if update and update.message:
        await update.message.reply_text("Произошла ошибка. Попробуй снова!")

def main():
    # Получаем токен из переменной окружения или файла .env
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Ошибка: Не указан TELEGRAM_BOT_TOKEN. Установите переменную окружения TELEGRAM_BOT_TOKEN с токеном вашего бота или проверьте файл .env.")

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("meditate", meditate))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^/"), handle_input))
    application.add_handler(MessageHandler(filters.COMMAND & ~filters.Regex("^/start$|^/meditate$"), handle_first_message))
    application.add_handler(CallbackQueryHandler(button))
    application.add_error_handler(error_handler)

    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()