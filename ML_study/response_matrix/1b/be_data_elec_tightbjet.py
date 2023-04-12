import torch
import torch.nn as nn

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

import pandas as pd
from ROOT import TCanvas, gStyle, TH1F,TH2F, TLegend, TFile, RooRealVar, RooCBShape, gROOT, RooFit, RooAddPdf, RooDataHist, RooDataSet
from ROOT import RooArgList

from array import array

from acc_eff_elec import value, be_value


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

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

load_features = [
    "e1_eta",
    "e1_phi",
    "e1_pt",
    "e2_eta",
    "e2_phi",
    "e2_pt",
    "bjet1_pt",
    "bjet1_eta",
    "bjet1_phi",
    "lb_angle",
    "nbjets",
    "met",
    "min_bl_mass",

    "bjet1_mb1_dR",
    "bjet1_mb2_dR",
    "r",
    "dielectron_mass",
    "dielectron_mass_gen",
    "wgt_nominal",
    "dataset",
]

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_sizes, num_classes):
        super(NeuralNet, self).__init__()
        layers = []
        layers.append(nn.Linear(input_size, hidden_sizes[0]))
        layers.append(nn.ELU())

        for i in range(len(hidden_sizes)-1):

            layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i+1]))
            layers.append(nn.ELU())
            #layers.append(nn.Dropout(p=0.1))

        layers.append(nn.Linear(hidden_sizes[-1], num_classes))
        layers.append(nn.Sigmoid())
        self.layers = nn.ModuleList(layers)
    def forward(self, x):
        out = self.layers[0](x)
        for i in range(1, len(self.layers)):
            out = self.layers[i](out)

        return out


if (len(load_features)-7) < 16:
   input_size = (len(load_features)-7)
   print(len(load_features)-7)
#   hidden_sizes = [6]
   hidden_sizes = [128, 64, 32, 16]
   print(hidden_sizes)
else:

   input_size = len(load_features) - 3
   hidden_sizes = [128, 64, 32, 16, 16, 16, 16, 16, 16]

num_classes = 1

model = NeuralNet(input_size, hidden_sizes, num_classes).to(device)
model = model.double()
model.load_state_dict(torch.load("model_year2018.ckpt"))
model.eval()

data_path = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/data_*/*parquet"

dy_path = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/dy*/*parquet"

bkg_path1 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/ttbar*/*parquet"
bkg_path2 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/tW/*parquet"
bkg_path3 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/Wantitop/*parquet"
bkg_path4 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/WW*/*parquet"
bkg_path5 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/WZ*/*parquet"
bkg_path6 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/ZZ*/*parquet"

#data_path = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/data_*/*parquet"
#
#dy_path = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/dy*/*parquet"
#
#bkg_path1 = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/ttbar*/*parquet"
#bkg_path2 = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/tW/*parquet"
#bkg_path3 = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/Wantitop/*parquet"
#bkg_path4 = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/WW*/*parquet"
#bkg_path5 = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/WZ*/*parquet"
#bkg_path6 = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/ZZ*/*parquet"


data_files = glob.glob(data_path)
dy_files = glob.glob(dy_path)

bkg_files1 = glob.glob(bkg_path1)
bkg_files2 = glob.glob(bkg_path2)
bkg_files3 = glob.glob(bkg_path3)
bkg_files4 = glob.glob(bkg_path4)
bkg_files5 = glob.glob(bkg_path5)
bkg_files6 = glob.glob(bkg_path6)


df1  = dd.read_parquet(bkg_files1)
df2  = dd.read_parquet(bkg_files2)
df3  = dd.read_parquet(bkg_files3)
df4  = dd.read_parquet(bkg_files4)
df5  = dd.read_parquet(bkg_files5)
df6  = dd.read_parquet(bkg_files6)

frames = [df1, df2, df3, df4, df5, df6]

df_bkg = dd.concat(frames)

df_data  = dd.read_parquet(data_files)
df_dy    = dd.read_parquet(dy_files)

df_bkg = df_bkg[load_features]
df_data = df_data[load_features]
df_dy = df_dy[load_features]


node_ip = "128.211.148.61"
client = Client(f"{node_ip}:{args.slurm_port}")

print("connected to cluster")

#print(df_bkg.bjet1_mb2_dR.compute().unique())

df_data = df_data[(df_data["r"]==f"{parameters['regions']}") & (df_data["dielectron_mass"] > 200.) & (df_data["nbjets"]==1) & (df_data["bjet1_mb1_dR"] == False) & (df_data["bjet1_mb2_dR"] == False) ]

df_dy   = df_dy[(df_dy["r"]==f"{parameters['regions']}") & (df_dy["dielectron_mass"] > 200.) & (df_dy["dielectron_mass_gen"] > 200) & (df_dy["nbjets"]==1) & (df_dy["bjet1_mb1_dR"] == False) & (df_dy["bjet1_mb2_dR"] == False) ]

