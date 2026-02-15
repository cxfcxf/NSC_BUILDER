from enum import IntEnum

class _CompatIntEnum(IntEnum):
	def __str__(self):
		return f'{self.__class__.__name__}.{self.name}'

class Content(_CompatIntEnum):
	PROGRAM = 0x0
	META = 0x1
	CONTROL = 0x2
	MANUAL = 0x3
	DATA = 0x4
	PUBLIC_DATA = 0x5

class Fs(_CompatIntEnum):
	NONE = 0x0
	PFS0 = 0x2
	ROMFS = 0x3

class Crypto(_CompatIntEnum):
	ERR = 0
	NONE = 1
	XTS = 2
	CTR = 3
	BKTR = 4
	NCA0 = 0x3041434E

class TicketSignature(IntEnum):
	RSA_4096_SHA1 = 0x010000
	RSA_2048_SHA1 = 0x010001
	ECDSA_SHA1 = 0x010002
	RSA_4096_SHA256 = 0x010003
	RSA_2048_SHA256 = 0x010004
	ECDSA_SHA256 = 0x010005