from DataEmitter import *
import random
from time import sleep

emitter = DataEmitter(debug=True)
while 1:
    emitter.emit({
        "gyroX": random.random(),
        "accX": random.random(),
        "accZ": random.random(),
        "accY": random.random()
    })
    sleep(0.1)