df_bkg =  df_bkg[(df_bkg["r"]==f"{parameters['regions']}") & (df_bkg["dielectron_mass"] > 200.) & (df_bkg["dielectron_mass_gen"] > 200.) & (~((df_bkg["dataset"] == "ttbar_lep_inclusive") & (df_bkg["dielectron_mass_gen"] > 500))) & (~((df_bkg["dataset"] == "WWinclusive") & (df_bkg["dielectron_mass_gen"] > 200))) & (df_bkg["nbjets"]==1) & (df_bkg["bjet1_mb1_dR"] == False) & (df_bkg["bjet1_mb2_dR"] == False) ]

                 

reco_mass_data = df_data["dielectron_mass"].compute().values
reco_mass_dyy   = df_dy["dielectron_mass"].compute()
reco_mass_dy   = df_dy["dielectron_mass"].compute().values
reco_mass_bkg  = df_bkg["dielectron_mass"].compute().values

gen_mass_dyy   = df_dy["dielectron_mass_gen"].compute()
gen_mass_dy   = df_dy["dielectron_mass_gen"].compute().values

wgt_data = df_data["wgt_nominal"].compute().values
wgt_dyy   = df_dy["wgt_nominal"].compute()
wgt_dy   = df_dy["wgt_nominal"].compute().values
wgt_bkg  = df_bkg["wgt_nominal"].compute().values


df_dy_model =   df_dy.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass", "r"])
df_data_model = df_data.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass", "r"])
df_bkg_model =  df_bkg.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass", "r"])

dy = df_dy_model.compute().values
data = df_data_model.compute().values
bkg = df_bkg_model.compute().values

dy = torch.from_numpy(dy).to(device)
dy_scores = model(dy.double())
dy_scores = dy_scores.cpu().detach().numpy()
dy_scores = dy_scores.ravel()

data = torch.from_numpy(data).to(device)
data_scores = model(data.double())
data_scores = data_scores.cpu().detach().numpy()
data_scores = data_scores.ravel()

bkg = torch.from_numpy(bkg).to(device)
bkg_scores = model(bkg.double())
bkg_scores = bkg_scores.cpu().detach().numpy()
bkg_scores = bkg_scores.ravel()





#test_size = int(0.5*len(reco_mass_dyy))

#df_dy_test = reco_mass_dyy.iloc[:test_size]
#df_dy_test = df_dy_test.values
#
#df_dy_val = reco_mass_dyy.iloc[test_size:]
#df_dy_val = df_dy_val.values
#
#df_dy_gen_test = gen_mass_dyy.iloc[:test_size]
#df_dy_gen_test = df_dy_gen_test.values
#
#df_dy_gen_val = gen_mass_dyy.iloc[test_size:]
#df_dy_gen_val = df_dy_gen_val.values
#
#df_dy_wgt_test = wgt_dyy.iloc[:test_size]
#df_dy_wgt_test = df_dy_wgt_test.values
#
#df_dy_wgt_val =  wgt_dyy.iloc[test_size:]
#df_dy_wgt_val = df_dy_wgt_val.values

df_temp = pd.DataFrame(columns=['acc_eff'])
df_temp_gen = pd.DataFrame(columns=['acc_eff_gen'])

df_temp['acc_eff'] = reco_mass_dyy

df_temp_gen['acc_eff_gen'] = gen_mass_dyy

if(f"{parameters['regions']}"== 'bb'):
    df_temp['acc_eff'] = df_temp.acc_eff.apply(value)
    df_temp_gen['acc_eff_gen'] = df_temp_gen.acc_eff_gen.apply(value)
else:
    df_temp['acc_eff'] = df_temp.acc_eff.apply(be_value)
    df_temp_gen['acc_eff_gen'] = df_temp_gen.acc_eff_gen.apply(be_value)

acc_eff_reco = df_temp['acc_eff'].values
acc_eff_gen = df_temp_gen['acc_eff_gen'].values

corr_wgt_reco = np.divide(wgt_dy, acc_eff_reco)
corr_wgt_gen  = np.divide(wgt_dy, acc_eff_gen)

#binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2500, 2800, 3100, 3500]  ##15 bins
binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1700, 2100, 2700, 3500]  ##12 bins
#binsx = [200, 300, 400, 600, 900, 1250, 1610, 2000, 2500, 3000, 3500]
#binsx = [200, 300, 400, 600, 900, 1250, 1610, 2000, 3500] # 8 bins original

histdata_el =  TH1F("data_el", "data_el", 11, array('d', binsx))
hdy_reco = TH1F("dy_reco_el", "dy_reco_el", 11, array('d', binsx))
hdy_gen = TH1F("dy_gen_el", "dy_gen_el", 11, array('d', binsx))

#hdy_reco_val = TH1F("dy_reco_el_val", "dy_reco_el_val", 12, array('d', binsx))
#hdy_gen_val = TH1F("dy_gen_el_val", "dy_gen_el_val", 12, array('d', binsx))


