import FaBo9Axis_MPU9250
import time

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

while True:
    acc = mpu9250.readAccel()
    gyro = mpu9250.readGyro()
    mag = mpu9250.readMagnet()
    temp = mpu9250.readTemperature()
    print("acc", acc, "gyro:", gyro, "mag:", mag, "temp:", temp)
    time.sleep(0.1)
