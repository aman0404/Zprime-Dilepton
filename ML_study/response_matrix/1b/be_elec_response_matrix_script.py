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

bkg_path = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/dy*/*parquet"
#bkg_path = "/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/dy*/*parquet"


bkg_files = glob.glob(bkg_path)

df  = dd.read_parquet(bkg_files)

node_ip = "128.211.148.61"
client = Client(f"{node_ip}:{args.slurm_port}")

print("connected to cluster")

df = df[load_features]

df = df[(df["r"]==f"{parameters['regions']}") & (df["dielectron_mass"] > 200.) & (df["dielectron_mass_gen"] > 200) & (df["nbjets"]==1) & (df["bjet1_mb1_dR"] == False) & (df["bjet1_mb2_dR"] == False)]


reco_mass = df["dielectron_mass"].compute().values

gen_mass = df["dielectron_mass_gen"].compute().values

wgt = df["wgt_nominal"].compute().values

print("wgt ",len(wgt))
print("reco",len(reco_mass))
print("gen ",len(gen_mass))

df_model = df.drop(columns = ["wgt_nominal", "dataset", "dielectron_mass", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "r"])

dy  = df_model.compute().values
dy = torch.from_numpy(dy).to(device)
dy_scores = model(dy.double())
dy_scores = dy_scores.cpu().detach().numpy()
dy_scores = dy_scores.ravel()


binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1700, 2100, 2700, 3500]
#binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 3500] 
#binsx = [ 200,  300,  400,  600,  900, 1250, 1610, 2000, 2500, 3000, 3500]
#binsx = [ 200,  300,  400,  600,  900, 1250, 1610, 2000, 3500]
hist2del = TH2F("response_el","response_el", 11, array('d',binsx), 11, array('d',binsx))
#hist2del = TH2F("response_el","response_el",8,array('d',binsx), 8, array('d',binsx))

dnn_cut = 0.6

for i in range(len(reco_mass[dy_scores > dnn_cut])):
    hist2del.Fill(reco_mass[dy_scores > dnn_cut][i], gen_mass[dy_scores > dnn_cut][i], wgt[dy_scores > dnn_cut][i])

normalize_el = []
for i in range(hist2del.GetNbinsY()):
    sums=0
    for j in range(hist2del.GetNbinsX()):
        sums += hist2del.GetBinContent(j+1, i+1)
    normalize_el.append(sums)

for i in range(hist2del.GetNbinsX()):
    for j in range(hist2del.GetNbinsY()):
        hist2del.SetBinContent(i+1, j+1, hist2del.GetBinContent(i+1,j+1)/normalize_el[j])
        hist2del.SetBinError(i+1, j+1, hist2del.GetBinError(i+1,j+1)/normalize_el[j])

hist2del.ClearUnderflowAndOverflow()

hist2del.GetYaxis().SetTitle("Generated Mass")
hist2del.GetXaxis().SetTitle("Reconstructed Mass")

file1 = TFile("out_response_matrix_el_be_script_0b.root","RECREATE")
#file1 = TFile("dilep_out_response_matrix_el_bb_script_0b.root","RECREATE")
#file1 = TFile("out_response_matrix_el_be_script.root","RECREATE")
file1.cd()
hist2del.Write()
file1.Close()


