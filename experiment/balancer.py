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

def balance(x, y, throttle):
    tr=0
    tl=0
    br=0
    bl=0

    if x>0:
        tr+=x
        br+=x
    elif x<0:
        tl-=x
        bl-=x

    if y>0:
        tl+=y
        tr+=y
    elif y<0:
        bl-=y
        br-=y

    #maximum=max([tl, bl, tr, br])
    #for el in (tl, bl, tr, br): el/=maximum

    return tl*throttle, tr*throttle, bl*throttle, br*throttle

def scale(val, min, max):
    return min + (max - min) * val

