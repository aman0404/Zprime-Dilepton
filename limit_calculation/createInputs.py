import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
from array import array
import importlib
sys.path.append('cfgs/')
sys.path.append('input/')
from ctypes import c_double

import numpy as np

def getBinning(mass):


    if mass < 700:
        return [1,1000000]
    if mass < 1000:
        return [1,1000000]
    elif mass < 2000:
        return [2,1000000]
    else:
        return [5,500000]





def getRebinnedHistogram(hist,binning,name):
    # print "type(hist):  {0}".format(type(hist))
    # print "hist:  {0}".format(hist)
    return hist.Rebin(len(binning) - 1, name, array('d', binning))



def getJetFakeHistogram(fhist, binning, name1):
    return fhist.Rebin(len(binning) - 1, name1, array('d', binning)) 


def getStatUncertHistogram(hist,name,up=False):
    uncertHist = hist.Clone(name)
    for i in range(0,hist.GetNbinsX()+1):
        if up:
            uncertHist.SetBinContent(i,hist.GetBinContent(i)+hist.GetBinError(i))	
        else:
            uncertHist.SetBinContent(i,max(0,hist.GetBinContent(i)-hist.GetBinError(i)))	
    return uncertHist

def getHEEPUncertHistogram(hist,name,heep,up=False):
    uncertHist = hist.Clone(name)
    for i in range(1,hist.GetNbinsX()+1):
        if up:
            uncertHist.SetBinContent(i,hist.GetBinContent(i)+hist.GetBinContent(i)*heep[i-1])
        else:
            uncertHist.SetBinContent(i,hist.GetBinContent(i)-hist.GetBinContent(i)*heep[i-1])
    return uncertHist

def getPDFUncertHistogram(hist,name,pdf,up=False):
    uncertHist = hist.Clone(name)
    #for i in range(1,hist.GetNbinsX()):
    for i in range(1,hist.GetNbinsX()+1):
        if up:
            uncertHist.SetBinContent(i,hist.GetBinContent(i)+hist.GetBinContent(i)*pdf[i-1])	
        else:
            uncertHist.SetBinContent(i,hist.GetBinContent(i)-hist.GetBinContent(i)*pdf[i-1])	
    print(" ----  ")
    return uncertHist

def getBtagUncertHistogram(hist,name,btag_unc,up=False):
    uncertHist = hist.Clone(name)
    #for i in range(1,hist.GetNbinsX()):
    for i in range(1,hist.GetNbinsX()+1):
        if up:
            uncertHist.SetBinContent(i,hist.GetBinContent(i)+hist.GetBinContent(i)*btag_unc[i-1])
        else:
            uncertHist.SetBinContent(i,hist.GetBinContent(i)-hist.GetBinContent(i)*btag_unc[i-1])
    return uncertHist



## 0b channel systematics
#original values
btag_bc_corr = [0.02, 0.02, 0.02, 0.02, 0.03, 0.03, 0.03, 0.03]
btag_bc_uncorr = [0.02, 0.02, 0.02, 0.02, 0.03, 0.03, 0.03, 0.03]

btag_light_uncorr = [0.018, 0.02, 0.022286, 0.0236325, 0.0259413, 0.0284652, 0.0356554, 0.0356554]

btag_light_corr = [0.0218337, 0.0244117, 0.0270792, 0.028948, 0.0324466, 0.0351817, 0.0363449, 0.0363449 ]

##for bin testing 
#btag_bc_corr = [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]
#btag_bc_uncorr = [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]
#
#btag_light_uncorr = [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03] 
# 
#btag_light_corr = [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03] 


## 2b channel systematics
#btag_bc_corr = [0.03801, 0.02015, 0.025, 0.01509, 0.06436, 0.02551, 0.079,  0.079]
#
#btag_bc_uncorr = [0.04845, 0.01361, 0.02, 0.02, 0.05407, 0.02432, 0.08022, 0.08022]
#
#btag_light_corr = [0.04, 0.04, 0.03, 0.04, 0.04, 0.04, 0.04, 0.04]
#
#btag_light_uncorr = [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.04, 0.04]





inputFiles = {
    # "dimuon_2018_BB_AllB": ["0b_bb_2018.root","1b_bb_2018.root","2b_bb_2018.root"]    
    "dimuon_2018_ZeroB": "0b_2018.root",
    "dimuon_2017_ZeroB": "0b_2017.root",
    "dimuon_2016_pre_ZeroB": "0b_2016pre.root",
    "dimuon_2016_post_ZeroB": "0b_2016post.root",

    "dimuon_2018_OneB": "1b_2018.root",
    "dimuon_2017_OneB": "1b_2017.root",
    "dimuon_2016_pre_OneB": "1b_2016pre.root",
    "dimuon_2016_post_OneB": "1b_2016post.root",

    "dimuon_2018_BB_ZeroB": "0b_bb_2018.root",
    "dimuon_2018_BB_OneB": "1b_bb_2018.root",
    "dimuon_2018_BB_TwoB": "2b_bb_2018.root",
    # "dimuon_2018_BE_AllB": ["0b_be_2018.root","1b_be_2018.root","2b_be_2018.root"]    
    "dimuon_2018_BE_ZeroB": "0b_be_2018.root",
    "dimuon_2018_BE_OneB": "1b_be_2018.root",
    "dimuon_2018_BE_TwoB": "2b_be_2018.root",
    # "dimuon_2017_BB_AllB": ["0b_bb_2017.root","1b_bb_2017.root","2b_bb_2017.root"]    
    "dimuon_2017_BB_ZeroB": "0b_bb_2017.root",
    "dimuon_2017_BB_OneB": "1b_bb_2017.root",
    "dimuon_2017_BB_TwoB": "2b_bb_2017.root",
    # "dimuon_2017_BE_AllB": ["0b_be_2017.root","1b_be_2017.root","2b_be_2017.root"]    
    "dimuon_2017_BE_ZeroB": "0b_be_2017.root",
    "dimuon_2017_BE_OneB": "1b_be_2017.root",
    "dimuon_2017_BE_TwoB": "2b_be_2017.root",
    # "dimuon_2016_post_BB_AllB": ["0b_bb_2016post.root","1b_bb_2016post.root","2b_bb_2016post.root"]    
    "dimuon_2016_post_BB_ZeroB": "0b_bb_2016post.root",
    "dimuon_2016_post_BB_OneB": "1b_bb_2016post.root",
    "dimuon_2016_post_BB_TwoB": "2b_bb_2016post.root",
    # "dimuon_2016_post_BE_AllB": ["0b_be_2016post.root","1b_be_2016post.root","2b_be_2016post.root"]    
    "dimuon_2016_post_BE_ZeroB": "0b_be_2016post.root",
    "dimuon_2016_post_BE_OneB": "1b_be_2016post.root",
    "dimuon_2016_post_BE_TwoB": "2b_be_2016post.root",
    # "dimuon_2016_pre_BB_AllB": ["0b_bb_2016pre.root","1b_bb_2016pre.root","2b_bb_2016pre.root"]    
    "dimuon_2016_pre_BB_ZeroB": "0b_bb_2016pre.root",
    "dimuon_2016_pre_BB_OneB": "1b_bb_2016pre.root",
    "dimuon_2016_pre_BB_TwoB": "2b_bb_2016pre.root",
    # "dimuon_2016_pre_BE_AllB": ["0b_be_2016pre.root","1b_be_2016pre.root","2b_be_2016pre.root"]    
    "dimuon_2016_pre_BE_ZeroB": "0b_be_2016pre.root",
    "dimuon_2016_pre_BE_OneB": "1b_be_2016pre.root",
    "dimuon_2016_pre_BE_TwoB": "2b_be_2016pre.root",

    "dielectron_2018_ZeroB": "0b_2018.root",
    "dielectron_2017_ZeroB": "0b_2017.root",
    "dielectron_2016_pre_ZeroB": "0b_2016pre.root",
    "dielectron_2016_post_ZeroB": "0b_2016post.root",

    "dielectron_2018_OneB": "1b_2018.root",
    "dielectron_2017_OneB": "1b_2017.root",
    "dielectron_2016_pre_OneB": "1b_2016pre.root",
    "dielectron_2016_post_OneB": "1b_2016post.root",

    # "dielectron_2018_BB_AllB": ["0b_bb_2018.root","1b_bb_2018.root","2b_bb_2018.root"]    
    "dielectron_2018_BB_ZeroB": "0b_bb_2018.root",
    "dielectron_2018_BB_OneB": "1b_bb_2018.root",
    "dielectron_2018_BB_TwoB": "2b_bb_2018.root",
    # "dielectron_2018_BE_AllB": ["0b_be_2018.root","1b_be_2018.root","2b_be_2018.root"]    
    "dielectron_2018_BE_ZeroB": "0b_be_2018.root",
    "dielectron_2018_BE_OneB": "1b_be_2018.root",
    "dielectron_2018_BE_TwoB": "2b_be_2018.root",
    # "dielectron_2017_BB_AllB": ["0b_bb_2017.root","1b_bb_2017.root","2b_bb_2017.root"]    
    "dielectron_2017_BB_ZeroB": "0b_bb_2017.root",
    "dielectron_2017_BB_OneB": "1b_bb_2017.root",
    "dielectron_2017_BB_TwoB": "2b_bb_2017.root",
    # "dielectron_2017_BE_AllB": ["0b_be_2017.root","1b_be_2017.root","2b_be_2017.root"]    
    "dielectron_2017_BE_ZeroB": "0b_be_2017.root",
    "dielectron_2017_BE_OneB": "1b_be_2017.root",
    "dielectron_2017_BE_TwoB": "2b_be_2017.root",

    "dielectron_2016_post_BB_ZeroB": "0b_bb_2016post.root",
    "dielectron_2016_post_BB_OneB": "1b_bb_2016post.root",
    "dielectron_2016_post_BB_TwoB": "2b_bb_2016post.root",
    "dielectron_2016_post_BE_ZeroB": "0b_be_2016post.root",
    "dielectron_2016_post_BE_OneB": "1b_be_2016post.root",
    "dielectron_2016_post_BE_TwoB": "2b_be_2016post.root",

    "dielectron_2016_pre_BB_ZeroB": "0b_bb_2016pre.root",
    "dielectron_2016_pre_BB_OneB": "1b_bb_2016pre.root",
    "dielectron_2016_pre_BB_TwoB": "2b_bb_2016pre.root",
    "dielectron_2016_pre_BE_ZeroB": "0b_be_2016pre.root",
    "dielectron_2016_pre_BE_OneB": "1b_be_2016pre.root",
    "dielectron_2016_pre_BE_TwoB": "2b_be_2016pre.root",
}



def createHistogramsCI(L,interference,name,channel,scanConfigName,bbll = True):
    ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

    scanConfigName ="scanConfiguration_%s"%scanConfigName # options: mumu, elel or elmu
    scanConfig =  __import__(scanConfigName)
    
    #binning = scanConfig.binning #Aman default
  
    if "TwoB" in channel:

        binning = scanConfig.binning_2b
    else:
        binning = scanConfig.binning_0_1b

    print(binning)

    from array import array
 
    # print("inputFiles[channel]: {0}".format(inputFiles[channel]))

    if "dielectron" in channel:
        #inputFile = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/ee/"+inputFiles[channel], "OPEN")
        #inputFile = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Jan2024/ee/"+inputFiles[channel], "OPEN")
        #inputFile = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/ee/"+inputFiles[channel], "OPEN")
        inputFile = ROOT.TFile("/depot/cms/private/users/kaur214/output/elec_channel_2018_newSep_jan2024_trig_eff/dnn/stage3_templates/dielectron_mass/"+inputFiles[channel], "OPEN")
        fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/ee/preapproval/fake_"+inputFiles[channel], "OPEN")


        #if "ZeroB" in channel:
        #    fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/mumu/fake_bkg_0b.root", "OPEN")
        #elif "OneB" in channel:
        #    fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/mumu/fake_bkg_1b.root", "OPEN")
        #else:
        #    fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/mumu/fake_bkg_2b.root", "OPEN")

    else: # dimuon
        #inputFile = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/mumu_uncert/"+inputFiles[channel], "OPEN")
        #inputFile = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/mumu/"+inputFiles[channel], "OPEN")
        
        #inputFile = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/mumu/comb/"+inputFiles[channel], "OPEN")
        #inputFile = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/mumu/"+inputFiles[channel], "OPEN")

        ##with final DNN
        inputFile = ROOT.TFile("/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage3_templates/dimuon_mass/"+inputFiles[channel], "OPEN")
        #inputFile = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/mumu/preapproval/"+inputFiles[channel], "OPEN")
        fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/mumu/preapproval/fake_"+inputFiles[channel], "OPEN")



#        if "ZeroB" in channel:
#            fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/mumu/fake_bkg_0b.root", "OPEN")
            #fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/mumu/fake_bkg_0b.root", "OPEN")
#        elif "OneB" in channel:
#            fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/mumu/fake_bkg_1b.root", "OPEN")
#        else:
#            fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForHyeon/template_files/Oct24_2023/mumu/fake_bkg_2b.root", "OPEN")



    histFile = ROOT.TFile("%s.root"%name, "RECREATE") # output file


    # pdfUncert = [0.01,0.0125,0.02,0.035,0.065,0.10]
    # pdfUncertDY = [0.0133126577202494, 0.0147788328624159, 0.01842209757115, 0.0243644300786998, 0.039572839847093, 0.1144248733154136]
    # pdfUncertOther = [0.0358232181870253, 0.088892531404347, 0.1254268509362337, 0.1736824180528946, 0.2024257617076786, 0.3369525304968204]
    #pdfUncert = [0.01, 0.01, 0.01,0.0125,0.02,0.035]

    if ("OneB" in channel) or ("TwoB" in channel):
        if "BB" in channel:
              ttbar_uncert = [0.56769, 0.20715, 0.13428, 0.769523, 0.334064, 0.206764, 0.206764]
        else:
              ttbar_uncert = [0.774004, 0.6071, 0.84628, 0.800171, 0.603037, 0.300831, 0.497486]


    ##PDF Uncertainty original
    if "TwoB" in channel:
        pdfUncert =   [0.00156249, 0.0029808, 0.00518313, 0.0123567]
        pdfUncertDY = [0.01414670344, 0.01927992999, 0.02804822616, 0.04746036643]
        pdfUncertTT = [0.01964566484, 0.02769629981, 0.05196009012, 0.2532719835]
        pdfUncertVV = [0.0132467234,  0.02366424237, 0.1324849835, 0.1361711683]

    else:
        pdfUncert =   [0.00134735, 0.00156249, 0.00215549, 0.0029808, 0.00383769, 0.00518313, 0.00711226]
        pdfUncertDY = [0.01414670344, 0.01659019081, 0.01927992999, 0.02354107301, 0.02804822616, 0.04746036643]
        pdfUncertTT = [0.01964566484, 0.02306892944, 0.02769629981, 0.04407183593, 0.05196009012, 0.2532719835]
        pdfUncertVV = [0.0132467234,  0.01373970154, 0.01722591218, 0.02366424237, 0.1324849835, 0.1361711683]
        
        
        
        #pdfUncert =   [0.00131305, 0.00134735, 0.00156249, 0.00215549, 0.0029808, 0.00383769, 0.00518313, 0.00711226, 0.0123567]
        #pdfUncertDY = [0.01112166172, 0.01414670344, 0.01659019081, 0.01927992999, 0.02354107301, 0.02804822616, 0.04746036643]
        #pdfUncertTT = [0.01676181036, 0.01964566484, 0.02306892944, 0.02769629981, 0.04407183593, 0.05196009012, 0.2532719835]
        #pdfUncertVV = [0.01301770353, 0.0132467234,  0.01373970154, 0.01722591218, 0.02366424237, 0.1324849835, 0.1361711683]

#######

    ##PDF Uncertainty binning testing
