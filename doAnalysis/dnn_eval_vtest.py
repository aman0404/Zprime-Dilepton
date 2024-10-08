import torch
import numpy as np
import torch.nn as nn
import glob
import dask.dataframe as dd
import dask
import pandas as pd
from matplotlib import pyplot as plt
from dask.distributed import Client



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

load_features = [
    "mu1_eta",
    "mu1_phi",
    "mu1_pt",
    "mu2_eta",
    "mu2_phi",
    "mu2_pt",
    "bjet1_pt",
    "bjet1_eta",
    "bjet1_phi",
    "lb_angle",
    "nbjets",
    "met",
    "min_bl_mass",

    "bjet1_mb1_dR",
    "bjet1_mb2_dR",

    "dimuon_mass",
    "dimuon_mass_gen",
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
            layers.append(nn.Dropout(p=0.4))

        layers.append(nn.Linear(hidden_sizes[-1], num_classes))
        layers.append(nn.Sigmoid())
        self.layers = nn.ModuleList(layers)
    def forward(self, x):
        out = self.layers[0](x)
        for i in range(1, len(self.layers)):
            out = self.layers[i](out)
      
        return out


if (len(load_features)-6) < 16:
   input_size = (len(load_features)-6)
   print(len(load_features)-6)
   hidden_sizes = [128, 64, 32, 16]
   print(hidden_sizes)
else:

   input_size = len(load_features) - 3
   hidden_sizes = [128, 64, 32, 16, 16, 16, 16, 16, 16]


num_classes = 1

model = NeuralNet(input_size, hidden_sizes, num_classes).to(device)
model = model.double()


model.load_state_dict(torch.load("ML_study/newSep/mar2024/2017/model_year2017_div_bbll_vtest.ckpt", map_location=device))

#model.load_state_dict(torch.load("ML_study/newSep/mar2024/model_year2018_div_bbll_vtest.ckpt", map_location=device))



#model.load_state_dict(torch.load("ML_study/newSep/mar2024/model_year2018_div_bbll_v7.ckpt", map_location=device))
#model.load_state_dict(torch.load("ML_study/signal_studies/model_year2018.ckpt"))
model.eval()


def model_eval(dfs):
    dfs = dfs[load_features]
    dfs = dfs.drop(columns = ["wgt_nominal", "dataset",  "bjet1_mb1_dR", "bjet1_mb2_dR", "dimuon_mass_gen", "dimuon_mass"])

    sig = dfs.values
    sig = torch.from_numpy(sig).to(device)
    df_scores = model(sig.double()) 
    df_scores = df_scores.cpu().detach().numpy()
    df_scores = df_scores.ravel()

    return df_scores



