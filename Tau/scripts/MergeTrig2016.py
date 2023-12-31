#! /usr/bin/env python
# Author: Alexei Raspereza (March 2023)
# Description: merges datacards of UL2016_preVFP and UL2016_postVFP 
#              datasets

from ROOT import TFile, TH1, TH1D, TCanvas, TLegend, TH2, gROOT, TF1, TVirtualFitter, kCyan, gStyle, TString, TColor, TPad, TLegend, TLine
import TauFW.Plotter.HighPT.utilsHighPT as utils
from array import array
import TauFW.Plotter.HighPT.stylesHighPT as styles
import os

##########################
# Plotting distributions #
##########################
def PlotWToTauNu(h_data_input,h_fake_input,h_tau_input,h_bkg_input,h_sig_input,
                 wp,era,var,wpVsMu,wpVsE,trigger):
    
    # protection from zero entries
    xb1 = max(h_bkg_input.GetBinContent(1),0.1)
    h_bkg_input.SetBinContent(1,xb1)

    h_data = h_data_input.Clone("data_plot")
    h_fake = h_fake_input.Clone("fake_plot")
    h_bkg = h_bkg_input.Clone("bkg_plot")
    h_tau = h_tau_input.Clone("tau_plot")
    h_sig = h_sig_input.Clone("sig_plot")

    styles.InitData(h_data)
    styles.InitHist(h_bkg,"","",TColor.GetColor("#6F2D35"),1001)
    styles.InitHist(h_sig,"","",TColor.GetColor("#FFCC66"),1001)
    styles.InitHist(h_fake,"","",TColor.GetColor("#FFCCFF"),1001)
    styles.InitHist(h_tau,"","",TColor.GetColor("#c6f74a"),1001)

    h_tau.Add(h_tau,h_bkg,1.,1.)
    h_fake.Add(h_fake,h_tau,1.,1.)
    h_sig.Add(h_sig,h_fake,1.,1.)
    h_tot = h_sig.Clone("total")
    styles.InitTotalHist(h_tot)

    h_ratio = utils.histoRatio(h_data,h_tot,'ratio')
    h_tot_ratio = utils.createUnitHisto(h_tot,'tot_ratio')

    styles.InitRatioHist(h_ratio)

    h_ratio.GetYaxis().SetRangeUser(0.001,1.999)
    
    nbins = h_ratio.GetNbinsX()

    utils.zeroBinErrors(h_sig)
    utils.zeroBinErrors(h_bkg)
    utils.zeroBinErrors(h_fake)
    utils.zeroBinErrors(h_tau)

    ymax = h_data.GetMaximum()
    if h_tot.GetMaximum()>ymax: ymax = h_tot.GetMaximum()
    h_data.GetYaxis().SetRangeUser(1.,100*ymax)
    h_data.GetXaxis().SetLabelSize(0)
    h_data.GetYaxis().SetTitle("events / bin")
    h_ratio.GetYaxis().SetTitle("obs/exp")
    h_ratio.GetXaxis().SetTitle(utils.XTitle[var])
    
    # canvas 
    canvas = styles.MakeCanvas("canv","",600,700)

    # upper pad
    upper = TPad("upper", "pad",0,0.31,1,1)
    upper.Draw()
    upper.cd()
    styles.InitUpperPad(upper)    
    
    h_data.Draw('e1')
    h_sig.Draw('hsame')
    h_fake.Draw('hsame')
    h_tau.Draw('hsame')
    h_bkg.Draw('hsame')
    h_data.Draw('e1same')
    h_tot.Draw('e2same')

    leg = TLegend(0.65,0.4,0.90,0.75)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.047)
    if trigger=='_trig':
        leg.SetHeader(wp+" (passed)")
    else:
        leg.SetHeader(wp+" (failed)")
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_sig,'W#rightarrow #tau#nu','f')
    leg.AddEntry(h_fake,'j#rightarrow#tau misId','f')
    leg.AddEntry(h_tau,'true #tau','f')
    leg.AddEntry(h_bkg,'e/#mu#rightarrow#tau misId','f')
    leg.Draw()

    styles.CMS_label(upper,era=era)

    upper.Draw("SAME")
    upper.RedrawAxis()
    upper.Modified()
    upper.Update()
    upper.SetLogx(True)
    upper.SetLogy(True)
    canvas.cd()

    # lower pad
    lower = TPad("lower", "pad",0,0,1,0.30)
    lower.Draw()
    lower.cd()
    styles.InitLowerPad(lower)

    h_ratio.Draw('e1')
    h_tot_ratio.Draw('e2same')
    h_ratio.Draw('e1same')

    nbins = h_ratio.GetNbinsX()
    xmin = h_ratio.GetXaxis().GetBinLowEdge(1)    
    xmax = h_ratio.GetXaxis().GetBinLowEdge(nbins+1)
    line = TLine(xmin,1.,xmax,1.)
    line.SetLineStyle(1)
    line.SetLineWidth(2)
    line.SetLineColor(4)
    line.Draw()

    lower.Modified()
    lower.RedrawAxis()
    lower.SetLogx(True)

    # update canvas 
    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    print
    print('Creating control plot')
    canvas.Print(utils.figuresFolderWTauNu+"/"+wpVsMu+"VsMu_"+wpVsE+"VsE/wtaunu_"+wp+trigger+"_"+era+".png")

