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




import sys
import argparse
parser = argparse.ArgumentParser()

parser.add_argument(
    "-sl",
    "--slurm",
    dest="slurm_port",
    default=None,
    action="store",
    help="Slurm cluster port (if not specified, will create a local cluster)",
)
args = parser.parse_args()




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


if (len(load_features)-6) < 16:
   input_size = (len(load_features)-6)
   print(len(load_features)-6)
#   hidden_sizes = [6]
   hidden_sizes = [128, 64, 32, 16]
   print(hidden_sizes)
else:

   input_size = len(load_features) - 3
   hidden_sizes = [128, 64, 32, 16, 16, 16, 16, 16, 16]


#input_size = len(load_features) - 3
#hidden_sizes = [128, 64, 32, 16, 16, 16, 16, 16, 16]
num_classes = 1

model = NeuralNet(input_size, hidden_sizes, num_classes).to(device)
model = model.double()
model.load_state_dict(torch.load("model_year2018.ckpt"))
model.eval()

data_path = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/data_*/*parquet"

sig_path1 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/bsll_lambda1TeV_M*/*parquet"
sig_path2 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/bbll_10TeV_M*_posLL/*parquet"
sig_path3 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/bbll_14TeV_M*_posLL/*parquet"
sig_path4 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/bbll_22TeV_M*_posLL/*parquet"
bkg_path = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/ttbar*/*parquet"
#bkg_path = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/ttbar_lep_*/*parquet"
bkg_path1 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/tW/*parquet"
bkg_path2 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/Wantitop/*parquet"
bkg_path3 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/dy0J*/*parquet"
bkg_path4 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/dy1J*/*parquet"
bkg_path5 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/dy2J*/*parquet"
bkg_path6 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/WW*/*parquet"
bkg_path7 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/WZ*/*parquet"
bkg_path8 = "/depot/cms/private/users/kaur214/output/elec_channel_2018_allCuts/stage1_output/2018/ZZ*/*parquet"


#sig_path = "output/trainData_v1/2018/sig/bbll_4TeV_*_posLL/*parquet"
#bkg_path = "output/trainData_v1/2018/bkg/*/*parquet"
#data_path = "output/trainData_v1/2018/data/*/*parquet"

data_files = glob.glob(data_path)

sig_files1 = glob.glob(sig_path1)
sig_files2 = glob.glob(sig_path2)
sig_files3 = glob.glob(sig_path3)
sig_files4 = glob.glob(sig_path4)

bkg_files = glob.glob(bkg_path)
bkg_files1 = glob.glob(bkg_path1)
bkg_files2 = glob.glob(bkg_path2)


bkg_files3 = glob.glob(bkg_path3)
bkg_files4 = glob.glob(bkg_path4)
bkg_files5 = glob.glob(bkg_path5)
bkg_files6 = glob.glob(bkg_path6)
bkg_files7 = glob.glob(bkg_path7)
bkg_files8 = glob.glob(bkg_path8)

df_data = dd.read_parquet(data_files)

df_sig1 = dd.read_parquet(sig_files1)
df_sig2 = dd.read_parquet(sig_files2)
df_sig3 = dd.read_parquet(sig_files3)
df_sig4 = dd.read_parquet(sig_files4)

#for col in df_sig.columns:
#    print(col)

df_bkg0 = dd.read_parquet(bkg_files)
df_bkg1 = dd.read_parquet(bkg_files1)
df_bkg2 = dd.read_parquet(bkg_files2)


df_bkg3 = dd.read_parquet(bkg_files3)
df_bkg4 = dd.read_parquet(bkg_files4)
df_bkg5 = dd.read_parquet(bkg_files5)
df_bkg6 = dd.read_parquet(bkg_files6)
df_bkg7 = dd.read_parquet(bkg_files7)
df_bkg8 = dd.read_parquet(bkg_files8)


df_data = df_data[load_features]

df_sig1 = df_sig1[load_features]
df_sig2 = df_sig2[load_features]
df_sig3 = df_sig3[load_features]
df_sig4 = df_sig4[load_features]

