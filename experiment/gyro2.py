'''
		Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
	http://www.electronicwings.com
'''
import smbus			#import SMBus module of I2C
import math
from time import sleep, time          #import

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
		high = bus.read_byte_data(Device_Address, addr)
		low = bus.read_byte_data(Device_Address, addr+1)
	
		#concatenate higher and lower value
		value = ((high << 8) | low)
		
		#to get signed value from mpu6050
		if(value > 32768):
				value = value - 65536
		return value

def dist(*l):
	return math.sqrt(sum([x**2 for x in l]))

def get_pitch(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return math.degrees(radians)

def get_roll(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return -math.degrees(radians)
 
def get_yaw(x,y,z):
    radians = math.atan2(z, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()
CLK = 0.01

print (" Reading Data of Gyroscope and Accelerometer")

while True:

	r_start = time()
	
	#Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0

	Gx = gyro_x/131.0
	Gy = gyro_y/131.0
	Gz = gyro_z/131.0

	print("Gx {: >7,.2f}\u00b0 {: >7,.2f}\u00b0/s, Gy {: >7,.2f}\u00b0 {: >7,.2f}\u00b0/s, Gz {: >7,.2f}\u00b0 {: >7,.2f}\u00b0/s, Ax {: >7,.2f}g, Ay {: >7,.2f}g, Az {: >7,.2f}g, Dist: {: >7,.2f}g".format(get_pitch(Ax,Ay,Az), Gx, get_roll(Ax, Ay, Az), Gy, get_yaw(Ax, Ay, Az), Gz, Ax, Ay, Az, dist(Ax, Ay, Az)))
	
	r_end = time()
	
	if CLK - (r_end - r_start) > 0:
		sleep(CLK - (r_end - r_start))