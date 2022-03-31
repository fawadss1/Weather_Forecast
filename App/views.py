from django.contrib import messages
from django.shortcuts import render
import requests


def index(request):
    if request.method == 'POST' and 'cityName' in request.POST:
        city = request.POST.get('city').title()
        try:
            response = requests.get(
                f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=10&appid=0d82669c229f73426179f838f2c97210').json()
            if not response:
                messages.error(request, "Sorry! Your City Cannot Be Found ")
        except requests.exceptions.ConnectionError:
            messages.error(request, "Sorry! You Have No Internet Access")
            response = {}
        return render(request, 'index.html', {'cityData': response})
    if request.method == 'POST':
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid=0d82669c229f73426179f838f2c97210').json()
        weather_data = {
            'city': response['name'],
            'country': response['sys']['country'],
            'current_temp': response['main']['temp'],
            'min_temp': response['main']['temp_min'],
            'max_temp': response['main']['temp_max'],
            'feels_like': response['main']['feels_like'],
            'pressure': response['main']['pressure'],
            'humidity': response['main']['humidity'],
            'wind_spd': response['wind']['speed'],
            'wind_direction': response['wind']['deg'],
            'icon': response['weather'][0]['icon'],
            'desc': response['weather'][0]['description'],
        }
    else:
        weather_data = {}
    return render(request, 'index.html', {'weatherData': weather_data})
