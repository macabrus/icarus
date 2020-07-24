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
hl = 10

# (math.cos(x-3)+1)
lam = lambda x,y: y * (1.5**x - 1)

def fun(arr, lam):
    a = arr[:]
    for i, val in enumerate(a):
        a[i] = lam(i, val)
    return a[:]

def get_steepness(arr, step_size):
    return sum([x - arr[i - 1] for i, x in enumerate(arr)][1:])/(step_size * len(arr))

data_rate = 0.1

while 1:
    history['x_normal'].append(data['x_normal'])
    if len(history['x_normal']) > hl:
        history['x_normal'].pop(0)
    to_send['x_weighted'] = sum(fun(history['x_normal'], lam))/sum(fun([1] * hl, lam))
    to_send['x_normal'] = data['x_normal']
    print("steepness", get_steepness(history['x_normal'], 0.1))
    data['x_normal'] += random.random() - 0.5
    emitter.emit(to_send)
    sleep(data_rate)
