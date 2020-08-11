from BitEncoderEnhanced import BitEncoder
import binascii

e = BitEncoder()
data = {
	"ax": 4.54,
	"ay": 2.6653,
	"az": 54.235436,
	"t": 324
}
print('Raw data:', data)
print('Encoded data:', binascii.hexlify(e.pack(data)))
print('Decoded data:', e.unpack(e.pack(data)))