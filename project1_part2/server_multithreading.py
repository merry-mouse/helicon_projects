import socket
import threading # to handle multiple clients 
import base64
import struct


# define ip address and the port
IP = socket.gethostbyname(socket.gethostname())
PORT = 65432 
ADDR = (IP,PORT)


# decodes given temp and humidity numbers recieved from the client into 2 integers
def decode(given_str):
    # print(f"given string = {given_str}")
    # decoding the string from base 64 to bytes
    decoded = base64.b64decode(given_str)
    # print(f"decoded str = {decoded}")

    try:
        # unpacking it into a tuple, using < for writing bytes into little-indian
        unpacked = struct.unpack('<2h',decoded)
        
        # representing given integers into floats
        temperature = unpacked[0]
        humidity = unpacked[1]

        # convert the numbers to floats
        temperature = float("{:.2f}".format(temperature*10**-2))
        humidity = float("{:.2f}".format(humidity*10**-2))

        return temperature, humidity
    except struct.error:
        print("Struct Error")
        


def handle_client(conn, addr):
    # denote that new connection was created
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            data = conn.recv(1024)
            # send message to the client
            conn.send(b"Connected")
            decoded_temp, decoded_humidity = decode(data)
            # check if client is misbehaving
            if (decoded_temp >= -50.00 and decoded_temp <= 120.00)\
                and (decoded_humidity >= 0.00 and decoded_humidity <= 100.00):
                print(f"Temperature is: {decoded_temp} and Humidity is: {decoded_humidity}")
            else:
                # send message that client is disconnected
                conn.send(b"Disconnected")
                print("Misbehaved client disconnected.")
                connected = False
        except TimeoutError:
                # send message that client is disconnected
                conn.send(b"Timeout Error")
                print("Timeout Error.")
                connected = False
    conn.close()


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # takes port and addr in a tuple
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
            # accfept connection from any client
            conn,addr = server.accept()
            conn.settimeout(10.1)
            # create separate thread for a client
            thread = threading.Thread(target=handle_client, args=(conn,addr))
            thread.start()
            # print active connections
            # -1 because there is a connection called main
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



if __name__ == "__main__":
    main()
    
