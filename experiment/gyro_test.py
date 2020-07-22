#!/usr/bin/python
import smbus
import math
import struct
from time import sleep, time

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


# TODO - OPTIMIZE BY READING WHOLE BLOCK AT ONCE
# TEST TEST TEST!!!

#def to_signed_short(val):
#    return -(val & 0x8000) | (val & 0x7fff)

def read_block_2c(reg, len):
    block = bytearray(bus.read_i2c_block_data(address, reg, len*2))
    return struct.unpack('h'*len, block)

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_pitch(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return math.degrees(radians)

def get_roll(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return -math.degrees(radians)
 
def get_yaw(x,y,z):
    radians = math.atan2(z, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

clock = 0.1

while 1:
    r_start = time()
    
    ### Accel readings
    ax, ay, az = read_word_2c(0x43), read_word_2c(0x45), read_word_2c(0x47)
    #ax, ay, az = read_block_2c(0x43,3) # POTENTIALLY FASTER
    ax, ay, az = ax/131, ay/131, az/131
    
    ### Gyro readings
    gx, gy, gz = read_word_2c(0x3b), read_word_2c(0x3d), read_word_2c(0x3f)
    #gx, gy, gz = read_block_2c(0x3b,3) # POTENTIALLY FASTER
    gx, gy, gz = gx/16384, gy/16384, gz/16384
    
    r_end = time()
    
    ### Output
    print('Gyr: Pitch: {: >7,.2f}°, Roll: {: >7,.2f}° Yaw: {: >7,.2f}°'.format(get_pitch(gx, gy, gz), get_roll(gx, gy, gz), get_yaw(gx, gy, gz)),
          'Acc: X: {: >7,.2f}, Y: {: >7,.2f}, Z: {: >7,.2f}'.format(ax, ay, az),
          'T-Read: {: >5.3f} s'.format(r_end - r_start))
    if clock - (r_end - r_start) > 0:
        sleep(clock - (r_end - r_start))
