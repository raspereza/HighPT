#! /usr/bin/env python3
# Author: Alexei Raspereza (December 2022)
# High pT tau ID SF measurements 
# Datacards producer for the signal region (W*->tau+v) 
import ROOT
import os
from array import array
import math

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-eraD','--eraD',dest='eraD',action='store_true')
args = parser.parse_args()

name = 'Summer23Prompt23_RunC_v1.root'
if args.eraD: name = 'Summer23BPixPrompt23_RunD_v1.root'

print('')
print('filename : %s'%(name))
print('')

rootFile = ROOT.TFile(name)
hist = rootFile.Get('jetvetomap')
nbinsX = hist.GetNbinsX()
nbinsY = hist.GetNbinsY()
xmin = hist.GetXaxis().GetBinLowEdge(1)
xmax = hist.GetXaxis().GetBinLowEdge(nbinsX+1)
ymin = hist.GetYaxis().GetBinLowEdge(1)
ymax = hist.GetYaxis().GetBinLowEdge(nbinsY+1)

print('')
print('X : [%5.2f,%4.2f]  nbinsX=%2i'%(xmin,xmax,nbinsX))
print('Y : [%5.2f,%4.2f]  nbinsY=%2i'%(ymin,ymax,nbinsY))
print('')

for xb in range(1,nbinsX+1):
    for yb in range (1,nbinsY+1):
        x = hist.GetBinContent(xb,yb)
        if x>0:
            x1 = hist.GetXaxis().GetBinLowEdge(xb)
            x2 = hist.GetXaxis().GetBinLowEdge(xb+1)
            y1 = hist.GetYaxis().GetBinLowEdge(yb)
            y2 = hist.GetYaxis().GetBinLowEdge(yb+1)
            print('[%2i,%2i]  -> [%5.2f:%5.2f,%5.2f:%5.2f]'%(xb,yb,x1,x2,y1,y2))



