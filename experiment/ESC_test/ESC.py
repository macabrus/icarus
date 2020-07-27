# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.

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

def manual_drive(): #You will use this function to program your ESC if required
    print("Value between 0 and max value:")    
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
        elif inp == "control":
            control() #
            break
        elif inp == "arm":
            arm()
            break    
        else:
            pi.set_servo_pulsewidth(ESC,inp)
                
def calibrate():   #the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, min_value)
            print("Wierd eh! Special tone")
            time.sleep(2)
            print("Wait for it ....")
            #time.sleep (5)
            print("Im working on it, DONT WORRY JUST WAIT.....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print("Arming ESC now...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print("See.... uhhhhh")
            control() # You can change this to any other function you want
            
def control(): 
    print("Starting the motor. I hope its calibrated and armed, if not restart by giving 'x'")
    #time.sleep(1)
    speed = 1500    # speed should be between 700 and 2000
    print("Controls - \na - decrease speed\n d - increase speed\nq - decrease a lot of speed\ne - increase a lot of speed")
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()
        
        if inp == "q":
            speed -= 100    # decrementing the speed
            print("speed = %d" % speed)
        elif inp == "e":    
            speed += 100    # incrementing the speed
            print("speed = %d" % speed)
        elif inp == "d":
            speed += 10     # incrementing the speed 
            print("speed = %d" % speed)
        elif inp == "a":
            speed -= 10     # decrementing the speed
            print("speed = %d" % speed)
        elif inp == "stop":
            stop()          #going for the stop function
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break    
        else:
            print("Press a,q,d or e")
            
def arm(): #the arming procedure of an ESC 
    print("Connect the battery and press Enter")
    inp = input()    
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        control() 
        
def stop(): #This will stop every action your Pi is performing for ESC.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

print("For the first time launch, select 'calibrate'")
print("calibrate \ manual \ control \ arm \ stop")

inp = input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else:
    print("Thank You for not following the things I'm saying... now you gotta restart the program!")

