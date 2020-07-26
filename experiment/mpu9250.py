import FaBo9Axis_MPU9250
import time
# to import from parent directory
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from emitter.DataEmitter import DataEmitter

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

em = DataEmitter(debug=True)
while True:
    acc = mpu9250.readAccel()
    gyro = mpu9250.readGyro()
    mag = mpu9250.readMagnet()
    temp = mpu9250.readTemperature()
    em.emit({"accX":acc["x"],"accY":acc["y"],"accZ":acc["z"],
             "magX":mag["x"],"magY":mag["y"],"magZ":mag["z"],
             "gyrX":gyro["x"],"gyrY":gyro["y"],"gyrZ":gyro["z"],
             "temp": temp})
    time.sleep(0.1155)
