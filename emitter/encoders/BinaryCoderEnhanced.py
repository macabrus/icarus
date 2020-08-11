# Packager for tightly packing
# drone communication & diagnostics data

import struct
import os
import json

scheme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagnostic_scheme.json')

# Even more enhanced version that doesn't waste space in buffer on variables that were not sent
class BitEncoder:

	def __init__(self, scheme_path=scheme_path):
		with open(scheme_path, 'r') as f:
			self.scheme = json.loads(f.read())
			self.control_len = self.scheme['control_len']
			self.mask_len = int(len(self.scheme['vars']) / 8) + 1

	# dictionary data will be embedded
	# into tightly packed byte buffer to be sent
	def pack(self, data: dict) -> bytearray:
		control = 1
		mask = 0
		bit = self.mask_len * 8 - 1
		vars = []
		fmt = ''
		for var in self.scheme['vars']:
			if var['name'] in data:
				mask += 1 << bit
				vars.append(data[var['name']])
				fmt += var['type']
			bit -= 1
		return (control.to_bytes(self.control_len, byteorder=self.scheme['endianness']) +
			mask.to_bytes(self.mask_len, byteorder=self.scheme['endianness']) +
			struct.pack(fmt, *vars))

	# unpacking received controller data according to spec
	# in protocol.md
	def unpack(self, data: bytearray) -> dict:
		vars = []
		fmt = ''
		mask = int.from_bytes(data[self.control_len : self.control_len + self.mask_len], byteorder=self.scheme['endianness'])
		for i in range(0, self.mask_len * 8):
			if mask & 1 << (self.mask_len * 8 - 1 - i):
				vars.append(self.scheme['vars'][i]['name'])
				fmt += self.scheme['vars'][i]['type']
		vals = struct.unpack_from(fmt, data, offset=self.control_len + self.mask_len)
		return dict(zip(vars, vals))