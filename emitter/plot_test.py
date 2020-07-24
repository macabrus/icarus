from DataEmitter import *
import random
from time import sleep
import math

emitter = DataEmitter(debug=True)

data = {
    "gyroX": random.random(),
    "accX": random.random(),
    "accZ": random.random(),
    "accY": random.random(),
    "x_normal": random.random(),
}

history = {
    "gyroX": [],
    "accX": [],
    "accY": [],
    "accZ": [],
    "x_normal": [],
}

to_send = {}
hl = 3

# (math.cos(x-3)+1)
lam = lambda x,y: y * (1.5**x - 1)

def fun(arr, lam):
    a = arr[:]
    for i, val in enumerate(a):
        a[i] = lam(i, val)
    return a[:]

while 1:
    history['x_normal'].append(data['x_normal'])
    if len(history['x_normal']) > hl:
        history['x_normal'].pop(0)
    print(history)
    to_send['x_weighted'] = sum(fun(history['x_normal'], lam))/sum(fun([1] * hl, lam))
    to_send['x_normal'] = data['x_normal']
    
    data['x_normal'] += random.random() - 0.5
    emitter.emit(to_send)
    sleep(random.random() * 0.3)
