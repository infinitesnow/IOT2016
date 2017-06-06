#!/usr/bin/env python3
import sys
import serial
import struct
import math
import time

c1= -2.0468
c2=  0.0367
c3= -1.5955*pow(10,-6)
d1= -40
d2=  0.01

ser=serial.Serial('/dev/ttyUSB0', 115200, timeout=5)
ser.flushInput()
time.sleep(0.1)
starttime=time.time()
while(time.time()-starttime<1):
	ser.readline()

data={}
while(True):
	data_raw = ser.readline()
	if data_raw==b'': continue
	try:
		data_array=struct.unpack_from('>IIIHH',data_raw,2)
	except:
		print("Failed to parse, continuing...", file=sys.stderr)
		continue
	data["counter"] = data_array[2]
	data["temperature"] = d1 + d2*data_array[3]
	data["humidity"] = c1 + c2*data_array[4] + c3*pow(data_array[4],2)
	print('{{ "id": {}, "temperature": {}, "humidity": {} }}'
		.format(data["counter"],round(data["temperature"],2),round(data["humidity"],2)))