histbkg_el =  TH1F("bkg_el", "bkg_el", 11, array('d', binsx))

hdy_el_corr_reco = TH1F("hdy_el_corr_reco", "hdy_el_corr_reco", 11, array('d', binsx))
hdy_el_corr_gen = TH1F("hdy_el_corr_gen", "hdy_el_corr_gen", 11, array('d', binsx))

dnn_cut = 0.6
    
for i in range(len(reco_mass_data[data_scores > dnn_cut])):
    histdata_el.Fill(reco_mass_data[data_scores > dnn_cut][i])


for i in range(len(reco_mass_bkg[bkg_scores > dnn_cut])):
    histbkg_el.Fill(reco_mass_bkg[bkg_scores > dnn_cut][i], wgt_bkg[bkg_scores > dnn_cut][i])

for i in range(len(reco_mass_dy[dy_scores > dnn_cut])):
    hdy_reco.Fill(reco_mass_dy[dy_scores > dnn_cut][i], wgt_dy[dy_scores > dnn_cut][i])
    hdy_gen.Fill(gen_mass_dy[dy_scores > dnn_cut][i], wgt_dy[dy_scores > dnn_cut][i])
    hdy_el_corr_reco.Fill(reco_mass_dy[dy_scores > dnn_cut][i], corr_wgt_reco[dy_scores > dnn_cut][i])
    hdy_el_corr_gen.Fill(gen_mass_dy[dy_scores > dnn_cut][i], corr_wgt_gen[dy_scores > dnn_cut][i])

## new histos ###
#for i in range(len(reco_mass_dy)):
#    hdy_el_corr_reco.Fill(reco_mass_dy[i], corr_wgt_reco[i])
#    hdy_el_corr_gen.Fill(gen_mass_dy[i], corr_wgt_gen[i])
#
#
#for i in range(len(df_dy_test)):
#    hdy_reco.Fill(df_dy_test[i], df_dy_wgt_test[i])
#    hdy_gen.Fill(df_dy_gen_test[i], df_dy_wgt_test[i])
#
#
#for i in range(len(df_dy_val)):
#    hdy_reco_val.Fill(df_dy_val[i], df_dy_wgt_val[i])
#    hdy_gen_val.Fill(df_dy_gen_val[i], df_dy_wgt_val[i])

## new histos ###


#for i in range(0, histdata_el.GetNbinsX()):
#    print(binsx[i], binsx[i+1], histdata_el.GetBinContent(i+1), round(histbkg_el.GetBinContent(i+1),2))
#
#for i in range(0, histdata_el.GetNbinsX()):
#    histdata_el.SetBinContent(i+1, histdata_el.GetBinContent(i+1)/histdata_el.GetBinWidth(i+1))
#    histbkg_el.SetBinContent(i+1, histbkg_el.GetBinContent(i+1)/histbkg_el.GetBinWidth(i+1))
#    hdy_reco.SetBinContent(i+1, hdy_reco.GetBinContent(i+1)/hdy_reco.GetBinWidth(i+1))
#    hdy_gen.SetBinContent(i+1, hdy_gen.GetBinContent(i+1)/hdy_gen.GetBinWidth(i+1))
#    hdy_el_corr_reco.SetBinContent(i+1, hdy_el_corr_reco.GetBinContent(i+1)/hdy_el_corr_reco.GetBinWidth(i+1))
#    hdy_el_corr_gen.SetBinContent(i+1, hdy_el_corr_gen.GetBinContent(i+1)/hdy_el_corr_gen.GetBinWidth(i+1))
#
#    histdata_el.SetBinError(i+1, histdata_el.GetBinError(i+1)/histdata_el.GetBinWidth(i+1))
#    histbkg_el.SetBinError(i+1, histbkg_el.GetBinError(i+1)/histbkg_el.GetBinWidth(i+1))
#    hdy_reco.SetBinError(i+1, hdy_reco.GetBinError(i+1)/hdy_reco.GetBinWidth(i+1))
#    hdy_gen.SetBinError(i+1, hdy_gen.GetBinError(i+1)/hdy_gen.GetBinWidth(i+1))
#    hdy_el_corr_reco.SetBinError(i+1, hdy_el_corr_reco.GetBinError(i+1)/hdy_el_corr_reco.GetBinWidth(i+1))
#    hdy_el_corr_gen.SetBinError(i+1, hdy_el_corr_gen.GetBinError(i+1)/hdy_el_corr_gen.GetBinWidth(i+1))


#file2 = TFile("dilep_data_elec_2018_bb_script_0b.root","RECREATE")
file2 = TFile("data_elec_2018_be_script_0b.root","RECREATE")
file2.cd()
histdata_el.Write()
hdy_reco.Write()
hdy_gen.Write()
histbkg_el.Write()
hdy_el_corr_reco.Write()
hdy_el_corr_gen.Write()
#hdy_reco_val.Write()
#hdy_gen_val.Write()
file2.Close()
