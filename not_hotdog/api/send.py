import pika, time, json

# establishing a connection with the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=1000, blocked_connection_timeout=1000))
channel = connection.channel()


# method parameter is the information about a message and body is the message to be sent
def send_message(method, body): # handles the sending of the message
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='photos', body=json.dumps(body), properties=properties)
    print('\n----MESSAGE WAS SENT TO THE RECEIVER----\n')
