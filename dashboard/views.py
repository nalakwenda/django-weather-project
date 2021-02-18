from django.shortcuts import render,redirect
import json
import datetime
from django.conf import settings as settings
import urllib.request




def timeConversion(time):
    convertedtime = datetime.datetime.fromtimestamp( int(time) ).strftime('%a, %d %b %Y %I%p')
    return convertedtime

def dashboard(request):
    if request.method == "GET":

        city = str(request.GET.get('search'))
        latitude, longitude = coordinates(city)
        #date_history, aqi_history, gases_history = history()
        date_forecast, aqi_forecast, gases_forecast = forecast(latitude,longitude)
        current_data = current(latitude,longitude)



        context ={ "current_data" : current_data,

             "aqi_forecast": aqi_forecast,
             "gases_forecast" : gases_forecast,
             "date_forecast": date_forecast,
             "city": city,
             }


        return render(request, 'dashboard/dashboard.html', context)
    else:
        city = ""
        latitude, longitude = coordinates(city)
        date_forecast, aqi_forecast, gases_forecast = forecast(latitude,longitude)
        current_data = current(latitude,longitude)

        print(city)

        context ={ "current_data" : current_data,

             "aqi_forecast": aqi_forecast,
             "gases_forecast" : gases_forecast,
             "date_forecast": date_forecast,

             }



        return render(request, 'dashboard/dashboard.html', context)

def coordinates(city):
    url= urllib.request.urlopen(
            "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&&appid="+ settings.API_KEY).read()

    data = json.loads(url)
    print(data)
    longitude = str(data['coord']['lon'])
    latitude = str(data['coord']['lat'])

    return latitude, longitude

def current(latitude,longitude):
    current_data = {}
    try:
        current= urllib.request.urlopen(
            "https://api.openweathermap.org/data/2.5/air_pollution?lat=" + latitude + "&lon=-" + longitude +"&appid=" +settings.API_KEY).read()
        list_of_current_data = json.loads(current)
        current_data= {
        "aqi" : list_of_current_data['list'][0]['main']['aqi'],
        "co" : list_of_current_data['list'][0]['components']['co'],
        "no"  : list_of_current_data['list'][0]['components']['no'],
        "no2"  : list_of_current_data['list'][0]['components']['no2'],
        "o3"  : list_of_current_data['list'][0]['components']['o3'],
        "so2"  : list_of_current_data['list'][0]['components']['so2'],
        "pm2_5"  : list_of_current_data['list'][0]['components']['pm2_5'],
        "pm10"  : list_of_current_data['list'][0]['components']['pm10'],
        "nh3"  : list_of_current_data['list'][0]['components']['nh3'],

    }
        return current_data
    except urllib.error.URLError as e:
       print(e.reason)
       return current_data

def forecast(latitude,longitude):

    date, aqi_forecast, gases_forecast = {},{},{}
    co,no,no2,o3,so2,pm2_5,pm10,nh3,dt,aqi=[],[],[],[],[],[],[],[],[],[]
    try:
        forecast= urllib.request.urlopen(
            "https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=" + latitude + "&lon=-" + longitude +"&appid=" + settings.API_KEY).read()
        list_of_forecast_data= json.loads(forecast)

        length=len(list_of_forecast_data['list'])
    #print(list_of_forecast_data['list'])

        for key in range(length):


            co.append(list_of_forecast_data['list'][key]['components']['co'])
            no.append(list_of_forecast_data['list'][key]['components']['no'])
            no2.append(list_of_forecast_data['list'][key]['components']['no2'])
            o3.append(list_of_forecast_data['list'][key]['components']['o3'])
            so2.append(list_of_forecast_data['list'][key]['components']['so2'])
            pm2_5.append(list_of_forecast_data['list'][key]['components']['pm2_5'])
            pm10.append(list_of_forecast_data['list'][key]['components']['pm10'])
            nh3.append(list_of_forecast_data['list'][key]['components']['nh3'])
            dt.append(list_of_forecast_data['list'][key]['dt'])
            aqi.append(list_of_forecast_data['list'][key]['main']['aqi'])

        for key in range(length):
            dt[key]=timeConversion(list_of_forecast_data['list'][key]['dt'])


            gases_forecast= {

        "CO" : co,
        "NO"  : no,
        "NO2"  : no2,
        "O3"  : o3,
        "SO2"  : so2,
        "PM2_5"  : pm2_5,
        "PM10"  : pm10,
        "NH3"  : nh3,

        }
        date = {"Date": dt}
        aqi_forecast = {
         "aqi" : aqi,

        }
        return date, aqi_forecast, gases_forecast
    except urllib.error.URLError as e:
       print(e.reason)
       return date, aqi_forecast, gases_forecast




"""
def history():

    try:
      history= urllib.request.urlopen(
            "https://api.openweathermap.org/data/2.5/air_pollution/history?lat=33.441792&lon=-94.037689&start=1606223802&end=1606482999&appid=d591b6d9bb2f9e4e998c427f3f0fe8ad").read()
    except urllib.error.URLError as e:
       print(e.reason)

    list_of_history_data= json.loads(history)
    length=len(list_of_history_data['list'])
    co,no,no2,o3,so2,pm2_5,pm10,nh3,dt,aqi=[],[],[],[],[],[],[],[],[],[]
    for key in range(length):
        #print(list_of_forecast_data['list'][key])
        #print(list_of_history_data['list'][key]['components']['co'])

        co.append(list_of_history_data['list'][key]['components']['co'])
        no.append(list_of_history_data['list'][key]['components']['no'])
        no2.append(list_of_history_data['list'][key]['components']['no2'])
        o3.append(list_of_history_data['list'][key]['components']['o3'])
        so2.append(list_of_history_data['list'][key]['components']['so2'])
        pm2_5.append(list_of_history_data['list'][key]['components']['pm2_5'])
        pm10.append(list_of_history_data['list'][key]['components']['pm10'])
        nh3.append(list_of_history_data['list'][key]['components']['nh3'])
        dt.append(list_of_history_data['list'][key]['dt'])
        aqi.append(list_of_history_data['list'][key]['main']['aqi'])

        #Convert date from UCT to datetime
        dt[key]=timeConversion(list_of_history_data['list'][key]['main']['aqi'])
    gases_history= {

        "CO2" : co,
        "NO"  : no,
        "NO2"  : no2,
        "O3"  : o3,
        "SO2"  : so2,
        "PM2_5"  : pm2_5,
        "PM10"  : pm10,
        "NH3"  : nh3,

        }
    date = {"Date": dt}
    aqi_history = {
         "aqi" : aqi,

        }
    return date, aqi_history, gases_history

"""""
