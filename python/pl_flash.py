

def write(dev, data):
	dev.write_raw('PL:FLASH:WR' + data)
	r = dev.read_raw()
	if len(r) > 0:
		raise RuntimeError('unexpected PL:FLASH:WR response')

def read(dev, data, sz):
	dev.write_raw('PL:FLASH:RD #H%X#' % sz + data)
	r = dev.read_raw()
	if len(r) != len(data) + sz:
		raise RuntimeError('unexpected PL:FLASH:RD response')
	return r[len(data):]

def read_id(dev):
	r = read(dev, '\x9f', 3)
	return ord(r[0]), ord(r[1]), ord(r[2])

def read_status(dev, i = 1):
	assert i == 1 or i == 2
	r = read(dev, '\x05' if i == 1 else '\x35', 1)
	return ord(r[0])

def write_en(dev, en):
	write(dev, '\x06' if en else '\x04')

def erase_all(dev):
	write(dev, '\xC7')

def wait_busy(dev, tout_ms):
	tout = dev.timeout
	dev.timeout = tout_ms + 1000
	dev.write_raw('PL:FLASH:WAit #%u' % tout_ms)
	r = dev.read_raw()
	dev.timeout = tout
	if len(r) != 1:
		raise RuntimeError('unexpected PL:FLASH:WAit response')
	return (ord(r[0]) & 1) == 0

if __name__ == '__main__':
	import pyvisa as pv
	import sys

	def open(res = None):
		rm = pv.ResourceManager()
		if not res:
			res = rm.list_resources()[0]		
		return rm.open_resource(res)

	dev = open()
	if '--erase' in sys.argv:
		write_en(dev, True)
		erase_all(dev)
		assert wait_busy(dev, 4000)
		print 'chip erased'
	else:
		print 'ID =', read_id(dev)

	print 'Status-1 = %#x' % read_status(dev, 1)
	print 'Status-2 = %#x' % read_status(dev, 2)

