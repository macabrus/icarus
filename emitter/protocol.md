
# Emitted packet data format specification
Note: all float/double data is in little-endian!
Offsets represent starts of data block in packet
Lists of tuples represent (address, length) to denote length of register.

## CONTROL_BUFFER (with offset 0x00):
- 0x00, 4

## ACCELEROMETER: (with offset 0x04)
- 0x00, 8 - ACCELEROMETER_X
- 0x08, 8 - ACCELEROMETER_Y
- 0x10, 8 - ACCELEROMETER_Z

## GYROSCOPE: (with offset 0x18)
- 0x00, 8 - GYROSCOPE_X
- 0x08, 8 - GYROSCOPE_Y
- 0x10, 8 - GYROSCOPE_Z

## MAGNETOMETER: (with offset 0x1C)
- 0x00, 8 - MAGNETOMETER_X
- 0x08, 8 - MAGNETOMETER_Y
- 0x10, 8 - MAGNETOMETER_Z

## TEMPERATURE: (with offset 0x2C)
- 0x00, 8 - TEMPERATURE

Total: 84 bytes
