#! /usr/bin/env python

from ROOT import TMath

x_array = [1,2,3,4,5,6,7,8,9,10]
for i in range(0,len(x_array)):
    print(i,x_array[i])

s = TMath.Cos(2)
print('cos(2)=',s)
