#!/usr/bin/env python3

import csv
import sys

with open(sys.argv[1],'r') as input:
    acq=list(csv.reader(input))

acq=[ [float(row[0]),float(row[1]),float(row[2])] for row in acq] 

timeaxis=range(len(acq))
temp=[x[0] for x in acq]
humid=[x[1] for x in acq]
light=[x[2] for x in acq]

import matplotlib.pyplot as p

_,axis=p.subplots(3, sharex=True)
axis[0].plot(timeaxis, temp, 'r')
axis[0].set_title("Temperature")
p.tight_layout()
axis[1].plot(timeaxis, humid, 'b')
axis[1].set_title("Humidity")
axis[2].plot(timeaxis, light, 'g')
axis[2].set_title("Light")
filename=sys.argv[1].replace(".csv","")
p.savefig("../latex/images/"+filename+".png")
