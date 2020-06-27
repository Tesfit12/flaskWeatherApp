import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def index():
    key_code = '93373de30fe2fe54c87196440b0c1627'
    city_name = 'Israel'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={key_code}'
    r = requests.get(url).json()

    weather_obj = {
        'city': r['name'],
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    return render_template('weather.html', weather_obj=weather_obj)

     