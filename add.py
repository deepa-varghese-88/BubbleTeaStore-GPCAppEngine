from flask import redirect, request, url_for, render_template, flash
from flask.views import MethodView
import gbmodel
import requests
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


class Add(MethodView):
    def get(self):
        """
        Render form to add entry in BubbleTea table
        """
        return render_template('add.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """

        model = gbmodel.get_model()

        #-------- sentiment-text analysis on review----------------
        review = request.form['review']

        rating = self.sentiment_analysis(review)
        #--------finish sentiment-text analysis--------------------

        result = model.insert(request.form['name'], rating, review, request.form['drink_to_order'])
        if result == False:
            flash("specified store:" + str(request.form['name']) + " could not be added to our database!")
        else:
            flash("Store " + str(request.form['name']) + " added, thank you!")
        return render_template('index.html')
    

    #SENTIMENT ANALYSIS
    def sentiment_analysis(self, review):

        client = language.LanguageServiceClient()
        try:
            review = review.decode('utf-8')
        except AttributeError:
            pass

        #create plain Text Document
        document = types.Document(
                content=review,
                type=enums.Document.Type.PLAIN_TEXT)

        #detect sentiment in the document.
        sentiment = client.analyze_sentiment(document).document_sentiment

        score = sentiment.score
        magnitude = sentiment.magnitude
        
        #set rating based on score
        if score <= -0.6:
            rating = 1
        elif score <= -0.2 and score > -0.6:
            rating = 2
        elif score <= 0.2 and score > -0.2:
            rating = 3
        elif score <= 0.6 and score > 0.2:
            rating = 4
        elif score <= 1 and score > 0.6:
            rating = 5

        return rating
        
