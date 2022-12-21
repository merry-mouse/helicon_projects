# import pika, sys, os
import json
import pika
import django
from sys import path
from os import environ
import requests
import time


path.append('/Users/stash/Desktop/my_projects/not_hotdog/') # path to settings.py file
# need to set up DJANGO_SETTINGS_MODULE because we are accessing a model while outside the main app
environ.setdefault('DJANGO_SETTINGS_MODULE', 'not_hotdog.settings') 
django.setup()
from photoapp.models import Photo

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='photos')

# will be called whenever a message is received
# The ch is the channel where communication occurs
# method is the information concerning message delivery
# properties are user-defined properties on the message
# body is the message received.
def callback(ch, method, properties, body):
    print("\nReceived in photos...")
    data = json.loads(body)
    id, image_path = data["id"], data["image"]
    use_higgingface_model_to_check_if_hotdog(id, image_path)


def use_higgingface_model_to_check_if_hotdog(id, path_to_uploaded_image):
    # connect to the higgung face api
    API_URL = "https://api-inference.huggingface.co/models/julien-c/hotdog-not-hotdog"
    headers = {"Authorization": "Write authorization key here"}
    
    # getting the reulting scores from the model
    try:
        with open(path_to_uploaded_image, "rb") as f:
            data = f.read()
        response = requests.request("POST", API_URL, headers=headers, data=data)
        time.sleep(2) # wait 2 sec for model to download
        scores_list_of_dicts = json.loads(response.content.decode("utf-8"))
        # separating scores values from the received list
        hotdog_score = scores_list_of_dicts[0]['score'] # probability, float value from 0 to 1
        not_hotdog_score = scores_list_of_dicts[1]['score'] # probability, float value from 0 to 1
        print("\nHotdog score = ", hotdog_score, "\n","NOT Hotdog score = ", not_hotdog_score)

        # changing not_hotdog_flag depending on the model score
        image_object = Photo.objects.get(id=id)
        probability_border_value = 0.7 # we agreed to count is as a hotdog if hotdog score is more than 70%
        if hotdog_score > probability_border_value:
            print("\nHotdog score was higher than 70%, setting image not_hotdog_flag to False.")
            image_object.not_hotdog_flag = False
            image_object.save()
            print("\nChanged not_hotdog_flag to False, It is a hotdog.")
        else:
            print("\nHotdog score is too low, setting image not_hotdog_flag to True.\n")
            image_object.not_hotdog_flag = True
            image_object.save()
            print("\nChanged not_hotdog_flag to True, it is not a hotdog")
        print("---------------------------------------------------")

    except KeyError:
        print("Key Error happened, not_hotdog_flag wasn't changed")


channel.basic_consume(queue='photos', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()