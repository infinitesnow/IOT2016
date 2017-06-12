#!/usr/bin/env python3

import csv
import sys

with open(sys.argv[1],'r') as input:
    acq=list(csv.reader(input))

acq=[ [abs(int(row[0])),abs(float(row[1])),abs(float(row[2]))] for row in acq if (float(row[0])<50000 and float(row[1])<40 and float(row[2])<70 and float(row[2])>5) ] 

timeaxis=[x[0] for x in acq]
temp=[x[1] for x in acq]
humid=[x[2] for x in acq]

import matplotlib.pyplot as p

p.plot(timeaxis, temp, 'r', timeaxis, humid, 'b')
p.savefig(sys.argv[1]+".png")

