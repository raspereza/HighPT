#! /usr/bin/env python3

import HighPT.Tau.utilsHighPT as utils
import os
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-e','--era', dest='era', default='2023',choices=['2022','2023'])

if not os.path.isdir(utils.baseFolder):
    print('folder %s does not exist, create it first'%(utils.baseFolder))
    exit()

baseFolderEra = utils.baseFolder + '/' + args.era
if not os.path.isdir(baseFolderEra):
    print('creating folder %s'%(baseFolderEra))

folders = ['figures','datacards','FF']

subdolders = ['WMuNu','WTauNu','Sys','FF','MetTrigger']

'%s/figures'%(baseFolderEra)
command = 'mkdir %s'%(folder)

#os.system(command)
#command = ''
