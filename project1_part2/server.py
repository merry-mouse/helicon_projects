import socket
import base64
import struct


# decodes given temp and humidity numbers recieved from the client into 2 integers
def decode(given_str):
    # print(f"given string = {given_str}")
    # decoding the string from base 64 to bytes
    decoded = base64.b64decode(given_str)
    # print(f"decoded str = {decoded}")

    # unpacking it into a tuple, using < for writing bytes into little-indian
    unpacked = struct.unpack('<2i',decoded)
    # print(f"unpacked = {unpacked}")
    

    # representing given integers into floats
    temperature = unpacked[0]
    humidity = unpacked[1]

    # print to check 
    # print(temperature)
    # print(humidity)

    # convert the numbers to floats
    temperature = float("{:.2f}".format(temperature*10**-2))
    humidity = float("{:.2f}".format(humidity*10**-2))

    return temperature, humidity
   


if __name__  == "__main__":
    # define ip address and the port
    HOST = "127.0.1"
    PORT = 65432 # Port to listen on

    # creating server socket
    # AF_INET is the Internet address family for IPv4
    # sock_stream uses TCP protocol by default
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # associate the socket with a specific network interface and port number 
        s.bind((HOST, PORT)) 
        # enables a server to accept connections
        s.listen() 
        # blocks execution and waits for an incoming connection
        conn, addr = s.accept() #  provides the client socket object conn
        
        with conn:
            print(f"Connected by {addr}")
            # reads whatever data the client sends and echoes it back using conn.sendall()
            
            while True:
                # bufsize argument of 1024, the maximum amount of data to be received at once
                data = conn.recv(1024) # will return 1024 bytes
                # decode data recieved from the client
                decoded_temp, decoded_humidity = decode(data)
                
                # check if client is misbehaving
                if (decoded_temp >= -50.00 and decoded_temp <= 120.00)\
                    and (decoded_humidity >= 0.00 and decoded_humidity <= 100.00):
                    print(f"Temperature is: {decoded_temp} and Humidity is: {decoded_humidity}")
                else:
                    print("Misbehaved client disconnected.")
                    conn.sendall(b"Disconnected")
                    conn.close()
                    break
                if not data:
                    conn.close()
                    conn.sendall(b"Disconnected")
                    break
                conn.sendall(b"Connected")
    s.close()
    