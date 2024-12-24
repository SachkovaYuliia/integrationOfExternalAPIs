import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

load_dotenv()
api_key = os.getenv('API_KEY')
api_token = os.getenv('TG_TOKEN')

user_states = {}

def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ua"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"Погода в {city.capitalize()}: {temp}°C, {description}."
    else:
        return "Не вдалося знайти погоду для вказаного міста. Спробуйте ще раз."

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я бот, який допоможе вам отримати погоду.\n"
        "Використовуйте /help, щоб дізнатися, що я вмію."
    )

async def help_command(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Список доступних команд:\n"
        "/start - Почати роботу з ботом\n"
        "/help - Отримати список команд\n"
        "/weather - Отримати поточну погоду"
    )

async def weather_command(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = "waiting_for_city"
    await update.message.reply_text("Вкажіть місто, для якого хочете отримати погоду:")

async def text_handler(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_states.get(user_id)

    if state == "waiting_for_city":
        city = update.message.text
        weather_info = get_weather(city)
        await update.message.reply_text(weather_info)
        user_states[user_id] = None  
    else:
        await update.message.reply_text(
            "Я вас не зрозумів. Використовуйте /help, щоб дізнатися, що я вмію."
        )

def main():
    application = Application.builder().token(api_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("weather", weather_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