#    pdfUncert =   [0.00131305, 0.00131305, 0.00131305, 0.00131305, 0.00131305, 0.00131305, 0.00131305, 0.00131305]
#
#    pdfUncertDY = [0.01112166172, 0.01414670344, 0.01659019081, 0.01927992999, 0.02354107301, 0.02804822616, 0.04746036643]
#    pdfUncertTT = [0.01676181036, 0.01964566484, 0.02306892944, 0.02769629981, 0.04407183593, 0.05196009012, 0.2532719835]
#
#    pdfUncertVV = [0.01301770353, 0.0132467234,  0.01373970154, 0.01722591218, 0.02366424237, 0.1324849835, 0.1361711683]


    if "TwoB" in channel:
        heepUncert = [0.014, 0.018, 0.037, 0.037]
    else:
        heepUncert = [0.012, 0.014, 0.016, 0.018, 0.023, 0.037, 0.037, 0.037]

    if "dielectron" in channel:
       IDName = "ID"
       pdfName = "pdf_dielectron"
    else:
       IDName = "ID"
       pdfName = "pdf_dilepton"

    ttbarUncertName = "ttbarUncert"
    scaleName = "massScale"
    eScaleName = "energyScale"
    smearName = "res"
    #pdfName = "pdf_dilepton"
    #IDName = "ID"
    ISOName = "ISO"
    HLTName = "HLT"
    PUName = "PU"
    # btagName = "btag"
    prefiringName = "l1prefiring"
    btagName_bc = "btagSF_bc"
    btagName_light = "btagSF_light"
    btagName_bc_corr = "btagSF_bc_corr"
    btagName_light_corr = "btagSF_light_corr"
    recoName = "reco"
 
    print("------------------------------------------------")
    print("inputFile: {0}".format(inputFile.Get("DYJets")))

    # bkg DY
    bkgHistDY = getRebinnedHistogram(inputFile.Get("DYJets"),binning,"bkgHistDY_%s"%channel)

    # setup the name of btag to be consistent with our correlation nomenclature
    if "dielectron" in channel:
       year_corr = "dielectron"
       if "2018" in channel:
           channel_corr = "dielectron18"
       elif "2017" in channel:
           channel_corr = "dielectron17"
       elif "2016" in channel:
           if "post" in channel:
               channel_corr = "dielectron16_post"
           else:
               channel_corr = "dielectron16_pre"
       else:
           print("invalid channel configuration")
    else:
       year_corr = "dilepton"
       if "2018" in channel:
           channel_corr = "dilepton18"
       elif "2017" in channel:
           channel_corr = "dilepton17"
       elif "2016" in channel:
           if "post" in channel:
               channel_corr = "dilepton16_post"
           else:
               channel_corr = "dilepton16_pre"
       else:
           print("invalid channel configuration")
           raise ValueError

    if "BB" in channel:
        zero_corr = channel.replace('BB_',"")
        # print "zero_corr: {0}".format(zero_corr)
    else:
        zero_corr = channel.replace('BE_',"")
       
    if "dielectron" in channel:
            bkgHistDYIDDown = getHEEPUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sDown"%(IDName,channel_corr), heepUncert)
            bkgHistDYIDUp =   getHEEPUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
            bkgHistDYIDDown = getRebinnedHistogram(inputFile.Get("DYJets_muIDDown"), binning, "bkgHistDY_%s_%sDown"%(IDName,zero_corr))
            bkgHistDYIDUp = getRebinnedHistogram(inputFile.Get("DYJets_muIDUp"), binning, "bkgHistDY_%s_%sUp"%(IDName,zero_corr))

            bkgHistDYISODown = getRebinnedHistogram(inputFile.Get("DYJets_muISODown"), binning, "bkgHistDY_%s_%sDown"%(ISOName,zero_corr))
            bkgHistDYISOUp = getRebinnedHistogram(inputFile.Get("DYJets_muISOUp"), binning, "bkgHistDY_%s_%sUp"%(ISOName,zero_corr))

            bkgHistDYHLTDown = getRebinnedHistogram(inputFile.Get("DYJets_muHLTDown"), binning, "bkgHistDY_%s_%sDown"%(HLTName,zero_corr))
            bkgHistDYHLTUp = getRebinnedHistogram(inputFile.Get("DYJets_muHLTUp"), binning, "bkgHistDY_%s_%sUp"%(HLTName,zero_corr))


    bkgHistDYl1prefiringUp = getRebinnedHistogram(inputFile.Get("DYJets_l1prefiringUp"), binning, "bkgHistDY_%s_%sUp"%(prefiringName,zero_corr))
    bkgHistDYl1prefiringDown = getRebinnedHistogram(inputFile.Get("DYJets_l1prefiringDown"), binning, "bkgHistDY_%s_%sDown"%(prefiringName,zero_corr))




    bkgHistDYSmearUp = getRebinnedHistogram(inputFile.Get("DYJets_resUnc"), binning, "bkgHistDY_%s_%sUp"%(smearName,zero_corr))
    bkgHistDYSmearDown = getRebinnedHistogram(inputFile.Get("DYJets_resUnc"), binning, "bkgHistDY_%s_%sDown"%(smearName,zero_corr))

    # bkgHistDYBTagUp = getRebinnedHistogram(inputFile.Get("DYJets_btagUp"), binning, "bkgHistDY_%s_%sUp"%(btagName,channel_corr))
    # bkgHistDYBTagDown = getRebinnedHistogram(inputFile.Get("DYJets_btagDown"), binning, "bkgHistDY_%s_%sDown"%(btagName,channel_corr))
    if "ZeroB" in channel:
        bkgHistDYBTag_bc_corrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
        bkgHistDYBTag_bc_corrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
        bkgHistDYBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
        bkgHistDYBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
        bkgHistDYBTag_light_corrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
        bkgHistDYBTag_light_corrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
        bkgHistDYBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
        bkgHistDYBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    else:
        bkgHistDYBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_bc_corr,year_corr))
        bkgHistDYBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_bc_corr,year_corr))
        bkgHistDYBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_bc,channel_corr))
        bkgHistDYBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_bc,channel_corr))
        bkgHistDYBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_light_corr,year_corr))
        bkgHistDYBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_light_corr,year_corr))
        bkgHistDYBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_light,channel_corr))
        bkgHistDYBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_light,channel_corr))
    if "dimuon" in channel:
        bkgHistDYRecoUp = getRebinnedHistogram(inputFile.Get("DYJets_recoup"), binning, "bkgHistDY_%s_%sUp"%(recoName,zero_corr))
        bkgHistDYRecoDown = getRebinnedHistogram(inputFile.Get("DYJets_recodown"), binning, "bkgHistDY_%s_%sDown"%(recoName,zero_corr))
    bkgHistDYPUUp = getRebinnedHistogram(inputFile.Get("DYJets_puUp"), binning, "bkgHistDY_%s_%sUp"%(PUName,channel_corr))
    bkgHistDYPUDown = getRebinnedHistogram(inputFile.Get("DYJets_puDown"), binning, "bkgHistDY_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        bkgHistDYScaleDown = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncDown"),binning,"bkgHistDY_%s_%sDown"%(scaleName,zero_corr))
        bkgHistDYScaleUp = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncUp"),binning,"bkgHistDY_%s_%sUp"%(scaleName,zero_corr))
    else:
        bkgHistDYScaleDown = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncDown"),binning,"bkgHistDY_%s_%sDown"%(eScaleName,zero_corr))
        bkgHistDYScaleUp = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncUp"),binning,"bkgHistDY_%s_%sUp"%(eScaleName,zero_corr))


    bkgHistDYPDFDown = getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sDown"%(pdfName), pdfUncertDY)
    bkgHistDYPDFUp =   getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sUp"%(pdfName),   pdfUncertDY,True)

    #bkgHistDYBTag_bc_corrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
    #bkgHistDYBTag_bc_corrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
    #bkgHistDYBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
    #bkgHistDYBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
    #bkgHistDYBTag_light_corrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
    #bkgHistDYBTag_light_corrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
    #bkgHistDYBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
    #bkgHistDYBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)



    # bkg Top
    bkgHistTop = getRebinnedHistogram(inputFile.Get("Top"),binning,"bkgHistTop_%s"%channel)

    if "dielectron" in channel:
        bkgHistTopIDDown = getHEEPUncertHistogram(bkgHistTop,"bkgHistTop_%s_%sDown"%(IDName,channel_corr), heepUncert)
        bkgHistTopIDUp =   getHEEPUncertHistogram(bkgHistTop,"bkgHistTop_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
        bkgHistTopIDDown = getRebinnedHistogram(inputFile.Get("Top_muIDDown"), binning, "bkgHistTop_%s_%sDown"%(IDName,zero_corr))
        bkgHistTopIDUp = getRebinnedHistogram(inputFile.Get("Top_muIDUp"), binning, "bkgHistTop_%s_%sUp"%(IDName,zero_corr))

        bkgHistTopISODown = getRebinnedHistogram(inputFile.Get("Top_muISODown"), binning, "bkgHistTop_%s_%sDown"%(ISOName,zero_corr))
        bkgHistTopISOUp = getRebinnedHistogram(inputFile.Get("Top_muISOUp"), binning, "bkgHistTop_%s_%sUp"%(ISOName,zero_corr))

        bkgHistTopHLTDown = getRebinnedHistogram(inputFile.Get("Top_muHLTDown"), binning, "bkgHistTop_%s_%sDown"%(HLTName,zero_corr))
        bkgHistTopHLTUp = getRebinnedHistogram(inputFile.Get("Top_muHLTUp"), binning, "bkgHistTop_%s_%sUp"%(HLTName,zero_corr))

    bkgHistTopl1prefiringUp = getRebinnedHistogram(inputFile.Get("Top_l1prefiringUp"), binning, "bkgHistTop_%s_%sUp"%(prefiringName,zero_corr))
    bkgHistTopl1prefiringDown = getRebinnedHistogram(inputFile.Get("Top_l1prefiringDown"), binning, "bkgHistTop_%s_%sDown"%(prefiringName,zero_corr))

    bkgHistTopSmearUp = getRebinnedHistogram(inputFile.Get("Top_resUnc"), binning, "bkgHistTop_%s_%sUp"%(smearName,zero_corr))
    bkgHistTopSmearDown = getRebinnedHistogram(inputFile.Get("Top_resUnc"), binning, "bkgHistTop_%s_%sDown"%(smearName,zero_corr))
    
    if "ZeroB" in channel:
        bkgHistTopBTag_bc_corrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
        bkgHistTopBTag_bc_corrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
        
        bkgHistTopBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
        
        bkgHistTopBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
        
        bkgHistTopBTag_light_corrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
        bkgHistTopBTag_light_corrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
        
        bkgHistTopBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
        
        bkgHistTopBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    else:
        #bkgHistTopBTagUp = getRebinnedHistogram(inputFile.Get("Top_btagUp"), binning, "bkgHistTop_%s_%sUp"%(btagName,channel_corr))
        #bkgHistTopBTagDown = getRebinnedHistogram(inputFile.Get("Top_btagDown"), binning, "bkgHistTop_%s_%sDown"%(btagName,channel_corr))
        bkgHistTopBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_bc_corr,year_corr))
        bkgHistTopBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_bc_corr,year_corr))
        bkgHistTopBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_bc,channel_corr))
        bkgHistTopBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_bc,channel_corr))
        bkgHistTopBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_light_corr,year_corr))
        bkgHistTopBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_light_corr,year_corr))
        bkgHistTopBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_light,channel_corr))
        bkgHistTopBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_light,channel_corr))


    if "dimuon" in channel: 
        bkgHistTopRecoUp = getRebinnedHistogram(inputFile.Get("Top_recoup"), binning, "bkgHistTop_%s_%sUp"%(recoName,zero_corr))
        bkgHistTopRecoDown = getRebinnedHistogram(inputFile.Get("Top_recodown"), binning, "bkgHistTop_%s_%sDown"%(recoName,zero_corr))
    bkgHistTopPUUp = getRebinnedHistogram(inputFile.Get("Top_puUp"), binning, "bkgHistTop_%s_%sUp"%(PUName,channel_corr))
    bkgHistTopPUDown = getRebinnedHistogram(inputFile.Get("Top_puDown"), binning, "bkgHistTop_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        bkgHistTopScaleDown = getRebinnedHistogram(inputFile.Get("Top_scaleUncDown"),binning,"bkgHistTop_%s_%sDown"%(scaleName,zero_corr))
        bkgHistTopScaleUp = getRebinnedHistogram(inputFile.Get("Top_scaleUncUp"),binning,"bkgHistTop_%s_%sUp"%(scaleName,zero_corr))
            
    else:
        bkgHistTopScaleDown = getRebinnedHistogram(inputFile.Get("Top_scaleUncDown"),binning,"bkgHistTop_%s_%sDown"%(eScaleName,zero_corr))
        bkgHistTopScaleUp = getRebinnedHistogram(inputFile.Get("Top_scaleUncUp"),binning,"bkgHistTop_%s_%sUp"%(eScaleName,zero_corr))


    if ("OneB" in channel) or ("TwoB" in channel):
        bkgHistTopttbarUncertDown = getPDFUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(ttbarUncertName, zero_corr), ttbar_uncert) 
        bkgHistTopttbarUncertUp   = getPDFUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(ttbarUncertName, zero_corr), ttbar_uncert, True)




    bkgHistTopPDFDown = getPDFUncertHistogram(bkgHistTop,"bkgHistTop_%sDown"%(pdfName), pdfUncertTT)
    bkgHistTopPDFUp =   getPDFUncertHistogram(bkgHistTop,"bkgHistTop_%sUp"%(pdfName),   pdfUncertTT,True)

