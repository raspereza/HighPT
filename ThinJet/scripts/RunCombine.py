#! /usr/bin/env python
# Author: Alexei Raspereza (December 2023)
# thin-jet ID SF measurements 
# Running fit with combine utility

import argparse
import os 


############
### MAIN ###
############
if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='UL2017', help="""Era : UL2016_preVFP, UL2016_postVFP, UL2017, UL2018""")
    parser.add_argument('-wp','--WP', dest='wp', default='VVLoose', help=""" tau ID WP : VVLoose, VLoose, Loose""")
    parser.add_argument('-prong','--prong', dest='dm', default='1prong', help=""" Decay mode : 1prong, 2prong, 3prong """)

    args = parser.parse_args()

    Prongs = ['1prong', '2prong', '3prong']
    WorkingPoints = ['VVLoose','VLoose','Loose']

    if args.wp not in WorkingPoints:
        print('unspecified WP',args.wp)
        print('available options',WorkingPoints)
        exit(1)

    if args.era not in ['UL2016_preVFP','UL2016_postVFP','UL2016','UL2017','UL2018']:
        print('unspecified era',args.era)
        print('available options',Eras)
        exit(1)

    if args.dm not in Prongs:
        print('unspecified prong',args.dm)
        print('available options',Prongs)
        exit(1)

    commandline = '$CMSSW_BASE/src/HighPT/ThinJet/scripts/RunCombineThinJet.bash %s %s %s '%(args.era,args.wp,args.dm)

    os.system(commandline)
