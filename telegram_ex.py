import requests
from telegram.ext import Application, CommandHandler, ContextTypes
from main import api_key, api_token


def get_weather(city: str) -> str:
    """
    :param city:
    :return:
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    print(response)
    data = response.json()
    print(data)
    if data.get("cod") != 200:
        return f"Не вдалося знайти погоду для міста {city}"
    weather_description = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    return (f"Погода в місті {city}:\n"
            f"Опис: {weather_description}\n"
            f"Температура: {temperature}\n"
            f"Вологість: {humidity}\n"
            f"Тиск: {pressure}\n")


async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привіт! Я бот погоди. Введіть /weather <місто>, щоб отримати погоду.')


async def weather(update, context: ContextTypes.DEFAULT_TYPE):
    """
    :param update:
    :param context:
    :return:
    """
    if not context.args:
        await update.message.reply_text("Введіть інше місто")
        return
    city = " ".join(context.args)
    weather_info = get_weather(city)
    await update.message.reply_text(weather_info)


def main():
    """
    :return:
    """
    application = Application.builder().token(api_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    application.run_polling()


if __name__ == '__main__':
    main()