frames_ttbar =   [df_bkg0, df_bkg1, df_bkg2]
frames_dy =      [df_bkg3, df_bkg4, df_bkg5]
frames_diboson = [df_bkg6, df_bkg7, df_bkg8]

dff_ttbar   = dd.concat(frames_ttbar)
dff_dy      = dd.concat(frames_dy)
dff_diboson = dd.concat(frames_diboson)

dff_ttbar   = dff_ttbar[load_features]
dff_dy      = dff_dy[load_features]
dff_diboson = dff_diboson[load_features]


df_data = df_data.loc[(df_data["nbjets"]>=1) & (df_data["dielectron_mass"] > 200) & (df_data["bjet1_mb1_dR"] == False) & (df_data["bjet1_mb2_dR"] == False), :]

df_sig1 = df_sig1.loc[(df_sig1["nbjets"]>=1) & (df_sig1["dielectron_mass"] > 200) & (df_sig1["bjet1_mb1_dR"] == False) & (df_sig1["bjet1_mb2_dR"] == False), :]

df_sig2 = df_sig2.loc[(df_sig2["nbjets"]>=1) & (df_sig2["dielectron_mass"] > 200) & (df_sig2["bjet1_mb1_dR"] == False) & (df_sig2["bjet1_mb2_dR"] == False), :]

df_sig3 = df_sig3.loc[(df_sig3["nbjets"]>=1) & (df_sig3["dielectron_mass"] > 200) & (df_sig3["bjet1_mb1_dR"] == False) & (df_sig3["bjet1_mb2_dR"] == False), :]

df_sig4 = df_sig4.loc[(df_sig4["nbjets"]>=1) & (df_sig4["dielectron_mass"] > 200) & (df_sig4["bjet1_mb1_dR"] == False) & (df_sig4["bjet1_mb2_dR"] == False), :]

data_wgt = df_data["wgt_nominal"].compute().values

#df_sig_wgt = df_sig[["wgt_nominal"]]
#df_sig_wgt = df_sig_wgt.compute()

sig_wgt1 = df_sig1["wgt_nominal"].compute().values
sig_wgt2 = df_sig2["wgt_nominal"].compute().values
sig_wgt3 = df_sig3["wgt_nominal"].compute().values
sig_wgt4 = df_sig4["wgt_nominal"].compute().values

