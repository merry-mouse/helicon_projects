# import pika, sys, os
import json
import pika
import django
from sys import path
from os import environ


path.append('/Users/stash/Desktop/my_projects/not_hotdog/') #Your path to settings.py file
environ.setdefault('DJANGO_SETTINGS_MODULE', 'not_hotdog.settings') 
django.setup()

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


channel.basic_consume(queue='photos', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()