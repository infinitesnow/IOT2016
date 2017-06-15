#!/usr/bin/env python3

import csv
import sys

if len(sys.argv)<2: 
    print("Usage: singleplot.py (datasource) (ymax)")
    exit(1)

with open(sys.argv[1],'r') as input:
    acq=list(csv.reader(input))

acq=[ [float(row[0]),float(row[1]),float(row[2])] for row in acq] 

switch={"temperature": 0, "humidity":1, "light":2 }
data=[ x[switch[sys.argv[2]]] for x in acq]


import matplotlib.pyplot as p

p.plot(data)
if len(sys.argv)==4: 
    ymax=int(sys.argv[3])
    p.gca().set_ylim([0,ymax])

filename=sys.argv[1].replace(".csv","")
p.savefig("../latex/images/"+filename+"-"+sys.argv[2]+".png")
