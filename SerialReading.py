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
from data_to_sent import data_sent
from rethinkdb import RethinkDB

r = RethinkDB()
conn = r.connect("localhost", 28015).repl()
RESET_TIME = 30
DATA_LEN = 13
SYNC_TIMES = 10
synced = 0
serial_port = serial.Serial('/dev/ttyACM1', 9600)
last_time = 0
data = []


def push_data(data_dict):
    print(data_dict)
    r.db("F1_data").table("sensor_data").insert(data_dict).run()


def parse_data(data_to_be_sent):
    print(data_to_be_sent)
    data_obj = data_sent(data_to_be_sent)
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
