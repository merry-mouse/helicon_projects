# import pika, sys, os
import json
import pika
import django
from sys import path
from os import environ

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
    print("Received in photos...")
    data = json.loads(body)
    print(data)
    id, title = data["id"], data["title"]
    check_if_hotdog_in_name(id, title)

def check_if_hotdog_in_name(image_id, image_title):
    image_object = Photo.objects.get(id=image_id)
    if "hotdog" in image_title.lower():
        print("Found word hotdog in name!")
        image_object.not_hotdog_flag = False
        image_object.save()
    else:
        image_object.not_hotdog_flag = True
        image_object.save()

channel.basic_consume(queue='photos', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()