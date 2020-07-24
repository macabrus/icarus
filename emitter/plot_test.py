from DataEmitter import *
import random
from time import sleep
import math

emitter = DataEmitter(debug=True)

data = {
    "gyrX": random.random(),
    "gyrY": random.random(),
    "gyrZ": random.random(),
    "accX": random.random(),
    "accZ": random.random(),
    "accY": random.random(),
    "magX": random.random(),
    "magY": random.random(),
    "magZ": random.random(),
    "temp": random.random(),
    "x_normal": random.random(),
}

data_rate = 0.1

while 1:
    for k in data.keys():
        data[k] += random.random() - 0.5
    emitter.emit(data)
    sleep(data_rate)
