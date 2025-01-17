#! /usr/bin/env python3
# Author: Alexei Raspereza (August 2024)
# High pT tau ID SF as a function of pT(tau)
import ROOT
import HighPT.Tau.utilsHighPT as utils
from array import array
import math
import HighPT.Tau.stylesHighPT as styles
import os

# WPvsJet_WPvsMu_WPvsE : {{lowpt,highpt}: {central value, stat., sys. }}
tauIDs_2016preVFP = {
    'Loose_Tight_VVLoose': {'lowpt': [0.889,0.054,0.101], 'highpt': [0.890,0.126,0.078]},
    'Loose_Tight_Tight':   {'lowpt': [0.863,0.043,0.091], 'highpt': [0.828,0.107,0.069]},
    'Medium_Tight_VVLoose': {'lowpt': [0.889,0.054,0.101], 'highpt': [0.890,0.126,0.078]},
    'Medium_Tight_Tight':   {'lowpt': [0.863,0.043,0.091], 'highpt': [0.828,0.107,0.069]},
    'Tight_Tight_VVLoose': {'lowpt': [0.889,0.054,0.101], 'highpt': [0.890,0.126,0.078]},
    'Tight_Tight_Tight':   {'lowpt': [0.863,0.043,0.091], 'highpt': [0.828,0.107,0.069]},
    'VTight_Tight_VVLoose': {'lowpt': [0.889,0.054,0.101], 'highpt': [0.890,0.126,0.078]},
    'VTight_Tight_Tight':   {'lowpt': [0.863,0.043,0.091], 'highpt': [0.828,0.107,0.069]}
}

tauIDs_2016postVFP = {
    'Loose_Tight_VVLoose': {'lowpt': [0.968,0.049,0.080], 'highpt': [0.889,0.103,0.069]},
    'Loose_Tight_Tight':   {'lowpt': [0.909,0.046,0.074], 'highpt': [0.856,0.098,0.061]},
    'Medium_Tight_VVLoose': {'lowpt': [0.968,0.049,0.080], 'highpt': [0.889,0.103,0.069]},
    'Medium_Tight_Tight':   {'lowpt': [0.909,0.046,0.074], 'highpt': [0.856,0.098,0.061]},
    'Tight_Tight_VVLoose': {'lowpt': [0.968,0.049,0.080], 'highpt': [0.889,0.103,0.069]},
    'Tight_Tight_Tight':   {'lowpt': [0.909,0.046,0.074], 'highpt': [0.856,0.098,0.061]},
    'VTight_Tight_VVLoose': {'lowpt': [0.968,0.049,0.080], 'highpt': [0.889,0.103,0.069]},
    'VTight_Tight_Tight':   {'lowpt': [0.909,0.046,0.074], 'highpt': [0.856,0.098,0.061]}
}

tauIDs_2017 = {
    'Loose_Tight_VVLoose': {'lowpt': [1.092,0.040,0.086], 'highpt': [1.014,0.077,0.073]},
    'Loose_Tight_Tight':   {'lowpt': [1.049,0.036,0.078], 'highpt': [0.881,0.073,0.064]},
    'Medium_Tight_VVLoose': {'lowpt': [1.092,0.040,0.086], 'highpt': [1.014,0.077,0.073]},
    'Medium_Tight_Tight':   {'lowpt': [1.049,0.036,0.078], 'highpt': [0.881,0.073,0.064]},
    'Tight_Tight_VVLoose': {'lowpt': [1.092,0.040,0.086], 'highpt': [1.014,0.077,0.073]},
    'Tight_Tight_Tight':   {'lowpt': [1.049,0.036,0.078], 'highpt': [0.881,0.073,0.064]},
    'VTight_Tight_VVLoose': {'lowpt': [1.092,0.040,0.086], 'highpt': [1.014,0.077,0.073]},
    'VTight_Tight_Tight':   {'lowpt': [1.049,0.036,0.078], 'highpt': [0.881,0.073,0.064]}
}

