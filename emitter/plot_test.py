from DataEmitter import *
import random
from time import sleep

emitter = DataEmitter(debug=True)

data = {
    "gyroX": random.random(),
    "accX": random.random(),
    "accZ": random.random(),
    "accY": random.random()
}

while 1:
    data['gyroX'] += random.random() - 0.5
    data['accX'] += random.random() - 0.5
    data['accY'] += random.random() - 0.5
    data['accZ'] += random.random() - 0.5
    emitter.emit(data)
    sleep(0.1)
