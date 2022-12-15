import pika, time, json

# establishing a connection with the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# channel.queue_declare(queue='hello')
# for i in range(10):
#     channel.basic_publish(exchange='',
#     routing_key='hello',
#     body=f'Hello from Helicon!, message {i}')
#     print(f"Sent 'Hello from Helicon! message {i}'")
#     time.sleep(2)
# connection.close()

# method parameter is the information about a message and body is the message to be sent
def send_message(method, body): # handles the sending of the message
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='photos', body=json.dumps(body), properties=properties)
    print('\n----MESSAGE WAS SENT TO THE RECEIVER----\n')
