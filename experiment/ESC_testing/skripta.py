import os
import time
import signal
import sys
os.system("sudo pigpiod")

time.sleep(1)


import pigpio


ESC=7

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 500)

'''
def signal_handler(sig, frame):
    pi.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
'''

while True:
    for i in range(500, 2500):
        pi.set_servo_pulsewidth(ESC, i)
        print(i)
        time.sleep(0.01)
    for i in range(2500, 500, -1):
        pi.set_servo_pulsewidth(ESC, i)
        print(i)
        time.sleep(0.01)


