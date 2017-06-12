#!/usr/bin/env python3

import csv
import sys

with open(sys.argv[1],'r') as input:
    acq=list(csv.reader(input))

acq=[ [int(row[0]),float(row[1]),float(row[2])] for row in acq] 

timeaxis=[x[0] for x in acq]
temp=[x[1] for x in acq]
humid=[x[2] for x in acq]

import matplotlib.pyplot as p

p.plot(timeaxis, temp, 'r', timeaxis, humid, 'b')
p.savefig(sys.argv[1]+".png")
