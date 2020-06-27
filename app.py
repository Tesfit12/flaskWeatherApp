import requests
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from requests.api import request

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

# create DB
db = SQLAlchemy(app)


# create table
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)




@app.route('/', methods=['GET', 'POST'])
def index():
    key_code = '93373de30fe2fe54c87196440b0c1627'


    if request.method == 'POST': # get the city from the input
        input_value = request.form.get('city_name')
        new_city = City(name=input_value)
        city_from_db = City.query.filter_by(name=input_value).first()
        
        if new_city and city_from_db is None: # check if city not exist
            db.session.add(new_city)
            db.session.commit()
            

    list_of_citys = []
    all_citys = City.query.all()

    for city in all_citys:

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city.name}&units=imperial&appid={key_code}'
        r = requests.get(url).json()

        weather_obj_list = {
            'city': r['name'],
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        list_of_citys.append(weather_obj_list)

    return render_template('weather.html', list_of_citys=list_of_citys)



@app.route('/delete_all')
def delete_all():
    all_city = City.query.all()
    for city in all_city:
        db.session.delete(city)
    db.session.commit()
    return redirect('/')

     
