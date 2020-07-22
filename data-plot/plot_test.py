from DataEmitter import *
import random
from time import sleep

emitter = DataEmitter(debug=True)
while 1:
    emitter.emit({"randomData": random.random(), "var2": random.random()})
    sleep(0.1)
