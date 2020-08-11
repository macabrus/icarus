# to import from parent directory
import sys, os
sys.path.append(os.path.abspath('../emitter'))

import time
import FaBo9Axis_MPU9250
from DataEmitter import DataEmitter
from balancer import balance, scale, esc1, esc2, esc3, esc4, pi

mpu9250 = FaBo9Axis_MPU9250.MPU9250()
em = DataEmitter(debug=False)

err = (0,0,0)

lower = 1030

def thread_job():
    while True:
        acc = mpu9250.readAccel()
        #gyro = mpu9250.readGyro()
        #mag = mpu9250.readMagnet()
        #temp = mpu9250.readTemperature()
        #print({"accX":acc["x"],"accY":acc["y"],"accZ":acc["z"],
        #         "magX":mag["x"],"magY":mag["y"],"magZ":mag["z"],
        #         "gyrX":gyro["x"],"gyrY":gyro["y"],"gyrZ":gyro["z"],
        #         "temp": temp})
        res = balance(acc['x'] - err[0], acc['y'] - err[1], 1)
        #print(("{:1.4f} "*7).format(acc['x'], acc['y'], acc['z'], *balance(acc['x'], acc['y'], 1)))
        pi.set_servo_pulsewidth(esc1, scale(res[1], lower, 1100))
        pi.set_servo_pulsewidth(esc2, scale(res[0], lower, 1100))
        pi.set_servo_pulsewidth(esc3, scale(res[2], lower, 1100))
        pi.set_servo_pulsewidth(esc4, scale(res[3], lower, 1100))
        time.sleep(0.1)
        #time.sleep(0.1155)

from threading import Thread

Thread(target=thread_job).start()
i = input()
