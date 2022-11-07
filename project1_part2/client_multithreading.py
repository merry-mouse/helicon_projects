import socket
import random
import time
import struct
import base64


# define ip address and the port
IP = socket.gethostbyname(socket.gethostname())
PORT = 65432 
ADDR = (IP,PORT)
DISCONNECT_MSG = "!DISCONNECT"

# generate random floats for temp and humidity in a given range
def make_random_floats():
    # use uniform module to generate floats for temp and humidity
    random_humidity_float = random.uniform(0.00, 100.00)
    random_temp_float = random.uniform(-50.00, 120.00)

    # convert randomized floats to int
    humidity_int = int(random_humidity_float *10**2)
    temperature_int = int(random_temp_float *10**2)

    # pack them into a struct
    packed = struct.pack('<2h',temperature_int, humidity_int)

    # pack them into base 64
    encoded = base64.b64encode(packed)

    return encoded

def main():
     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     client.connect(ADDR)
     print(f"[CONNECTED] Client connected to server {IP}:{PORT}")
     connected = True
     while connected:
        encoded_data = make_random_floats()
        client.sendall(encoded_data)
        print(f"Sent encoded data")
        # read the server’s reply
        msg = client.recv(1024) # will return up to 1024 bytes
        if msg == b"Disconnected" or msg == b"Timeout Error":
            connected = False
            print(msg)
            break
        elif msg == b"Connected":
            print(msg)
            time.sleep(10.0)
            continue

if __name__ == "__main__":
    main()
    