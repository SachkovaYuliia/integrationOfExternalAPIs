import requests
from http.client import responses
from dotenv import load_dotenv
import os
import logging
import time

load_dotenv()

api_key = os.getenv('API_KEY')
api_token = os.getenv('TG_TOKEN')

logging.basicConfig(
    filename='app.log', 
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s',  
)

start_time = time.time()
elapsed_time = time.time() - start_time

city = input("Введіть місто: ")
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Температура в {city}: {data['main']['temp']} C")
else:
    print(f"temperature: Error: {response.status_code}")