df_data_plot = df_data.drop(columns = ["e1_eta", "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","dielectron_mass","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])

df_sig_plot1 = df_sig1.drop(columns = ["e1_eta", "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","dielectron_mass","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])
df_sig_plot2 = df_sig2.drop(columns = ["e1_eta", "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","dielectron_mass","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])
df_sig_plot3 = df_sig3.drop(columns = ["e1_eta", "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","dielectron_mass","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])
df_sig_plot4 = df_sig4.drop(columns = ["e1_eta", "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","dielectron_mass","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])


df_data_model = df_data.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass"])

df_sig_model1 = df_sig1.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass"])
df_sig_model2 = df_sig2.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass"])
df_sig_model3 = df_sig3.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass"])
df_sig_model4 = df_sig4.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass"])


node_ip = "128.211.148.61"
client = Client(f"{node_ip}:{args.slurm_port}")

print("connected to cluster")

#df_sig_model  = df_sig_model.compute()
sig1  = df_sig_model1.compute().values
sig2  = df_sig_model2.compute().values
sig3  = df_sig_model3.compute().values
sig4  = df_sig_model4.compute().values

data_model = df_data_model.compute().values

dff_ttbar = dff_ttbar.loc[(dff_ttbar["nbjets"]>=1) & (dff_ttbar["dielectron_mass"] > 200) & (dff_ttbar["bjet1_mb1_dR"] == False) & (dff_ttbar["bjet1_mb2_dR"] == False) & (~((dff_ttbar["dataset"] == "ttbar_lep_inclusive") & (dff_ttbar["dielectron_mass_gen"] > 500))) & (~((dff_ttbar["dataset"] == "WWinclusive") & (dff_ttbar["dielectron_mass_gen"] > 200))), :]

dff_dy = dff_dy.loc[(dff_dy["nbjets"]>=1) & (dff_dy["dielectron_mass"] > 200) & (dff_dy["bjet1_mb1_dR"] == False) & (dff_dy["bjet1_mb2_dR"] == False) & (~((dff_dy["dataset"] == "ttbar_lep_inclusive") & (dff_dy["dielectron_mass_gen"] > 500))) & (~((dff_dy["dataset"] == "WWinclusive") & (dff_dy["dielectron_mass_gen"] > 200))), :]

dff_diboson = dff_diboson.loc[(dff_diboson["nbjets"]>=1) & (dff_diboson["dielectron_mass"] > 200) & (dff_diboson["bjet1_mb1_dR"] == False) & (dff_diboson["bjet1_mb2_dR"] == False) & (~((dff_diboson["dataset"] == "ttbar_lep_inclusive") & (dff_diboson["dielectron_mass_gen"] > 500))) & (~((dff_diboson["dataset"] == "WWinclusive") & (dff_diboson["dielectron_mass_gen"] > 200))), :]


df_ttbar_wgt = dff_ttbar[["wgt_nominal"]].compute()
ttbar_wgt = df_ttbar_wgt["wgt_nominal"].values

df_dy_wgt = dff_dy[["wgt_nominal"]].compute()
dy_wgt = df_dy_wgt["wgt_nominal"].values


diboson_wgt = dff_diboson[["wgt_nominal"]].compute().values

df_ttbar_plot = dff_ttbar.drop(columns = ["e1_eta" , "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","dielectron_mass","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])

df_dy_plot = dff_dy.drop(columns = ["e1_eta" , "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","dielectron_mass","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])

df_diboson_plot = dff_diboson.drop(columns = ["e1_eta", "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","dielectron_mass","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])


df_ttbar_model = dff_ttbar.drop(columns = ["wgt_nominal", "dataset",  "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass"])

df_dy_model = dff_dy.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass"])

df_diboson_model = dff_diboson.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen", "dielectron_mass"])



bkg_ttbar = df_ttbar_model.compute().values
bkg_dy = df_dy_model.compute().values
bkg_diboson = df_diboson_model.compute().values

print("computing done")


sig1 = torch.from_numpy(sig1).to(device)
sig_scores1 = model(sig1.double()) 
sig_scores1 = sig_scores1.cpu().detach().numpy()
sig_scores1 = sig_scores1.ravel()

sig2 = torch.from_numpy(sig2).to(device)
sig_scores2 = model(sig2.double())
sig_scores2 = sig_scores2.cpu().detach().numpy()
sig_scores2 = sig_scores2.ravel()

sig3 = torch.from_numpy(sig3).to(device)
sig_scores3 = model(sig3.double())
sig_scores3 = sig_scores3.cpu().detach().numpy()
sig_scores3 = sig_scores3.ravel()

sig4 = torch.from_numpy(sig4).to(device)
sig_scores4 = model(sig4.double())
sig_scores4 = sig_scores4.cpu().detach().numpy()
sig_scores4 = sig_scores4.ravel()


data_model = torch.from_numpy(data_model).to(device)
data_scores = model(data_model.double())
data_scores = data_scores.cpu().detach().numpy()
data_scores = data_scores.ravel()


bkg_ttbar   = torch.from_numpy(bkg_ttbar).to(device)
bkg_dy      = torch.from_numpy(bkg_dy).to(device)
bkg_diboson = torch.from_numpy(bkg_diboson).to(device)

ttbar_bkg_scores = model(bkg_ttbar.double())
ttbar_bkg_scores = ttbar_bkg_scores.cpu().detach().numpy()
ttbar_bkg_scores = ttbar_bkg_scores.ravel()

dy_bkg_scores = model(bkg_dy.double())
dy_bkg_scores = dy_bkg_scores.cpu().detach().numpy()
dy_bkg_scores = dy_bkg_scores.ravel()

diboson_bkg_scores = model(bkg_diboson.double())
diboson_bkg_scores = diboson_bkg_scores.cpu().detach().numpy()
diboson_bkg_scores = diboson_bkg_scores.ravel()

#binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1700, 2100, 2700, 3500]

hdy_reco = TH1F("dy_reco_mu", "dy_reco_mu", 10,0, 10)
histbkg_top =  TH1F("bkg_top", "bkg_top", 10,0, 10)
histbkg_diboson =  TH1F("bkg_diboson", "bkg_diboson", 10,0, 10)
hsignal1 = TH1F("hsignal1", "hsignal1", 10,0, 10)
hsignal2 = TH1F("hsignal2", "hsignal2", 10,0, 10)
hsignal3 = TH1F("hsignal3", "hsignal3", 10,0, 10)
hsignal4 = TH1F("hsignal4", "hsignal4", 10,0, 10)

#histdata_mu =  TH1F("data_mu", "data_mu", 11, array('d', binsx))

for key in df_sig_plot1.columns.to_list():
    if(key == "nbjets"):

       print("key ", key)
       df_sig_val1 = df_sig_plot1[[key]].compute()
       df_sig_val2 = df_sig_plot2[[key]].compute()
       df_sig_val3 = df_sig_plot3[[key]].compute()
       df_sig_val4 = df_sig_plot4[[key]].compute()
       #df_data_val = df_data_plot[[key]].compute()
       
       df_ttbar_val   = df_ttbar_plot[[key]].compute()
       df_dy_val      = df_dy_plot[[key]].compute()
       df_diboson_val = df_diboson_plot[[key]].compute()

       print("compute done")

       fea_sig1 = df_sig_val1.values
       fea_sig2 = df_sig_val2.values
       fea_sig3 = df_sig_val3.values
       fea_sig4 = df_sig_val4.values

#       fea_data = df_data_val.values
       fea_ttbar   = df_ttbar_val.values
       fea_dy      = df_dy_val.values
       fea_diboson = df_diboson_val.values

       dnn_cut = 0.6
       for i in range(len(fea_sig1[sig_scores1 > dnn_cut])):
           hsignal1.Fill(fea_sig1[sig_scores1 > dnn_cut][i], sig_wgt1[sig_scores1 > dnn_cut][i])         

       for i in range(len(fea_sig2[sig_scores2 > dnn_cut])):
           hsignal2.Fill(fea_sig2[sig_scores2 > dnn_cut][i], sig_wgt2[sig_scores2 > dnn_cut][i])

       for i in range(len(fea_sig3[sig_scores3 > dnn_cut])):
           hsignal3.Fill(fea_sig3[sig_scores3 > dnn_cut][i], sig_wgt3[sig_scores3 > dnn_cut][i])

       for i in range(len(fea_sig4[sig_scores4 > dnn_cut])):
           hsignal4.Fill(fea_sig4[sig_scores4 > dnn_cut][i], sig_wgt4[sig_scores4 > dnn_cut][i])

#       for i in range(len(fea_data[data_scores > dnn_cut])):
#           histdata_mu.Fill(fea_data[data_scores > dnn_cut][i], data_wgt[data_scores > dnn_cut][i])


       for i in range(len(fea_ttbar[ttbar_bkg_scores > dnn_cut])):
           histbkg_top.Fill(fea_ttbar[ttbar_bkg_scores > dnn_cut][i], ttbar_wgt[ttbar_bkg_scores > dnn_cut][i])

       for i in range(len(fea_dy[dy_bkg_scores > dnn_cut])):
           hdy_reco.Fill(fea_dy[dy_bkg_scores > dnn_cut][i], dy_wgt[dy_bkg_scores > dnn_cut][i])

       for i in range(len(fea_diboson[diboson_bkg_scores > dnn_cut])):
           histbkg_diboson.Fill(fea_diboson[diboson_bkg_scores > dnn_cut][i], diboson_wgt[diboson_bkg_scores > dnn_cut][i])

file2 = TFile("nbjets_2018_muon_1b.root","RECREATE")
file2.cd()
#histdata_mu.Write()
hsignal1.Write()
hsignal2.Write()
hsignal3.Write()
hsignal4.Write()
hdy_reco.Write()
histbkg_top.Write()
histbkg_diboson.Write()
file2.Close()


