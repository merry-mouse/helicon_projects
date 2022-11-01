# importing modules
import struct
import base64

def decode(given_str):

    # decoding the string from base 64 to bytes
    decoded = base64.b64decode(given_str)

    # unpacking it into a tupleß
    unpacked = struct.unpack('2f',decoded)


    # representing given integers into floats
    temperature = unpacked[0]
    humidity = unpacked[1]

    # get rid of exponentioal and additional numbers after .
    temperature = ("{:.2f}".format(temperature/10**-42))
    humidity = ("{:.2f}".format(humidity/10**-42))

    print(f"Temperature is: {temperature} and Humidity is: {humidity}")

# given encoded str
coded_string = 'NAkAALoLAAA='

if __name__ == '__main__':
    decode(coded_string)


