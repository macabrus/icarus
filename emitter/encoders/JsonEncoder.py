# JSON format encoder

import json


class JsonEncoder:

	# def __init__(self):
	# 	pass

	# dictionary data will be embedded
	# into tightly packed byte buffer to be sent
	def pack(self, data: dict) -> bytearray:
		return json.dumps(data).encode()

	# unpacking received controller data according to spec
	# in protocol.md
	def unpack(self, data: bytearray) -> dict:
		return json.loads(data.decode('utf8'))