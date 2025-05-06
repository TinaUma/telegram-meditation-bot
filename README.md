# Telegram Meditation Bot

Бот для релаксации и персонализированных медитаций.  
Помогает пользователям достигать состояния спокойствия через короткие аудио-медитации с YouTube, подобранные под настроение.  
Все медитации длиной 5–10 минут от **Toki Well-being** и **Milky Vegan Yoga**.  
Бот предоставляет удобную клавиатуру с кнопками для навигации.

## 🐍 Требования

- Python 3.10 или выше
- Аккаунт Telegram
- YouTube-доступ

## 🚀 Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/TinaUma/telegram-meditation-bot
cd telegram-meditation-bot
```

2. Создайте виртуальное окружение и активируйте его:

```bash
python -m venv .venv
.venv\Scripts\activate  # Для Windows
source .venv/bin/activate  # Для macOS/Linux
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте бота в Telegram через [@BotFather](https://t.me/BotFather) и получите токен.

5. Скопируйте файл `.env.example` и переименуйте его в `.env`:

```bash
cp .env.example .env  # или вручную скопируйте содержимое
```

6. Запустите бота:

```bash
python python_telegram-bot.py
```

## 📱 Использование

1. При запуске бота нажмите кнопку **"СТАРТ"** (она появляется автоматически).
2. Выберите **"Новая медитация"**, чтобы получить подборку под настроение:
   - Тревожно
   - Грустно
   - Спокойно
3. Бот отправит ссылку на подходящую аудио-медитацию с YouTube.
4. Используйте кнопки **"Начать заново"**, **"Новая медитация"**, **"Завершить"** для навигации.
5. Нажмите **"МЕНЮ"**, чтобы вернуться к выбору действий.

---

✨ *Наслаждайтесь моментом тишины и заботы о себе.*

## 🖼️ Примеры работы

### Начало работы (кнопка "СТАРТ")
![Начало работы](screenshots/ipad_start.jpg)

### Работа на iPad
![Работа на iPad](screenshots/ipad.jpg)

### Работа на iPhone
![Работа на iPhone](screenshots/iphone.jpg)

## 📄 Файл .env.example

```env
# Telegram API token
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Настроения (можно адаптировать список)
MOODS=Тревожно,Грустно,Спокойно

# Ссылки на медитации (по одному для каждого настроения)
YOUTUBE_LINK_TREVOGA=https://youtube.com/example1
YOUTUBE_LINK_GRUST=https://youtube.com/example2
YOUTUBE_LINK_SPOKOJNO=https://youtube.com/example3
```