#    bkgHistTopBTag_bc_corrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
#    bkgHistTopBTag_bc_corrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
#
#    bkgHistTopBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
#
#    bkgHistTopBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
#
#    bkgHistTopBTag_light_corrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
#    bkgHistTopBTag_light_corrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
#
#    bkgHistTopBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
#
#    bkgHistTopBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)



    # bkg Diboson
    bkgHistDiboson = getRebinnedHistogram(inputFile.Get("Diboson"),binning,"bkgHistDiboson_%s"%channel)

    if "dielectron" in channel:
            bkgHistDibosonIDDown = getHEEPUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%s_%sDown"%(IDName,channel_corr), heepUncert)
            bkgHistDibosonIDUp =   getHEEPUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
            bkgHistDibosonIDDown = getRebinnedHistogram(inputFile.Get("Diboson_muIDDown"), binning, "bkgHistDiboson_%s_%sDown"%(IDName,zero_corr))
            bkgHistDibosonIDUp = getRebinnedHistogram(inputFile.Get("Diboson_muIDUp"), binning, "bkgHistDiboson_%s_%sUp"%(IDName,zero_corr))

            bkgHistDibosonISODown = getRebinnedHistogram(inputFile.Get("Diboson_muISODown"), binning, "bkgHistDiboson_%s_%sDown"%(ISOName,zero_corr))
            bkgHistDibosonISOUp = getRebinnedHistogram(inputFile.Get("Diboson_muISOUp"), binning, "bkgHistDiboson_%s_%sUp"%(ISOName,zero_corr))

            bkgHistDibosonHLTDown = getRebinnedHistogram(inputFile.Get("Diboson_muHLTDown"), binning, "bkgHistDiboson_%s_%sDown"%(HLTName,zero_corr))
            bkgHistDibosonHLTUp = getRebinnedHistogram(inputFile.Get("Diboson_muHLTUp"), binning, "bkgHistDiboson_%s_%sUp"%(HLTName,zero_corr))

    bkgHistDibosonl1prefiringUp = getRebinnedHistogram(inputFile.Get("Diboson_l1prefiringUp"), binning, "bkgHistDiboson_%s_%sUp"%(prefiringName,zero_corr))
    bkgHistDibosonl1prefiringDown = getRebinnedHistogram(inputFile.Get("Diboson_l1prefiringDown"), binning, "bkgHistDiboson_%s_%sDown"%(prefiringName,zero_corr))


    bkgHistDibosonSmearUp = getRebinnedHistogram(inputFile.Get("Diboson_resUnc"), binning, "bkgHistDiboson_%s_%sUp"%(smearName,zero_corr))
    bkgHistDibosonSmearDown = getRebinnedHistogram(inputFile.Get("Diboson_resUnc"), binning, "bkgHistDiboson_%s_%sDown"%(smearName,zero_corr))
    # bkgHistDibosonBTagUp = getRebinnedHistogram(inputFile.Get("Diboson_btagUp"), binning, "bkgHistDiboson_%s_%sUp"%(btagName,channel_corr))
    # bkgHistDibosonBTagDown = getRebinnedHistogram(inputFile.Get("Diboson_btagDown"), binning, "bkgHistDiboson_%s_%sDown"%(btagName,channel_corr))
    #bkgHistDibosonBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_bc_corr,year_corr))
    #bkgHistDibosonBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_bc_corr,year_corr))
    #bkgHistDibosonBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_bc,channel_corr))
    #bkgHistDibosonBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_bc,channel_corr))
    #bkgHistDibosonBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_light_corr,year_corr))
    #bkgHistDibosonBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_light_corr,year_corr))
    #bkgHistDibosonBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_light,channel_corr))
    #bkgHistDibosonBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_light,channel_corr))


    if "dimuon" in channel:
        bkgHistDibosonRecoUp = getRebinnedHistogram(inputFile.Get("Diboson_recoup"), binning, "bkgHistDiboson_%s_%sUp"%(recoName,zero_corr))
        bkgHistDibosonRecoDown = getRebinnedHistogram(inputFile.Get("Diboson_recodown"), binning, "bkgHistDiboson_%s_%sDown"%(recoName,zero_corr))
    bkgHistDibosonPUUp = getRebinnedHistogram(inputFile.Get("Diboson_puUp"), binning, "bkgHistDiboson_%s_%sUp"%(PUName,channel_corr))
    bkgHistDibosonPUDown = getRebinnedHistogram(inputFile.Get("Diboson_puDown"), binning, "bkgHistDiboson_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        bkgHistDibosonScaleDown = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncDown"),binning,"bkgHistDiboson_%s_%sDown"%(scaleName,zero_corr))
        bkgHistDibosonScaleUp = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncUp"),binning,"bkgHistDiboson_%s_%sUp"%(scaleName,zero_corr))
    else:
        bkgHistDibosonScaleDown = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncDown"),binning,"bkgHistDiboson_%s_%sDown"%(eScaleName,zero_corr))
        bkgHistDibosonScaleUp = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncUp"),binning,"bkgHistDiboson_%s_%sUp"%(eScaleName,zero_corr))


    bkgHistDibosonPDFDown = getPDFUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%sDown"%(pdfName), pdfUncertVV)
    bkgHistDibosonPDFUp =   getPDFUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%sUp"%(pdfName),   pdfUncertVV,True)

    if "ZeroB" in channel:
        bkgHistDibosonBTag_bc_corrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
        bkgHistDibosonBTag_bc_corrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
        bkgHistDibosonBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
        bkgHistDibosonBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
        bkgHistDibosonBTag_light_corrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
        bkgHistDibosonBTag_light_corrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
        bkgHistDibosonBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
        bkgHistDibosonBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    else: 
        bkgHistDibosonBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_bc_corr,year_corr))
        bkgHistDibosonBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_bc_corr,year_corr))
        bkgHistDibosonBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_bc,channel_corr))
        bkgHistDibosonBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_bc,channel_corr))
        bkgHistDibosonBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_light_corr,year_corr))
        bkgHistDibosonBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_light_corr,year_corr))
        bkgHistDibosonBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_light,channel_corr))
        bkgHistDibosonBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_light,channel_corr))



    if bbll:
         signalName = "bbll_lambda%sTeV_%s"%(L,interference)
    else:
         signalName = "bsll_lambda%sTeV"%L    

    #print("signalName: {0}".format(signalName))

    # signal
    sigHist = getRebinnedHistogram(inputFile.Get(signalName),binning,"sigHist_%s"%channel)
    if "dielectron" in channel:
            sigHistIDDown = getHEEPUncertHistogram(sigHist,"sigHist_%s_%sDown"%(IDName,channel_corr), heepUncert)
            sigHistIDUp =   getHEEPUncertHistogram(sigHist,"sigHist_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
            sigHistIDDown = getRebinnedHistogram(inputFile.Get("%s_muIDDown"%signalName), binning, "sigHist_%s_%sDown"%(IDName,zero_corr))
            sigHistIDUp = getRebinnedHistogram(inputFile.Get("%s_muIDUp"%signalName), binning, "sigHist_%s_%sUp"%(IDName,zero_corr))

            sigHistISODown = getRebinnedHistogram(inputFile.Get("%s_muISODown"%signalName), binning, "sigHist_%s_%sDown"%(ISOName,zero_corr))
            sigHistISOUp = getRebinnedHistogram(inputFile.Get("%s_muISOUp"%signalName), binning, "sigHist_%s_%sUp"%(ISOName,zero_corr))

            sigHistHLTDown = getRebinnedHistogram(inputFile.Get("%s_muHLTDown"%signalName), binning, "sigHist_%s_%sDown"%(HLTName,zero_corr))
            sigHistHLTUp = getRebinnedHistogram(inputFile.Get("%s_muHLTUp"%signalName), binning, "sigHist_%s_%sUp"%(HLTName,zero_corr))

    sigHistl1prefiringUp = getRebinnedHistogram(inputFile.Get("%s_l1prefiringUp"%signalName), binning, "sigHist_%s_%sUp"%(prefiringName,zero_corr))
    sigHistl1prefiringDown = getRebinnedHistogram(inputFile.Get("%s_l1prefiringDown"%signalName), binning, "sigHist_%s_%sDown"%(prefiringName,zero_corr))

    sigHistSmearUp = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalName), binning, "sigHist_%s_%sUp"%(smearName,zero_corr))
    sigHistSmearDown = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalName), binning, "sigHist_%s_%sDown"%(smearName,zero_corr))
    # sigHistBTagUp = getRebinnedHistogram(inputFile.Get("%s_btagUp"%signalName), binning, "sigHist_%s_%sUp"%(btagName,channel_corr))
    # sigHistBTagDown = getRebinnedHistogram(inputFile.Get("%s_btagDown"%signalName), binning, "sigHist_%s_%sDown"%(btagName,channel_corr))
    #sigHistBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%signalName), binning, "sigHist_%s_%sUp"%(btagName_bc_corr,year_corr))
    #sigHistBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%signalName), binning, "sigHist_%s_%sDown"%(btagName_bc_corr,year_corr))
    #sigHistBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%signalName), binning, "sigHist_%s_%sUp"%(btagName_bc,channel_corr))
    #sigHistBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%signalName), binning, "sigHist_%s_%sDown"%(btagName_bc,channel_corr))
    #sigHistBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%signalName), binning, "sigHist_%s_%sUp"%(btagName_light_corr,year_corr))
    #sigHistBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%signalName), binning, "sigHist_%s_%sDown"%(btagName_light_corr,year_corr))
    #sigHistBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%signalName), binning, "sigHist_%s_%sUp"%(btagName_light,channel_corr))
    #sigHistBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%signalName), binning, "sigHist_%s_%sDown"%(btagName_light,channel_corr))

    if "dimuon" in channel:
        sigHistRecoUp = getRebinnedHistogram(inputFile.Get("%s_recoup"%signalName), binning, "sigHist_%s_%sUp"%(recoName,zero_corr))
        sigHistRecoDown = getRebinnedHistogram(inputFile.Get("%s_recodown"%signalName), binning, "sigHist_%s_%sDown"%(recoName,zero_corr))
    sigHistPUUp = getRebinnedHistogram(inputFile.Get("%s_puUp"%signalName), binning, "sigHist_%s_%sUp"%(PUName,channel_corr))
    sigHistPUDown = getRebinnedHistogram(inputFile.Get("%s_puDown"%signalName), binning, "sigHist_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        sigHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalName),binning,"sigHist_%s_%sDown"%(scaleName,zero_corr))
        sigHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalName),binning,"sigHist_%s_%sUp"%(scaleName,zero_corr))
            
    else: # electron
        sigHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalName),binning,"sigHist_%s_%sDown"%(eScaleName,zero_corr))
        sigHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalName),binning,"sigHist_%s_%sUp"%(eScaleName,zero_corr))


    sigHistPDFDown = getPDFUncertHistogram(sigHist,"sigHist_%sDown"%(pdfName), pdfUncert)
    sigHistPDFUp =   getPDFUncertHistogram(sigHist,"sigHist_%sUp"%(pdfName),   pdfUncert,True)

    sigHistBTag_bc_corrUp = getBtagUncertHistogram(sigHist, "sigHist_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
    sigHistBTag_bc_corrDown = getBtagUncertHistogram(sigHist, "sigHist_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)

    sigHistBTag_bc_uncorrUp = getBtagUncertHistogram(sigHist, "sigHist_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)

    sigHistBTag_bc_uncorrDown = getBtagUncertHistogram(sigHist, "sigHist_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)

    sigHistBTag_light_corrUp = getBtagUncertHistogram(sigHist, "sigHist_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
    sigHistBTag_light_corrDown = getBtagUncertHistogram(sigHist, "sigHist_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)

    sigHistBTag_light_uncorrUp = getBtagUncertHistogram(sigHist, "sigHist_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)

    sigHistBTag_light_uncorrDown = getBtagUncertHistogram(sigHist, "sigHist_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)


    print("now rebinning fake") 
    if "muon" in channel:
        bkgHistJets = getRebinnedHistogram(fake_file.Get("mu_data_obs"), binning, "bkgHistJets_%s"%channel)
    else:
        bkgHistJets = getRebinnedHistogram(fake_file.Get("data_obs"), binning, "bkgHistJets_%s"%channel)

    if "muon" in channel:
        dataHist = getRebinnedHistogram(inputFile.Get("mu_data_obs"), binning, "dataHist_%s"%channel)
    else: # electron
        dataHist = getRebinnedHistogram(inputFile.Get("data_obs"), binning, "dataHist_%s"%channel)



    bkgIntegralDY = bkgHistDY.Integral()		
    bkgIntegralTop = bkgHistTop.Integral()		
    bkgIntegralDiboson = bkgHistDiboson.Integral()		
    sigIntegral = sigHist.Integral()

    bkgIntegralJets = bkgHistJets.Integral()

    histFile.Write()
    histFile.Close()


    #return [bkgIntegralDY,bkgIntegralTop,bkgIntegralDiboson,sigIntegral] # without JET default 
    return [bkgIntegralDY,bkgIntegralTop,bkgIntegralDiboson, bkgIntegralJets, sigIntegral] #default



####Aman destructive

def createHistogramsIntCI(L,interference,name,channel,scanConfigName,dataFile=""):
    ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)



    scanConfigName ="scanConfiguration_%s"%scanConfigName
    scanConfig =  __import__(scanConfigName)

    #binning = scanConfig.binning
    if "TwoB" in channel:

        binning = scanConfig.binning_2b
    else:
        binning = scanConfig.binning_0_1b

    print(binning)

    from array import array

    if "dielectron" in channel:
        inputFile = ROOT.TFile("/depot/cms/private/users/kaur214/output/elec_channel_2018_newSep_jan2024_trig_eff/dnn/stage3_templates/dielectron_mass/"+inputFiles[channel], "OPEN")
        fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/ee/preapproval/fake_"+inputFiles[channel], "OPEN")

    else: # dimuon
        ##with final DNN
        inputFile = ROOT.TFile("/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage3_templates/dimuon_mass/"+inputFiles[channel], "OPEN")
        fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/mumu/preapproval/fake_"+inputFiles[channel], "OPEN")

    if 'electron' in channel:
        lowestMass = 300
    elif 'muon' in channel:
        lowestMass = 300


    histFile = ROOT.TFile("%s.root"%name, "RECREATE")

    if ("OneB" in channel) or ("TwoB" in channel):
        if "BB" in channel:
              ttbar_uncert = [0.56769, 0.20715, 0.13428, 0.769523, 0.334064, 0.206764, 0.206764]
        else:
              ttbar_uncert = [0.774004, 0.6071, 0.84628, 0.800171, 0.603037, 0.300831, 0.497486]




    ##PDF Uncertainty original
    if "TwoB" in channel:
        pdfUncert =   [0.00156249, 0.0029808, 0.00518313, 0.0123567]
        pdfUncertDY = [0.01414670344, 0.01927992999, 0.02804822616, 0.04746036643]
        pdfUncertTT = [0.01964566484, 0.02769629981, 0.05196009012, 0.2532719835]
        pdfUncertVV = [0.0132467234,  0.02366424237, 0.1324849835, 0.1361711683]

    else:
        pdfUncert =   [0.00134735, 0.00156249, 0.00215549, 0.0029808, 0.00383769, 0.00518313, 0.00711226]
        pdfUncertDY = [0.01414670344, 0.01659019081, 0.01927992999, 0.02354107301, 0.02804822616, 0.04746036643]
        pdfUncertTT = [0.01964566484, 0.02306892944, 0.02769629981, 0.04407183593, 0.05196009012, 0.2532719835]
        pdfUncertVV = [0.0132467234,  0.01373970154, 0.01722591218, 0.02366424237, 0.1324849835, 0.1361711683]

        
        
#        pdfUncert =   [0.00131305, 0.00134735, 0.00156249, 0.00215549, 0.0029808, 0.00383769, 0.00518313, 0.00711226, 0.0123567]
#        pdfUncertDY = [0.01112166172, 0.01414670344, 0.01659019081, 0.01927992999, 0.02354107301, 0.02804822616, 0.04746036643]
#        pdfUncertTT = [0.01676181036, 0.01964566484, 0.02306892944, 0.02769629981, 0.04407183593, 0.05196009012, 0.2532719835]
#        pdfUncertVV = [0.01301770353, 0.0132467234,  0.01373970154, 0.01722591218, 0.02366424237, 0.1324849835, 0.1361711683]

    if "TwoB" in channel:
        heepUncert = [0.014, 0.018, 0.037, 0.037]
    else:
        heepUncert = [0.012, 0.014, 0.016, 0.018, 0.023, 0.037, 0.037, 0.037]

    if "dielectron" in channel:
       IDName = "ID"
       pdfName = "pdf_dielectron"
    else:
       IDName = "ID"
       pdfName = "pdf_dilepton"

    ttbarUncertName = "ttbarUncert"
    scaleName = "massScale"
    eScaleName = "energyScale"
    smearName = "res"
    #pdfName = "pdf_dilepton"
    #IDName = "ID"
    ISOName = "ISO"
    HLTName = "HLT"
    PUName = "PU"
    # btagName = "btag"
    prefiringName = "l1prefiring"
    btagName_bc = "btagSF_bc"
    btagName_light = "btagSF_light"
    btagName_bc_corr = "btagSF_bc_corr"
    btagName_light_corr = "btagSF_light_corr"
    recoName = "reco"

    print("------------------------------------------------")
    print("inputFile: {0}".format(inputFile.Get("DYJets")))

    # bkg DY
    bkgHistDY = getRebinnedHistogram(inputFile.Get("DYJets"),binning,"bkgHistDY_%s"%channel)

    # setup the name of btag to be consistent with our correlation nomenclature
    if "dielectron" in channel:
       year_corr = "dielectron"
       if "2018" in channel:
           channel_corr = "dielectron18"
       elif "2017" in channel:
           channel_corr = "dielectron17"
       elif "2016" in channel:
           if "post" in channel:
               channel_corr = "dielectron16_post"
           else:
               channel_corr = "dielectron16_pre"
       else:
           print("invalid channel configuration")
    else:
       year_corr = "dilepton"
       if "2018" in channel:
           channel_corr = "dilepton18"
       elif "2017" in channel:
           channel_corr = "dilepton17"
       elif "2016" in channel:
           if "post" in channel:
               channel_corr = "dilepton16_post"
           else:
               channel_corr = "dilepton16_pre"
       else:
           print("invalid channel configuration")
           raise ValueError

    if "BB" in channel:
        zero_corr = channel.replace('BB_',"")
        # print "zero_corr: {0}".format(zero_corr)
    else:
        zero_corr = channel.replace('BE_',"")

    if "dielectron" in channel:
            bkgHistDYIDDown = getHEEPUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sDown"%(IDName,channel_corr), heepUncert)
            bkgHistDYIDUp =   getHEEPUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
            bkgHistDYIDDown = getRebinnedHistogram(inputFile.Get("DYJets_muIDDown"), binning, "bkgHistDY_%s_%sDown"%(IDName,zero_corr))
            bkgHistDYIDUp = getRebinnedHistogram(inputFile.Get("DYJets_muIDUp"), binning, "bkgHistDY_%s_%sUp"%(IDName,zero_corr))

            bkgHistDYISODown = getRebinnedHistogram(inputFile.Get("DYJets_muISODown"), binning, "bkgHistDY_%s_%sDown"%(ISOName,zero_corr))
            bkgHistDYISOUp = getRebinnedHistogram(inputFile.Get("DYJets_muISOUp"), binning, "bkgHistDY_%s_%sUp"%(ISOName,zero_corr))

            bkgHistDYHLTDown = getRebinnedHistogram(inputFile.Get("DYJets_muHLTDown"), binning, "bkgHistDY_%s_%sDown"%(HLTName,zero_corr))
            bkgHistDYHLTUp = getRebinnedHistogram(inputFile.Get("DYJets_muHLTUp"), binning, "bkgHistDY_%s_%sUp"%(HLTName,zero_corr))


    bkgHistDYl1prefiringUp = getRebinnedHistogram(inputFile.Get("DYJets_l1prefiringUp"), binning, "bkgHistDY_%s_%sUp"%(prefiringName,zero_corr))
    bkgHistDYl1prefiringDown = getRebinnedHistogram(inputFile.Get("DYJets_l1prefiringDown"), binning, "bkgHistDY_%s_%sDown"%(prefiringName,zero_corr))


    bkgHistDYSmearUp = getRebinnedHistogram(inputFile.Get("DYJets_resUnc"), binning, "bkgHistDY_%s_%sUp"%(smearName,zero_corr))
    bkgHistDYSmearDown = getRebinnedHistogram(inputFile.Get("DYJets_resUnc"), binning, "bkgHistDY_%s_%sDown"%(smearName,zero_corr))

    # bkgHistDYBTagUp = getRebinnedHistogram(inputFile.Get("DYJets_btagUp"), binning, "bkgHistDY_%s_%sUp"%(btagName,channel_corr))
    # bkgHistDYBTagDown = getRebinnedHistogram(inputFile.Get("DYJets_btagDown"), binning, "bkgHistDY_%s_%sDown"%(btagName,channel_corr))
    if "ZeroB" in channel:
        bkgHistDYBTag_bc_corrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
        bkgHistDYBTag_bc_corrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
        bkgHistDYBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
        bkgHistDYBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
        bkgHistDYBTag_light_corrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
        bkgHistDYBTag_light_corrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
        bkgHistDYBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
        bkgHistDYBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    else:
        bkgHistDYBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_bc_corr,year_corr))
        bkgHistDYBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_bc_corr,year_corr))
        bkgHistDYBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_bc,channel_corr))
        bkgHistDYBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_bc,channel_corr))
        bkgHistDYBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_light_corr,year_corr))
        bkgHistDYBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_light_corr,year_corr))
        bkgHistDYBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_light,channel_corr))
        bkgHistDYBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_light,channel_corr))

    if "dimuon" in channel:
        bkgHistDYRecoUp = getRebinnedHistogram(inputFile.Get("DYJets_recoup"), binning, "bkgHistDY_%s_%sUp"%(recoName,zero_corr))
        bkgHistDYRecoDown = getRebinnedHistogram(inputFile.Get("DYJets_recodown"), binning, "bkgHistDY_%s_%sDown"%(recoName,zero_corr))
    bkgHistDYPUUp = getRebinnedHistogram(inputFile.Get("DYJets_puUp"), binning, "bkgHistDY_%s_%sUp"%(PUName,channel_corr))
    bkgHistDYPUDown = getRebinnedHistogram(inputFile.Get("DYJets_puDown"), binning, "bkgHistDY_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        bkgHistDYScaleDown = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncDown"),binning,"bkgHistDY_%s_%sDown"%(scaleName,zero_corr))
        bkgHistDYScaleUp = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncUp"),binning,"bkgHistDY_%s_%sUp"%(scaleName,zero_corr))
    else:
        bkgHistDYScaleDown = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncDown"),binning,"bkgHistDY_%s_%sDown"%(eScaleName,zero_corr))
        bkgHistDYScaleUp = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncUp"),binning,"bkgHistDY_%s_%sUp"%(eScaleName,zero_corr))


    bkgHistDYPDFDown = getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sDown"%(pdfName), pdfUncertDY)
    bkgHistDYPDFUp =   getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sUp"%(pdfName),   pdfUncertDY,True)


    # bkg Top
    bkgHistTop = getRebinnedHistogram(inputFile.Get("Top"),binning,"bkgHistTop_%s"%channel)

    if "dielectron" in channel:
        bkgHistTopIDDown = getHEEPUncertHistogram(bkgHistTop,"bkgHistTop_%s_%sDown"%(IDName,channel_corr), heepUncert)
        bkgHistTopIDUp =   getHEEPUncertHistogram(bkgHistTop,"bkgHistTop_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
        bkgHistTopIDDown = getRebinnedHistogram(inputFile.Get("Top_muIDDown"), binning, "bkgHistTop_%s_%sDown"%(IDName,zero_corr))
        bkgHistTopIDUp = getRebinnedHistogram(inputFile.Get("Top_muIDUp"), binning, "bkgHistTop_%s_%sUp"%(IDName,zero_corr))

        bkgHistTopISODown = getRebinnedHistogram(inputFile.Get("Top_muISODown"), binning, "bkgHistTop_%s_%sDown"%(ISOName,zero_corr))
        bkgHistTopISOUp = getRebinnedHistogram(inputFile.Get("Top_muISOUp"), binning, "bkgHistTop_%s_%sUp"%(ISOName,zero_corr))

        bkgHistTopHLTDown = getRebinnedHistogram(inputFile.Get("Top_muHLTDown"), binning, "bkgHistTop_%s_%sDown"%(HLTName,zero_corr))
        bkgHistTopHLTUp = getRebinnedHistogram(inputFile.Get("Top_muHLTUp"), binning, "bkgHistTop_%s_%sUp"%(HLTName,zero_corr))

    bkgHistTopl1prefiringUp = getRebinnedHistogram(inputFile.Get("Top_l1prefiringUp"), binning, "bkgHistTop_%s_%sUp"%(prefiringName,zero_corr))
    bkgHistTopl1prefiringDown = getRebinnedHistogram(inputFile.Get("Top_l1prefiringDown"), binning, "bkgHistTop_%s_%sDown"%(prefiringName,zero_corr))

    bkgHistTopSmearUp = getRebinnedHistogram(inputFile.Get("Top_resUnc"), binning, "bkgHistTop_%s_%sUp"%(smearName,zero_corr))
    bkgHistTopSmearDown = getRebinnedHistogram(inputFile.Get("Top_resUnc"), binning, "bkgHistTop_%s_%sDown"%(smearName,zero_corr))

    if "ZeroB" in channel:
        bkgHistTopBTag_bc_corrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
        bkgHistTopBTag_bc_corrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)

        bkgHistTopBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)

        bkgHistTopBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)

        bkgHistTopBTag_light_corrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
        bkgHistTopBTag_light_corrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)

        bkgHistTopBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)

        bkgHistTopBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    else:
        #bkgHistTopBTagUp = getRebinnedHistogram(inputFile.Get("Top_btagUp"), binning, "bkgHistTop_%s_%sUp"%(btagName,channel_corr))
        #bkgHistTopBTagDown = getRebinnedHistogram(inputFile.Get("Top_btagDown"), binning, "bkgHistTop_%s_%sDown"%(btagName,channel_corr))
        bkgHistTopBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_bc_corr,year_corr))
        bkgHistTopBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_bc_corr,year_corr))
        bkgHistTopBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_bc,channel_corr))
        bkgHistTopBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_bc,channel_corr))
        bkgHistTopBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_light_corr,year_corr))
        bkgHistTopBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_light_corr,year_corr))

        bkgHistTopBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_light,channel_corr))
        bkgHistTopBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_light,channel_corr))


    if "dimuon" in channel:
        bkgHistTopRecoUp = getRebinnedHistogram(inputFile.Get("Top_recoup"), binning, "bkgHistTop_%s_%sUp"%(recoName,zero_corr))
        bkgHistTopRecoDown = getRebinnedHistogram(inputFile.Get("Top_recodown"), binning, "bkgHistTop_%s_%sDown"%(recoName,zero_corr))
    bkgHistTopPUUp = getRebinnedHistogram(inputFile.Get("Top_puUp"), binning, "bkgHistTop_%s_%sUp"%(PUName,channel_corr))
    bkgHistTopPUDown = getRebinnedHistogram(inputFile.Get("Top_puDown"), binning, "bkgHistTop_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        bkgHistTopScaleDown = getRebinnedHistogram(inputFile.Get("Top_scaleUncDown"),binning,"bkgHistTop_%s_%sDown"%(scaleName,zero_corr))
        bkgHistTopScaleUp = getRebinnedHistogram(inputFile.Get("Top_scaleUncUp"),binning,"bkgHistTop_%s_%sUp"%(scaleName,zero_corr))

    else:
        bkgHistTopScaleDown = getRebinnedHistogram(inputFile.Get("Top_scaleUncDown"),binning,"bkgHistTop_%s_%sDown"%(eScaleName,zero_corr))
        bkgHistTopScaleUp = getRebinnedHistogram(inputFile.Get("Top_scaleUncUp"),binning,"bkgHistTop_%s_%sUp"%(eScaleName,zero_corr))


    if ("OneB" in channel) or ("TwoB" in channel):
        bkgHistTopttbarUncertDown = getPDFUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(ttbarUncertName, zero_corr), ttbar_uncert)
        bkgHistTopttbarUncertUp   = getPDFUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(ttbarUncertName, zero_corr), ttbar_uncert, True)





    bkgHistTopPDFDown = getPDFUncertHistogram(bkgHistTop,"bkgHistTop_%sDown"%(pdfName), pdfUncertTT)
    bkgHistTopPDFUp =   getPDFUncertHistogram(bkgHistTop,"bkgHistTop_%sUp"%(pdfName),   pdfUncertTT,True)


    # bkg Diboson
    bkgHistDiboson = getRebinnedHistogram(inputFile.Get("Diboson"),binning,"bkgHistDiboson_%s"%channel)

    if "dielectron" in channel:
            bkgHistDibosonIDDown = getHEEPUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%s_%sDown"%(IDName,channel_corr), heepUncert)
            bkgHistDibosonIDUp =   getHEEPUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
            bkgHistDibosonIDDown = getRebinnedHistogram(inputFile.Get("Diboson_muIDDown"), binning, "bkgHistDiboson_%s_%sDown"%(IDName,zero_corr))
            bkgHistDibosonIDUp = getRebinnedHistogram(inputFile.Get("Diboson_muIDUp"), binning, "bkgHistDiboson_%s_%sUp"%(IDName,zero_corr))

            bkgHistDibosonISODown = getRebinnedHistogram(inputFile.Get("Diboson_muISODown"), binning, "bkgHistDiboson_%s_%sDown"%(ISOName,zero_corr))
            bkgHistDibosonISOUp = getRebinnedHistogram(inputFile.Get("Diboson_muISOUp"), binning, "bkgHistDiboson_%s_%sUp"%(ISOName,zero_corr))

            bkgHistDibosonHLTDown = getRebinnedHistogram(inputFile.Get("Diboson_muHLTDown"), binning, "bkgHistDiboson_%s_%sDown"%(HLTName,zero_corr))
            bkgHistDibosonHLTUp = getRebinnedHistogram(inputFile.Get("Diboson_muHLTUp"), binning, "bkgHistDiboson_%s_%sUp"%(HLTName,zero_corr))

    bkgHistDibosonl1prefiringUp = getRebinnedHistogram(inputFile.Get("Diboson_l1prefiringUp"), binning, "bkgHistDiboson_%s_%sUp"%(prefiringName,zero_corr))
    bkgHistDibosonl1prefiringDown = getRebinnedHistogram(inputFile.Get("Diboson_l1prefiringDown"), binning, "bkgHistDiboson_%s_%sDown"%(prefiringName,zero_corr))


    bkgHistDibosonSmearUp = getRebinnedHistogram(inputFile.Get("Diboson_resUnc"), binning, "bkgHistDiboson_%s_%sUp"%(smearName,zero_corr))
    bkgHistDibosonSmearDown = getRebinnedHistogram(inputFile.Get("Diboson_resUnc"), binning, "bkgHistDiboson_%s_%sDown"%(smearName,zero_corr))


    if "dimuon" in channel:
        bkgHistDibosonRecoUp = getRebinnedHistogram(inputFile.Get("Diboson_recoup"), binning, "bkgHistDiboson_%s_%sUp"%(recoName,zero_corr))
        bkgHistDibosonRecoDown = getRebinnedHistogram(inputFile.Get("Diboson_recodown"), binning, "bkgHistDiboson_%s_%sDown"%(recoName,zero_corr))
    bkgHistDibosonPUUp = getRebinnedHistogram(inputFile.Get("Diboson_puUp"), binning, "bkgHistDiboson_%s_%sUp"%(PUName,channel_corr))
    bkgHistDibosonPUDown = getRebinnedHistogram(inputFile.Get("Diboson_puDown"), binning, "bkgHistDiboson_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        bkgHistDibosonScaleDown = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncDown"),binning,"bkgHistDiboson_%s_%sDown"%(scaleName,zero_corr))
        bkgHistDibosonScaleUp = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncUp"),binning,"bkgHistDiboson_%s_%sUp"%(scaleName,zero_corr))
    else:
        bkgHistDibosonScaleDown = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncDown"),binning,"bkgHistDiboson_%s_%sDown"%(eScaleName,zero_corr))
        bkgHistDibosonScaleUp = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncUp"),binning,"bkgHistDiboson_%s_%sUp"%(eScaleName,zero_corr))


    bkgHistDibosonPDFDown = getPDFUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%sDown"%(pdfName), pdfUncertVV)
    bkgHistDibosonPDFUp =   getPDFUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%sUp"%(pdfName),   pdfUncertVV,True)


    if "ZeroB" in channel:
        bkgHistDibosonBTag_bc_corrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
        bkgHistDibosonBTag_bc_corrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
        bkgHistDibosonBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
        bkgHistDibosonBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
        bkgHistDibosonBTag_light_corrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
        bkgHistDibosonBTag_light_corrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
        bkgHistDibosonBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
        bkgHistDibosonBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    else:
        bkgHistDibosonBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_bc_corr,year_corr))
        bkgHistDibosonBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_bc_corr,year_corr))
        bkgHistDibosonBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_bc,channel_corr))
        bkgHistDibosonBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_bc,channel_corr))
        bkgHistDibosonBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_light_corr,year_corr))
        bkgHistDibosonBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_light_corr,year_corr))
        bkgHistDibosonBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_light,channel_corr))
        bkgHistDibosonBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_light,channel_corr))




