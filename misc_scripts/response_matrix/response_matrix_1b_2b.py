import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import dask.dataframe as dd
from dask.distributed import Client, LocalCluster
import glob
import math
from itertools import repeat
import mplhep as hep
import time
import copy
import random as rand
import sys
import argparse

import torch
import numpy as np
import torch.nn as nn
import glob
import dask.dataframe as dd
import dask
import pandas as pd
from matplotlib import pyplot as plt
from dask.distributed import Client

from ROOT import TCanvas, gStyle, TH1F,TH2F, TLegend, TFile, RooRealVar, RooCBShape, gROOT, RooFit, RooAddPdf, RooDataHist, RooDataSet
from ROOT import RooArgList

from array import array



parser = argparse.ArgumentParser()

parser.add_argument(
    "-sl",
    "--slurm",
    dest="slurm_port",
    default=None,
    action="store",
    help="Slurm cluster port (if not specified, will create a local cluster)",
)

parser.add_argument(
    "-r",
    "--region",
    dest="region",
    default=None,
    action="store",
    help="chose region (bb or be)",
)


args = parser.parse_args()


parameters = {
"regions" : args.region
}


#bkg_path = "/depot/cms/private/users/kaur214/output/muchannel_2018_newSep/stage1_output/2018/dy*J*/*parquet"
bkg_path = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2018/dy*J*/*parquet"


bkg_files = glob.glob(bkg_path)

df  = dd.read_parquet(bkg_files)

node_ip = "128.211.148.61"
client = Client(f"{node_ip}:{args.slurm_port}")

print("connected to cluster")

from dnn_eval_vtest import model_eval

df = df[(df["r"]==f"{parameters['regions']}") & (df["dimuon_mass"] > 200.) & (df["dimuon_mass_gen"] > 200) & (df["nbjets"]>=1) ]
df = df.compute()

scores = model_eval(df)

df["scores"] = scores

df = df[ (df["nbjets"]>=1) & (df["scores"] > 0.6) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True)]

#df = df[(df["r"]==f"{parameters['regions']}") & (df["dimuon_mass"] > 200.) & (df["dimuon_mass_gen"] > 200) & (df["nbjets"]==1) ]


reco_mass = df["dimuon_mass"].values

gen_mass = df["dimuon_mass_gen"].values

wgt = df["wgt_nominal"].values

wgt_ID_up = df["wgt_muID_up"].values
wgt_ID_dn = df["wgt_muID_down"].values 

wgt_l1prefire_up = df["wgt_l1prefiring_wgt_up"].values
wgt_l1prefire_dn = df["wgt_l1prefiring_wgt_down"].values

wgt_res = df["dimuon_mass_resUnc"].values

wgt_reco = df["wgt_recowgt_down"].values

wgt_pu_up = df["wgt_pu_wgt_up"].values
wgt_pu_dn = df["wgt_pu_wgt_down"].values

wgt_scale_up = df["dimuon_mass_scaleUncUp"].values
wgt_scale_dn = df["dimuon_mass_scaleUncDown"].values


wgt_iso_up = df["wgt_muISO_up"].values
wgt_iso_dn = df["wgt_muISO_down"].values

wgt_hlt_up = df["wgt_muHLT_up"].values
wgt_hlt_dn = df["wgt_muHLT_down"].values


#print("wgt ",len(wgt))
#print("reco",len(reco_mass))
#print("gen ",len(gen_mass))


binsx = [200, 400, 700,1100,6000]
#binsx = [200, 300, 400,500,700,1100,1900,6000]

#binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1700, 2100, 2700, 3500]
#binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 3500]  ## 12 bins
#binsx = [ 200,  300,  400,  600,  900, 1250, 1610, 2000, 2500, 3000, 3500]        ## 10 bins
#binsx = [ 200,  300,  400,  600,  900, 1250, 1610, 2000, 3500] ##8 bins original

hist2dmu = TH2F("response_mu","response_mu", 4 ,array('d',binsx), 4, array('d',binsx))

hist2dmu_id_up    = TH2F("hist2dmu_id_up","hist2dmu_id_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_id_dn    = TH2F("hist2dmu_id_dn","hist2dmu_id_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_l1_up    = TH2F("hist2dmu_l1_up","hist2dmu_l1_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_l1_dn    = TH2F("hist2dmu_l1_dn","hist2dmu_l1_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_pu_up    = TH2F("hist2dmu_pu_up","hist2dmu_pu_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_pu_dn    = TH2F("hist2dmu_pu_dn","hist2dmu_pu_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_iso_up   = TH2F("hist2dmu_iso_up","hist2dmu_iso_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_iso_dn   = TH2F("hist2dmu_iso_dn","hist2dmu_iso_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_hlt_up   = TH2F("hist2dmu_hlt_up","hist2dmu_hlt_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_hlt_dn   = TH2F("hist2dmu_hlt_dn","hist2dmu_hlt_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_reco     = TH2F("hist2dmu_reco","hist2dmu_reco", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_pdf_up   = TH2F("hist2dmu_pdf_up","hist2dmu_pdf_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_pdf_dn   = TH2F("hist2dmu_pdf_dn","hist2dmu_pdf_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_res      = TH2F("hist2dmu_res","hist2dmu_res", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_scale_up = TH2F("hist2dmu_scale_up","hist2dmu_scale_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2dmu_scale_dn = TH2F("hist2dmu_scale_dn","hist2dmu_scale_dn", 4 ,array('d',binsx), 4, array('d',binsx))

#hist2dmu = TH2F("response_mu","response_mu",8,array('d',binsx), 8, array('d',binsx))
#pdf_unc = [0.01112166172, 0.01414670344, 0.01659019081, 0.01927992999, 0.02354107301, 0.02804822616, 0.04746036643]

pdf_unc = [0.01414670344, 0.01927992999, 0.02804822616, 0.04746036643]

for i in range(len(reco_mass)):
    hist2dmu.Fill(reco_mass[i], gen_mass[i], wgt[i])

###systematic uncertainty
##PDF
for i in range(len(reco_mass)):
    hist2dmu_pdf_up.Fill(reco_mass[i], gen_mass[i], wgt[i])
    hist2dmu_pdf_dn.Fill(reco_mass[i], gen_mass[i], wgt[i])


for j in range(1, hist2dmu_pdf_up.GetNbinsX()+1):
    hist2dmu_pdf_up.SetBinContent(j, hist2dmu_pdf_up.GetBinContent(j)+hist2dmu_pdf_up.GetBinContent(j)*pdf_unc[j-1])
    hist2dmu_pdf_dn.SetBinContent(j, hist2dmu_pdf_dn.GetBinContent(j)-hist2dmu_pdf_dn.GetBinContent(j)*pdf_unc[j-1])

##resolution
    
for i in range(len(wgt_res)):
    hist2dmu_res.Fill(wgt_res[i], gen_mass[i], wgt[i])

##scale
for i in range(len(wgt_scale_up)):
    hist2dmu_scale_up.Fill(wgt_scale_up[i], gen_mass[i], wgt[i])

for i in range(len(wgt_scale_dn)):
    hist2dmu_scale_dn.Fill(wgt_scale_dn[i], gen_mass[i], wgt[i])

##reco
for i in range(len(reco_mass)):
    hist2dmu_reco.Fill(reco_mass[i], gen_mass[i], wgt_reco[i])

## ID
for i in range(len(reco_mass)):
    hist2dmu_id_up.Fill(reco_mass[i], gen_mass[i], wgt_ID_up[i])

for i in range(len(reco_mass)):
    hist2dmu_id_dn.Fill(reco_mass[i], gen_mass[i], wgt_ID_dn[i])

#ISO
for i in range(len(reco_mass)):
    hist2dmu_iso_up.Fill(reco_mass[i], gen_mass[i], wgt_iso_up[i])

for i in range(len(reco_mass)):
    hist2dmu_iso_dn.Fill(reco_mass[i], gen_mass[i], wgt_iso_dn[i])

#HLT 
for i in range(len(reco_mass)):
    hist2dmu_hlt_up.Fill(reco_mass[i], gen_mass[i], wgt_hlt_up[i])

for i in range(len(reco_mass)):
    hist2dmu_hlt_dn.Fill(reco_mass[i], gen_mass[i], wgt_hlt_dn[i])

##L1 prefiring
for i in range(len(reco_mass)):
    hist2dmu_l1_up.Fill(reco_mass[i], gen_mass[i], wgt_l1prefire_up[i])

for i in range(len(reco_mass)):
    hist2dmu_l1_dn.Fill(reco_mass[i], gen_mass[i], wgt_l1prefire_dn[i])

##PU
for i in range(len(reco_mass)):
    hist2dmu_pu_up.Fill(reco_mass[i], gen_mass[i], wgt_pu_up[i])

for i in range(len(reco_mass)):
    hist2dmu_pu_dn.Fill(reco_mass[i], gen_mass[i], wgt_pu_dn[i])

##########################

normalize_mu = []

normalize_mu_pdf_up = []
normalize_mu_pdf_dn = []

normalize_mu_res = []
normalize_mu_reco = []

normalize_mu_scale_up = []
normalize_mu_scale_dn = [] 

normalize_mu_iso_up = []
normalize_mu_iso_dn = []

normalize_mu_id_up = []
normalize_mu_id_dn = []

normalize_mu_hlt_up = []
normalize_mu_hlt_dn = []

normalize_mu_l1_up = []
normalize_mu_l1_dn = []

normalize_mu_pu_up = []
normalize_mu_pu_dn = []


for i in range(hist2dmu.GetNbinsY()):
    sums=0

    sums_res = 0
    sums_reco = 0

    sums_pdf_up = 0
    sums_pdf_dn = 0

    sums_scale_up = 0
    sums_scale_dn = 0

    sums_id_up = 0
    sums_id_dn = 0

    sums_iso_up = 0
    sums_iso_dn = 0

    sums_hlt_up = 0
    sums_hlt_dn = 0

    sums_pu_up = 0
    sums_pu_dn = 0

    sums_l1_up = 0
    sums_l1_dn = 0


    for j in range(hist2dmu.GetNbinsX()):
        sums += hist2dmu.GetBinContent(j+1, i+1)

        sums_res += hist2dmu_res.GetBinContent(j+1, i+1)
        sums_reco += hist2dmu_reco.GetBinContent(j+1, i+1) 

        sums_pdf_up += hist2dmu_pdf_up.GetBinContent(j+1, i+1)
        sums_pdf_dn += hist2dmu_pdf_dn.GetBinContent(j+1, i+1)

        sums_scale_up += hist2dmu_scale_up.GetBinContent(j+1, i+1)
        sums_scale_dn += hist2dmu_scale_dn.GetBinContent(j+1, i+1)

        sums_id_up += hist2dmu_id_up.GetBinContent(j+1, i+1)
        sums_id_dn += hist2dmu_id_dn.GetBinContent(j+1, i+1)
  
        sums_iso_up += hist2dmu_iso_up.GetBinContent(j+1, i+1)
        sums_iso_dn += hist2dmu_iso_dn.GetBinContent(j+1, i+1)

        sums_hlt_up += hist2dmu_hlt_up.GetBinContent(j+1, i+1)
        sums_hlt_dn += hist2dmu_hlt_dn.GetBinContent(j+1, i+1)

        sums_pu_up  += hist2dmu_pu_up.GetBinContent(j+1, i+1) 
        sums_pu_dn  += hist2dmu_pu_dn.GetBinContent(j+1, i+1) 

        sums_l1_up  += hist2dmu_l1_up.GetBinContent(j+1, i+1) 
        sums_l1_dn  += hist2dmu_l1_dn.GetBinContent(j+1, i+1)

    normalize_mu.append(sums)

    normalize_mu_pdf_up.append(sums_pdf_up)
    normalize_mu_pdf_dn.append(sums_pdf_dn)

    normalize_mu_res.append(sums_res)
    normalize_mu_reco.append(sums_reco)

    normalize_mu_scale_up.append(sums_scale_up)
    normalize_mu_scale_dn.append(sums_scale_dn)

    normalize_mu_iso_up.append(sums_iso_up)
    normalize_mu_iso_dn.append(sums_iso_dn)

    normalize_mu_id_up.append(sums_id_up)
    normalize_mu_id_dn.append(sums_id_dn)

    normalize_mu_hlt_up.append(sums_hlt_up)
    normalize_mu_hlt_dn.append(sums_hlt_dn)

    normalize_mu_l1_up.append(sums_l1_up)
    normalize_mu_l1_dn.append(sums_l1_dn)

    normalize_mu_pu_up.append(sums_pu_up)
    normalize_mu_pu_dn.append(sums_l1_dn)


for i in range(hist2dmu.GetNbinsX()):
    for j in range(hist2dmu.GetNbinsY()):
        hist2dmu.SetBinContent(i+1, j+1, hist2dmu.GetBinContent(i+1,j+1)/normalize_mu[j])
        hist2dmu.SetBinError(i+1, j+1, hist2dmu.GetBinError(i+1,j+1)/normalize_mu[j])

        hist2dmu_id_up.SetBinContent(i+1, j+1, hist2dmu_id_up.GetBinContent(i+1,j+1)/normalize_mu_id_up[j])
        hist2dmu_id_up.SetBinError(i+1, j+1, hist2dmu_id_up.GetBinError(i+1,j+1)/normalize_mu_id_up[j])

        hist2dmu_id_dn.SetBinContent(i+1, j+1, hist2dmu_id_dn.GetBinContent(i+1,j+1)/normalize_mu_id_dn[j])
        hist2dmu_id_dn.SetBinError(i+1, j+1, hist2dmu_id_dn.GetBinError(i+1,j+1)/normalize_mu_id_dn[j])

        hist2dmu_l1_up.SetBinContent(i+1, j+1, hist2dmu_l1_up.GetBinContent(i+1,j+1)/normalize_mu_l1_up[j])
        hist2dmu_l1_up.SetBinError(i+1, j+1, hist2dmu_l1_up.GetBinError(i+1,j+1)/normalize_mu_l1_up[j])

        hist2dmu_l1_dn.SetBinContent(i+1, j+1, hist2dmu_l1_dn.GetBinContent(i+1,j+1)/normalize_mu_l1_dn[j])
        hist2dmu_l1_dn.SetBinError(i+1, j+1, hist2dmu_l1_dn.GetBinError(i+1,j+1)/normalize_mu_l1_dn[j])

        hist2dmu_pu_up.SetBinContent(i+1, j+1, hist2dmu_pu_up.GetBinContent(i+1,j+1)/normalize_mu_pu_up[j])
        hist2dmu_pu_up.SetBinError(i+1, j+1, hist2dmu_pu_up.GetBinError(i+1,j+1)/normalize_mu_pu_up[j])

        hist2dmu_pu_dn.SetBinContent(i+1, j+1, hist2dmu_pu_dn.GetBinContent(i+1,j+1)/normalize_mu_pu_dn[j])
        hist2dmu_pu_dn.SetBinError(i+1, j+1, hist2dmu_pu_dn.GetBinError(i+1,j+1)/normalize_mu_pu_dn[j])

        hist2dmu_iso_up.SetBinContent(i+1, j+1, hist2dmu_iso_up.GetBinContent(i+1,j+1)/normalize_mu_iso_up[j])
        hist2dmu_iso_up.SetBinError(i+1, j+1, hist2dmu_iso_up.GetBinError(i+1,j+1)/normalize_mu_iso_up[j])

        hist2dmu_iso_dn.SetBinContent(i+1, j+1, hist2dmu_iso_dn.GetBinContent(i+1,j+1)/normalize_mu_iso_dn[j])
        hist2dmu_iso_dn.SetBinError(i+1, j+1, hist2dmu_iso_dn.GetBinError(i+1,j+1)/normalize_mu_iso_dn[j])
        
        hist2dmu_hlt_up.SetBinContent(i+1, j+1, hist2dmu_hlt_up.GetBinContent(i+1,j+1)/normalize_mu_hlt_up[j])
        hist2dmu_hlt_up.SetBinError(i+1, j+1, hist2dmu_hlt_up.GetBinError(i+1,j+1)/normalize_mu_hlt_up[j])

        hist2dmu_hlt_dn.SetBinContent(i+1, j+1, hist2dmu_hlt_dn.GetBinContent(i+1,j+1)/normalize_mu_hlt_dn[j])
        hist2dmu_hlt_dn.SetBinError(i+1, j+1, hist2dmu_hlt_dn.GetBinError(i+1,j+1)/normalize_mu_hlt_dn[j])

        hist2dmu_pdf_up.SetBinContent(i+1, j+1, hist2dmu_pdf_up.GetBinContent(i+1,j+1)/normalize_mu_pdf_up[j])
        hist2dmu_pdf_up.SetBinError(i+1, j+1, hist2dmu_pdf_up.GetBinError(i+1,j+1)/normalize_mu_pdf_up[j])

        hist2dmu_pdf_dn.SetBinContent(i+1, j+1, hist2dmu_pdf_dn.GetBinContent(i+1,j+1)/normalize_mu_pdf_dn[j])
        hist2dmu_pdf_dn.SetBinError(i+1, j+1, hist2dmu_pdf_dn.GetBinError(i+1,j+1)/normalize_mu_pdf_dn[j])

        hist2dmu_scale_up.SetBinContent(i+1, j+1, hist2dmu_scale_up.GetBinContent(i+1,j+1)/normalize_mu_scale_up[j])
        hist2dmu_scale_up.SetBinError(i+1, j+1, hist2dmu_scale_up.GetBinError(i+1,j+1)/normalize_mu_scale_up[j])

        hist2dmu_scale_dn.SetBinContent(i+1, j+1, hist2dmu_scale_dn.GetBinContent(i+1,j+1)/normalize_mu_scale_dn[j])
        hist2dmu_scale_dn.SetBinError(i+1, j+1, hist2dmu_scale_dn.GetBinError(i+1,j+1)/normalize_mu_scale_dn[j])

        hist2dmu_res.SetBinContent(i+1, j+1, hist2dmu_res.GetBinContent(i+1,j+1)/normalize_mu_res[j])
        hist2dmu_res.SetBinError(i+1, j+1, hist2dmu_res.GetBinError(i+1,j+1)/normalize_mu_res[j])

        hist2dmu_reco.SetBinContent(i+1, j+1, hist2dmu_reco.GetBinContent(i+1,j+1)/normalize_mu_reco[j])
        hist2dmu_reco.SetBinError(i+1, j+1, hist2dmu_reco.GetBinError(i+1,j+1)/normalize_mu_reco[j])


hist2dmu.ClearUnderflowAndOverflow()

hist2dmu_id_up.ClearUnderflowAndOverflow()
hist2dmu_id_dn.ClearUnderflowAndOverflow()

hist2dmu_l1_up.ClearUnderflowAndOverflow()
hist2dmu_l1_dn.ClearUnderflowAndOverflow()

hist2dmu_pu_up.ClearUnderflowAndOverflow()
hist2dmu_pu_dn.ClearUnderflowAndOverflow()

hist2dmu_iso_up.ClearUnderflowAndOverflow()
hist2dmu_iso_dn.ClearUnderflowAndOverflow()

hist2dmu_hlt_up.ClearUnderflowAndOverflow()
hist2dmu_hlt_dn.ClearUnderflowAndOverflow()

hist2dmu_pdf_up.ClearUnderflowAndOverflow()
hist2dmu_pdf_dn.ClearUnderflowAndOverflow()

hist2dmu_scale_up.ClearUnderflowAndOverflow()
hist2dmu_scale_dn.ClearUnderflowAndOverflow()

hist2dmu_res.ClearUnderflowAndOverflow()
hist2dmu_reco.ClearUnderflowAndOverflow()



hist2dmu.GetYaxis().SetTitle("Generated Mass")
hist2dmu.GetXaxis().SetTitle("Reconstructed Mass")

#file1 = TFile("dilep_out_response_matrix_mu_bb_script_0b.root","RECREATE")
file1 = TFile("out_response_matrix_mu_be_script_1b_2b.root","RECREATE")
file1.cd()
hist2dmu.Write()

hist2dmu_id_up.Write()
hist2dmu_id_dn.Write()

hist2dmu_l1_up.Write()
hist2dmu_l1_dn.Write()

hist2dmu_pu_up.Write()
hist2dmu_pu_dn.Write()

hist2dmu_iso_up.Write()
hist2dmu_iso_dn.Write()

hist2dmu_hlt_up.Write()
hist2dmu_hlt_dn.Write()

hist2dmu_pdf_up.Write()
hist2dmu_pdf_dn.Write()

hist2dmu_scale_up.Write()
hist2dmu_scale_dn.Write()

hist2dmu_res.Write()
hist2dmu_reco.Write()

file1.Close()


