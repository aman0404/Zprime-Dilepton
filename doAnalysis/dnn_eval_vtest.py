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


#if (len(load_features)-6) < 16:
#   input_size = (len(load_features)-6)
#   print(len(load_features)-6)
#   hidden_sizes = [128, 64, 32, 16]
#   print(hidden_sizes)
#else:
#
#   input_size = len(load_features) - 3
#   hidden_sizes = [128, 64, 32, 16, 16, 16, 16, 16, 16]
#
#
#num_classes = 1
#
#model = NeuralNet(input_size, hidden_sizes, num_classes).to(device)
#model = model.double()




def model_eval(dfs, year, flavor):

    if flavor == "mu":
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
    if flavor == "el":
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
           
               "dielectron_mass",
               "dielectron_mass_gen",
               "wgt_nominal",
               "dataset",
           ]
    if flavor == "emu":
        load_features = [
               "eta_mu",
               "phi_mu",
               "pt_mu",
               "eta_el",
               "phi_el",
               "pt_el",
               "bjet1_pt",
               "bjet1_eta",
               "bjet1_phi",
               "lb_angle",
               "nbjets",
               "met",
               "min_bl_mass",
           
               "bjet1_ll_dR",
               "bjet1_ll_dR",

               "dilepton_mass",
               "dilepton_mass_gen",
               "wgt_nominal",
               "dataset",
           ]
    if "2016" in year:
        if "mu" in flavor:
            model_path = "ML_study/trained_models/dimuon/model_year2017_div_bbll_vtest.ckpt"
        elif flavor == "el":
            model_path = "ML_study/trained_models/dielectron/model_year2016_div_bbll_vtest.ckpt"
        else:
            raise ValueError("Flavor must be 'mu' or 'el'")
    elif year == "2017":
        if "mu" in flavor:
            model_path = "ML_study/trained_models/dimuon/model_year2017_div_bbll_vtest.ckpt"
        elif flavor == "el":
            model_path = "ML_study/trained_models/dielectron/model_year2017_div_bbll_vtest.ckpt"
        else:
            raise ValueError("Flavor must be 'mu' or 'el'")
    elif year == "2018":
        if "mu" in flavor:
            model_path = "ML_study/trained_models/dimuon/model_year2018_div_bbll_vtest.ckpt"
        elif flavor == "el":
            model_path = "ML_study/trained_models/dielectron/model_year2018_div_bbll_vtest.ckpt"
        else:
            raise ValueError(f"Flavor must be 'mu' or 'el'")
    else:
        raise ValueError(f"Model for year {year} is not available.")

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

    model.eval()
    dfs = dfs[load_features]

    if flavor == "mu":
        dfs = dfs.drop(columns = ["wgt_nominal", "dataset",  "bjet1_mb1_dR", "bjet1_mb2_dR", "dimuon_mass_gen", "dimuon_mass"])
    
    if flavor == "el":
        dfs = dfs.drop(columns = ["wgt_nominal", "dataset",  "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass"])

    if flavor == "emu":
        dfs = dfs.drop(columns = ["wgt_nominal", "dataset",  "bjet1_ll_dR", "bjet1_ll_dR", "dilepton_mass_gen", "dilepton_mass"])

    sig = dfs.values
    sig = torch.from_numpy(sig).to(device)
    df_scores = model(sig.double()) 
    df_scores = df_scores.cpu().detach().numpy()
    df_scores = df_scores.ravel()

    return df_scores