##now starting to add the signal hist and all other related histograms
## sigHist bbll constructive + bbll destructive /2 
##intHist : bbll destructive

    signalName = "bbll_lambda%sTeV_%s"%(L,interference)

    DYName     = "bbll_100000TeV_negLL"
    # Replace "neg" with "pos" in the interference string
    interference_con = interference.replace("neg", "pos")

    signalConName = "bbll_lambda%sTeV_%s"%(L,interference_con)


    sigHistOrg = getRebinnedHistogram(inputFile.Get(signalName),binning,"sigHist_%s"%channel)

    sigHist = sigHistOrg.Clone()

    sigHistCon = getRebinnedHistogram(inputFile.Get(signalConName),binning,"sigHistCon_%s"%channel)


    sigHist.Add(sigHistCon.Clone())
   
    DYHist = getRebinnedHistogram(inputFile.Get(DYName), binning,"DYHist_%s"%channel)


    sigHist.Add(DYHist.Clone(), -1)
    sigHist.Scale(0.5)

##### sigHist Uncertainties
    if "dielectron" in channel:

        sigHistIDDown = getHEEPUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sDown"%(IDName,channel_corr), heepUncert)
        sigHistIDDownCon =  getHEEPUncertHistogram(sigHistCon,"sigHistCon_%s_%sDown"%(IDName,channel_corr), heepUncert)
        sigHistIDDown.Add(sigHistIDDownCon.Clone())

        DYHistIDDown = getHEEPUncertHistogram(DYHist, "DYHist_%s_%sDown"%(IDName,channel_corr), heepUncert)
        sigHistIDDown.Add(DYHistIDDown.Clone(), -1)
        sigHistIDDown.Scale(0.5)

        sigHistIDUp = getHEEPUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sUp"%(IDName,channel_corr), heepUncert , True)
        sigHistIDUpCon =  getHEEPUncertHistogram(sigHistCon,"sigHistCon_%s_%sUp"%(IDName,channel_corr), heepUncert , True)
        sigHistIDUp.Add(sigHistIDUpCon.Clone())

        DYHistIDUp = getHEEPUncertHistogram(DYHist, "DYHist_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
        sigHistIDUp.Add(DYHistIDUp.Clone(), -1)
        sigHistIDUp.Scale(0.5)
   
    else:
        sigHistIDDown = getRebinnedHistogram(inputFile.Get("%s_muIDDown"%signalName), binning, "sigHist_%s_%sDown"%(IDName,zero_corr))
        sigHistIDDownCon = getRebinnedHistogram(inputFile.Get("%s_muIDDown"%signalConName), binning, "sigHistCon_%s_%sDown"%(IDName,zero_corr))
        sigHistIDDown.Add(sigHistIDDownCon.Clone())
        DYHistIDDown = getRebinnedHistogram(inputFile.Get("%s_muIDDown"%DYName), binning,"DYHist_%s_%sDown"%(IDName,zero_corr))
        sigHistIDDown.Add(DYHistIDDown.Clone(), -1)
        sigHistIDDown.Scale(0.5)

        sigHistIDUp = getRebinnedHistogram(inputFile.Get("%s_muIDUp"%signalName), binning, "sigHist_%s_%sUp"%(IDName,zero_corr))
        sigHistIDUpCon = getRebinnedHistogram(inputFile.Get("%s_muIDUp"%signalConName), binning, "sigHistCon_%s_%sUp"%(IDName,zero_corr))
        sigHistIDUp.Add(sigHistIDUpCon.Clone())
        DYHistIDUp = getRebinnedHistogram(inputFile.Get("%s_muIDUp"%DYName), binning,"DYHist_%s_%sUp"%(IDName,zero_corr))
        sigHistIDUp.Add(DYHistIDUp.Clone(), -1)
        sigHistIDUp.Scale(0.5)

        ##muon isolation
        sigHistISODown = getRebinnedHistogram(inputFile.Get("%s_muISODown"%signalName), binning, "sigHist_%s_%sDown"%(ISOName,zero_corr))
        sigHistISODownCon = getRebinnedHistogram(inputFile.Get("%s_muISODown"%signalConName), binning, "sigHistCon_%s_%sDown"%(ISOName,zero_corr))
        sigHistISODown.Add(sigHistISODownCon.Clone())
        DYHistISODown = getRebinnedHistogram(inputFile.Get("%s_muISODown"%DYName), binning,"DYHist_%s_%sDown"%(ISOName,zero_corr))
        sigHistISODown.Add(DYHistISODown.Clone(), -1)
        sigHistISODown.Scale(0.5)

        sigHistISOUp = getRebinnedHistogram(inputFile.Get("%s_muISOUp"%signalName), binning, "sigHist_%s_%sUp"%(ISOName,zero_corr))
        sigHistISOUpCon = getRebinnedHistogram(inputFile.Get("%s_muISOUp"%signalConName), binning, "sigHistCon_%s_%sUp"%(ISOName,zero_corr))
        sigHistISOUp.Add(sigHistISOUpCon.Clone())
        DYHistISOUp = getRebinnedHistogram(inputFile.Get("%s_muISOUp"%DYName), binning,"DYHist_%s_%sUp"%(ISOName,zero_corr))
        sigHistISOUp.Add(DYHistISOUp.Clone(), -1) 
        sigHistISOUp.Scale(0.5)

        ##muon HLT
        sigHistHLTDown = getRebinnedHistogram(inputFile.Get("%s_muHLTDown"%signalName), binning, "sigHist_%s_%sDown"%(HLTName,zero_corr))
        sigHistHLTDownCon = getRebinnedHistogram(inputFile.Get("%s_muHLTDown"%signalConName), binning, "sigHistCon_%s_%sDown"%(HLTName,zero_corr))
        sigHistHLTDown.Add(sigHistHLTDownCon.Clone())
        DYHistHLTDown = getRebinnedHistogram(inputFile.Get("%s_muHLTDown"%DYName), binning,"DYHist_%s_%sDown"%(HLTName,zero_corr))
        sigHistHLTDown.Add(DYHistHLTDown.Clone(), -1)
        sigHistHLTDown.Scale(0.5)

        sigHistHLTUp = getRebinnedHistogram(inputFile.Get("%s_muHLTUp"%signalName), binning, "sigHist_%s_%sUp"%(HLTName,zero_corr))
        sigHistHLTUpCon = getRebinnedHistogram(inputFile.Get("%s_muHLTUp"%signalConName), binning, "sigHistCon_%s_%sUp"%(HLTName,zero_corr))
        sigHistHLTUp.Add(sigHistHLTUpCon.Clone())
        DYHistHLTUp = getRebinnedHistogram(inputFile.Get("%s_muHLTUp"%DYName), binning,"DYHist_%s_%sUp"%(HLTName,zero_corr))
        sigHistHLTUp.Add(DYHistHLTUp.Clone(), -1)
        sigHistHLTUp.Scale(0.5)

    ##L1 prefiring
    sigHistl1prefiringDown = getRebinnedHistogram(inputFile.Get("%s_l1prefiringDown"%signalName), binning, "sigHist_%s_%sDown"%(prefiringName,zero_corr))
    sigHistl1prefiringDownCon = getRebinnedHistogram(inputFile.Get("%s_l1prefiringDown"%signalConName), binning, "sigHistCon_%s_%sDown"%(prefiringName,zero_corr))
    sigHistl1prefiringDown.Add(sigHistl1prefiringDownCon.Clone())
    DYHistl1prefiringDown = getRebinnedHistogram(inputFile.Get("%s_l1prefiringDown"%DYName), binning,"DYHist_%s_%sDown"%(prefiringName,zero_corr))
    sigHistl1prefiringDown.Add(DYHistl1prefiringDown.Clone(), -1)
    sigHistl1prefiringDown.Scale(0.5)

    sigHistl1prefiringUp = getRebinnedHistogram(inputFile.Get("%s_l1prefiringUp"%signalName), binning, "sigHist_%s_%sUp"%(prefiringName,zero_corr))
    sigHistl1prefiringUpCon = getRebinnedHistogram(inputFile.Get("%s_l1prefiringUp"%signalConName), binning, "sigHistCon_%s_%sUp"%(prefiringName,zero_corr))
    sigHistl1prefiringUp.Add(sigHistl1prefiringUpCon.Clone())
    DYHistl1prefiringUp = getRebinnedHistogram(inputFile.Get("%s_l1prefiringUp"%DYName), binning,"DYHist_%s_%sUp"%(prefiringName,zero_corr))
    sigHistl1prefiringUp.Add(DYHistl1prefiringUp.Clone(), -1)
    sigHistl1prefiringUp.Scale(0.5)

    ##Smearing

    sigHistSmearDown = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalName), binning, "sigHist_%s_%sDown"%(smearName,zero_corr))
    sigHistSmearDownCon = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalConName), binning, "sigHistCon_%s_%sDown"%(smearName,zero_corr))
    sigHistSmearDown.Add(sigHistSmearDownCon.Clone())
    DYHistSmearDown = getRebinnedHistogram(inputFile.Get("%s_resUnc"%DYName), binning,"DYHist_%s_%sDown"%(smearName,zero_corr))
    sigHistSmearDown.Add(DYHistSmearDown.Clone(), -1)
    sigHistSmearDown.Scale(0.5)

    sigHistSmearUp = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalName), binning, "sigHist_%s_%sUp"%(smearName,zero_corr))
    sigHistSmearUpCon = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalConName), binning, "sigHistCon_%s_%sUp"%(smearName,zero_corr))
    sigHistSmearUp.Add(sigHistSmearUpCon.Clone())
    DYHistSmearUp = getRebinnedHistogram(inputFile.Get("%s_resUnc"%DYName), binning,"DYHist_%s_%sUp"%(smearName,zero_corr))
    sigHistSmearUp.Add(DYHistSmearUp.Clone(), -1)
    sigHistSmearUp.Scale(0.5)


    ##muon reco
    if "dimuon" in channel:
        sigHistRecoDown = getRebinnedHistogram(inputFile.Get("%s_recodown"%signalName), binning, "sigHist_%s_%sDown"%(recoName,zero_corr))
        sigHistRecoDownCon = getRebinnedHistogram(inputFile.Get("%s_recodown"%signalConName), binning, "sigHistCon_%s_%sDown"%(recoName,zero_corr))
        sigHistRecoDown.Add(sigHistRecoDownCon.Clone())
        DYHistRecoDown = getRebinnedHistogram(inputFile.Get("%s_recodown"%DYName), binning,"DYHist_%s_%sDown"%(recoName,zero_corr))
        sigHistRecoDown.Add(DYHistRecoDown.Clone(), -1)
        sigHistRecoDown.Scale(0.5)
    
        sigHistRecoUp = getRebinnedHistogram(inputFile.Get("%s_recoup"%signalName), binning, "sigHist_%s_%sUp"%(recoName,zero_corr))
        sigHistRecoUpCon = getRebinnedHistogram(inputFile.Get("%s_recoup"%signalConName), binning, "sigHistCon_%s_%sUp"%(recoName,zero_corr))
        sigHistRecoUp.Add(sigHistRecoUpCon.Clone())
        DYHistRecoUp = getRebinnedHistogram(inputFile.Get("%s_recoup"%DYName), binning,"DYHist_%s_%sUp"%(recoName,zero_corr))
        sigHistRecoUp.Add(DYHistRecoUp.Clone(), -1)
        sigHistRecoUp.Scale(0.5)

    ##scale uncertainty

    if "muon" in zero_corr:
        sigHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalName), binning, "sigHist_%s_%sDown"%(scaleName,zero_corr))
        sigHistScaleDownCon = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalConName), binning, "sigHistCon_%s_%sDown"%(scaleName,zero_corr))
        sigHistScaleDown.Add(sigHistScaleDownCon.Clone())
        DYHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%DYName), binning,"DYHist_%s_%sDown"%(scaleName,zero_corr))
        sigHistScaleDown.Add(DYHistScaleDown.Clone(), -1)
        sigHistScaleDown.Scale(0.5)

        sigHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalName), binning, "sigHist_%s_%sUp"%(scaleName,zero_corr))
        sigHistScaleUpCon = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalConName), binning, "sigHistCon_%s_%sUp"%(scaleName,zero_corr))
        sigHistScaleUp.Add(sigHistScaleUpCon.Clone())
        DYHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%DYName), binning,"DYHist_%s_%sUp"%(scaleName,zero_corr))
        sigHistScaleUp.Add(DYHistScaleUp.Clone(), -1)
        sigHistScaleUp.Scale(0.5)

    else:
        sigHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalName), binning, "sigHist_%s_%sDown"%(eScaleName,zero_corr))
        sigHistScaleDownCon = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalConName), binning, "sigHistCon_%s_%sDown"%(eScaleName,zero_corr))
        sigHistScaleDown.Add(sigHistScaleDownCon.Clone())
        DYHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%DYName), binning,"DYHist_%s_%sDown"%(eScaleName,zero_corr))
        sigHistScaleDown.Add(DYHistScaleDown.Clone(), -1)
        sigHistScaleDown.Scale(0.5)

        sigHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalName), binning, "sigHist_%s_%sUp"%(eScaleName,zero_corr))
        sigHistScaleUpCon = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalConName), binning, "sigHistCon_%s_%sUp"%(eScaleName,zero_corr))
        sigHistScaleUp.Add(sigHistScaleUpCon.Clone())
        DYHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%DYName), binning,"DYHist_%s_%sUp"%(eScaleName,zero_corr))
        sigHistScaleUp.Add(DYHistScaleUp.Clone(), -1)
        sigHistScaleUp.Scale(0.5)

    ##PileUp

    sigHistPUDown = getRebinnedHistogram(inputFile.Get("%s_puDown"%signalName), binning, "sigHist_%s_%sDown"%(PUName,channel_corr))
    sigHistPUDownCon = getRebinnedHistogram(inputFile.Get("%s_puDown"%signalConName), binning, "sigHistCon_%s_%sDown"%(PUName,channel_corr))
    sigHistPUDown.Add(sigHistPUDownCon.Clone())
    DYHistPUDown = getRebinnedHistogram(inputFile.Get("%s_puDown"%DYName), binning,"DYHist_%s_%sDown"%(PUName,channel_corr))
    sigHistPUDown.Add(DYHistPUDown.Clone(), -1)
    sigHistPUDown.Scale(0.5)

    sigHistPUUp = getRebinnedHistogram(inputFile.Get("%s_puUp"%signalName), binning, "sigHist_%s_%sUp"%(PUName,channel_corr))
    sigHistPUUpCon = getRebinnedHistogram(inputFile.Get("%s_puUp"%signalConName), binning, "sigHistCon_%s_%sUp"%(PUName,channel_corr))
    sigHistPUUp.Add(sigHistPUUpCon.Clone())
    DYHistPUUp = getRebinnedHistogram(inputFile.Get("%s_puUp"%DYName), binning,"DYHist_%s_%sUp"%(PUName,channel_corr))
    sigHistPUUp.Add(DYHistPUUp.Clone(), -1)
    sigHistPUUp.Scale(0.5)


    ##PDF

    sigHistPDFDown = getPDFUncertHistogram(sigHistOrg.Clone(),"sigHist_%sDown"%(pdfName), pdfUncert)
    #print("sigHistPDFDown", sigHistPDFDown.Integral())
    sigHistPDFDownCon =  getPDFUncertHistogram(sigHistCon,"sigHistCon_%sDown"%(pdfName), pdfUncert)
    sigHistPDFDown.Add(sigHistPDFDownCon.Clone())
    #print("sigHistPDFDown", sigHistPDFDown.Integral())


    DYHistPDFDown = getPDFUncertHistogram(DYHist, "DYHist_%sDown"%(pdfName), pdfUncert)
    sigHistPDFDown.Add(DYHistPDFDown.Clone(), -1)
    sigHistPDFDown.Scale(0.5)

    #print("sigHistPDFDown", sigHistPDFDown.Integral())

    sigHistPDFUp = getPDFUncertHistogram(sigHistOrg.Clone(),"sigHist_%sUp"%(pdfName), pdfUncert, True)
    sigHistPDFUpCon =  getPDFUncertHistogram(sigHistCon,"sigHistCon_%sUp"%(pdfName), pdfUncert, True)
    sigHistPDFUp.Add(sigHistPDFUpCon.Clone())

    DYHistPDFUp = getPDFUncertHistogram(DYHist, "DYHist_%sUp"%(pdfName), pdfUncert, True)
    sigHistPDFUp.Add(DYHistPDFUp.Clone(), -1)
    sigHistPDFUp.Scale(0.5)


    ##btag uncertainty
    sigHistBTag_bc_corrDown = getBtagUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sDown"%(btagName_bc_corr, year_corr), btag_bc_corr)
    sigHistBTag_bc_corrDownCon =  getBtagUncertHistogram(sigHistCon,"sigHistCon_%s_%sDown"%(btagName_bc_corr, year_corr), btag_bc_corr)
    sigHistBTag_bc_corrDown.Add(sigHistBTag_bc_corrDownCon.Clone())

    DYHistBTag_bc_corrDown = getBtagUncertHistogram(DYHist, "DYHist_%s_%sDown"%(btagName_bc_corr, year_corr), btag_bc_corr)
    sigHistBTag_bc_corrDown.Add(DYHistBTag_bc_corrDown.Clone(), -1)

    sigHistBTag_bc_corrDown.Scale(0.5)

    sigHistBTag_bc_corrUp = getBtagUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sUp"%(btagName_bc_corr, year_corr), btag_bc_corr, True)
    sigHistBTag_bc_corrUpCon =  getBtagUncertHistogram(sigHistCon,"sigHistCon_%s_%sUp"%(btagName_bc_corr, year_corr), btag_bc_corr, True)
    sigHistBTag_bc_corrUp.Add(sigHistBTag_bc_corrUpCon.Clone())

    DYHistBTag_bc_corrUp = getBtagUncertHistogram(DYHist, "DYHist_%s_%sUp"%(btagName_bc_corr, year_corr), btag_bc_corr, True)
    sigHistBTag_bc_corrUp.Add(DYHistBTag_bc_corrUp.Clone(), -1)
    sigHistBTag_bc_corrUp.Scale(0.5)

    ####bc uncorr
    sigHistBTag_bc_uncorrDown = getBtagUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sDown"%(btagName_bc, channel_corr), btag_bc_uncorr)
    sigHistBTag_bc_uncorrDownCon =  getBtagUncertHistogram(sigHistCon,"sigHistCon_%s_%sDown"%(btagName_bc, channel_corr), btag_bc_uncorr)
    sigHistBTag_bc_uncorrDown.Add(sigHistBTag_bc_uncorrDownCon.Clone())

    DYHistBTag_bc_uncorrDown = getBtagUncertHistogram(DYHist, "DYHist_%s_%sDown"%(btagName_bc, channel_corr), btag_bc_uncorr)
    sigHistBTag_bc_uncorrDown.Add(DYHistBTag_bc_uncorrDown.Clone(), -1)
    sigHistBTag_bc_uncorrDown.Scale(0.5)

    sigHistBTag_bc_uncorrUp = getBtagUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sUp"%(btagName_bc, channel_corr), btag_bc_uncorr, True)
    sigHistBTag_bc_uncorrUpCon =  getBtagUncertHistogram(sigHistCon,"sigHistCon_%s_%sUp"%(btagName_bc, channel_corr), btag_bc_uncorr, True)
    sigHistBTag_bc_uncorrUp.Add(sigHistBTag_bc_uncorrUpCon.Clone())

    DYHistBTag_bc_uncorrUp = getBtagUncertHistogram(DYHist, "DYHist_%s_%sUp"%(btagName_bc, channel_corr), btag_bc_uncorr, True)
    sigHistBTag_bc_uncorrUp.Add(DYHistBTag_bc_uncorrUp.Clone(), -1)
    sigHistBTag_bc_uncorrUp.Scale(0.5)


    ### light corr
    sigHistBTag_light_corrDown = getBtagUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sDown"%(btagName_light_corr, year_corr), btag_light_corr)
    sigHistBTag_light_corrDownCon =  getBtagUncertHistogram(sigHistCon,"sigHistCon_%s_%sDown"%(btagName_light_corr, year_corr), btag_light_corr)
    sigHistBTag_light_corrDown.Add(sigHistBTag_light_corrDownCon.Clone())

    DYHistBTag_light_corrDown = getBtagUncertHistogram(DYHist, "DYHist_%s_%sDown"%(btagName_light_corr, year_corr), btag_light_corr)
    sigHistBTag_light_corrDown.Add(DYHistBTag_light_corrDown.Clone(), -1)
    sigHistBTag_light_corrDown.Scale(0.5)

    sigHistBTag_light_corrUp = getBtagUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sUp"%(btagName_light_corr, year_corr), btag_light_corr, True)
    sigHistBTag_light_corrUpCon =  getBtagUncertHistogram(sigHistCon,"sigHistCon_%s_%sUp"%(btagName_light_corr, year_corr), btag_light_corr, True)
    sigHistBTag_light_corrUp.Add(sigHistBTag_light_corrUpCon.Clone())

    DYHistBTag_light_corrUp = getBtagUncertHistogram(DYHist, "DYHist_%s_%sUp"%(btagName_light_corr, year_corr), btag_light_corr, True)
    sigHistBTag_light_corrUp.Add(DYHistBTag_light_corrUp.Clone(), -1)
    sigHistBTag_light_corrUp.Scale(0.5)


    ### light uncorr
    sigHistBTag_light_uncorrDown = getBtagUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sDown"%(btagName_light, channel_corr), btag_light_uncorr)
    sigHistBTag_light_uncorrDownCon =  getBtagUncertHistogram(sigHistCon,"sigHistCon_%s_%sDown"%(btagName_light, channel_corr), btag_light_uncorr)
    sigHistBTag_light_uncorrDown.Add(sigHistBTag_light_uncorrDownCon.Clone())

    DYHistBTag_light_uncorrDown = getBtagUncertHistogram(DYHist, "DYHist_%s_%sDown"%(btagName_light, channel_corr), btag_light_uncorr)
    sigHistBTag_light_uncorrDown.Add(DYHistBTag_light_uncorrDown.Clone(), -1)
    sigHistBTag_light_uncorrDown.Scale(0.5)

    sigHistBTag_light_uncorrUp = getBtagUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sUp"%(btagName_light, channel_corr), btag_light_uncorr, True)
    sigHistBTag_light_uncorrUpCon =  getBtagUncertHistogram(sigHistCon,"sigHistCon_%s_%sUp"%(btagName_light, channel_corr), btag_light_uncorr, True)
    sigHistBTag_light_uncorrUp.Add(sigHistBTag_light_uncorrUpCon.Clone())

    DYHistBTag_light_uncorrUp = getBtagUncertHistogram(DYHist, "DYHist_%s_%sUp"%(btagName_light, channel_corr), btag_light_uncorr, True)
    sigHistBTag_light_uncorrUp.Add(DYHistBTag_light_uncorrUp.Clone(), -1)
    sigHistBTag_light_uncorrUp.Scale(0.5)



    ##handling negative systematics
    # Apply max(0, val) to avoid negative bin contents
    # Function to apply max(0, val) to each bin in a histogram
    def apply_max_zero(histogram):
        for bin_idx in range(1, histogram.GetNbinsX() + 1):
            val = histogram.GetBinContent(bin_idx) # Apply max(0, val)
            histogram.SetBinContent(bin_idx, max(0, val))


    if "dimuon" in channel:
        histograms = [sigHist, sigHistIDDown, sigHistIDUp, sigHistISODown, sigHistISOUp, sigHistHLTDown, sigHistHLTUp, sigHistl1prefiringDown, sigHistl1prefiringUp, sigHistSmearDown, sigHistSmearUp, sigHistRecoDown, sigHistRecoUp, sigHistScaleDown, sigHistScaleUp, sigHistPUDown, sigHistPUUp, sigHistPDFDown, sigHistPDFUp, sigHistBTag_bc_corrDown, sigHistBTag_bc_corrUp, sigHistBTag_bc_uncorrDown, sigHistBTag_bc_uncorrUp, sigHistBTag_light_corrDown, sigHistBTag_light_corrUp, sigHistBTag_light_uncorrDown, sigHistBTag_light_uncorrUp ]
    else:
        histograms = [sigHist, sigHistIDDown, sigHistIDUp, sigHistl1prefiringDown, sigHistl1prefiringUp, sigHistSmearDown, sigHistSmearUp, sigHistScaleDown, sigHistScaleUp, sigHistPUDown, sigHistPUUp, sigHistPDFDown, sigHistPDFUp, sigHistBTag_bc_corrDown, sigHistBTag_bc_corrUp, sigHistBTag_bc_uncorrDown, sigHistBTag_bc_uncorrUp, sigHistBTag_light_corrDown, sigHistBTag_light_corrUp, sigHistBTag_light_uncorrDown, sigHistBTag_light_uncorrUp ]

    
    for hist in histograms:
        apply_max_zero(hist)
        if(hist.Integral() ==0):
            hist.SetBinContent(3, 0.00001)



    ##interference histogram
    intHistOrg = getRebinnedHistogram(inputFile.Get(signalName),binning,"intHist_%s"%channel) 
    intHist = intHistOrg.Clone()
    intHist.Add(DYHist.Clone(), -1)
    intHist.Add(bkgHistDY.Clone())

    #print("intHist ", intHist.Integral())
    #print("intHistOrg ", intHistOrg.Integral())

    if "dielectron" in channel:
        intHistIDDown = getHEEPUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sDown"%(IDName,channel_corr), heepUncert)
        intHistIDDown.Add(DYHistIDDown.Clone(), -1)
        intHistIDDown.Add(bkgHistDYIDDown.Clone())

        intHistIDUp = getHEEPUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
        intHistIDUp.Add(DYHistIDUp.Clone(), -1)
        intHistIDUp.Add(bkgHistDYIDUp.Clone())
    else:
        intHistIDDown = getRebinnedHistogram(inputFile.Get("%s_muIDDown"%signalName), binning, "intHist_%s_%sDown"%(IDName,zero_corr))
        intHistIDDown.Add(DYHistIDDown.Clone(), -1)
        intHistIDDown.Add(bkgHistDYIDDown.Clone())

        intHistIDUp  = getRebinnedHistogram(inputFile.Get("%s_muIDUp"%signalName), binning, "intHist_%s_%sUp"%(IDName,zero_corr))
        intHistIDUp.Add(DYHistIDUp.Clone(), -1)
        intHistIDUp.Add(bkgHistDYIDUp.Clone())

        ##muon isolation
        intHistISODown = getRebinnedHistogram(inputFile.Get("%s_muISODown"%signalName), binning, "intHist_%s_%sDown"%(ISOName,zero_corr))
        intHistISODown.Add(DYHistISODown.Clone(), -1)
        intHistISODown.Add(bkgHistDYISODown.Clone())

        intHistISOUp  = getRebinnedHistogram(inputFile.Get("%s_muISOUp"%signalName), binning, "intHist_%s_%sUp"%(ISOName,zero_corr))
        intHistISOUp.Add(DYHistISOUp.Clone(), -1)
        intHistISOUp.Add(bkgHistDYISOUp.Clone())

        ##muon HLT
        intHistHLTDown = getRebinnedHistogram(inputFile.Get("%s_muHLTDown"%signalName), binning, "intHist_%s_%sDown"%(HLTName,zero_corr))       
        intHistHLTDown.Add(DYHistHLTDown.Clone(), -1)
        intHistHLTDown.Add(bkgHistDYHLTDown.Clone())
        
        intHistHLTUp  = getRebinnedHistogram(inputFile.Get("%s_muHLTUp"%signalName), binning, "intHist_%s_%sUp"%(HLTName,zero_corr))
        intHistHLTUp.Add(DYHistHLTUp.Clone(), -1)
        intHistHLTUp.Add(bkgHistDYHLTUp.Clone())
        #print("HLT ",intHistHLTUp.Integral())

    #print("HLT ",intHistHLTUp.Integral())

  
    ##L1 prefiring
    intHistl1prefiringDown = getRebinnedHistogram(inputFile.Get("%s_l1prefiringDown"%signalName), binning, "intHist_%s_%sDown"%(prefiringName,zero_corr))
    intHistl1prefiringDown.Add(DYHistl1prefiringDown.Clone(), -1)
    intHistl1prefiringDown.Add(bkgHistDYl1prefiringDown.Clone())

    intHistl1prefiringUp  = getRebinnedHistogram(inputFile.Get("%s_l1prefiringUp"%signalName), binning, "intHist_%s_%sUp"%(prefiringName,zero_corr))
    intHistl1prefiringUp.Add(DYHistl1prefiringUp.Clone(), -1)
    intHistl1prefiringUp.Add(bkgHistDYl1prefiringUp.Clone())


    ##smearing
    intHistSmearDown = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalName), binning, "intHist_%s_%sDown"%(smearName,zero_corr))
    intHistSmearDown.Add(DYHistSmearDown.Clone(), -1)
    intHistSmearDown.Add(bkgHistDYSmearDown.Clone())

    intHistSmearUp  = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalName), binning, "intHist_%s_%sUp"%(smearName,zero_corr))
    intHistSmearUp.Add(DYHistSmearUp.Clone(), -1)
    intHistSmearUp.Add(bkgHistDYSmearUp.Clone())

    ##muon reco
    if "dimuon" in channel:
        intHistRecoDown = getRebinnedHistogram(inputFile.Get("%s_recodown"%signalName), binning, "intHist_%s_%sDown"%(recoName,zero_corr))
        intHistRecoDown.Add(DYHistRecoDown.Clone(), -1)
        intHistRecoDown.Add(bkgHistDYRecoDown.Clone())
    
        intHistRecoUp  = getRebinnedHistogram(inputFile.Get("%s_recoup"%signalName), binning, "intHist_%s_%sUp"%(recoName,zero_corr))
        intHistRecoUp.Add(DYHistRecoUp.Clone(), -1)
        intHistRecoUp.Add(bkgHistDYRecoUp.Clone())


    ##scale uncertainty
    if "muon" in zero_corr:
        intHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalName), binning, "intHist_%s_%sDown"%(scaleName,zero_corr))
        intHistScaleDown.Add(DYHistScaleDown.Clone(), -1)
        intHistScaleDown.Add(bkgHistDYScaleDown.Clone())

        intHistScaleUp  = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalName), binning, "intHist_%s_%sUp"%(scaleName,zero_corr))
        intHistScaleUp.Add(DYHistScaleUp.Clone(), -1)
        intHistScaleUp.Add(bkgHistDYScaleUp.Clone())

    else:
        intHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalName), binning, "intHist_%s_%sDown"%(eScaleName,zero_corr))
        intHistScaleDown.Add(DYHistScaleDown.Clone(), -1)
        intHistScaleDown.Add(bkgHistDYScaleDown.Clone())

        intHistScaleUp  = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalName), binning, "intHist_%s_%sUp"%(eScaleName,zero_corr))
        intHistScaleUp.Add(DYHistScaleUp.Clone(), -1)
        intHistScaleUp.Add(bkgHistDYScaleUp.Clone())


    ##Pileup
    intHistPUDown = getRebinnedHistogram(inputFile.Get("%s_puDown"%signalName), binning, "intHist_%s_%sDown"%(PUName,channel_corr))
    intHistPUDown.Add(DYHistPUDown.Clone(), -1)
    intHistPUDown.Add(bkgHistDYPUDown.Clone())

    intHistPUUp  = getRebinnedHistogram(inputFile.Get("%s_puUp"%signalName), binning, "intHist_%s_%sUp"%(PUName,channel_corr))
    intHistPUUp.Add(DYHistPUUp.Clone(), -1)
    intHistPUUp.Add(bkgHistDYPUUp.Clone())

    ###PDF
    intHistPDFDown = getPDFUncertHistogram(intHistOrg.Clone(), "intHist_%sDown"%(pdfName), pdfUncert)
    intHistPDFDown.Add(DYHistPDFDown.Clone(), -1)
    intHistPDFDown.Add(bkgHistDYPDFDown.Clone())

    intHistPDFUp = getPDFUncertHistogram(intHistOrg.Clone(), "intHist_%sUp"%(pdfName), pdfUncert, True)
    intHistPDFUp.Add(DYHistPDFUp.Clone(), -1)
    intHistPDFUp.Add(bkgHistDYPDFUp.Clone())

    ##btag bc corr
    intHistBTag_bc_corrDown = getBtagUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sDown"%(btagName_bc_corr, year_corr), btag_bc_corr)
    intHistBTag_bc_corrDown.Add(DYHistBTag_bc_corrDown.Clone(), -1)
    intHistBTag_bc_corrDown.Add(bkgHistDYBTag_bc_corrDown.Clone())

    intHistBTag_bc_corrUp = getBtagUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sUp"%(btagName_bc_corr, year_corr), btag_bc_corr, True)
    intHistBTag_bc_corrUp.Add(DYHistBTag_bc_corrUp.Clone(), -1)
    intHistBTag_bc_corrUp.Add(bkgHistDYBTag_bc_corrUp.Clone())

    ##btag bc uncorr
    intHistBTag_bc_uncorrDown = getBtagUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sDown"%(btagName_bc, channel_corr), btag_bc_uncorr)
    intHistBTag_bc_uncorrDown.Add(DYHistBTag_bc_uncorrDown.Clone(), -1)
    intHistBTag_bc_uncorrDown.Add(bkgHistDYBTag_bc_uncorrDown.Clone())

    intHistBTag_bc_uncorrUp = getBtagUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sUp"%(btagName_bc, channel_corr), btag_bc_uncorr, True)
    intHistBTag_bc_uncorrUp.Add(DYHistBTag_bc_uncorrUp.Clone(), -1)
    intHistBTag_bc_uncorrUp.Add(bkgHistDYBTag_bc_uncorrUp.Clone())

    ##btag light corr
    intHistBTag_light_corrDown = getBtagUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sDown"%(btagName_light_corr, year_corr), btag_light_corr)
    intHistBTag_light_corrDown.Add(DYHistBTag_light_corrDown.Clone(), -1)
    intHistBTag_light_corrDown.Add(bkgHistDYBTag_light_corrDown.Clone())

    intHistBTag_light_corrUp = getBtagUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sUp"%(btagName_light_corr, year_corr), btag_light_corr, True)
    intHistBTag_light_corrUp.Add(DYHistBTag_light_corrUp.Clone(), -1)
    intHistBTag_light_corrUp.Add(bkgHistDYBTag_light_corrUp.Clone())

    ##btag light uncorr
    intHistBTag_light_uncorrDown = getBtagUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sDown"%(btagName_light, channel_corr), btag_light_uncorr)
    intHistBTag_light_uncorrDown.Add(DYHistBTag_light_uncorrDown.Clone(), -1)
    intHistBTag_light_uncorrDown.Add(bkgHistDYBTag_light_uncorrDown.Clone())

    intHistBTag_light_uncorrUp = getBtagUncertHistogram(intHistOrg.Clone(), "intHist_%s_%sUp"%(btagName_light, channel_corr), btag_light_uncorr, True)
    intHistBTag_light_uncorrUp.Add(DYHistBTag_light_uncorrUp.Clone(), -1)
    intHistBTag_light_uncorrUp.Add(bkgHistDYBTag_light_uncorrUp.Clone())



    if "dimuon" in channel:
        histograms_int = [intHist, intHistIDDown, intHistIDUp, intHistISODown, intHistISOUp, intHistHLTDown, intHistHLTUp, intHistl1prefiringDown, intHistl1prefiringUp, intHistSmearDown, intHistSmearUp, intHistRecoDown, intHistRecoUp, intHistScaleDown, intHistScaleUp, intHistPUDown, intHistPUUp, intHistPDFDown, intHistPDFUp, intHistBTag_bc_corrDown, intHistBTag_bc_corrUp, intHistBTag_bc_uncorrDown, intHistBTag_bc_uncorrUp, intHistBTag_light_corrDown, intHistBTag_light_corrUp, intHistBTag_light_uncorrDown, intHistBTag_light_uncorrUp ]
    else:
        histograms_int = [intHist, intHistIDDown, intHistIDUp, intHistl1prefiringDown, intHistl1prefiringUp, intHistSmearDown, intHistSmearUp, intHistScaleDown, intHistScaleUp, intHistPUDown, intHistPUUp, intHistPDFDown, intHistPDFUp, intHistBTag_bc_corrDown, intHistBTag_bc_corrUp, intHistBTag_bc_uncorrDown, intHistBTag_bc_uncorrUp, intHistBTag_light_corrDown, intHistBTag_light_corrUp, intHistBTag_light_uncorrDown, intHistBTag_light_uncorrUp ]


    for hist in histograms_int:
        apply_max_zero(hist)




    ##Jet background
    print("now rebinning fake")
    if "muon" in channel:
        bkgHistJets = getRebinnedHistogram(fake_file.Get("mu_data_obs"), binning, "bkgHistJets_%s"%channel)
    else:
        bkgHistJets = getRebinnedHistogram(fake_file.Get("data_obs"), binning, "bkgHistJets_%s"%channel)

    if "muon" in channel:
        dataHist = getRebinnedHistogram(inputFile.Get("mu_data_obs"), binning, "dataHist_%s"%channel)
    else: # electron
        dataHist = getRebinnedHistogram(inputFile.Get("data_obs"), binning, "dataHist_%s"%channel)




    intIntegral = intHist.Integral()
    bkgIntegralDY = bkgHistDY.Integral()
    bkgIntegralTop = bkgHistTop.Integral()
    bkgIntegralDiboson = bkgHistDiboson.Integral()
    bkgIntegralJets = bkgHistJets.Integral()
    sigIntegral = sigHist.Integral()

    histFile.Write()
    histFile.Close()


    return [bkgIntegralDY,bkgIntegralTop, bkgIntegralDiboson,bkgIntegralJets,sigIntegral,intIntegral]






