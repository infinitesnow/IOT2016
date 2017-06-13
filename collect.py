#!/usr/bin/env python3
import sys
import serial
import struct
import math
import time

c1= -2.0468
c2=0.0367
c3= -1.5955*pow(10,-6)
d1= -40
d2=0.01

ser=serial.Serial('/dev/ttyUSB0', 115200, timeout=2.5)

starttime=time.time()
def flush():
	print("Flushing...",file=sys.stderr)
	while(time.time()-starttime<2):
		ser.read(19)

data={}
flush()

while(True):
	data_raw = ser.read(19)
	print("Raw data: "+str(data_raw),file=sys.stderr)

	if len(data_raw)<19: 
		print("Package too small, continuing...", file=sys.stderr)
		continue
	try:
		data_array=struct.unpack_from('>BBBHHBBBHHHHB',data_raw)
		if data_array[0]!=0x7e or data_array[12]!=0x7e:
			print("Package invalid, flushing...", file=sys.stderr)
			flush()
			continue
	except:
		print("Failed to parse, continuing...", file=sys.stderr)
		continue
	
	data["temperature"] = d1 + d2*data_array[8]
	data["humidity"] = c1 + c2*data_array[9] + c3*pow(data_array[9],2)
	
	# Compute the raw voltage on the photodiode
	luxv=float(data_array[10])
	luxvsensor = (luxv/4096)*1.5
	# Compute the current through 100kOhm resistor
	luxi = luxvsensor/100000
	data["light"] = 0.625*pow(10,6) * luxi * 1000
	
	print('{{ "temperature": {}, "humidity": {}, "light": {} }}'
		.format(round(data["temperature"],2),round(data["humidity"],2),round(data["light"],2)))

	# Print a copy to log
	print('{{ "temperature": {}, "humidity": {}, "light": {} }}'
		.format(round(data["temperature"],2),round(data["humidity"],2),round(data["light"],2)),
		file=sys.stderr)
