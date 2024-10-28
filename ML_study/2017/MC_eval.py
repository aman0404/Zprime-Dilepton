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


from sklearn.metrics import roc_curve, auc


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
            #layers.append(nn.Dropout(p=0.4))

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
   #hidden_sizes = [128, 64, 32, 32, 16]
   hidden_sizes = [128, 64, 32, 16] #default
   print(hidden_sizes)
else:

   input_size = len(load_features) - 3
   hidden_sizes = [128, 64, 32, 16, 16, 16, 16, 16, 16]


#input_size = len(load_features) - 3
#hidden_sizes = [128, 64, 32, 16, 16, 16, 16, 16, 16]
num_classes = 1

model = NeuralNet(input_size, hidden_sizes, num_classes).to(device)
model = model.double()
model.load_state_dict(torch.load("model_year2017_div_bbll_vtest.ckpt"))
#model.load_state_dict(torch.load("model_year2018_div_bbll.ckpt"))
#model.load_state_dict(torch.load("model_year2018.ckpt"))
#model.load_state_dict(torch.load("model_year2018_noPhi.ckpt"))
model.eval()

#sig_path = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2018/bbll_26TeV_M*_posLL/*parquet"
#sig_path = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2018/bbll_6TeV_M*_posLL/*parquet"
#sig_path = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2018/bbll_26TeV_M*_posLL/*parquet"
sig_path = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/bsll_lambda2TeV_M500*/*parquet"

#sig_path = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2018/bsll_lambda6TeV_M*/*parquet"

bkg_path = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/tt*/*parquet"
bkg_path11 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/ZG*/*parquet"
bkg_path1 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/tW/*parquet"
bkg_path2 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/Wantitop/*parquet"
bkg_path3 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/dy0J*/*parquet"
bkg_path4 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/dy1J*/*parquet"
bkg_path5 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/dy2J*/*parquet"
bkg_path6 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/WW*/*parquet"
bkg_path7 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/WZ*/*parquet"
bkg_path8 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2017/ZZ*/*parquet"


#sig_path = "output/trainData_v1/2018/sig/bbll_4TeV_*_posLL/*parquet"
#bkg_path = "output/trainData_v1/2018/bkg/*/*parquet"
#data_path = "output/trainData_v1/2018/data/*/*parquet"
sig_files = glob.glob(sig_path)
bkg_files = glob.glob(bkg_path)
bkg_files11 = glob.glob(bkg_path11)
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
df_bkg00 = dd.read_parquet(bkg_files11)
df_bkg1 = dd.read_parquet(bkg_files1)
df_bkg2 = dd.read_parquet(bkg_files2)


df_bkg3 = dd.read_parquet(bkg_files3)
df_bkg4 = dd.read_parquet(bkg_files4)
df_bkg5 = dd.read_parquet(bkg_files5)
df_bkg6 = dd.read_parquet(bkg_files6)
df_bkg7 = dd.read_parquet(bkg_files7)
df_bkg8 = dd.read_parquet(bkg_files8)


df_sig = df_sig[load_features]

frames_ttbar =   [df_bkg0, df_bkg1, df_bkg2, df_bkg00]
frames_dy =      [df_bkg3, df_bkg4, df_bkg5]
frames_diboson = [df_bkg6, df_bkg7, df_bkg8]



dff_ttbar   = dd.concat(frames_ttbar)
dff_dy      = dd.concat(frames_dy)
dff_diboson = dd.concat(frames_diboson)

dff_ttbar   = dff_ttbar[load_features]
dff_dy      = dff_dy[load_features]
dff_diboson = dff_diboson[load_features]

dff_bkg = dd.concat([dff_ttbar, dff_dy, dff_diboson])

df_sig = df_sig.loc[(df_sig["nbjets"]==1) & (df_sig["dimuon_mass"] > 200) & (df_sig["bjet1_mb1_dR"] == True) & (df_sig["bjet1_mb2_dR"] == True), :]


df_sig_wgt = df_sig[["wgt_nominal"]]
df_sig_wgt = df_sig_wgt.compute()
sig_wgt = df_sig_wgt["wgt_nominal"].values

