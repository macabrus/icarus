from DataEmitter import *
from encoders.BitEncoder import BitEncoder
import random
from time import sleep
import math

emitter = DataEmitter(debug=True)

encoder = BitEncoder()
print(encoder.unpack(encoder.pack({"accX":653.35})))

data = {
    "accX": random.random(),
    "accZ": random.random(),
    "accY": random.random(),
    "gyrX": random.random(),
    "gyrY": random.random(),
    "gyrZ": random.random(),
    "magX": random.random(),
    "magY": random.random(),
    "magZ": random.random(),
    "temp": random.random(),
}

data_rate = 0.1

while 1:
    for k in data.keys():
        data[k] += random.random() - 0.5
    emitter.emit(data)
    sleep(data_rate)
