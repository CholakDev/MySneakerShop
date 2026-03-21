from telegram import Update, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import json

# Вставьте ваш токен бота здесь
BOT_TOKEN = "8643343159:AAHNdJ_QEMQYjX63umN1lcQweHTxrs7N1aM"
# Ссылка на ваше Mini App (обязательно HTTPS)
WEBAPP_URL = "https://ваша-ссылка.ru/sneaker_shop.html"

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Кнопка для открытия WebApp
    keyboard = [
        [InlineKeyboardButton("Открыть Магазин Обуви", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Привет! Нажми на кнопку ниже, чтобы открыть наш магазин:", reply_markup=reply_markup)

# Функция для обработки данных, полученных из WebApp (tg.sendData)
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Данные приходят в update.effective_message.web_app_data
    webapp_data = update.effective_message.web_app_data.data
    
    # Декодируем JSON, который мы отправили из JS
    data = json.loads(webapp_data)
    
    item = data.get('item', 'Неизвестный товар')
    size = data.get('size', 'Неизвестный размер')
    user_name = update.effective_user.first_name
    
    # Формируем сообщение админу (вам)
    admin_message = f"🚨 НОВЫЙ ЗАКАЗ! 🚨\n\nПокупатель: {user_name}\nТовар: {item}\nРазмер: {size}\n\nНе забудьте связаться с клиентом!"
    
    # Отправляем подтверждение пользователю
    await update.message.reply_text(f"Спасибо за заказ, {user_name}! Вы выбрали {item}, размер {size}. Мы свяжемся с вами в ближайшее время.")
    
    # Для теста отправляем это сообщение в тот же чат (чтобы вы видели, что заказ пришел)
    await update.message.reply_text(admin_message)

if __name__ == '__main__':
    # Создаем приложение
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Добавляем обработчик для команды /start
    application.add_handler(CommandHandler('start', start))
    
    # Добавляем обработчик для данных из WebApp
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    
    print("Бот запущен. Откройте Telegram и отправьте /start.")
    
    # Запускаем бота
    application.run_polling()