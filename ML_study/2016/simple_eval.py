import torch
import numpy as np
import torch.nn as nn
import glob
import dask.dataframe as dd
import dask
import pandas as pd
from matplotlib import pyplot as plt
from dask.distributed import Client

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
model.load_state_dict(torch.load("model_year2016.ckpt"))
model.eval()


sig_path = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/bsll_lambda1TeV_M500to1000*/*parquet"
bkg_path = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/ttbar_lep_*/*parquet"
bkg_path1 = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/tW/*parquet"
bkg_path2 = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/Wantitop/*parquet"
bkg_path3 = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/dy0J*/*parquet"
bkg_path4 = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/dy1J*/*parquet"
bkg_path5 = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/dy2J*/*parquet"
bkg_path6 = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/WW*/*parquet"
bkg_path7 = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/WZ*/*parquet"
bkg_path8 = "/depot/cms/private/users/kaur214/output/elec_channel_2016/stage1_output/2016*/ZZ*/*parquet"


#sig_path = "output/trainData_v1/2018/sig/bbll_4TeV_*_posLL/*parquet"
#bkg_path = "output/trainData_v1/2018/bkg/*/*parquet"
#data_path = "output/trainData_v1/2018/data/*/*parquet"
sig_files = glob.glob(sig_path)
bkg_files = glob.glob(bkg_path)
bkg_files1 = glob.glob(bkg_path1)
bkg_files2 = glob.glob(bkg_path2)


bkg_files3 = glob.glob(bkg_path3)
bkg_files4 = glob.glob(bkg_path4)
bkg_files5 = glob.glob(bkg_path5)
bkg_files6 = glob.glob(bkg_path6)
bkg_files7 = glob.glob(bkg_path7)
bkg_files8 = glob.glob(bkg_path8)

df_sig = dd.read_parquet(sig_files)

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


#def cal_dtheta(mu1_eta,bjet1_eta):
#    theta_mu1 = 2*np.arctan(np.exp(-1*mu1_eta))
#    theta_bjet1 = 2*np.arctan(np.exp(-1*bjet1_eta))
#    dtheta = np.fabs(theta_mu1-theta_bjet1)
#    return dtheta
#
#sig_dtheta = np.ones(len(df_sig))
#bkg_dtheta = np.ones(len(df_bkg))
##bkg_dtheta = []
#
#for i in range(len(df_sig)):
#    sig_mueta = df_sig["mu1_eta"].iloc[i]
#    sig_bjeteta = df_sig["bjet1_eta"].iloc[i]
#    sig_dtheta[i] = cal_dtheta(sig_mueta, sig_bjeteta)
#
#for i in range(len(df_bkg)):
#    bkg_mueta = df_bkg["mu1_eta"].iloc[i]
#    bkg_bjeteta = df_bkg["bjet1_eta"].iloc[i]
#    bkg_dtheta[i] = cal_dtheta(bkg_mueta, bkg_bjeteta)
#
#
#df_sig["dtheta"] = sig_dtheta
#df_bkg["dtheta"] = bkg_dtheta


df_sig = df_sig[load_features]

frames = [df_bkg0, df_bkg1, df_bkg2, df_bkg3, df_bkg4, df_bkg5, df_bkg6, df_bkg7, df_bkg8]
dff_bkg = dd.concat(frames)

dff_bkg = dff_bkg[load_features]


df_sig = df_sig.loc[(df_sig["nbjets"]==1) & (df_sig["dielectron_mass"] > 200) & (df_sig["bjet1_mb1_dR"] == False) & (df_sig["bjet1_mb2_dR"] == False), :]


df_sig_wgt = df_sig[["wgt_nominal"]]
df_sig_wgt = df_sig_wgt.compute()
sig_wgt = df_sig_wgt["wgt_nominal"].values

