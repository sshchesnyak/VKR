import json
import requests
import pyowm


class WeatherWorker:
    def __init__(self):
        self.wind = 0
        self.precipitation = 0
        self.key = "9c81ec14b5ba45dbbc8171216222905"

    def get_weather(self, lat, lon):
        url = "http://api.weatherapi.com/v1/current.json"
        params = {'key': self.key, 'q': str(lat)+","+str(lon)}
        response = requests.get(url, params)
        raw_data = response.json()
        condition = raw_data.get('current')
        wind = condition.get('wind_kph')*10/36
        precipitation = condition.get('precip_mm')
        self.wind = wind
        self.precipitation = precipitation

    def wind_grade(self, landing_spot):
        grade = 0
        if 0 <= self.wind < 12:
            grade = -25/300*self.wind+1
        else:
            grade = 0
        landing_spot.wind = grade

    def precipitation_grade(self, landing_spot):
        grade = 0
        if 0 <= self.precipitation < 10:
            grade = -0.1*self.precipitation+1
        else:
            grade = 0
        landing_spot.precipitation = grade