tauIDs_2018 = {
    'Loose_Tight_VVLoose': {'lowpt': [0.906,0.048,0.099], 'highpt': [1.094,0.060,0.084]},
    'Loose_Tight_Tight':   {'lowpt': [0.971,0.033,0.078], 'highpt': [0.982,0.059,0.065]},
    'Medium_Tight_VVLoose': {'lowpt': [0.906,0.048,0.099], 'highpt': [1.094,0.060,0.084]},
    'Medium_Tight_Tight':   {'lowpt': [0.971,0.033,0.078], 'highpt': [0.982,0.059,0.065]},
    'Tight_Tight_VVLoose': {'lowpt': [0.906,0.048,0.099], 'highpt': [1.094,0.060,0.084]},
    'Tight_Tight_Tight':   {'lowpt': [0.971,0.033,0.078], 'highpt': [0.982,0.059,0.065]},
    'VTight_Tight_VVLoose': {'lowpt': [0.906,0.048,0.099], 'highpt': [1.094,0.060,0.084]},
    'VTight_Tight_Tight':   {'lowpt': [0.971,0.033,0.078], 'highpt': [0.982,0.059,0.065]}
}

tauIDs_2022 = {
    'Loose_Tight_VVLoose':  {'lowpt': [1.04,0.05,0.06], 'highpt': [0.91,0.14,0.10]},
    'Loose_Tight_Tight':    {'lowpt': [0.99,0.06,0.05], 'highpt': [0.99,0.10,0.07]},
    'Medium_Tight_VVLoose': {'lowpt': [1.04,0.05,0.05], 'highpt': [0.98,0.10,0.08]},
    'Medium_Tight_Tight':   {'lowpt': [1.00,0.06,0.05], 'highpt': [0.96,0.09,0.07]},
    'Tight_Tight_VVLoose':  {'lowpt': [1.04,0.05,0.05], 'highpt': [1.12,0.12,0.09]},
    'Tight_Tight_Tight':    {'lowpt': [0.98,0.06,0.05], 'highpt': [1.01,0.09,0.07]},
    'VTight_Tight_VVLoose': {'lowpt': [1.05,0.05,0.05], 'highpt': [1.13,0.11,0.09]},
    'VTight_Tight_Tight':   {'lowpt': [0.98,0.06,0.05], 'highpt': [0.99,0.09,0.07]}
}

tauIDs = {
    'UL2016_preVFP': tauIDs_2016preVFP,
    'UL2016_postVFP': tauIDs_2016postVFP,
    'UL2017': tauIDs_2017,
    'UL2018': tauIDs_2018,
    '2022': tauIDs_2022
}