def createSingleBinCI(L,interference,name,channel,scanConfigName,mThresh,dataFile=""):
    ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

    mThresh = float(mThresh)

    #configName ="channelConfig_%s"%channel
    #config =  __import__(configName)

    binning = [1000, 6000]

            
#    binning = [ 200,  250,  300,  350,  400,  450,  500,  550,  600,  650,  700,
#        750,  800,  850,  900,  950, 1000, 1050, 1100, 1150, 1200, 1250,
#       1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800,
#       1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250, 2300, 2350,
#       2400, 2450, 2500, 2550, 2600, 2650, 2700, 2750, 2800, 2850, 2900,
#       2950, 3000, 3050, 3100, 3150, 3200, 3250, 3300, 3350, 3400, 3450,
#       3500, 3550, 3600, 3650, 3700, 3750, 3800, 3850, 3900, 3950, 4000,
#       4050, 4100, 4150, 4200, 4250, 4300, 4350, 4400, 4450, 4500, 4550,
#       4600, 4650, 4700, 4750, 4800, 4850, 4900, 4950, 5000, 5050, 5100,
#       5150, 5200, 5250, 5300, 5350, 5400, 5450, 5500, 5550, 5600, 5650,
#       5700, 5750, 5800, 5850, 5900, 5950, 6000]
#    binning = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200,1300,1400, 1500, 1600, 1700, 1800, 1900, 3500]
    
    scanConfigName ="scanConfiguration_%s"%scanConfigName
    scanConfig =  __import__(scanConfigName)

    
    result = {}	
    
    from array import array

    # print("inputFiles[channel]: {0}".format(inputFiles[channel]))

    if "dielectron" in channel:
        inputFile = ROOT.TFile("/depot/cms/private/users/kaur214/output/elec_channel_2018_newSep_jan2024_trig_eff/dnn/stage3_templates/dielectron_mass/"+inputFiles[channel], "OPEN")
        fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/ee/preapproval/fake_"+inputFiles[channel], "OPEN")


    else: # dimuon
        inputFile = ROOT.TFile("/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage3_templates/dimuon_mass/"+inputFiles[channel], "OPEN")
        fake_file = ROOT.TFile("/depot/cms/users/kaur214/ForLimits/mumu/preapproval/fake_"+inputFiles[channel], "OPEN")


    btag_bc_corr = [0.03, 0.03]
    btag_bc_uncorr = [0.03, 0.03]
    btag_light_uncorr = [0.0356554, 0.0356554]
    btag_light_corr = [0.0363449, 0.0363449 ]
    #btag_bc_corr =  np.full(116, 0.03)
    #btag_bc_uncorr = np.full(116, 0.03) 
    #btag_light_uncorr = np.full(116, 0.036) 
    #btag_light_corr = np.full(116, 0.036) 


    pdfUncert =   [ 0.00518313, 0.0123567]
    pdfUncertDY = [0.02804822616, 0.04746036643]
    pdfUncertTT = [0.05196009012, 0.2532719835]
    pdfUncertVV = [0.1324849835, 0.1361711683]

    heepUncert = [0.037, 0.037]

    if ("OneB" in channel) or ("TwoB" in channel):
        if "BB" in channel:
              ttbar_uncert = [ 0.206764, 0.206764]
        else:
              ttbar_uncert = [ 0.300831, 0.497486]




    ##PDF Uncertainty original
    #pdfUncert = [0.0007175333999999999, 0.0008748659000000002, 0.0010321984000000001, 0.0011895309, 0.0013468634, 0.0015041959, 0.0016615284000000001, 0.0018188609000000001, 0.0019761934000000004, 0.0021335259, 0.0022908584, 0.0024481909, 0.0026055234, 0.0027628559, 0.0029201884, 0.0030775209, 0.0032348534000000003, 0.0033921859, 0.0035495184000000003, 0.0037068509, 0.0038641834000000003, 0.0040215159000000006, 0.004178848400000001, 0.004336180900000001, 0.0044935134, 0.0046508459000000005, 0.004808178400000001, 0.004965510900000001, 0.0051228434, 0.0052801759000000005, 0.005437508400000001, 0.005594840900000001, 0.0057521734, 0.0059095059000000005, 0.006066838400000001, 0.006224170900000001, 0.006381503400000001, 0.0065388359000000005, 0.006696168400000001, 0.006853500900000001, 0.007010833400000001, 0.0071681659000000005, 0.007325498400000001, 0.007482830900000001, 0.007640163400000001, 0.0077974959000000005, 0.0079548284, 0.0081121609, 0.008269493400000001, 0.0084268259, 0.008584158400000002, 0.008741490900000001, 0.0088988234, 0.009056155900000001, 0.0092134884, 0.0093708209, 0.009528153400000001, 0.0096854859, 0.009842818400000002, 0.010000150900000001, 0.0101574834, 0.010314815900000001, 0.0104721484, 0.010629480900000002, 0.010786813400000001, 0.0109441459, 0.011101478400000002, 0.011258810900000001, 0.0114161434, 0.011573475900000001, 0.0117308084, 0.011888140900000002, 0.012045473400000001, 0.0122028059, 0.012360138400000002, 0.012517470900000001, 0.012674803400000002, 0.012832135900000001, 0.0129894684, 0.013146800900000002, 0.013304133400000001, 0.0134614659, 0.013618798400000002, 0.013776130900000001, 0.013933463400000002, 0.014090795900000001, 0.0142481284, 0.014405460900000002, 0.014562793400000001, 0.0147201259, 0.014877458400000002, 0.015034790900000001, 0.015192123400000002, 0.015349455900000001, 0.0155067884, 0.015664120900000002, 0.0158214534, 0.0159787859, 0.0161361184, 0.016293450900000003, 0.016450783400000002, 0.0166081159, 0.0167654484, 0.0169227809, 0.017080113400000003, 0.017237445900000002, 0.0173947784, 0.0175521109, 0.0177094434, 0.017866775900000003, 0.018024108400000002, 0.0181814409, 0.0183387734, 0.0184961059, 0.0186534384, 0.018810770900000003, 0.018968103400000002] 

    #pdfUncertDY = [0.012331253984000146, 0.01301510309999987, 0.013699366464000162, 0.014384044076000135, 0.015069135936000011, 0.01575464204400001, 0.016440562400000136, 0.017126897004000163, 0.017813645856000093, 0.018500808955999926, 0.019188386304000105, 0.019876377899999964, 0.020564783743999948, 0.021253603836000057, 0.021942838176000068, 0.02263248676399998, 0.02332254960000002, 0.024013026684000183, 0.024703918016000026, 0.025395223595999994, 0.026086943423999864, 0.02677907750000008, 0.02747162582399998, 0.028164588396, 0.028857965215999926, 0.029551756284000197, 0.03024596160000015, 0.030940581164000003, 0.031635614976000204, 0.032331063036000085, 0.03302692534400009, 0.0337232019, 0.03441989270400003, 0.03511699775599997, 0.03581451705600003, 0.03651245060399999, 0.03721079840000008, 0.03790956044400007, 0.03860873673599996, 0.03930832727599998, 0.04000833206400012, 0.04070875109999994, 0.04140958438399989, 0.04211083191600018, 0.04281249369600015, 0.04351456972400003, 0.04421706000000003, 0.044919964524000155, 0.04562328329599996, 0.046327016316000114, 0.047031163583999946, 0.047735725100000126, 0.048440700863999986, 0.04914609087599997, 0.04985189513600008, 0.05055811364400009, 0.051264746400000005, 0.051971793404000044, 0.05267925465600021, 0.05338713015600005, 0.05409541990400002, 0.05480412389999989, 0.05551324214400011, 0.056222774636000006, 0.05693272137600003, 0.05764308236399995, 0.0583538576, 0.059065047083999955, 0.05977665081600003, 0.06048866879600023, 0.061201101024000115, 0.06191394750000012, 0.06262720822400003, 0.06334088319600006, 0.064054972416, 0.06476947588400006, 0.06548439360000002, 0.06619972556400011, 0.0669154717760001, 0.067631632236, 0.06834820694400001, 0.06906519590000015, 0.06978259910399998, 0.07050041655599992, 0.07121864825600022, 0.07193729420400019, 0.07265635440000007, 0.07337582884400007, 0.0740957175360002, 0.074816020476, 0.07553673766399993, 0.07625786909999999, 0.07697941478400017, 0.07770137471600003, 0.07842374889600001, 0.07914653732400012, 0.07986974000000013, 0.08059335692400005, 0.08131738809600009, 0.08204183351600025, 0.0827666931840001, 0.08349196710000006, 0.08421765526399994, 0.08494375767600015, 0.08567027433600005, 0.08639720524400007, 0.0871245504, 0.08785230980400005, 0.088580483456, 0.08930907135600008, 0.09003807350400006, 0.09076748990000016, 0.09149732054399995, 0.09222756543600008, 0.09295822457600011, 0.09368929796400005, 0.09442078560000011]
 
    #pdfUncertTT = [0.01755119455999976, 0.0173639523437501, 0.017839332459999913, 0.0188724671037499, 0.02036495296000007, 0.02222485120374973, 0.02436668749999993, 0.026711452003750136, 0.02918659936000001, 0.03172604870374984, 0.03427018366000012, 0.03676585234374996, 0.03916636736000001, 0.04143150580374977, 0.04352750926000004, 0.045427083803749824, 0.04710939999999986, 0.04856009290374996, 0.04977126205999993, 0.05074147150374997, 0.0514757497599998, 0.05198558984375001, 0.05228894925999983, 0.05241025000374999, 0.052380378559999885, 0.05223668590374997, 0.052022987500000006, 0.05178956330374995, 0.05159315775999973, 0.051496979803749676, 0.05157070285999987, 0.05189046484374993, 0.052538868160000085, 0.05360497970374989, 0.05518433085999974, 0.05737891750374979, 0.06029719999999994, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835, 0.2532719835] 

    #pdfUncertVV = [0.0015220279999998976, 0.0066835437499999095, 0.011757463000000135, 0.016743785749999907, 0.02164251199999989, 0.026453641749999868, 0.031177175000000057, 0.035813111750000015, 0.040361451999999964, 0.044822195749999905, 0.04919534300000006, 0.05348089374999998, 0.057678847999999894, 0.0617892057499998, 0.06581196700000014, 0.06974713175000002, 0.0735946999999999, 0.07735467174999999, 0.08102704700000007, 0.08461182574999992, 0.08810900799999999, 0.09151859375000004, 0.09484058300000009, 0.0980749757499999, 0.10122177199999993, 0.10428097174999995, 0.10725257499999996, 0.11013658174999996, 0.11293299199999995, 0.11564180574999994, 0.11826302299999991, 0.12079664374999988, 0.12324266800000006, 0.12560109575, 0.12787192699999994, 0.13005516174999987, 0.1321507999999998, 0.13415884174999992, 0.13607928700000005, 0.13791213574999994, 0.13965738800000005, 0.14131504374999992, 0.142885103, 0.14436756574999987, 0.14576243200000016, 0.14706970175, 0.14828937499999983, 0.1494214517500001, 0.15046593200000014, 0.15142281574999994, 0.15229210299999996, 0.15307379374999996, 0.15376788799999996, 0.15437438574999995, 0.15489328699999994, 0.15532459175000013, 0.1556683000000001, 0.15592441175000005, 0.156092927, 0.15617384574999993, 0.15616716800000008, 0.15607289375, 0.1558910229999999, 0.15562155575000003, 0.15526449199999992, 0.15481983175000003, 0.1542875749999999, 0.15366772174999999, 0.15296027200000006, 0.1521652257499999, 0.15128258299999997, 0.15031234375000002, 0.14925450799999984, 0.14810907574999987, 0.1468760469999999, 0.14555542175000014, 0.14414719999999992, 0.14265138174999992, 0.14106796700000013, 0.1393969557500001, 0.13763834799999985, 0.13579214374999982, 0.133858343, 0.13183694574999993, 0.12972795199999987, 0.12753136175000002, 0.12524717500000015, 0.12287539175000006, 0.12041601199999996, 0.11786903574999985, 0.11523446299999973, 0.11251229375000005, 0.10970252800000013, 0.10680516574999999, 0.10382020700000005, 0.10074765174999989, 0.09758749999999994, 0.09433975174999976, 0.09100440700000001, 0.08758146575000003, 0.08407092800000004, 0.08047279375000005, 0.07678706300000004, 0.07301373575000003, 0.06915281200000001, 0.06520429174999975, 0.061168174999999936, 0.057044461749999886, 0.05283315200000005, 0.04853424574999998, 0.044147742999999906, 0.03967364375000004, 0.03511194799999995, 0.030462655750000067, 0.025725766999999955, 0.020901281750000056, 0.015989199999999926]  


    #heepUncert =  [0.0122, 0.0133, 0.0144, 0.0156, 0.0167, 0.0178, 0.0189, 0.02, 0.0211, 0.0222, 0.0233, 0.0244, 0.0256, 0.0267, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374, 0.0374] 

    if "dielectron" in channel:
       IDName = "ID"
       pdfName = "pdf_dielectron"
    else:
       IDName = "ID"
       pdfName = "pdf_dilepton"

    ttbarUncertName = "ttbarUncert"
    scaleName = "massScale"
    eScaleName = "energyScale"
    smearName = "res"
    #pdfName = "pdf_dilepton"
    #IDName = "ID"
    ISOName = "ISO"
    HLTName = "HLT"
    PUName = "PU"
    # btagName = "btag"
    prefiringName = "l1prefiring"
    btagName_bc = "btagSF_bc"
    btagName_light = "btagSF_light"
    btagName_bc_corr = "btagSF_bc_corr"
    btagName_light_corr = "btagSF_light_corr"
    recoName = "reco"

    print("------------------------------------------------")
    print("inputFile: {0}".format(inputFile.Get("DYJets")))

    # bkg DY
    bkgHistDY = getRebinnedHistogram(inputFile.Get("DYJets"),binning,"bkgHistDY_%s"%channel)

    # setup the name of btag to be consistent with our correlation nomenclature
    if "dielectron" in channel:
       year_corr = "dielectron"
       if "2018" in channel:
           channel_corr = "dielectron18"
       elif "2017" in channel:
           channel_corr = "dielectron17"
       elif "2016" in channel:
           if "post" in channel:
               channel_corr = "dielectron16_post"
           else:
               channel_corr = "dielectron16_pre"
       else:
           print("invalid channel configuration")
    else:
       year_corr = "dilepton"
       if "2018" in channel:
           channel_corr = "dilepton18"
       elif "2017" in channel:
           channel_corr = "dilepton17"
       elif "2016" in channel:
           if "post" in channel:
               channel_corr = "dilepton16_post"
           else:
               channel_corr = "dilepton16_pre"
       else:
           print("invalid channel configuration")
           raise ValueError

    if "BB" in channel:
        zero_corr = channel.replace('BB_',"")
        # print "zero_corr: {0}".format(zero_corr)
    else:
        zero_corr = channel.replace('BE_',"")

    if "dielectron" in channel:
            bkgHistDYIDDown = getHEEPUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sDown"%(IDName,channel_corr), heepUncert)
            bkgHistDYIDUp =   getHEEPUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
            bkgHistDYIDDown = getRebinnedHistogram(inputFile.Get("DYJets_muIDDown"), binning, "bkgHistDY_%s_%sDown"%(IDName,zero_corr))
            bkgHistDYIDUp = getRebinnedHistogram(inputFile.Get("DYJets_muIDUp"), binning, "bkgHistDY_%s_%sUp"%(IDName,zero_corr))

            bkgHistDYISODown = getRebinnedHistogram(inputFile.Get("DYJets_muISODown"), binning, "bkgHistDY_%s_%sDown"%(ISOName,zero_corr))
            bkgHistDYISOUp = getRebinnedHistogram(inputFile.Get("DYJets_muISOUp"), binning, "bkgHistDY_%s_%sUp"%(ISOName,zero_corr))

            bkgHistDYHLTDown = getRebinnedHistogram(inputFile.Get("DYJets_muHLTDown"), binning, "bkgHistDY_%s_%sDown"%(HLTName,zero_corr))
            bkgHistDYHLTUp = getRebinnedHistogram(inputFile.Get("DYJets_muHLTUp"), binning, "bkgHistDY_%s_%sUp"%(HLTName,zero_corr))


    bkgHistDYl1prefiringUp = getRebinnedHistogram(inputFile.Get("DYJets_l1prefiringUp"), binning, "bkgHistDY_%s_%sUp"%(prefiringName,zero_corr))
    bkgHistDYl1prefiringDown = getRebinnedHistogram(inputFile.Get("DYJets_l1prefiringDown"), binning, "bkgHistDY_%s_%sDown"%(prefiringName,zero_corr))




    bkgHistDYSmearUp = getRebinnedHistogram(inputFile.Get("DYJets_resUnc"), binning, "bkgHistDY_%s_%sUp"%(smearName,zero_corr))
    bkgHistDYSmearDown = getRebinnedHistogram(inputFile.Get("DYJets_resUnc"), binning, "bkgHistDY_%s_%sDown"%(smearName,zero_corr))

    if "ZeroB" in channel:
        bkgHistDYBTag_bc_corrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
        bkgHistDYBTag_bc_corrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
        bkgHistDYBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
        bkgHistDYBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
        bkgHistDYBTag_light_corrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
        bkgHistDYBTag_light_corrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
        bkgHistDYBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
        bkgHistDYBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistDY, "bkgHistDY_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    else:
        bkgHistDYBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_bc_corr,year_corr))
        bkgHistDYBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_bc_corr,year_corr))
        bkgHistDYBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_bc,channel_corr))
        bkgHistDYBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_bc,channel_corr))
        bkgHistDYBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_light_corr,year_corr))
        bkgHistDYBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_light_corr,year_corr))
        bkgHistDYBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sUp"%(btagName_light,channel_corr))
        bkgHistDYBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"DYJets"), binning, "bkgHistDY_%s_%sDown"%(btagName_light,channel_corr))
    if "dimuon" in channel:
        bkgHistDYRecoUp = getRebinnedHistogram(inputFile.Get("DYJets_recoup"), binning, "bkgHistDY_%s_%sUp"%(recoName,zero_corr))

        bkgHistDYRecoDown = getRebinnedHistogram(inputFile.Get("DYJets_recodown"), binning, "bkgHistDY_%s_%sDown"%(recoName,zero_corr))
    bkgHistDYPUUp = getRebinnedHistogram(inputFile.Get("DYJets_puUp"), binning, "bkgHistDY_%s_%sUp"%(PUName,channel_corr))
    bkgHistDYPUDown = getRebinnedHistogram(inputFile.Get("DYJets_puDown"), binning, "bkgHistDY_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        bkgHistDYScaleDown = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncDown"),binning,"bkgHistDY_%s_%sDown"%(scaleName,zero_corr))
        bkgHistDYScaleUp = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncUp"),binning,"bkgHistDY_%s_%sUp"%(scaleName,zero_corr))
    else:
        bkgHistDYScaleDown = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncDown"),binning,"bkgHistDY_%s_%sDown"%(eScaleName,zero_corr))
        bkgHistDYScaleUp = getRebinnedHistogram(inputFile.Get("DYJets_scaleUncUp"),binning,"bkgHistDY_%s_%sUp"%(eScaleName,zero_corr))


    bkgHistDYPDFDown = getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sDown"%(pdfName), pdfUncertDY)
    bkgHistDYPDFUp =   getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sUp"%(pdfName),   pdfUncertDY,True)

    # bkg Top
    bkgHistTop = getRebinnedHistogram(inputFile.Get("Top"),binning,"bkgHistTop_%s"%channel)

    if "dielectron" in channel:
        bkgHistTopIDDown = getHEEPUncertHistogram(bkgHistTop,"bkgHistTop_%s_%sDown"%(IDName,channel_corr), heepUncert)
        bkgHistTopIDUp =   getHEEPUncertHistogram(bkgHistTop,"bkgHistTop_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
        bkgHistTopIDDown = getRebinnedHistogram(inputFile.Get("Top_muIDDown"), binning, "bkgHistTop_%s_%sDown"%(IDName,zero_corr))
        bkgHistTopIDUp = getRebinnedHistogram(inputFile.Get("Top_muIDUp"), binning, "bkgHistTop_%s_%sUp"%(IDName,zero_corr))

        bkgHistTopISODown = getRebinnedHistogram(inputFile.Get("Top_muISODown"), binning, "bkgHistTop_%s_%sDown"%(ISOName,zero_corr))
        bkgHistTopISOUp = getRebinnedHistogram(inputFile.Get("Top_muISOUp"), binning, "bkgHistTop_%s_%sUp"%(ISOName,zero_corr))

        bkgHistTopHLTDown = getRebinnedHistogram(inputFile.Get("Top_muHLTDown"), binning, "bkgHistTop_%s_%sDown"%(HLTName,zero_corr))
        bkgHistTopHLTUp = getRebinnedHistogram(inputFile.Get("Top_muHLTUp"), binning, "bkgHistTop_%s_%sUp"%(HLTName,zero_corr))

    bkgHistTopl1prefiringUp = getRebinnedHistogram(inputFile.Get("Top_l1prefiringUp"), binning, "bkgHistTop_%s_%sUp"%(prefiringName,zero_corr))
    bkgHistTopl1prefiringDown = getRebinnedHistogram(inputFile.Get("Top_l1prefiringDown"), binning, "bkgHistTop_%s_%sDown"%(prefiringName,zero_corr))

    bkgHistTopSmearUp = getRebinnedHistogram(inputFile.Get("Top_resUnc"), binning, "bkgHistTop_%s_%sUp"%(smearName,zero_corr))
    bkgHistTopSmearDown = getRebinnedHistogram(inputFile.Get("Top_resUnc"), binning, "bkgHistTop_%s_%sDown"%(smearName,zero_corr))


    if "ZeroB" in channel:
        bkgHistTopBTag_bc_corrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
        bkgHistTopBTag_bc_corrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)

        bkgHistTopBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)

        bkgHistTopBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)

        bkgHistTopBTag_light_corrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
        bkgHistTopBTag_light_corrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)

        bkgHistTopBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)

        bkgHistTopBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    else:
        #bkgHistTopBTagUp = getRebinnedHistogram(inputFile.Get("Top_btagUp"), binning, "bkgHistTop_%s_%sUp"%(btagName,channel_corr))
        #bkgHistTopBTagDown = getRebinnedHistogram(inputFile.Get("Top_btagDown"), binning, "bkgHistTop_%s_%sDown"%(btagName,channel_corr))
        bkgHistTopBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_bc_corr,year_corr))
        bkgHistTopBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_bc_corr,year_corr))
        bkgHistTopBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_bc,channel_corr))
        bkgHistTopBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_bc,channel_corr))
        bkgHistTopBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_light_corr,year_corr))
        bkgHistTopBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_light_corr,year_corr))

        bkgHistTopBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sUp"%(btagName_light,channel_corr))
        bkgHistTopBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"Top"), binning, "bkgHistTop_%s_%sDown"%(btagName_light,channel_corr))


    if "dimuon" in channel:
        bkgHistTopRecoUp = getRebinnedHistogram(inputFile.Get("Top_recoup"), binning, "bkgHistTop_%s_%sUp"%(recoName,zero_corr))
        bkgHistTopRecoDown = getRebinnedHistogram(inputFile.Get("Top_recodown"), binning, "bkgHistTop_%s_%sDown"%(recoName,zero_corr))
    bkgHistTopPUUp = getRebinnedHistogram(inputFile.Get("Top_puUp"), binning, "bkgHistTop_%s_%sUp"%(PUName,channel_corr))
    bkgHistTopPUDown = getRebinnedHistogram(inputFile.Get("Top_puDown"), binning, "bkgHistTop_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        bkgHistTopScaleDown = getRebinnedHistogram(inputFile.Get("Top_scaleUncDown"),binning,"bkgHistTop_%s_%sDown"%(scaleName,zero_corr))
        bkgHistTopScaleUp = getRebinnedHistogram(inputFile.Get("Top_scaleUncUp"),binning,"bkgHistTop_%s_%sUp"%(scaleName,zero_corr))

    else:
        bkgHistTopScaleDown = getRebinnedHistogram(inputFile.Get("Top_scaleUncDown"),binning,"bkgHistTop_%s_%sDown"%(eScaleName,zero_corr))
        bkgHistTopScaleUp = getRebinnedHistogram(inputFile.Get("Top_scaleUncUp"),binning,"bkgHistTop_%s_%sUp"%(eScaleName,zero_corr))


    bkgHistTopPDFDown = getPDFUncertHistogram(bkgHistTop,"bkgHistTop_%sDown"%(pdfName), pdfUncertTT)
    bkgHistTopPDFUp =   getPDFUncertHistogram(bkgHistTop,"bkgHistTop_%sUp"%(pdfName),   pdfUncertTT,True)

    if ("OneB" in channel) or ("TwoB" in channel):
        bkgHistTopttbarUncertDown = getPDFUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sDown"%(ttbarUncertName, zero_corr), ttbar_uncert)
        bkgHistTopttbarUncertUp   = getPDFUncertHistogram(bkgHistTop, "bkgHistTop_%s_%sUp"%(ttbarUncertName, zero_corr), ttbar_uncert, True)


    # bkg Diboson
    bkgHistDiboson = getRebinnedHistogram(inputFile.Get("Diboson"),binning,"bkgHistDiboson_%s"%channel)

    if "dielectron" in channel:
            bkgHistDibosonIDDown = getHEEPUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%s_%sDown"%(IDName,channel_corr), heepUncert)
            bkgHistDibosonIDUp =   getHEEPUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
    else:
            bkgHistDibosonIDDown = getRebinnedHistogram(inputFile.Get("Diboson_muIDDown"), binning, "bkgHistDiboson_%s_%sDown"%(IDName,zero_corr))
            bkgHistDibosonIDUp = getRebinnedHistogram(inputFile.Get("Diboson_muIDUp"), binning, "bkgHistDiboson_%s_%sUp"%(IDName,zero_corr))

            bkgHistDibosonISODown = getRebinnedHistogram(inputFile.Get("Diboson_muISODown"), binning, "bkgHistDiboson_%s_%sDown"%(ISOName,zero_corr))
            bkgHistDibosonISOUp = getRebinnedHistogram(inputFile.Get("Diboson_muISOUp"), binning, "bkgHistDiboson_%s_%sUp"%(ISOName,zero_corr))

            bkgHistDibosonHLTDown = getRebinnedHistogram(inputFile.Get("Diboson_muHLTDown"), binning, "bkgHistDiboson_%s_%sDown"%(HLTName,zero_corr))
            bkgHistDibosonHLTUp = getRebinnedHistogram(inputFile.Get("Diboson_muHLTUp"), binning, "bkgHistDiboson_%s_%sUp"%(HLTName,zero_corr))

    bkgHistDibosonl1prefiringUp = getRebinnedHistogram(inputFile.Get("Diboson_l1prefiringUp"), binning, "bkgHistDiboson_%s_%sUp"%(prefiringName,zero_corr))
    bkgHistDibosonl1prefiringDown = getRebinnedHistogram(inputFile.Get("Diboson_l1prefiringDown"), binning, "bkgHistDiboson_%s_%sDown"%(prefiringName,zero_corr))


    bkgHistDibosonSmearUp = getRebinnedHistogram(inputFile.Get("Diboson_resUnc"), binning, "bkgHistDiboson_%s_%sUp"%(smearName,zero_corr))
    bkgHistDibosonSmearDown = getRebinnedHistogram(inputFile.Get("Diboson_resUnc"), binning, "bkgHistDiboson_%s_%sDown"%(smearName,zero_corr))

    if "dimuon" in channel:
        bkgHistDibosonRecoUp = getRebinnedHistogram(inputFile.Get("Diboson_recoup"), binning, "bkgHistDiboson_%s_%sUp"%(recoName,zero_corr))
        bkgHistDibosonRecoDown = getRebinnedHistogram(inputFile.Get("Diboson_recodown"), binning, "bkgHistDiboson_%s_%sDown"%(recoName,zero_corr))
    bkgHistDibosonPUUp = getRebinnedHistogram(inputFile.Get("Diboson_puUp"), binning, "bkgHistDiboson_%s_%sUp"%(PUName,channel_corr))
    bkgHistDibosonPUDown = getRebinnedHistogram(inputFile.Get("Diboson_puDown"), binning, "bkgHistDiboson_%s_%sDown"%(PUName,channel_corr))
    if "muon" in zero_corr:
        bkgHistDibosonScaleDown = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncDown"),binning,"bkgHistDiboson_%s_%sDown"%(scaleName,zero_corr))
        bkgHistDibosonScaleUp = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncUp"),binning,"bkgHistDiboson_%s_%sUp"%(scaleName,zero_corr))
    else:
        bkgHistDibosonScaleDown = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncDown"),binning,"bkgHistDiboson_%s_%sDown"%(eScaleName,zero_corr))
        bkgHistDibosonScaleUp = getRebinnedHistogram(inputFile.Get("Diboson_scaleUncUp"),binning,"bkgHistDiboson_%s_%sUp"%(eScaleName,zero_corr))


    bkgHistDibosonPDFDown = getPDFUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%sDown"%(pdfName), pdfUncertVV)
    bkgHistDibosonPDFUp =   getPDFUncertHistogram(bkgHistDiboson,"bkgHistDiboson_%sUp"%(pdfName),   pdfUncertVV,True)


    if "ZeroB" in channel:
        bkgHistDibosonBTag_bc_corrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
        bkgHistDibosonBTag_bc_corrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
        bkgHistDibosonBTag_bc_uncorrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
        bkgHistDibosonBTag_bc_uncorrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
        bkgHistDibosonBTag_light_corrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
        bkgHistDibosonBTag_light_corrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
        bkgHistDibosonBTag_light_uncorrUp = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
        bkgHistDibosonBTag_light_uncorrDown = getBtagUncertHistogram(bkgHistDiboson, "bkgHistDiboson_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    else:
        bkgHistDibosonBTag_bc_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_bc_corr,year_corr))
        bkgHistDibosonBTag_bc_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_bc_corr,year_corr))
        bkgHistDibosonBTag_bc_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_bcUp_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_bc,channel_corr))
        bkgHistDibosonBTag_bc_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_bcDown_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_bc,channel_corr))
        bkgHistDibosonBTag_light_corrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_light_corr,year_corr))
        bkgHistDibosonBTag_light_corrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_correlated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_light_corr,year_corr))
        bkgHistDibosonBTag_light_uncorrUp = getRebinnedHistogram(inputFile.Get("%s_btag_lightUp_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sUp"%(btagName_light,channel_corr))
        bkgHistDibosonBTag_light_uncorrDown = getRebinnedHistogram(inputFile.Get("%s_btag_lightDown_uncorrelated"%"Diboson"), binning, "bkgHistDiboson_%s_%sDown"%(btagName_light,channel_corr))

    #signalName = "bbll_lambda6TeV_posLL"
    #signalName = "bsll_lambda%sTeV"%L


    signalName = "bbll_lambda%sTeV_%s"%(L,interference)
    DYName     = "bbll_100000TeV_negLL"

    print("signalName: {0}".format(signalName))

    # signal
    #sigHist = getRebinnedHistogram(inputFile.Get(signalName),binning,"sigHist_%s"%channel)

    sigHistOrg = getRebinnedHistogram(inputFile.Get(signalName),binning,"sigHist_%s"%channel)

    sigHist = sigHistOrg.Clone()

    DYHistOrg = getRebinnedHistogram(inputFile.Get(DYName), binning,"DYHist_%s"%channel)
    DYHist = DYHistOrg.Clone()

    sigHist.Add(DYHist.Clone(), -1)


    if "dielectron" in channel:
            sigHistIDDown = getHEEPUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sDown"%(IDName,channel_corr), heepUncert)
            DYHistIDDown = getHEEPUncertHistogram(DYHistOrg.Clone(), "DYHist_%s_%sDown"%(IDName,channel_corr), heepUncert)
            sigHistIDDown.Add(DYHistIDDown.Clone(), -1)


            sigHistIDUp =   getHEEPUncertHistogram(sigHistOrg.Clone(),"sigHist_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
            DYHistIDUp = getHEEPUncertHistogram(DYHistOrg.Clone(), "DYHist_%s_%sUp"%(IDName,channel_corr), heepUncert, True)
            sigHistIDUp.Add(DYHistIDUp.Clone(), -1)


    else:
            sigHistIDDown = getRebinnedHistogram(inputFile.Get("%s_muIDDown"%signalName), binning, "sigHist_%s_%sDown"%(IDName,zero_corr))
            DYHistIDDown = getRebinnedHistogram(inputFile.Get("%s_muIDDown"%DYName), binning,"DYHist_%s_%sDown"%(IDName,zero_corr))
            sigHistIDDown.Add(DYHistIDDown.Clone(), -1)
            
            sigHistIDUp = getRebinnedHistogram(inputFile.Get("%s_muIDUp"%signalName), binning, "sigHist_%s_%sUp"%(IDName,zero_corr))
            DYHistIDUp = getRebinnedHistogram(inputFile.Get("%s_muIDUp"%DYName), binning,"DYHist_%s_%sUp"%(IDName,zero_corr))
            sigHistIDUp.Add(DYHistIDUp.Clone(), -1)


            sigHistISODown = getRebinnedHistogram(inputFile.Get("%s_muISODown"%signalName), binning, "sigHist_%s_%sDown"%(ISOName,zero_corr))
            DYHistISODown = getRebinnedHistogram(inputFile.Get("%s_muISODown"%DYName), binning,"DYHist_%s_%sDown"%(ISOName,zero_corr))
            sigHistISODown.Add(DYHistISODown.Clone(), -1)

            sigHistISOUp = getRebinnedHistogram(inputFile.Get("%s_muISOUp"%signalName), binning, "sigHist_%s_%sUp"%(ISOName,zero_corr))
            DYHistISOUp = getRebinnedHistogram(inputFile.Get("%s_muISOUp"%DYName), binning,"DYHist_%s_%sUp"%(ISOName,zero_corr))
            sigHistISOUp.Add(DYHistISOUp.Clone(), -1)

            sigHistHLTDown = getRebinnedHistogram(inputFile.Get("%s_muHLTDown"%signalName), binning, "sigHist_%s_%sDown"%(HLTName,zero_corr))
            DYHistHLTDown = getRebinnedHistogram(inputFile.Get("%s_muHLTDown"%DYName), binning,"DYHist_%s_%sDown"%(HLTName,zero_corr))
            sigHistHLTDown.Add(DYHistHLTDown.Clone(), -1)

            sigHistHLTUp = getRebinnedHistogram(inputFile.Get("%s_muHLTUp"%signalName), binning, "sigHist_%s_%sUp"%(HLTName,zero_corr))
            DYHistHLTUp = getRebinnedHistogram(inputFile.Get("%s_muHLTUp"%DYName), binning,"DYHist_%s_%sUp"%(HLTName,zero_corr))
            sigHistHLTUp.Add(DYHistHLTUp.Clone(), -1)


##prefiring

    sigHistl1prefiringUp = getRebinnedHistogram(inputFile.Get("%s_l1prefiringUp"%signalName), binning, "sigHist_%s_%sUp"%(prefiringName,zero_corr))
    DYHistl1prefiringUp = getRebinnedHistogram(inputFile.Get("%s_l1prefiringUp"%DYName), binning,"DYHist_%s_%sUp"%(prefiringName,zero_corr))
    sigHistl1prefiringUp.Add(DYHistl1prefiringUp.Clone(), -1)

    sigHistl1prefiringDown = getRebinnedHistogram(inputFile.Get("%s_l1prefiringDown"%signalName), binning, "sigHist_%s_%sDown"%(prefiringName,zero_corr))
    DYHistl1prefiringDown = getRebinnedHistogram(inputFile.Get("%s_l1prefiringDown"%DYName), binning,"DYHist_%s_%sDown"%(prefiringName,zero_corr))
    sigHistl1prefiringDown.Add(DYHistl1prefiringDown.Clone(), -1)


##smearing
    sigHistSmearUp = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalName), binning, "sigHist_%s_%sUp"%(smearName,zero_corr))
    DYHistSmearUp = getRebinnedHistogram(inputFile.Get("%s_resUnc"%DYName), binning,"DYHist_%s_%sUp"%(smearName,zero_corr))
    sigHistSmearUp.Add(DYHistSmearUp.Clone(), -1)

    sigHistSmearDown = getRebinnedHistogram(inputFile.Get("%s_resUnc"%signalName), binning, "sigHist_%s_%sDown"%(smearName,zero_corr))
    DYHistSmearDown = getRebinnedHistogram(inputFile.Get("%s_resUnc"%DYName), binning,"DYHist_%s_%sDown"%(smearName,zero_corr))
    sigHistSmearDown.Add(DYHistSmearDown.Clone(), -1)