df_sig_plot = df_sig.drop(columns = [ "dimuon_mass_gen", "mu1_pt","mu2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","nbjets","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])


df_sig_model = df_sig.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dimuon_mass_gen", "dimuon_mass"])


node_ip = "128.211.148.61"
client = Client(f"{node_ip}:{args.slurm_port}")

print("connected to cluster")

df_sig_model  = df_sig_model.compute()
sig  = df_sig_model.values



dff_ttbar = dff_ttbar.loc[(dff_ttbar["nbjets"]==1) & (dff_ttbar["dimuon_mass"] > 200) & (dff_ttbar["bjet1_mb1_dR"] == True) & (dff_ttbar["bjet1_mb2_dR"] == True) & (~((dff_ttbar["dataset"] == "ttbar_lep_inclusive") & (dff_ttbar["dimuon_mass_gen"] > 500))) & (~((dff_ttbar["dataset"] == "WWinclusive") & (dff_ttbar["dimuon_mass_gen"] > 200))), :]

dff_dy = dff_dy.loc[(dff_dy["nbjets"]==1) & (dff_dy["dimuon_mass"] > 200) & (dff_dy["bjet1_mb1_dR"] == True) & (dff_dy["bjet1_mb2_dR"] == True) & (~((dff_dy["dataset"] == "ttbar_lep_inclusive") & (dff_dy["dimuon_mass_gen"] > 500))) & (~((dff_dy["dataset"] == "WWinclusive") & (dff_dy["dimuon_mass_gen"] > 200))), :]

dff_diboson = dff_diboson.loc[(dff_diboson["nbjets"]==1) & (dff_diboson["dimuon_mass"] > 200) & (dff_diboson["bjet1_mb1_dR"] == True) & (dff_diboson["bjet1_mb2_dR"] == True) & (~((dff_diboson["dataset"] == "ttbar_lep_inclusive") & (dff_diboson["dimuon_mass_gen"] > 500))) & (~((dff_diboson["dataset"] == "WWinclusive") & (dff_diboson["dimuon_mass_gen"] > 200))), :]


dff_bkg = dd.concat([dff_ttbar, dff_dy, dff_diboson])
dff_bkg_wgt = dff_bkg["wgt_nominal"].compute()

#bkg_yield = sum(dff_bkg_wgt)
#sig_yield = sum(df_sig.wgt_nominal)
#df_sig_wgt = df_sig_wgt*(bkg_yield/sig_yield)

#sig_wgt = df_sig_wgt.values



df_ttbar_wgt = dff_ttbar[["wgt_nominal"]].compute()
ttbar_wgt = df_ttbar_wgt["wgt_nominal"].values

df_dy_wgt = dff_dy[["wgt_nominal"]].compute()
dy_wgt = df_dy_wgt["wgt_nominal"].values


diboson_wgt = dff_diboson[["wgt_nominal"]].compute().values

df_ttbar_plot = dff_ttbar.drop(columns = [ "dimuon_mass_gen", "mu1_pt","mu2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","nbjets","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])

df_dy_plot = dff_dy.drop(columns = [ "dimuon_mass_gen", "mu1_pt","mu2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","nbjets","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])

df_diboson_plot = dff_diboson.drop(columns = ["dimuon_mass_gen", "mu1_pt","mu2_pt",                                      "bjet1_pt","bjet1_eta","bjet1_phi","lb_angle","nbjets","met","min_bl_mass", "bjet1_mb1_dR","bjet1_mb2_dR","wgt_nominal","dataset","wgt_nominal", "dataset"])


df_ttbar_model = dff_ttbar.drop(columns = ["wgt_nominal", "dataset",  "bjet1_mb1_dR", "bjet1_mb2_dR", "dimuon_mass_gen", "dimuon_mass"])

df_dy_model = dff_dy.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dimuon_mass_gen", "dimuon_mass"])

df_diboson_model = dff_diboson.drop(columns = ["wgt_nominal", "dataset", "bjet1_mb1_dR", "bjet1_mb2_dR", "dimuon_mass_gen", "dimuon_mass"])



bkg_ttbar = df_ttbar_model.compute().values
bkg_dy = df_dy_model.compute().values
bkg_diboson = df_diboson_model.compute().values

print("computing done")


sig = torch.from_numpy(sig).to(device)
sig_scores = model(sig.double()) 
sig_scores = sig_scores.cpu().detach().numpy()
sig_scores = sig_scores.ravel()

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

bins = np.linspace(0, 1, 100)
plt.rcParams['font.size'] = 18
plt.rcParams["figure.figsize"] = (9,8)
plt.hist(sig_scores, bins, weights=sig_wgt, alpha=0.3, label='signal')
plt.hist(ttbar_bkg_scores, bins, weights=ttbar_wgt, alpha=0.3, label='ttbar')
#plt.hist(dy_bkg_scores, bins, weights=dy_wgt, alpha=0.3, label='DY')
#plt.hist(diboson_bkg_scores, bins, weights=diboson_wgt, alpha=0.3, label='Diboson')
plt.yscale('log')
plt.ylim(1e-5)
plt.xlabel('DNN Score')
plt.ylabel('Events')
#plt.ylim(bottom=2) 
plt.legend(loc='upper right')
plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/dnn_scores_model_div_bbll_10TeV_vtest.png")
plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/dnn_scores_model_div_bbll_10TeV_vtest.pdf")
plt.clf()

#plotting ROC curve
y_true = np.concatenate([np.ones_like(sig_scores), np.zeros_like(ttbar_bkg_scores), np.zeros_like(dy_bkg_scores), np.zeros_like(diboson_bkg_scores)])
#y_true = np.concatenate([np.ones_like(sig_scores), np.zeros_like(ttbar_bkg_scores)])

y_score = np.concatenate([sig_scores, ttbar_bkg_scores, dy_bkg_scores, diboson_bkg_scores])

## Compute ROC curve and ROC area for each class
fpr, tpr, _ = roc_curve(y_true, y_score)
roc_auc = auc(fpr, tpr)
#
# Plot ROC curve
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/ROC_bsll_allbkg_vtest_M500_2TeV.png")
plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/ROC_bsll_allbkg_vtest_M500_2TeV.pdf")
plt.clf()



binsx = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1700, 2100, 2700, 3500]

hdy_reco_0p2 = TH1F("hdy_reco_0p2", "hdy_reco_0p2", 11, array('d', binsx))
histbkg_top_0p2 =  TH1F("histbkg_top_0p2", "histbkg_top_0p2", 11, array('d', binsx))
histbkg_diboson_0p2 =  TH1F("histbkg_diboson_0p2", "histbkg_diboson_0p2", 11, array('d', binsx))
hsignal_0p2 = TH1F("hsignal_0p2", "hsignal_0p2", 11, array('d', binsx))

hdy_reco_0p4 = TH1F("hdy_reco_0p4", "hdy_reco_0p4", 11, array('d', binsx))
histbkg_top_0p4 =  TH1F("histbkg_top_0p4", "histbkg_top_0p4", 11, array('d', binsx))
histbkg_diboson_0p4 =  TH1F("histbkg_diboson_0p4", "histbkg_diboson_0p4", 11, array('d', binsx))
hsignal_0p4 = TH1F("hsignal_0p4", "hsignal_0p4", 11, array('d', binsx))

hdy_reco_0p6 = TH1F("hdy_reco_0p6", "hdy_reco_0p6", 11, array('d', binsx))
histbkg_top_0p6 =  TH1F("histbkg_top_0p6", "histbkg_top_0p6", 11, array('d', binsx))
histbkg_diboson_0p6 =  TH1F("histbkg_diboson_0p6", "histbkg_diboson_0p6", 11, array('d', binsx))
hsignal_0p6 = TH1F("hsignal_0p6", "hsignal_0p6", 11, array('d', binsx))

hdy_reco_0p8 = TH1F("hdy_reco_0p8", "hdy_reco_0p8", 11, array('d', binsx))
histbkg_top_0p8 =  TH1F("histbkg_top_0p8", "histbkg_top_0p8", 11, array('d', binsx))
histbkg_diboson_0p8 =  TH1F("histbkg_diboson_0p8", "histbkg_diboson_0p8", 11, array('d', binsx))
hsignal_0p8 = TH1F("hsignal_0p8", "hsignal_0p8", 11, array('d', binsx))

hdy_reco_1p0 = TH1F("hdy_reco_1p0", "hdy_reco_1p0", 11, array('d', binsx))
histbkg_top_1p0 =  TH1F("histbkg_top_1p0", "histbkg_top_1p0", 11, array('d', binsx))
histbkg_diboson_1p0 =  TH1F("histbkg_diboson_1p0", "histbkg_diboson_1p0", 11, array('d', binsx))
hsignal_1p0 = TH1F("hsignal_1p0", "hsignal_1p0", 11, array('d', binsx))


for key in df_sig_plot.columns.to_list():
    if(key == "dimuon_mass"):
        print("key ", key)
        df_sig_val = df_sig_plot[[key]].compute()


        df_ttbar_val   = df_ttbar_plot[[key]].compute()
        df_dy_val      = df_dy_plot[[key]].compute()
        df_diboson_val = df_diboson_plot[[key]].compute()

        print("compute done")

        fea_sig = df_sig_val.values

        fea_ttbar   = df_ttbar_val.values
        fea_dy      = df_dy_val.values
        fea_diboson = df_diboson_val.values

        #dimuon_mass_all = np.concatenate([df_ttbar_val, df_dy_val, df_diboson_val])
        dimuon_mass_all_bkg = np.concatenate([df_ttbar_val, df_dy_val, df_diboson_val])
        dimuon_mass_top = np.concatenate([df_ttbar_val])
        dimuon_mass_all = np.concatenate([fea_sig])
        #dimuon_mass_all = np.concatenate([fea_sig, df_ttbar_val, df_dy_val, df_diboson_val])
        #scores_all =  np.concatenate([ttbar_bkg_scores, dy_bkg_scores, diboson_bkg_scores])
        scores_all_bkg =  np.concatenate([ttbar_bkg_scores, dy_bkg_scores, diboson_bkg_scores])
        scores_top =  np.concatenate([ttbar_bkg_scores])
        scores_all =  np.concatenate([sig_scores])
        #scores_all =  np.concatenate([sig_scores, ttbar_bkg_scores, dy_bkg_scores, diboson_bkg_scores])
#plot the data
        plt.figure(figsize=(8,6))
        plt.scatter(dimuon_mass_all, scores_all, s= 10, alpha=0.5)
        plt.xlabel('Dimuon mass')
        plt.ylabel('Pred')
        plt.xlim(200, 4000)
        plt.grid(True)
        plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/correlate_sig_vtest_M500_2TeV.png")
        #plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/correlate_allbkg_vtest.png")
        plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/correlate_sig_vtest_M500_2TeV.pdf")
        #plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/correlate_allbkg_vtest.pdf")
        plt.clf()

#plot the data
        plt.figure(figsize=(8,6))
        plt.scatter(dimuon_mass_top, scores_top, s= 10, alpha=0.5)
        plt.xlabel('Dimuon mass')
        plt.ylabel('Pred')
        plt.xlim(200, 4000)
        plt.grid(True)
        #plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/correlate_sig_vtest.png")
        plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/correlate_top_vtest.png")
        #plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/correlate_sig_vtest.pdf")
        plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/correlate_top_vtest.pdf")
        plt.clf()



#        dnn_cut1 = 0.0
#        dnn_cut2 = 0.2
#        dnn_cut3 = 0.4
#        dnn_cut4 = 0.6
#        dnn_cut5 = 0.8
#        dnn_cut6 = 1.0
#       #print(fea_sig[sig_scores > dnn_cut][0])
#
#        for i in range(len(fea_sig[(sig_scores > dnn_cut1) & (sig_scores < dnn_cut2) ])):
#            hsignal_0p2.Fill(fea_sig[(sig_scores > dnn_cut1) & (sig_scores < dnn_cut2)][i], sig_wgt[(sig_scores > dnn_cut1) & (sig_scores < dnn_cut2)][i])         
#
#        for i in range(len(fea_ttbar[(ttbar_bkg_scores > dnn_cut1) & (ttbar_bkg_scores < dnn_cut2)])):
#            histbkg_top_0p2.Fill(fea_ttbar[(ttbar_bkg_scores > dnn_cut1) & (ttbar_bkg_scores < dnn_cut2)][i], ttbar_wgt[(ttbar_bkg_scores > dnn_cut1) & (ttbar_bkg_scores < dnn_cut2)][i])

        for i in range(len(fea_ttbar[(ttbar_bkg_scores > 0.6)])):
            histbkg_top_0p2.Fill(fea_ttbar[(ttbar_bkg_scores > 0.6)][i], ttbar_wgt[(ttbar_bkg_scores > 0.6)][i])

        print(histbkg_top_0p2.Integral())
#        for i in range(len(fea_dy[(dy_bkg_scores > dnn_cut1) & (dy_bkg_scores < dnn_cut2)])):
#            hdy_reco_0p2.Fill(fea_dy[(dy_bkg_scores > dnn_cut1) & (dy_bkg_scores < dnn_cut2)][i], dy_wgt[(dy_bkg_scores > dnn_cut1) & (dy_bkg_scores < dnn_cut2)][i])
#
#        for i in range(len(fea_diboson[(diboson_bkg_scores > dnn_cut1) & (diboson_bkg_scores < dnn_cut2)])):
#            histbkg_diboson_0p2.Fill(fea_diboson[(diboson_bkg_scores > dnn_cut1) & (diboson_bkg_scores < dnn_cut2)][i], diboson_wgt[(diboson_bkg_scores > dnn_cut1) & (diboson_bkg_scores < dnn_cut2)][i])
#
#        ###cut 0.2 to 0.4
#        for i in range(len(fea_sig[(sig_scores > dnn_cut2) & (sig_scores < dnn_cut3) ])):
#            hsignal_0p4.Fill(fea_sig[(sig_scores > dnn_cut2) & (sig_scores < dnn_cut3)][i], sig_wgt[(sig_scores > dnn_cut2) & (sig_scores < dnn_cut3)][i])         
#
#        for i in range(len(fea_ttbar[(ttbar_bkg_scores > dnn_cut2) & (ttbar_bkg_scores < dnn_cut3)])):
#            histbkg_top_0p4.Fill(fea_ttbar[(ttbar_bkg_scores > dnn_cut2) & (ttbar_bkg_scores < dnn_cut3)][i], ttbar_wgt[(ttbar_bkg_scores > dnn_cut2) & (ttbar_bkg_scores < dnn_cut3)][i])
#
#        for i in range(len(fea_dy[(dy_bkg_scores > dnn_cut2) & (dy_bkg_scores < dnn_cut3)])):
#            hdy_reco_0p4.Fill(fea_dy[(dy_bkg_scores > dnn_cut2) & (dy_bkg_scores < dnn_cut3)][i], dy_wgt[(dy_bkg_scores > dnn_cut2) & (dy_bkg_scores < dnn_cut3)][i])
#
#        for i in range(len(fea_diboson[(diboson_bkg_scores > dnn_cut2) & (diboson_bkg_scores < dnn_cut3)])):
#            histbkg_diboson_0p4.Fill(fea_diboson[(diboson_bkg_scores > dnn_cut2) & (diboson_bkg_scores < dnn_cut3)][i], diboson_wgt[(diboson_bkg_scores > dnn_cut2) & (diboson_bkg_scores < dnn_cut3)][i])
#######
#
#        ###cut 0.4 to 0.6
#        for i in range(len(fea_sig[(sig_scores > dnn_cut3) & (sig_scores < dnn_cut4) ])):
#            hsignal_0p6.Fill(fea_sig[(sig_scores > dnn_cut3) & (sig_scores < dnn_cut4)][i], sig_wgt[(sig_scores > dnn_cut3) & (sig_scores < dnn_cut4)][i])         
#
#        for i in range(len(fea_ttbar[(ttbar_bkg_scores > dnn_cut3) & (ttbar_bkg_scores < dnn_cut4)])):
#            histbkg_top_0p6.Fill(fea_ttbar[(ttbar_bkg_scores > dnn_cut3) & (ttbar_bkg_scores < dnn_cut4)][i], ttbar_wgt[(ttbar_bkg_scores > dnn_cut3) & (ttbar_bkg_scores < dnn_cut4)][i])
#
#        for i in range(len(fea_dy[(dy_bkg_scores > dnn_cut3) & (dy_bkg_scores < dnn_cut4)])):
#            hdy_reco_0p6.Fill(fea_dy[(dy_bkg_scores > dnn_cut3) & (dy_bkg_scores < dnn_cut4)][i], dy_wgt[(dy_bkg_scores > dnn_cut3) & (dy_bkg_scores < dnn_cut4)][i])
#
#        for i in range(len(fea_diboson[(diboson_bkg_scores > dnn_cut3) & (diboson_bkg_scores < dnn_cut4)])):
#            histbkg_diboson_0p6.Fill(fea_diboson[(diboson_bkg_scores > dnn_cut3) & (diboson_bkg_scores < dnn_cut4)][i], diboson_wgt[(diboson_bkg_scores > dnn_cut3) & (diboson_bkg_scores < dnn_cut4)][i])
#######
#
#        ###cut 0.6 to 0.8
#        for i in range(len(fea_sig[(sig_scores > dnn_cut4) & (sig_scores < dnn_cut5) ])):
#            hsignal_0p8.Fill(fea_sig[(sig_scores > dnn_cut4) & (sig_scores < dnn_cut5)][i], sig_wgt[(sig_scores > dnn_cut4) & (sig_scores < dnn_cut5)][i])         
#
#        for i in range(len(fea_ttbar[(ttbar_bkg_scores > dnn_cut4) & (ttbar_bkg_scores < dnn_cut5)])):
#            histbkg_top_0p8.Fill(fea_ttbar[(ttbar_bkg_scores > dnn_cut4) & (ttbar_bkg_scores < dnn_cut5)][i], ttbar_wgt[(ttbar_bkg_scores > dnn_cut4) & (ttbar_bkg_scores < dnn_cut5)][i])
#
#        for i in range(len(fea_dy[(dy_bkg_scores > dnn_cut4) & (dy_bkg_scores < dnn_cut5)])):
#            hdy_reco_0p8.Fill(fea_dy[(dy_bkg_scores > dnn_cut4) & (dy_bkg_scores < dnn_cut5)][i], dy_wgt[(dy_bkg_scores > dnn_cut4) & (dy_bkg_scores < dnn_cut5)][i])
#
#        for i in range(len(fea_diboson[(diboson_bkg_scores > dnn_cut4) & (diboson_bkg_scores < dnn_cut5)])):
#            histbkg_diboson_0p8.Fill(fea_diboson[(diboson_bkg_scores > dnn_cut4) & (diboson_bkg_scores < dnn_cut5)][i], diboson_wgt[(diboson_bkg_scores > dnn_cut4) & (diboson_bkg_scores < dnn_cut5)][i])
#######
#
#        ###cut 0.8 to 1.0
#        for i in range(len(fea_sig[(sig_scores > dnn_cut5) & (sig_scores < dnn_cut6) ])):
#            hsignal_1p0.Fill(fea_sig[(sig_scores > dnn_cut5) & (sig_scores < dnn_cut6)][i], sig_wgt[(sig_scores > dnn_cut5) & (sig_scores < dnn_cut6)][i])         
#
#        for i in range(len(fea_ttbar[(ttbar_bkg_scores > dnn_cut5) & (ttbar_bkg_scores < dnn_cut6)])):
#            histbkg_top_1p0.Fill(fea_ttbar[(ttbar_bkg_scores > dnn_cut5) & (ttbar_bkg_scores < dnn_cut6)][i], ttbar_wgt[(ttbar_bkg_scores > dnn_cut5) & (ttbar_bkg_scores < dnn_cut6)][i])
#
#        for i in range(len(fea_dy[(dy_bkg_scores > dnn_cut5) & (dy_bkg_scores < dnn_cut6)])):
#            hdy_reco_1p0.Fill(fea_dy[(dy_bkg_scores > dnn_cut5) & (dy_bkg_scores < dnn_cut6)][i], dy_wgt[(dy_bkg_scores > dnn_cut5) & (dy_bkg_scores < dnn_cut6)][i])
#
#        for i in range(len(fea_diboson[(diboson_bkg_scores > dnn_cut5) & (diboson_bkg_scores < dnn_cut6)])):
#            histbkg_diboson_1p0.Fill(fea_diboson[(diboson_bkg_scores > dnn_cut5) & (diboson_bkg_scores < dnn_cut6)][i], diboson_wgt[(diboson_bkg_scores > dnn_cut5) & (diboson_bkg_scores < dnn_cut6)][i])
#######
#
#
#file2 = TFile("eta_div_ML_ttbar_data_muon_2018_bb_script_1b.root","RECREATE")
#file2.cd()
#hsignal_0p2.Write()
#hdy_reco_0p2.Write()
#histbkg_top_0p2.Write()
#histbkg_diboson_0p2.Write()
#
#hsignal_0p4.Write()
#hdy_reco_0p4.Write()
#histbkg_top_0p4.Write()
#histbkg_diboson_0p4.Write()
#
#hsignal_0p6.Write()
#hdy_reco_0p6.Write()
#histbkg_top_0p6.Write()
#histbkg_diboson_0p6.Write()
#
#hsignal_0p8.Write()
#hdy_reco_0p8.Write()
#histbkg_top_0p8.Write()
#histbkg_diboson_0p8.Write()
#
#hsignal_1p0.Write()
#hdy_reco_1p0.Write()
#histbkg_top_1p0.Write()
#histbkg_diboson_1p0.Write()
#
#file2.Close()


