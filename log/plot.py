#!/usr/bin/env python3

import csv
import sys

with open(sys.argv[1],'r') as input:
    acq=list(csv.reader(input))

acq=[ [float(row[0]),float(row[1])] for row in acq] 

timeaxis=range(len(acq))
temp=[x[0] for x in acq]
humid=[x[1] for x in acq]

import matplotlib.pyplot as p

_,axis=p.subplots(2, sharex=True)
axis[0].plot(timeaxis, temp, 'r')
axis[1].plot(timeaxis, humid, 'b')
filename=sys.argv[1].replace(".csv","")
p.savefig("../latex/images/"+filename+".png")
