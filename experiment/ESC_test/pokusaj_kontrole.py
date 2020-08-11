import os
import time
import signal
os.system("sudo pigpiod")

time.sleep(1)


import pigpio


ESC=7

pi = pigpio.pi()
#pi.set_servo_pulsewidth(ESC, 500)

pi.set_servo_pulsewidth(ESC, 790)
time.sleep(3)




while True:
    for i in range(1015, 1500, 1):
        pi.set_servo_pulsewidth(ESC, i)
        print(i)
        time.sleep(0.1)


