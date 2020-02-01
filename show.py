from flask import render_template
from flask.views import MethodView
import gbmodel
import requests
import os

class Show(MethodView):
    def get(self):
        """
        Displays all records of the bbtlocations table in entries.db database
        """
        model = gbmodel.get_model()
        entries = []
        for row in model.select():
            #---Call the PLACES API-------------
            place = self.places(row[0])
            #-----------------------------------
            #---Call the NUTRITIONIX API--------
            nutrition = self.nutritionix(row[3])
            #-----------------------------------
            if place != []:
                for p in place:
                    address = p['vicinity'] if 'vicinity' in p.keys() else 'unknown'
                    opening = p['opening_hours']['open_now'] if 'opening_hours' in p.keys() else 'unknown'
                    entries.append(dict(name=row[0], address=address, opening=opening,  rating=row[1], review=row[2], drink_to_order=row[3], nutrition=nutrition))
            

        return render_template('show.html', entries=entries)


    #PLACES API
    def places(self, keyword):
    
        api_key = os.environ.get('PLACES_API_KEY')#'AIzaSyBI8179aNanZ5-Sl2ORlJOzhlFQOlW-1Uc' #need api key of placesAPI
        # Base URL for Google Places API
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        # Lat/Long of Portland, OR
        location = 'location=45.517485,-122.679291&radius=30000'
        # Places type variable
        place = 'restaurant'
        # API response
        response = requests.get(url + location + '&type=' + place +'&keyword=' + keyword + '&key=' + api_key)

        r = response.json()
        return r['results']

    #Nutrition API
    def nutritionix(self, ingredient):

        url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
        # Declare the api header with api key (Fill in your own App ID and Key)
        api_id = os.environ.get('NUTRITION_API_ID')
        api_key = os.environ.get('NUTRITION_API_KEY')
        headers = {"Content-Type":"application/json", "x-app-id":"5c2df34a","x-app-key":"8fe8b429f197772c882ff65b93dfa7fa"}
        # Declare POST query as a dictionary, set query field to ingredient
        body = {"query":ingredient,"timezone": "US/Western"}
        # Make request to API endpoint, parse JSON response and return dict
        response = requests.post(url, headers = headers, json = body)
        r = response.json()

        if "foods" in r.keys():
            serving_weight_grams = r["foods"][0]["serving_weight_grams"] if "serving_weight_grams" in r["foods"][0].keys() else None
            nf_calories = r["foods"][0]["nf_calories"] if "nf_calories" in r["foods"][0].keys() else None
            nf_total_fat = r["foods"][0]["nf_total_fat"] if "nf_total_fat" in r["foods"][0].keys() else None
            nf_total_carbohydrate = r["foods"][0]["nf_total_carbohydrate"] if "nf_total_carbohydrate" in r["foods"][0].keys() else None
            nf_protein = r["foods"][0]["nf_protein"] if "nf_protein" in r["foods"][0].keys() else None
            result = dict(serving_weight_grams=serving_weight_grams, nf_calories=nf_calories, nf_total_fat=nf_total_fat, nf_total_carbohydrate=nf_total_carbohydrate, nf_protein=nf_protein)
        else:
            result = {"nutrition index": "unknown"}
            
        return result
