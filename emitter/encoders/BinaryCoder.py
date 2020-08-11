# Packager for tightly packing
# drone communication & diagnostics data

import struct


class BinaryCoder:

	# def __init__(self):
	# 	pass

	# dictionary data will be embedded
	# into tightly packed byte buffer to be sent
	def pack(self, data: dict) -> bytearray:
		return struct.pack('<hI'+ 'd' * 9 + 'f', *self.lookup(data))

	# unpacking received controller data according to spec
	# in protocol.md
	def unpack(self, data: bytearray) -> dict:
		vars = [
			'accX', 'accY', 'accZ',
			'gyrX', 'gyrY', 'gyrZ',
			'magX', 'magY', 'magZ',
			'temp'
		]
		vals = struct.unpack('<hI'+ 'd' * 9 + 'f', data)
		control = vals[0]
		mask = vals[1]
		vals = vals[2:]
		js = {}
		for i, var in enumerate(vars):
			js[var] = vals[i]
		return js

	def lookup(self, data: dict) -> list:
		control = 1
		mask = 0
		variables = [
			'accX', 'accY', 'accZ',
			'gyrX', 'gyrY', 'gyrZ',
			'magX', 'magY', 'magZ',
			'temp'
		]
		byte_data = [control]
		bit = 31
		for v in variables:
			if v in data:
				mask += 1 << bit
				byte_data.append(data[v])
			else:
				byte_data.append(0)
			bit -= 1
		byte_data.insert(1, mask)
		return byte_data
