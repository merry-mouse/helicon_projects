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
    id, path_to_uploaded_image = data["id"], data["image"]
    send_request_to_image_recognition_model(id, path_to_uploaded_image)


def send_request_to_image_recognition_model(id, path_to_uploaded_image):
    # sometimes hugging face model asks for additional time for loading, when it happens we want to try again a few times until we have the score
    MAX_TRIES = 2
    # try to get reulting scores from the model
    scores_list_of_dicts = query(path_to_uploaded_image)
    # we either get a list of dicts with scores or one dict with the error msg
    # if it is a 1 dict with error we will get key error and the we want to send 
    # the image to the model api again in max of MAX_TRIES attempts
    if type(scores_list_of_dicts) == list:
        # eerything fine, we got the scores, send no need to send a query again, just change flags according to the scores
        check_if_hotdog_and_change_flag(id, scores_list_of_dicts)
    else:
        for i in range(MAX_TRIES):
            print(f"Model required more time, starting another query, attempt number {i}...")
            scores_list_of_dicts = query(path_to_uploaded_image)
            if type(scores_list_of_dicts) == list:
                check_if_hotdog_and_change_flag(scores_list_of_dicts)
                break
            continue


# query to the pi with image classifier 
def query(path_to_uploaded_image):
    # connect to the hugging face model through api
    API_URL = "https://api-inference.huggingface.co/models/julien-c/hotdog-not-hotdog"
    headers = {"Authorization": "Bearer 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"}
    with open(path_to_uploaded_image, "rb") as f:
        data = f.read()
    response = requests.request("POST", API_URL, headers=headers, data=data)
    print(response)
    time.sleep(2)
    scores_list_of_dicts = json.loads(response.content.decode("utf-8"))
    print("\njson response from the model with API: ", scores_list_of_dicts)
    return scores_list_of_dicts


# changing not_hotdog_flag depending on the model score
def check_if_hotdog_and_change_flag(id, scores_list_of_dicts):
    image_object = Photo.objects.get(id=id) # get photo object to change it's hotdog_flag
    probability_border_value = 0.8 # we agreed to count is as a hotdog if hotdog score is more than 80%
    # separating scores values from the received list
    hotdog_score = scores_list_of_dicts[0]['score'] # probability, float value from 0 to 1
    not_hotdog_score = scores_list_of_dicts[1]['score'] # probability, float value from 0 to 1
    print("\nHotdog score = ", hotdog_score, "\n","NOT Hotdog score = ", not_hotdog_score)
    if hotdog_score > probability_border_value:
        print("\nHotdog score was higher than 80%, setting image not_hotdog_flag to False.")
        image_object.not_hotdog_flag = False
        image_object.save()
        print("\nChanged not_hotdog_flag to False, It is a hotdog.")
    else:
        print("\nHotdog score is too low, setting image not_hotdog_flag to True.\n")
        image_object.not_hotdog_flag = True
        image_object.save()
        print("\nChanged not_hotdog_flag to True, it is not a hotdog")
    print("---------------------------------------------------")


channel.basic_consume(queue='photos', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()