import pika, time, json

# establishing a connection with the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# method parameter is the information about a message and body is the message to be sent
def send_message(method, body): # handles the sending of the message
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='photos', body=json.dumps(body), properties=properties)
    print('\n----MESSAGE WAS SENT TO THE RECEIVER----\n')