def PlotSF(sf_lowpt,sf_highpt,**kwargs):

    era = kwargs.get('era','2018')
    WPvsJet = kwargs.get('WPvsJet','Medium')
    WPvsMu = kwargs.get('WPvsMu','Tight')
    WPvsE = kwargs.get('WPvsE','VVLoose')
    ymin = kwargs.get('ymin',0.58)
    ymax = kwargs.get('ymax',1.3)
    
    frame = ROOT.TH2D('frame','',2,99.9,1000.01,2,ymin,ymax)    
    frame.GetYaxis().SetTitle('tau ID SF')
    frame.GetXaxis().SetTitle('p_{T}^{#tau} (GeV)')
    frame.GetXaxis().SetNdivisions(505)
    frame.GetXaxis().SetMoreLogLabels()
    frame.GetXaxis().SetNoExponent()  
    
    x = [145,250]
    ex_low = [45,50]
    ex_high = [55,750]

    y = []
    ey_stat = []
    ey_tot = []

    y.append(sf_lowpt[0])
    y.append(sf_highpt[0])

    ey_stat.append(sf_lowpt[1])
    ey_stat.append(sf_highpt[1])

    error_low_pt = math.sqrt(sf_lowpt[1]*sf_lowpt[1]+sf_lowpt[2]*sf_lowpt[2])
    error_high_pt = math.sqrt(sf_highpt[1]*sf_highpt[1]+sf_highpt[2]*sf_highpt[2])

    ey_tot.append(error_low_pt)
    ey_tot.append(error_high_pt)
    
    nbins = 2 
    
    graph_stat = ROOT.TGraphAsymmErrors(nbins,
                                        array('d',list(x)),
                                        array('d',list(y)),
                                        array('d',list(ex_low)),
                                        array('d',list(ex_high)),
                                        array('d',list(ey_stat)),
                                        array('d',list(ey_stat)))

    graph_stat.SetMarkerStyle(20)
    graph_stat.SetMarkerColor(2)
    graph_stat.SetLineColor(2)
    graph_stat.SetLineWidth(3)
    graph_stat.SetMarkerSize(1.6)    
    
    graph_tot = ROOT.TGraphAsymmErrors(nbins,
                                       array('d',list(x)),
                                       array('d',list(y)),
                                       array('d',list(ex_low)),
                                       array('d',list(ex_high)),
                                       array('d',list(ey_tot)),
                                       array('d',list(ey_tot)))

    graph_tot.SetMarkerStyle(0)
    graph_tot.SetMarkerColor(2)
    graph_tot.SetLineColor(4)
    graph_tot.SetLineWidth(2)
    graph_tot.SetMarkerSize(0)    
    
    # canvas 
    canv = styles.MakeCanvas("canv","",600,600)

    frame.Draw()
    graph_tot.Draw('esame')
    graph_stat.Draw('pe1same')

    legend = '#it{D_{jet}} %s, #it{D_{#mu}} %s, #it{D_{e}} %s'%(WPvsJet,WPvsMu,WPvsE)
    leg = ROOT.TLegend(0.35,0.17,0.9,0.32)
    leg.SetFillColor(0);
    leg.SetTextSize(0.035);
    leg.SetBorderSize(1);
    leg.SetHeader(legend)
    leg.AddEntry(graph_stat,'stat. unc.','lpe')
    leg.AddEntry(graph_tot,'total unc.','le')
    leg.Draw()

#    leg_latex = ROOT.TLatex()
#    leg_latex.SetNDC()
#    leg_latex.SetTextAngle(0)
#    leg_latex.SetTextSize(0.035)
#    leg_latex.SetTextColor(ROOT.kBlack)
#    leg_latex.DrawLatex(0.2,0.85,legend)
    
    styles.CMS_label(canv,era=era)
    canv.SetLogx(True)
    canv.SetGridx(True)
    canv.SetGridy(True)
    canv.Modified()
    canv.Update()
    canv.Print('/afs/cern.ch/user/r/rasp/public/highPT_comp/DeepTau_'+era+'_'+WPvsJet+'vsJet_'+WPvsMu+'vsMu_'+WPvsE+'vsE.png')


############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-era','--era',dest='era',default='UL2018', choices=['UL2016_preVFP','UL2016_postVFP','UL2017','UL2018','2022'],)
    parser.add_argument('-wpVsJet','--WPvsJet', dest='wpVsJet', default='Medium',choices=['Loose','Medium','Tight','VTight'])
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight',choices=['Tight'])
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VVLoose',choices=['VVLoose','Tight'])
    parser.add_argument('-ymin','--ymin',dest='ymin',type=float,default=0.48)
    parser.add_argument('-ymax','--ymax',dest='ymax',type=float,default=1.28)
    
    args = parser.parse_args() 

    WP = '%s_%s_%s'%(args.wpVsJet,args.wpVsMu,args.wpVsE)
    
    sf_lowpt = tauIDs[args.era][WP]['lowpt']
    sf_highpt = tauIDs[args.era][WP]['highpt']
    
    PlotSF(sf_lowpt,
           sf_highpt,
           era=args.era,
           WPvsJet=args.wpVsJet,
           WPvsMu=args.wpVsMu,
           WPvsE=args.wpVsE,
           ymin=args.ymin,
           ymax=args.ymax)