def CreateCardsWToMuNu(fileName,h_data,h_bkg,h_sig,uncs,era):

    x_data = h_data.GetSumOfWeights()
    x_bkg  = h_bkg.GetSumOfWeights()
    x_sig  = h_sig.GetSumOfWeights() 

    cardsFileName = fileName + ".txt"
    rootFileName = fileName + ".root"
    f = open(cardsFileName,"w")
    f.write("imax 1    number of channels\n")
    f.write("jmax *    number of backgrounds\n")
    f.write("kmax *    number of nuisance parameters\n")
    f.write("---------------------------\n")
    f.write("observation   %3.1f\n"%(x_data))
    f.write("---------------------------\n")
    f.write("shapes * *  "+rootFileName+"  munu/$PROCESS munu/$PROCESS_$SYSTEMATIC \n")
    f.write("---------------------------\n")
    f.write("bin                 WtoMuNu     WtoMuNu\n")
    f.write("process             wmunu       bkg_munu\n")
    f.write("process             1           2\n")
    f.write("rate                %4.3f   %4.3f\n"%(x_sig,x_bkg))
    f.write("---------------------------\n")
    f.write("muEff         lnN   1.02        -\n")
    f.write("bkgNorm_munu  lnN   -           1.2\n")
    for unc in uncs:
        f.write(unc+"    shape  1.0          -\n")
    f.write("normW  rateParam  WtoMuNu wmunu  1.0  [0.5,1.5]\n")
    f.write("* autoMCStats 0\n")
    groups = "sysUnc group = normW muEff bkgNorm_munu"
    for unc in uncs:
        groups = groups + " " + unc
    f.write(groups+"\n")

    f.close()