##muon reco

    if "dimuon" in channel:
        sigHistRecoUp = getRebinnedHistogram(inputFile.Get("%s_recoup"%signalName), binning, "sigHist_%s_%sUp"%(recoName,zero_corr))
        DYHistRecoUp = getRebinnedHistogram(inputFile.Get("%s_recoup"%DYName), binning,"DYHist_%s_%sUp"%(recoName,zero_corr))
        sigHistRecoUp.Add(DYHistRecoUp.Clone(), -1)

        sigHistRecoDown = getRebinnedHistogram(inputFile.Get("%s_recodown"%signalName), binning, "sigHist_%s_%sDown"%(recoName,zero_corr))
        DYHistRecoDown = getRebinnedHistogram(inputFile.Get("%s_recodown"%DYName), binning,"DYHist_%s_%sDown"%(recoName,zero_corr))
        sigHistRecoDown.Add(DYHistRecoDown.Clone(), -1)

##pileup
    sigHistPUUp = getRebinnedHistogram(inputFile.Get("%s_puUp"%signalName), binning, "sigHist_%s_%sUp"%(PUName,channel_corr))
    DYHistPUUp = getRebinnedHistogram(inputFile.Get("%s_puUp"%DYName), binning,"DYHist_%s_%sUp"%(PUName,channel_corr))
    sigHistPUUp.Add(DYHistPUUp.Clone(), -1)

    sigHistPUDown = getRebinnedHistogram(inputFile.Get("%s_puDown"%signalName), binning, "sigHist_%s_%sDown"%(PUName,channel_corr))
    DYHistPUDown = getRebinnedHistogram(inputFile.Get("%s_puDown"%DYName), binning,"DYHist_%s_%sDown"%(PUName,channel_corr))
    sigHistPUDown.Add(DYHistPUDown.Clone(), -1)

    if "muon" in zero_corr:
        sigHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalName),binning,"sigHist_%s_%sDown"%(scaleName,zero_corr))
        DYHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%DYName), binning,"DYHist_%s_%sDown"%(scaleName,zero_corr))
        sigHistScaleDown.Add(DYHistScaleDown.Clone(), -1)

        sigHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalName),binning,"sigHist_%s_%sUp"%(scaleName,zero_corr))
        DYHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%DYName), binning,"DYHist_%s_%sUp"%(scaleName,zero_corr))
        sigHistScaleUp.Add(DYHistScaleUp.Clone(), -1)

    else: # electron
        sigHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%signalName),binning,"sigHist_%s_%sDown"%(eScaleName,zero_corr))
        DYHistScaleDown = getRebinnedHistogram(inputFile.Get("%s_scaleUncDown"%DYName), binning,"DYHist_%s_%sDown"%(eScaleName,zero_corr))
        sigHistScaleDown.Add(DYHistScaleDown.Clone(), -1)

        sigHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%signalName),binning,"sigHist_%s_%sUp"%(eScaleName,zero_corr))
        DYHistScaleUp = getRebinnedHistogram(inputFile.Get("%s_scaleUncUp"%DYName), binning,"DYHist_%s_%sUp"%(eScaleName,zero_corr))
        sigHistScaleUp.Add(DYHistScaleUp.Clone(), -1)

