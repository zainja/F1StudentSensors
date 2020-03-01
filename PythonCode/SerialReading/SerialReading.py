"""
class for reading serial signals from the arduino
sync is done for 10 times before it is sent to the table
data array is constructed in the while loop
sent to data parsing where is it mapped to the different sensors
a dictionary constructed
push data sends the dictionary to the table
"""

import serial
import time
from PythonCode.SerialReading.data_to_sent import data_sent
from rethinkdb import RethinkDB
import sys

r = RethinkDB()
try:
    conn = r.connect("sam.soon.it", 8912).repl()
except:
    exit(0)
print("Server connected")
ARDUINO_PATH = ""
RESET_TIME = 30
DATA_LEN = 13
SYNC_TIMES = 10
synced = 0

'''
detect the OS
'''
if sys.platform.startswith('linux'):
    print("Linux")
    ARDUINO_PATH = '/dev/ttyACM1'
elif sys.platform.startswith('win'):
    ARDUINO_PATH = 'COM3'
elif sys.platform.startswith('darwin'):
    ARDUINO_PATH = '/dev/tty.usbmodemfa141'

try:
    serial_port = serial.Serial(ARDUINO_PATH, 9600)
except IOError:
        print("IO error")
        exit(0)

last_time = 0
data = []


def push_data(data_dict):
    print(data_dict)
    r.db("F1_data").table("sensor_data").insert(data_dict).run()


def parse_data(data_to_be_sent):
    print(data_to_be_sent)
    data_obj = data_sent(data_to_be_sent)
    print(data_obj.return_dict())
    push_data(data_obj.return_dict())


while True:
    byte = serial_port.read(1)[0]
    dt = (time.time() * 1000) - last_time
    last_time += dt

    if synced < SYNC_TIMES:
        if dt > RESET_TIME:
            synced += 1
            print("synced")
        # this is to go back after the while loop
        continue
    # read the next 13 byte
    if dt >= RESET_TIME:
        print("Clear data buffer")
        data = [byte]
    else:
        data.append(byte)

    if len(data) == DATA_LEN:
        parse_data(data)
        data = []
