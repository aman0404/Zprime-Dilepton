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


bkg_path = "/depot/cms/private/users/kaur214/output/elec_channel_2018_newSep_jan2024_trig_eff/stage1_output/2018/dy*J*/*parquet"
#bkg_path = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/dy*/*parquet"


bkg_files = glob.glob(bkg_path)

df  = dd.read_parquet(bkg_files)

node_ip = "128.211.148.61"
client = Client(f"{node_ip}:{args.slurm_port}")

print("connected to cluster")

from elec_dnn_eval_vtest import model_eval

df = df[(df["r"]==f"{parameters['regions']}") & (df["dielectron_mass"] > 200.) & (df["dielectron_mass_gen"] > 200) & (df["nbjets"]>=1)]

df = df.compute()

scores = model_eval(df)

df["scores"] = scores

df = df[ (df["nbjets"]>=1) & (df["scores"] > 0.6) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True)]

reco_mass = df["dielectron_mass"].values

gen_mass = df["dielectron_mass_gen"].values

wgt = df["wgt_nominal"].values

wgt_l1prefire_up = df["wgt_l1prefiring_wgt_up"].values
wgt_l1prefire_dn = df["wgt_l1prefiring_wgt_down"].values

wgt_pu_up = df["wgt_pu_wgt_up"].values
wgt_pu_dn = df["wgt_pu_wgt_down"].values

wgt_scale_up = df["dielectron_mass_scaleUncUp"].values
wgt_scale_dn = df["dielectron_mass_scaleUncDown"].values

#pdf_unc = [0.01112166172, 0.01414670344, 0.01659019081, 0.01927992999, 0.02354107301, 0.02804822616, 0.04746036643]

pdf_unc = [0.01414670344, 0.01927992999, 0.02804822616, 0.04746036643]

#heepUncert = [0.012, 0.014, 0.016, 0.018, 0.023, 0.037, 0.037]

heepUncert = [0.014, 0.018, 0.037, 0.037]

#binsx = [200, 300, 400,500,700,1100,1900,6000]

binsx = [200, 400, 700, 1100,6000]

#binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1700, 2100, 2700, 3500]
#binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 3500] 
#binsx = [ 200,  300,  400,  600,  900, 1250, 1610, 2000, 2500, 3000, 3500]
#binsx = [ 200,  300,  400,  600,  900, 1250, 1610, 2000, 3500]
hist2del = TH2F("response_el","response_el", 4, array('d',binsx), 4, array('d',binsx))
#hist2del = TH2F("response_el","response_el",8,array('d',binsx), 8, array('d',binsx))

