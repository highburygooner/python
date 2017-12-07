import redis
import time

def trans():
	pipeline=conn.pipeline()
	pipeline.incr('trans:')
	time.sleep(.1)
	pipeline.incr('trans:',-1)
	print pipeline.exec()[0]

	
if 1:
	for i in xrange(3):
		threading.Thread(target=trans).start()
	time.sleep(.5)
