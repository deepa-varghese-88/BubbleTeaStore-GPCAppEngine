from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision
from flask import redirect, request, url_for, render_template, flash
from flask.views import MethodView
import gbmodel
import os

class Fun(MethodView):
     
    def get(self):
        # Create a Cloud Datastore client.
        datastore_client = datastore.Client()

        # Use the Cloud Datastore client to fetch information from Datastore about each photo.
        query = datastore_client.query(kind='Pics')
        image_entities = list(query.fetch())

        # Return a Jinja2 HTML template and pass in image_entities as a parameter.
        return render_template('fun.html', image_entities=image_entities)

    def post(self):
        photo = request.files['file']

        #Upload image to Storage Bucket
        storage_client = storage.Client()
        # Get the bucket that the file will be uploaded to.
        CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')
        bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
        # Create a new blob and upload the file's content.
        blob = bucket.blob(photo.filename)
        blob.upload_from_string(
                photo.read(), content_type=photo.content_type)
        # Make the blob publicly viewable.
        blob.make_public()

        #-----VISION API for SafeSearch------
        ok = self.safesearch(blob, CLOUD_STORAGE_BUCKET)
        #-----------------------------------

        #Download image and info to Datastore
        # Create a Cloud Datastore client.
        if ok:
            datastore_client = datastore.Client()
            kind = 'Pics'
            # The name/ID for the new entity.
            name = blob.name
            # Create the Cloud Datastore key for the new entity.
            key = datastore_client.key(kind, name) 
            entity = datastore.Entity(key)
            entity['blob_name'] = blob.name
            entity['image_public_url'] = blob.public_url
        
            datastore_client.put(entity)
            flash("Image has been uploaded!")
        else:
            flash("Sorry, image was too inappropriate")
        
        return render_template('index.html')

    #VISION API - SafeSearch func        
    def safesearch(self,blob, CLOUD_STORAGE_BUCKET):
        
        storage_client = storage.Client()
        vision_client = vision.ImageAnnotatorClient()

        blob_uri = f'gs://{CLOUD_STORAGE_BUCKET}/{blob.name}'
        blob_source = {'source': {'image_uri': blob_uri}}

        result = vision_client.safe_search_detection(blob_source)
        detected = result.safe_search_annotation
        
        #processing Image
        if detected.adult >= 4 or detected.violence >= 4:
            ok = False
        else:
            ok = True

        return ok