def CreateCardsWToTauNu(fileName,h_data,h_fake,h_tau,h_bkg,h_sig,uncs_fake,uncs_sig,trigger):

    x_data = h_data.GetSumOfWeights()
    x_fake = h_fake.GetSumOfWeights()
    x_tau  = h_tau.GetSumOfWeights()
    x_bkg  = h_bkg.GetSumOfWeights()    
    x_sig  = h_sig.GetSumOfWeights() 

    cardsFileName = fileName + ".txt"
    rootFileName = fileName + ".root"
    f = open(cardsFileName,"w")
    f.write("imax 1    number of channels\n")
    f.write("jmax *    number of backgrounds\n")
    f.write("kmax *    number of nuisance parameters\n")
    f.write("---------------------------\n")
    f.write("observation   %3.1f\n"%(x_data))
    f.write("---------------------------\n")
    f.write("shapes * *  "+rootFileName+"  taunu"+trigger+"/$PROCESS taunu"+trigger+"/$PROCESS_$SYSTEMATIC \n")
    f.write("---------------------------\n")
    f.write("bin                  W"+trigger+"      W"+trigger+"      W"+trigger+"      W"+trigger+"\n")
    f.write("process              tau           wtaunu        fake          lfakes\n")
    f.write("process              -1            0             1             2\n")
    f.write("rate                 %4.3f         %4.3f      %4.3f      %4.3f\n"%(x_tau,x_sig,x_fake,x_bkg))
    f.write("---------------------------\n")
    f.write("extrapW        lnN   -             1.04          -             -\n")
    f.write("bkgNorm_taunu  lnN   1.2           -             -             -\n")
    f.write("lep_fakes      lnN   -             -             -           1.5\n")
    f.write("fake_closure"+trigger+"   lnN   -             -             1.15          -\n")
    for unc in uncs_sig:
        f.write(unc+"     shape   -             1.0           -             -\n")
    for unc in uncs_fake:
        f.write(unc+trigger+"     shape   -             -             1.0           -\n")
    f.write("normW  rateParam  W"+trigger+" wtaunu  1.0  [0.5,1.5]\n")
    f.write("* autoMCStats 0\n")
    groups = "sysUnc group = normW extrapW bkgNorm_taunu lep_fakes"
    for unc in uncs_sig:
        groups =  groups + " " + unc
    f.write(groups+"\n")
    f.close()


if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-wp','--WP', dest='wp', default='Medium', help=""" tau ID WP : Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight', help=""" WP vs. mu : VLoose, Loose, Medium, Tight""")
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VLoose', help=""" WP vs. e : VLoose, Loose, Medium, Tight, VTight, VVTight""")

    args = parser.parse_args()
    era = 'UL2016'
    var = 'pt_1'
    folder = utils.datacardsFolder + '/' + args.wpVsMu + 'VsMu_' + args.wpVsE + 'VsE'  

    uncert_names = ["JES","Unclustered","taues_1pr","taues_1pr1pi0","taues_3pr","taues_3pr1pi0"]

    for trigLabel in utils.trigLabels:
        fileName = folder + '/taunu_'+args.wp+trigLabel+'_UL2016'
        inputFile = TFile(fileName+'.root')
        directory = 'taunu'+trigLabel
        h_data = inputFile.Get(directory+'/data_obs')
        h_sig  = inputFile.Get(directory+'/wtaunu')
        h_fake = inputFile.Get(directory+'/fake')
        h_bkg_tau = inputFile.Get(directory+'/tau')
        h_bkg_lfakes = inputFile.Get(directory+'/lfakes')
        PlotWToTauNu(h_data,h_fake,h_bkg_tau,h_bkg_lfakes,h_sig,
                     args.wp,era,var,args.wpVsMu,args.wpVsE,trigLabel)

        uncs_fake = []
        for sampleLabel in ["ewk","qcd"]:
            for ptratioLabel in ["_ptratioLow","_ptratioHigh"]:
                for statUnc in ["_unc1","_unc2"]:
                    unc = sampleLabel+ptratioLabel+statUnc
                    uncs_fake.append(unc)

                    CreateCardsWToTauNu(fileName,
                            h_data,
                            h_fake,
                            h_bkg_tau,
                            h_bkg_lfakes,
                            h_sig,
                            uncs_fake,uncert_names,trigLabel)
        
        fileName = utils.datacardsFolder + '/munu_trig_UL2016'
        wmunuFile = TFile(fileName+'.root')
        h_data = wmunuFile.Get('munu/data_obs')
        h_bkg  = wmunuFile.Get('munu/bkg_munu')
        h_sig  = wmunuFile.Get('munu/wmunu')
        uncs = ['Unclustered','JES']
        CreateCardsWToMuNu(fileName,h_data,h_bkg,h_sig,uncs,era)
