from flask import render_template
from flask.views import MethodView
import requests
import json
from google.cloud import translate
from google.cloud import translate_v2 as translate
import six
import os

class Index(MethodView):
    def get(self):

        #get weather conditions for Portland city
        cur_weather = self.weather()

        #get translations of main text in Chinese and Hindi
        text1, text2, text4 = self.translate_text()
        return render_template('index.html',text1 = text1,text2 = text2, text4=text4, cur_weather=cur_weather)


    # WEATHER API - AccuWeather API from www.developer.accuweather.com
    def weather(self):
        # API key - generated for each developer on sign up
        api_key = os.environ.get('WEATHER_API_KEY')
        params = (('apikey', 'xRDLck9bfGJ8XTm1FsfyiXURXnrwyjM5'),)
        
        response = requests.get('http://dataservice.accuweather.com/currentconditions/v1/350473', params=params)
        
        #original request call
        #response = requests.get('http://dataservice.accuweather.com/currentconditions/v1/350473?apikey=xRDLck9bfGJ8XTm1FsfyiXURXnrwyjM5')
        res = json.loads(response.text)
        
        cur_weather = []
        cur_weather.append(res[0]['WeatherText'])
        cur_weather.append(str(res[0]['Temperature']['Imperial']['Value'])+res[0]['Temperature']['Imperial']['Unit'])
        cur_weather.append("Day" if res[0]['IsDayTime'] else "Night")

        return cur_weather
    
    #Google Translate API------------
    def translate_text(self):
        # [START translate_translate_text]
        t1 = 'Add new location'
        t2 = 'Check out all locations'
        #t3 = 'Store Shut Down? Let us know'
        t4 = 'Let us Know about your fun time'
        
        text1 = []
        text2 = []
        #text3 = []
        text4 = []

        translate_client = translate.Client()
        if isinstance(t1, six.binary_type):
            t1 = t1.decode('utf-8')
        if isinstance(t2, six.binary_type):
            t2 = t2.decode('utf-8')
        #if isinstance(text3, six.binary_type):
         #   t3 = t3.decode('utf-8')
        if isinstance(text4, six.binary_type):
            t4 = t4.decode('utf-8')
            
        target = ['zh', 'hi']
        for t in target:
            text1.append(translate_client.translate(t1, target_language=t)['translatedText'])
            text2.append(translate_client.translate(t2, target_language=t)['translatedText'])
            #text3.append(translate_client.translate(t3, target_language=t)['translatedText'])
            text4.append(translate_client.translate(t4, target_language=t)['translatedText'])
            
        return text1, text2, text4
        #[END translate_translate_text]
