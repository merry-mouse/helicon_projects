import socket
import random
import time
import struct
import base64

# generate random floats for temp and humidity in a given range
def make_random_floats():
    # use uniform module to generate floats for temp and humidity
    random_humidity_float = random.uniform(0.00, 100.00)
    random_temp_float = random.uniform(-50.00, 120.00)

    # convert randomized floats to int
    humidity_int = int(random_humidity_float *10**2)
    temperature_int = int(random_temp_float *10**2)

    # pack them into a struct
    packed = struct.pack('<2i',temperature_int, humidity_int)

    # pack them into base 64
    encoded = base64.b64encode(packed)

    return encoded


# define ip address and the port
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# creating server socket
# AF_INET is the Internet address family for IPv4
# sock_stream uses TCP protocol by default
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))

    # send package with randomized numbers every 10 seconds
    while True:
        encoded_data = make_random_floats()
        s.sendall(encoded_data)
        # read the server’s reply
        data = s.recv(1024).decode("utf-8") # will return up to 1024 bytes
        print(f"Sent encoded data: {data!r}")
        time.sleep(10.0)


    
