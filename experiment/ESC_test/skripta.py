import os
import time
import signal
import sys
import signal

os.system("sudo pigpiod")

time.sleep(1)


import pigpio


esc1=15
esc2=19
esc3=20
esc4=24


pi = pigpio.pi()

pi.set_servo_pulsewidth(esc1, 800)
pi.set_servo_pulsewidth(esc2, 800)
pi.set_servo_pulsewidth(esc3, 800)
pi.set_servo_pulsewidth(esc4, 800)

def stop(sig, frame): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(esc1, 0)
    pi.set_servo_pulsewidth(esc2, 0)
    pi.set_servo_pulsewidth(esc3, 0)
    pi.set_servo_pulsewidth(esc4, 0)
    pi.stop()
    print("stopped.")
    sys.exit(0)

signal.signal(signal.SIGINT, stop)


time.sleep(2)
'''
def signal_handler(sig, frame):
    pi.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
'''

speed=int(input())
while True:
    pi.set_servo_pulsewidth(esc1, speed)
    pi.set_servo_pulsewidth(esc2, speed)
    pi.set_servo_pulsewidth(esc3, speed)
    pi.set_servo_pulsewidth(esc4, speed)
    speed=int(input())

