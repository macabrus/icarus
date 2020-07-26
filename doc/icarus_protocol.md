# Icarus Data/Controller protocol
Note: all float/double data is in little-endian!
Offsets represent starts of data block in packet
Lists of tuples represent (address, length) to denote length of register.

## CONTROL_BUFFER (with offset 0x00):
- 0x00, 2 - CONTROL_SHORT
- 0x02, 4 - MASK (toggle whether i-th data at i-th variable sequentially is included)

## ACCELEROMETER: (with offset 0x06)
- 0x00, 8 - ACCELEROMETER_X
- 0x08, 8 - ACCELEROMETER_Y
- 0x10, 8 - ACCELEROMETER_Z

## GYROSCOPE: (with offset 0x1e)
- 0x00, 8 - GYROSCOPE_X
- 0x08, 8 - GYROSCOPE_Y
- 0x10, 8 - GYROSCOPE_Z

## MAGNETOMETER: (with offset 0x36)
- 0x00, 8 - MAGNETOMETER_X
- 0x08, 8 - MAGNETOMETER_Y
- 0x10, 8 - MAGNETOMETER_Z

## TEMPERATURE: (with offset 0x4e)
- 0x00, 4 - TEMPERATURE

Total: 82 bytes
