import os
import time
os.system ("sudo pigpiod")
time.sleep(1) # if this delay is removed you will get an error
import pigpio

ESC=4  #Connect the ESC in this GPIO pin 

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0) 

max_value = 2000 #change this if your ESC's max value is different
min_value = 700  #change this if your ESC's min value is different

def calibrate():   #the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery now. You will hear two beeps, then wait for a gradual falling tone and press Enter")
        inp = raw_input()
        if inp == '':
            print "processing..."#tu je bilo puno sleepova, ne znam zakaj. Možda ima razloga  
            pi.set_servo_pulsewidth(ESC, min_value)
            pi.set_servo_pulsewidth(ESC, 0)
            pi.set_servo_pulsewidth(ESC, min_value)
            
def arm(): #the arming procedure of an ESC 
    print "Connect the battery and press Enter"
    inp = raw_input()    
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        control()