##PDF

    sigHistPDFDown = getPDFUncertHistogram(sigHist,"sigHist_%sDown"%(pdfName), pdfUncert)
    DYHistPDFDown = getPDFUncertHistogram(DYHist, "DYHist_%sDown"%(pdfName), pdfUncert)
    sigHistPDFDown.Add(DYHistPDFDown.Clone(), -1)

    sigHistPDFUp =   getPDFUncertHistogram(sigHist,"sigHist_%sUp"%(pdfName),   pdfUncert,True)
    DYHistPDFUp = getPDFUncertHistogram(DYHist, "DYHist_%sUp"%(pdfName), pdfUncert, True)
    sigHistPDFUp.Add(DYHistPDFUp.Clone(), -1)

###btag uncertainty

    sigHistBTag_bc_corrUp = getBtagUncertHistogram(sigHist, "sigHist_%s_%sUp"%(btagName_bc_corr,year_corr), btag_bc_corr, True)
    DYHistBTag_bc_corrUp = getBtagUncertHistogram(DYHist, "DYHist_%s_%sUp"%(btagName_bc_corr, year_corr), btag_bc_corr, True)
    sigHistBTag_bc_corrUp.Add(DYHistBTag_bc_corrUp.Clone(), -1)

    sigHistBTag_bc_corrDown = getBtagUncertHistogram(sigHist, "sigHist_%s_%sDown"%(btagName_bc_corr,year_corr), btag_bc_corr)
    DYHistBTag_bc_corrDown = getBtagUncertHistogram(DYHist, "DYHist_%s_%sDown"%(btagName_bc_corr, year_corr), btag_bc_corr)
    sigHistBTag_bc_corrDown.Add(DYHistBTag_bc_corrDown.Clone(), -1)

    sigHistBTag_bc_uncorrUp = getBtagUncertHistogram(sigHist, "sigHist_%s_%sUp"%(btagName_bc,channel_corr), btag_bc_uncorr, True)
    DYHistBTag_bc_uncorrUp = getBtagUncertHistogram(DYHist, "DYHist_%s_%sUp"%(btagName_bc, channel_corr), btag_bc_uncorr, True)
    sigHistBTag_bc_uncorrUp.Add(DYHistBTag_bc_uncorrUp.Clone(), -1)

    sigHistBTag_bc_uncorrDown = getBtagUncertHistogram(sigHist, "sigHist_%s_%sDown"%(btagName_bc,channel_corr), btag_bc_uncorr)
    DYHistBTag_bc_uncorrDown = getBtagUncertHistogram(DYHist, "DYHist_%s_%sDown"%(btagName_bc, channel_corr), btag_bc_uncorr)
    sigHistBTag_bc_uncorrDown.Add(DYHistBTag_bc_uncorrDown.Clone(), -1)


    sigHistBTag_light_corrUp = getBtagUncertHistogram(sigHist, "sigHist_%s_%sUp"%(btagName_light_corr,year_corr), btag_light_corr, True)
    DYHistBTag_light_corrUp = getBtagUncertHistogram(DYHist, "DYHist_%s_%sUp"%(btagName_light_corr, year_corr), btag_light_corr, True)
    sigHistBTag_light_corrUp.Add(DYHistBTag_light_corrUp.Clone(), -1)

    sigHistBTag_light_corrDown = getBtagUncertHistogram(sigHist, "sigHist_%s_%sDown"%(btagName_light_corr,year_corr), btag_light_corr)
    DYHistBTag_light_corrDown = getBtagUncertHistogram(DYHist, "DYHist_%s_%sDown"%(btagName_light_corr, year_corr), btag_light_corr)
    sigHistBTag_light_corrDown.Add(DYHistBTag_light_corrDown.Clone(), -1)
    

    sigHistBTag_light_uncorrUp = getBtagUncertHistogram(sigHist, "sigHist_%s_%sUp"%(btagName_light,channel_corr), btag_light_uncorr, True)
    DYHistBTag_light_uncorrUp = getBtagUncertHistogram(DYHist, "DYHist_%s_%sUp"%(btagName_light, channel_corr), btag_light_uncorr, True)
    sigHistBTag_light_uncorrUp.Add(DYHistBTag_light_uncorrUp.Clone(), -1)
    

    sigHistBTag_light_uncorrDown = getBtagUncertHistogram(sigHist, "sigHist_%s_%sDown"%(btagName_light,channel_corr), btag_light_uncorr)
    DYHistBTag_light_uncorrDown = getBtagUncertHistogram(DYHist, "DYHist_%s_%sDown"%(btagName_light, channel_corr), btag_light_uncorr)
    sigHistBTag_light_uncorrDown.Add(DYHistBTag_light_uncorrDown.Clone(), -1)

    if "muon" in channel:
        dataHist = getRebinnedHistogram(inputFile.Get("mu_data_obs"), binning, "dataHist_%s"%channel)
        bkgHistJets = getRebinnedHistogram(fake_file.Get("mu_data_obs"), binning, "bkgHistJets_%s"%channel)
    
    else: # electron
        dataHist = getRebinnedHistogram(inputFile.Get("data_obs"), binning, "dataHist_%s"%channel)
        bkgHistJets = getRebinnedHistogram(fake_file.Get("data_obs"), binning, "bkgHistJets_%s"%channel)


    bkgIntegralDY = bkgHistDY.Integral()
    bkgIntegralTop = bkgHistTop.Integral()
    bkgIntegralDiboson = bkgHistDiboson.Integral()
    sigIntegral = sigHist.Integral()
    bkgIntegralJets = bkgHistJets.Integral()
    


    if "muon" in channel:
        label = "CITo2Mu_Lam%dTeV%s_%s"%(L,interference,channel)
    elif "electron" in channel:
        label = "CITo2E_Lam%dTeV%s_%s"%(L,interference,channel)

    print("mThresh", mThresh)
    #err = ROOT.Double(0)  
    err = c_double(0.)
    val = sigHist.IntegralAndError(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1, err)
    err = err.value
    result["sig"] = val