df_sig_plot = df_sig.drop(columns = ["e1_eta", "dielectron_mass", "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","nbjets","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])


#df_sig_plot = df_sig.drop(columns = ["wgt_nominal", "dataset"])
df_sig_model = df_sig.drop(columns = ["wgt_nominal", "dataset", "dielectron_mass", "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen"])
#df_sig_model = df_sig.drop(columns = ["wgt_nominal", "dataset", "dimuon_mass", "nbjets", "mu1_phi"])

#df_sig_plot = df_sig_plot.compute()

node_ip = "128.211.148.60"
client = Client(f"{node_ip}:{args.slurm_port}")

print("connected to cluster")

df_sig_model  = df_sig_model.compute()
sig  = df_sig_model.values



dff_bkg = dff_bkg.loc[(dff_bkg["nbjets"]==1) & (dff_bkg["dielectron_mass"] > 200) & (dff_bkg["bjet1_mb1_dR"] == False) & (dff_bkg["bjet1_mb2_dR"] == False) & (~((dff_bkg["dataset"] == "ttbar_lep_inclusive") & (dff_bkg["dielectron_mass_gen"] > 500))) & (~((dff_bkg["dataset"] == "WWinclusive") & (dff_bkg["dielectron_mass_gen"] > 200))), :]

#dff_bkg = dff_bkg.loc[(dff_bkg["bjet1_mb2_dR"] > 0.4), :]

df_bkg_wgt = dff_bkg[["wgt_nominal"]]
df_bkg_wgt = df_bkg_wgt.compute()
bkg_wgt = df_bkg_wgt["wgt_nominal"].values


df_bkg_plot = dff_bkg.drop(columns = ["e1_eta" ,"dielectron_mass", "dielectron_mass_gen", "e1_pt","e2_eta","e2_phi","e2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","nbjets","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])


#df_bkg_plot = dff_bkg.drop(columns = ["wgt_nominal", "dataset"])

df_bkg_model = dff_bkg.drop(columns = ["wgt_nominal", "dataset", "dielectron_mass",  "bjet1_mb1_dR", "bjet1_mb2_dR", "dielectron_mass_gen"])
#df_bkg_model = dff_bkg.drop(columns = ["wgt_nominal", "dataset", "dimuon_mass","nbjets", "mu1_phi"])


#df_bkg_plot = df_bkg_plot.compute()

df_bkg_model = df_bkg_model.compute()

print("computing done")

bkg =  df_bkg_model.values

sig = torch.from_numpy(sig).to(device)
sig_scores = model(sig.double()) 
sig_scores = sig_scores.cpu().detach().numpy()
sig_scores = sig_scores.ravel()

bkg = torch.from_numpy(bkg).to(device)
bkg_scores = model(bkg.double())
bkg_scores = bkg_scores.cpu().detach().numpy()
bkg_scores = bkg_scores.ravel()

bins = np.linspace(0, 1, 100)
plt.rcParams['font.size'] = 18
plt.rcParams["figure.figsize"] = (9,8)
plt.hist(sig_scores, bins, weights=sig_wgt, alpha=0.3, label='signal M=500')
plt.hist(bkg_scores, bins, weights=bkg_wgt, alpha=0.3, label='Total bkg')
plt.yscale('log')
plt.ylim(1e-1)
plt.xlabel('DNN Score')
plt.ylabel('Events')
#plt.ylim(bottom=2) 
plt.legend(loc='upper right')
plt.savefig("plots_2016/bsll_scores_M500to1000_total_model.png")
plt.savefig("plots_2016/bsll_scores_M500to1000_total_model.pdf")
plt.clf()


#for key in df_sig.drop(columns = ["wgt_nominal", "dataset"]).columns.to_list():

#node_ip = "128.211.148.61"
#slurm_port = "32856"
##f"{node_ip}:{args.slurm_port}"
#client = Client(f"{node_ip}:{slurm_port}")
##parameters["ncpus"] = len(client.scheduler_info()["workers"])
#print(f"Connected to cluster!")

for key in df_sig_plot.columns.to_list():
    print("key ", key)
    df_sig_val = df_sig_plot[[key]].compute()

    #print(df_sig_plot)

    df_bkg_val = df_bkg_plot[[key]].compute()

    print("compute done")

    fea_sig = df_sig_val.values
    fea_bkg = df_bkg_val.values

#    max_    = np.max(fea_bkg)
#    min_    = np.min(fea_bkg)

    maxbkg_ = np.max(fea_bkg)
    minbkg_ = np.min(fea_bkg)

    maxsig_ = np.max(fea_sig)
    minsig_ = np.min(fea_sig)

    max_    = max(maxbkg_, maxsig_)
    min_    = min(minbkg_, minsig_)

    if(key=="min_bl_mass"):
      bins = np.linspace(0.0, 1000, 50)
    else:
#      bins = np.linspace(0, 8000, 80)
      bins = np.linspace(min_, max_, 100)

    #dnn_cut = np.linspace(0.0, 1.0,50)
    dnn_cut = np.arange(0, 1, 0.01) 

#    if(key == "dimuon_mass"):
    if(key == "e1_phi"):
       sig_value = []
       bkg_value = []
       bins = np.linspace(-4.0, 4.0, 100)
       #bins_sig = plt.hist(fea_sig, bins, weights=sig_wgt, alpha=0.3, label='sig')
       for j in range(len(dnn_cut)):
           #print(dnn_cut[j]) 
           bins_sig = plt.hist(fea_sig[sig_scores > dnn_cut[j]], bins, weights=sig_wgt[sig_scores > dnn_cut[j]], alpha=0.3, label='sig')
           sig_value.append(sum(bins_sig[0]))
#           bins_sig = plt.hist(fea_sig[sig_scores>0.2], bins, weights=sig_wgt[sig_scores>0.2], alpha=0.3, label='sig')
#           print("signal ", sum(bins_sig[0]))
           #bins_bkg = plt.hist(fea_bkg, bins, weights=bkg_wgt, alpha=0.3, label='bkg')
           bins_bkg = plt.hist(fea_bkg[bkg_scores > dnn_cut[j]], bins, weights=bkg_wgt[bkg_scores > dnn_cut[j]], alpha=0.3, label='bkg')
           #bins_bkg = plt.hist(fea_bkg[bkg_scores>0.2], bins, weights=bkg_wgt[bkg_scores>0.2], alpha=0.3, label='bkg')
           bkg_value.append(sum(bins_bkg[0]))
           #print("bkg    ", sum(bins_bkg[0]))
           #print(sig_value)
           #print(bkg_value)
#       print(sig_value)
#       print(bkg_value)
       plt.yscale('log')

    else:
       plt.hist(fea_sig, bins, weights=sig_wgt, alpha=0.3, label='sig')
       plt.hist(fea_bkg, bins, weights=bkg_wgt, alpha=0.3, label='bkg')

    plt.yscale('log')
    plt.legend(loc='upper right')
    plt.savefig(f"plots_2016/bsll_4TeV_POSLL_0.2.png")
    plt.clf()
##    cut_range = (sig_scores > 0.6) & (sig_scores <= 0.8)
##    bkg_cut_range = (bkg_scores > 0.6) & (bkg_scores <=0.8) 
#    bins_sig = plt.hist(fea_sig[sig_scores>0.0], bins, weights=sig_wgt[sig_scores>0.0], alpha=0.3, label='sig')
#    #bins_sig = plt.hist(fea_sig[cut_range], bins, weights=sig_wgt[cut_range], alpha=0.3, label='sig')
#    #bins_bkg = plt.hist(fea_bkg[bkg_cut_range], bins, weights=bkg_wgt[bkg_cut_range], alpha=0.3, label='bkg')
#    bins_bkg = plt.hist(fea_bkg[bkg_scores>0.0], bins, weights=bkg_wgt[bkg_scores>0.0], alpha=0.3, label='bkg')
##    bkg_arr = []
##    signal_arr = []
##    for i in range(len(bins_sig[0])):
##         signal_arr.append(bins_sig[0][i])
##         bkg_arr.append(bins_bkg[0][i])
##
##    print(signal_arr)
##
##    print(bkg_arr)
#    print("signal = ", sum(bins_sig[0]))
#    print("bkg    = ", sum(bins_bkg[0]))
#
#    plt.yscale('log')
#    plt.legend(loc='upper right')
#    plt.savefig(f"pic_case13_1b/bsll_4TeV_POSLL_range_0p6_0p8.png")
#    plt.clf()