hist2del_id_up    = TH2F("hist2del_id_up","hist2del_id_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2del_id_dn    = TH2F("hist2del_id_dn","hist2del_id_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2del_l1_up    = TH2F("hist2del_l1_up","hist2del_l1_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2del_l1_dn    = TH2F("hist2del_l1_dn","hist2del_l1_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2del_pu_up    = TH2F("hist2del_pu_up","hist2del_pu_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2del_pu_dn    = TH2F("hist2del_pu_dn","hist2del_pu_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2del_pdf_up   = TH2F("hist2del_pdf_up","hist2del_pdf_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2del_pdf_dn   = TH2F("hist2del_pdf_dn","hist2del_pdf_dn", 4 ,array('d',binsx), 4, array('d',binsx))
hist2del_scale_up = TH2F("hist2del_scale_up","hist2del_scale_up", 4 ,array('d',binsx), 4, array('d',binsx))
hist2del_scale_dn = TH2F("hist2del_scale_dn","hist2del_scale_dn", 4 ,array('d',binsx), 4, array('d',binsx))


###systematic uncertainty
##PDF
for i in range(len(reco_mass)):
    hist2del_pdf_up.Fill(reco_mass[i], gen_mass[i], wgt[i])
    hist2del_pdf_dn.Fill(reco_mass[i], gen_mass[i], wgt[i])


for j in range(1, hist2del_pdf_up.GetNbinsX()+1):
    hist2del_pdf_up.SetBinContent(j, hist2del_pdf_up.GetBinContent(j)+hist2del_pdf_up.GetBinContent(j)*pdf_unc[j-1])
    hist2del_pdf_dn.SetBinContent(j, hist2del_pdf_dn.GetBinContent(j)-hist2del_pdf_dn.GetBinContent(j)*pdf_unc[j-1])

##scale
for i in range(len(wgt_scale_up)):
    hist2del_scale_up.Fill(wgt_scale_up[i], gen_mass[i], wgt[i])

for i in range(len(wgt_scale_dn)):
    hist2del_scale_dn.Fill(wgt_scale_dn[i], gen_mass[i], wgt[i])

## ID
for i in range(len(reco_mass)):
    hist2del_id_up.Fill(reco_mass[i], gen_mass[i], wgt[i])

for i in range(len(reco_mass)):
    hist2del_id_dn.Fill(reco_mass[i], gen_mass[i], wgt[i])

for j in range(1, hist2del_id_up.GetNbinsX()+1):
    hist2del_id_up.SetBinContent(j, hist2del_id_up.GetBinContent(j)+hist2del_id_up.GetBinContent(j)*heepUncert[j-1])
    hist2del_id_dn.SetBinContent(j, hist2del_id_dn.GetBinContent(j)-hist2del_id_dn.GetBinContent(j)*heepUncert[j-1])


##L1 prefiring
for i in range(len(reco_mass)):
    hist2del_l1_up.Fill(reco_mass[i], gen_mass[i], wgt_l1prefire_up[i])

for i in range(len(reco_mass)):
    hist2del_l1_dn.Fill(reco_mass[i], gen_mass[i], wgt_l1prefire_dn[i])

##PU
for i in range(len(reco_mass)):
    hist2del_pu_up.Fill(reco_mass[i], gen_mass[i], wgt_pu_up[i])

for i in range(len(reco_mass)):
    hist2del_pu_dn.Fill(reco_mass[i], gen_mass[i], wgt_pu_dn[i])

##nominal
for i in range(len(reco_mass)):
    hist2del.Fill(reco_mass[i], gen_mass[i], wgt[i])

normalize_el = []

normalize_el_pdf_up = []
normalize_el_pdf_dn = []

normalize_el_scale_up = []
normalize_el_scale_dn = []

normalize_el_id_up = []
normalize_el_id_dn = []

normalize_el_l1_up = []
normalize_el_l1_dn = []

normalize_el_pu_up = []
normalize_el_pu_dn = []


for i in range(hist2del.GetNbinsY()):
    sums=0

    sums_pdf_up = 0
    sums_pdf_dn = 0

    sums_scale_up = 0
    sums_scale_dn = 0

    sums_id_up = 0
    sums_id_dn = 0

    sums_pu_up = 0
    sums_pu_dn = 0

    sums_l1_up = 0
    sums_l1_dn = 0

    for j in range(hist2del.GetNbinsX()):
        sums += hist2del.GetBinContent(j+1, i+1)

        sums_pdf_up += hist2del_pdf_up.GetBinContent(j+1, i+1)
        sums_pdf_dn += hist2del_pdf_dn.GetBinContent(j+1, i+1)

        sums_scale_up += hist2del_scale_up.GetBinContent(j+1, i+1)
        sums_scale_dn += hist2del_scale_dn.GetBinContent(j+1, i+1)

        sums_id_up += hist2del_id_up.GetBinContent(j+1, i+1)
        sums_id_dn += hist2del_id_dn.GetBinContent(j+1, i+1)

        sums_pu_up  += hist2del_pu_up.GetBinContent(j+1, i+1)
        sums_pu_dn  += hist2del_pu_dn.GetBinContent(j+1, i+1)

        sums_l1_up  += hist2del_l1_up.GetBinContent(j+1, i+1)
        sums_l1_dn  += hist2del_l1_dn.GetBinContent(j+1, i+1)

    normalize_el.append(sums)

    normalize_el_pdf_up.append(sums_pdf_up)
    normalize_el_pdf_dn.append(sums_pdf_dn)

    normalize_el_scale_up.append(sums_scale_up)
    normalize_el_scale_dn.append(sums_scale_dn)

    normalize_el_id_up.append(sums_id_up)
    normalize_el_id_dn.append(sums_id_dn)

    normalize_el_l1_up.append(sums_l1_up)
    normalize_el_l1_dn.append(sums_l1_dn)

    normalize_el_pu_up.append(sums_pu_up)
    normalize_el_pu_dn.append(sums_l1_dn)


for i in range(hist2del.GetNbinsX()):
    for j in range(hist2del.GetNbinsY()):
        hist2del.SetBinContent(i+1, j+1, hist2del.GetBinContent(i+1,j+1)/normalize_el[j])
        hist2del.SetBinError(i+1, j+1, hist2del.GetBinError(i+1,j+1)/normalize_el[j])

        hist2del_id_up.SetBinContent(i+1, j+1, hist2del_id_up.GetBinContent(i+1,j+1)/normalize_el_id_up[j])
        hist2del_id_up.SetBinError(i+1, j+1, hist2del_id_up.GetBinError(i+1,j+1)/normalize_el_id_up[j])

        hist2del_id_dn.SetBinContent(i+1, j+1, hist2del_id_dn.GetBinContent(i+1,j+1)/normalize_el_id_dn[j])
        hist2del_id_dn.SetBinError(i+1, j+1, hist2del_id_dn.GetBinError(i+1,j+1)/normalize_el_id_dn[j])

        hist2del_l1_up.SetBinContent(i+1, j+1, hist2del_l1_up.GetBinContent(i+1,j+1)/normalize_el_l1_up[j])
        hist2del_l1_up.SetBinError(i+1, j+1, hist2del_l1_up.GetBinError(i+1,j+1)/normalize_el_l1_up[j])

        hist2del_l1_dn.SetBinContent(i+1, j+1, hist2del_l1_dn.GetBinContent(i+1,j+1)/normalize_el_l1_dn[j])
        hist2del_l1_dn.SetBinError(i+1, j+1, hist2del_l1_dn.GetBinError(i+1,j+1)/normalize_el_l1_dn[j])

        hist2del_pu_up.SetBinContent(i+1, j+1, hist2del_pu_up.GetBinContent(i+1,j+1)/normalize_el_pu_up[j])
        hist2del_pu_up.SetBinError(i+1, j+1, hist2del_pu_up.GetBinError(i+1,j+1)/normalize_el_pu_up[j])

        hist2del_pu_dn.SetBinContent(i+1, j+1, hist2del_pu_dn.GetBinContent(i+1,j+1)/normalize_el_pu_dn[j])
        hist2del_pu_dn.SetBinError(i+1, j+1, hist2del_pu_dn.GetBinError(i+1,j+1)/normalize_el_pu_dn[j])

        hist2del_pdf_up.SetBinContent(i+1, j+1, hist2del_pdf_up.GetBinContent(i+1,j+1)/normalize_el_pdf_up[j])
        hist2del_pdf_up.SetBinError(i+1, j+1, hist2del_pdf_up.GetBinError(i+1,j+1)/normalize_el_pdf_up[j])

        hist2del_pdf_dn.SetBinContent(i+1, j+1, hist2del_pdf_dn.GetBinContent(i+1,j+1)/normalize_el_pdf_dn[j])
        hist2del_pdf_dn.SetBinError(i+1, j+1, hist2del_pdf_dn.GetBinError(i+1,j+1)/normalize_el_pdf_dn[j])

        hist2del_scale_up.SetBinContent(i+1, j+1, hist2del_scale_up.GetBinContent(i+1,j+1)/normalize_el_scale_up[j])
        hist2del_scale_up.SetBinError(i+1, j+1, hist2del_scale_up.GetBinError(i+1,j+1)/normalize_el_scale_up[j])

        hist2del_scale_dn.SetBinContent(i+1, j+1, hist2del_scale_dn.GetBinContent(i+1,j+1)/normalize_el_scale_dn[j])
        hist2del_scale_dn.SetBinError(i+1, j+1, hist2del_scale_dn.GetBinError(i+1,j+1)/normalize_el_scale_dn[j])



hist2del.ClearUnderflowAndOverflow()

hist2del_id_up.ClearUnderflowAndOverflow()
hist2del_id_dn.ClearUnderflowAndOverflow()

hist2del_l1_up.ClearUnderflowAndOverflow()
hist2del_l1_dn.ClearUnderflowAndOverflow()

hist2del_pu_up.ClearUnderflowAndOverflow()
hist2del_pu_dn.ClearUnderflowAndOverflow()

hist2del_pdf_up.ClearUnderflowAndOverflow()
hist2del_pdf_dn.ClearUnderflowAndOverflow()

hist2del_scale_up.ClearUnderflowAndOverflow()
hist2del_scale_dn.ClearUnderflowAndOverflow()


hist2del.GetYaxis().SetTitle("Generated Mass")
hist2del.GetXaxis().SetTitle("Reconstructed Mass")

file1 = TFile("out_response_matrix_el_be_script_1b_2b.root","RECREATE")
#file1 = TFile("dilep_out_response_matrix_el_bb_script_0b.root","RECREATE")
#file1 = TFile("out_response_matrix_el_be_script.root","RECREATE")
file1.cd()
hist2del.Write()

hist2del_id_up.Write()
hist2del_id_dn.Write()

hist2del_l1_up.Write()
hist2del_l1_dn.Write()

hist2del_pu_up.Write()
hist2del_pu_dn.Write()

hist2del_pdf_up.Write()
hist2del_pdf_dn.Write()

hist2del_scale_up.Write()
hist2del_scale_dn.Write()

file1.Close()