#    if "2018" in channel:
#       result["sig"] = 0.44
#    elif "2017" in channel:
#       result["sig"] = 0.30
#    elif "2016_pre" in channel:
#       result["sig"] = 0.14
#    elif "2016_post" in channel:
#       result["sig"] = 0.12
#    else:
#       result["sig"] = 1.
 

    #result["sig"] = 0.5
    result["sigStats"] = 1. + err
    #result["sigStats"] = 1. 
    #signalYields_default[label][str(int(mThresh))][0]
    #err = signalYields_default[label][str(int(mThresh))][1]

    valScaleUp =    sigHistScaleUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    valScaleDown =  sigHistScaleDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    valIDUp      =  sigHistIDUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    valIDDown    =  sigHistIDDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    if "muon" in channel:
        valIsoUp =   sigHistISOUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
        valIsoDown = sigHistISODown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
        valHLTUp   = sigHistHLTUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
        valHLTDown = sigHistHLTDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
        valRecoUp  = sigHistRecoUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
        valRecoDown = sigHistRecoDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    valL1PrefiringUp   = sigHistl1prefiringUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    valL1PrefiringDown = sigHistl1prefiringDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    valSmearUp         = sigHistSmearUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    valSmearDown       = sigHistSmearDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    valPUUp  =  sigHistPUUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    valPUDown = sigHistPUDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    valPDFUp  = sigHistPDFUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    valPDFDown = sigHistPDFDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    valbcCorrUp = sigHistBTag_bc_corrUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    valbcCorrDown = sigHistBTag_bc_corrDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    valbcuncorrUp = sigHistBTag_bc_uncorrUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    valbcuncorrDown = sigHistBTag_bc_uncorrDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    vallightcorrUp = sigHistBTag_light_corrUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    vallightcorrDown = sigHistBTag_light_corrDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    vallightuncorrUp = sigHistBTag_light_uncorrUp.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)
    vallightuncorrDown = sigHistBTag_light_uncorrDown.Integral(sigHist.FindBin(mThresh), sigHist.GetNbinsX()+1)

    result["sigScale"] = [abs(valScaleDown/val), abs(valScaleUp/val)]
    result["sigID"] = [abs(valIDDown/val), abs(valIDUp/val)]
    result["sigL1Prefiring"] = [abs(valL1PrefiringDown/val), abs(valL1PrefiringUp/val)]
    result["sigRes"]       = [abs(valSmearDown/val), abs(valSmearUp/val)]
    result["sigPU"]          = [abs(valPUDown/val), abs(valPUUp/val)]
    result["sigPDF"]         = [abs(1.012), abs(1.012)]
    #result["sigPDF"]         = [abs(valPDFDown/val), abs(valPDFUp/val)]
    #result["sigbcCorr"]      = [abs(valbcCorrDown/val), abs(valbcCorrUp/val)]
    #result["sigbcUncorr"]    = [abs(valbcuncorrDown/val), abs(valbcuncorrUp/val)]
    #result["siglightCorr"]   = [abs(vallightcorrDown/val), abs(vallightcorrUp/val)]
    #result["siglightUncorr"] = [abs(vallightuncorrDown/val), abs(vallightuncorrUp/val)]

    result["sigbcCorr"]      = [abs(1.03), abs(1.03)]
    result["sigbcUncorr"]      = [abs(1.03), abs(1.03)]
    result["siglightCorr"]      = [abs(1.03), abs(1.03)]
    result["siglightUncorr"]      = [abs(1.03), abs(1.03)]

    if "muon" in channel:
        result["sigIso"]     = [abs(valIsoDown/val), abs(valIsoUp/val)]
        result["sigHLT"]     = [abs(valHLTDown/val), abs(valHLTUp/val)]
        result["sigReco"]    = [abs(valRecoDown/val), abs(valRecoUp/val)]
        
    

    #result["data"] = 0.	
    result["data"] = dataHist.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)	

    err = c_double(0.)
    val = bkgHistJets.IntegralAndError(bkgHistJets.FindBin(mThresh),bkgHistJets.GetNbinsX()+1,err)
    err = err.value
    result["bkgJets"] = val

    if val==0.:
        result["bkgJetsStats"] = 1.
    else:
        result["bkgJetsStats"] = 1.+err/val
 
    #err = ROOT.Double(0)	
    err = c_double(0.)
    val = bkgHistDY.IntegralAndError(bkgHistDY.FindBin(mThresh),bkgHistDY.GetNbinsX()+1,err)
    err = err.value
    result["bkgDY"] = val

    if val==0. :
        result["bkgDYStats"] = 1.
    else:
        result["bkgDYStats"] = 1.+err/val

    
    result["bkgDYl1prefiring"] =  [ abs(bkgHistDYl1prefiringUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYl1prefiringDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
    result["bkgDYID"] =  [ abs(bkgHistDYIDUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYIDDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
    result["bkgDYScale"] =  [ abs(bkgHistDYScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYScaleDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
    result["bkgDYRes"] = [ abs(bkgHistDYSmearUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYSmearDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
    result["bkgDYPU"] =  [ abs(bkgHistDYPUUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYPUDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
    result["bkgDYPDF"] = [ abs(bkgHistDYPDFUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYPDFDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
    result["bkgDYbcCorr"] = [ abs(bkgHistDYBTag_bc_corrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYBTag_bc_corrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
    result["bkgDYbcUncorr"] = [ abs(bkgHistDYBTag_bc_uncorrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYBTag_bc_uncorrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
    result["bkgDYlightCorr"] = [ abs(bkgHistDYBTag_light_corrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYBTag_light_corrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
    result["bkgDYlightUncorr"] = [ abs(bkgHistDYBTag_light_uncorrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYBTag_light_uncorrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]

    if "muon" in channel:
        result["bkgDYIso"] = [ abs(bkgHistDYISOUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYISODown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
        result["bkgDYHLT"] = [ abs(bkgHistDYHLTUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYHLTDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]
        result["bkgDYReco"] = [ abs(bkgHistDYRecoUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYRecoDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])]

###Top

    #err = ROOT.Double(0)	
    #err = 0.
    err = c_double(0.)
    val = bkgHistTop.IntegralAndError(bkgHistTop.FindBin(mThresh),bkgHistTop.GetNbinsX()+1,err)
    if(val < 0):
        val = 0.
    else:
        val =  val

    err = err.value
    result["bkgTop"] = val

    if val == 0.:
        result["bkgTopStats"] = 1.
    else:
        result["bkgTopStats"] = 1.+err/val

    if val == 0. :
       result["bkgTopl1prefiring"] =  [ abs(1.), abs(1.)]
       result["bkgTopID"]          =  [ abs(1.), abs(1.)]
       result["bkgTopScale"]       =  [ abs(1.), abs(1.)]
       result["bkgTopRes"]         =  [ abs(1.), abs(1.)]
       result["bkgTopPU"]          =  [ abs(1.), abs(1.)]
       result["bkgTopPDF"]         =  [ abs(1.), abs(1.)]
       result["bkgTopbcCorr"]      =  [ abs(1.), abs(1.)]
       result["bkgTopbcUncorr"]    =  [ abs(1.), abs(1.)]
       result["bkgToplightCorr"]   =  [ abs(1.), abs(1.)]
       result["bkgToplightUncorr"] =  [ abs(1.), abs(1.)]

       if ("OneB" in channel) or ("TwoB" in channel):
           result["bkgTopttbarUncert"] = [ abs(1.), abs(1.)]

       if "muon" in channel:
           result["bkgTopIso"] = [ abs(1.), abs(1.)]
           result["bkgTopHLT"] = [ abs(1.), abs(1.)]
           result["bkgTopReco"] = [ abs(1.), abs(1.)]
    else:
       if(bkgHistTopScaleDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1) == 0.):
           down_err = 1.
           down = 1.
       else:
           down_err = bkgHistTopScaleDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)
           down = result["bkgTop"]
       result["bkgTopScale"] =  [ abs(bkgHistTopScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(down_err/down)]
       
       result["bkgTopl1prefiring"] =  [ abs(bkgHistTopl1prefiringUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopl1prefiringDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
       result["bkgTopID"] =  [ abs(bkgHistTopIDUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopIDDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
       #result["bkgTopScale"] =  [ abs(bkgHistTopScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopScaleDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
       result["bkgTopRes"] = [ abs(bkgHistTopSmearUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopSmearDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
       result["bkgTopPU"] =  [ abs(bkgHistTopPUUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopPUDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
       result["bkgTopPDF"] = [ abs(bkgHistTopPDFUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopPDFDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
      
       if ("OneB" in channel) or ("TwoB" in channel):
           result["bkgTopttbarUncert"] = [ abs(bkgHistTopttbarUncertUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopttbarUncertDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
       
       
       result["bkgTopbcCorr"] = [ abs(bkgHistTopBTag_bc_corrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopBTag_bc_corrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
       result["bkgTopbcUncorr"] = [ abs(bkgHistTopBTag_bc_uncorrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopBTag_bc_uncorrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
       result["bkgToplightCorr"] = [ abs(bkgHistTopBTag_light_corrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopBTag_light_corrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
       result["bkgToplightUncorr"] = [ abs(bkgHistTopBTag_light_uncorrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopBTag_light_uncorrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
   
       if "muon" in channel:
           result["bkgTopIso"] = [ abs(bkgHistTopISOUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopISODown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
           result["bkgTopHLT"] = [ abs(bkgHistTopHLTUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopHLTDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]
           result["bkgTopReco"] = [ abs(bkgHistTopRecoUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"]) , abs(bkgHistTopRecoDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgTop"])]



##Diboson

    #err = ROOT.Double(0)	
    #err = 0.
    err = c_double(0.)
    val = bkgHistDiboson.IntegralAndError(bkgHistDiboson.FindBin(mThresh),bkgHistDiboson.GetNbinsX()+1,err)
    if(val < 0):
        val = 0.
    else:
        val =  val
    err = err.value
    result["bkgDiboson"] = val

    if val == 0. :
        result["bkgDibosonStats"] = 1.
    else:
        result["bkgDibosonStats"] = 1.+err/val
       
    if val == 0. :
       result["bkgDibosonl1prefiring"] =  [ abs(1.), abs(1.)]
       result["bkgDibosonID"]          =  [ abs(1.), abs(1.)]
       result["bkgDibosonScale"]       =  [ abs(1.), abs(1.)]
       result["bkgDibosonRes"]         =  [ abs(1.), abs(1.)]
       result["bkgDibosonPU"]          =  [ abs(1.), abs(1.)]
       result["bkgDibosonPDF"]         =  [ abs(1.), abs(1.)]
       result["bkgDibosonbcCorr"]      =  [ abs(1.), abs(1.)]
       result["bkgDibosonbcUncorr"]    =  [ abs(1.), abs(1.)]
       result["bkgDibosonlightCorr"]   =  [ abs(1.), abs(1.)]
       result["bkgDibosonlightUncorr"] =  [ abs(1.), abs(1.)]

       if "muon" in channel:
           result["bkgDibosonIso"] = [ abs(1.), abs(1.)]
           result["bkgDibosonHLT"] = [ abs(1.), abs(1.)]
           result["bkgDibosonReco"] = [ abs(1.), abs(1.)]

    else:
       result["bkgDibosonl1prefiring"] =  [ abs(bkgHistDibosonl1prefiringUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonl1prefiringDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]
       result["bkgDibosonID"] =  [ abs(bkgHistDibosonIDUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonIDDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]

       if(bkgHistDibosonScaleDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1) == 0.):
           down_err = 1.
           down  = 1.
       else: 
           down_err = bkgHistDibosonScaleDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)
           down = result["bkgDiboson"]
       result["bkgDibosonScale"] =  [ abs(bkgHistDibosonScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(down_err/down)]

       result["bkgDibosonRes"] = [ abs(bkgHistDibosonSmearUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonSmearDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]
       result["bkgDibosonPU"] =  [ abs(bkgHistDibosonPUUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonPUDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]
       result["bkgDibosonPDF"] = [ abs(bkgHistDibosonPDFUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonPDFDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]
       result["bkgDibosonbcCorr"] = [ abs(bkgHistDibosonBTag_bc_corrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonBTag_bc_corrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]
       result["bkgDibosonbcUncorr"] = [ abs(bkgHistDibosonBTag_bc_uncorrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonBTag_bc_uncorrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]
       result["bkgDibosonlightCorr"] = [ abs(bkgHistDibosonBTag_light_corrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonBTag_light_corrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]
       result["bkgDibosonlightUncorr"] = [ abs(bkgHistDibosonBTag_light_uncorrUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonBTag_light_uncorrDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]

       if "muon" in channel:
           result["bkgDibosonIso"] = [ abs(bkgHistDibosonISOUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonISODown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]
           result["bkgDibosonHLT"] = [ abs(bkgHistDibosonHLTUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonHLTDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]
           result["bkgDibosonReco"] = [ abs(bkgHistDibosonRecoUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"]) , abs(bkgHistDibosonRecoDown.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDiboson"])]

###
    

    #result["bkgJets"] = bkgHistJets.Integral(bkgHistJets.FindBin(mThresh),bkgHistJets.GetNbinsX()+1)

    return result
    
