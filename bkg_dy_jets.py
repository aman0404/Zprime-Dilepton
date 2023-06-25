import numpy as np
import dask.dataframe as dd
from dask.distributed import Client, LocalCluster
import glob
import math
from itertools import repeat
import mplhep as hep
import time
import matplotlib.pyplot as plt
import copy
import random as rand
import pandas as pd
from functools import reduce

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

print(f"region is: {parameters['regions']}") 

node_ip = "128.211.148.60"
client = Client(f"{node_ip}:{args.slurm_port}")

print("connected to cluster")

load_fields = [
        "dilepton_mass",
        "r",
        "dilepton_mass_gen",
        "nbjets",
        "wgt_nominal",
        "bjet1_ll_dR",
    ]


# paths = "/depot/cms/users/kaur214/output/muchannel_2018_allCuts_debug_Zpeak/stage1_output/2018/dyInclusive50/*parquet"

# paths_data = "/depot/cms/users/kaur214/output/muchannel_2018_allCuts_debug_Zpeak/stage1_output/2018/data_*/*parquet"

# paths_ttbar = "/depot/cms/users/kaur214/output/muchannel_2018_allCuts_debug_Zpeak/stage1_output/2018/ttbar_lep_inclusive/*parquet"
# paths_ww = "/depot/cms/users/kaur214/output/muchannel_2018_allCuts_debug_Zpeak/stage1_output/2018/W*/*parquet"
# paths_zz = "/depot/cms/users/kaur214/output/muchannel_2018_allCuts_debug_Zpeak/stage1_output/2018/Z*/*parquet"

paths = "/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/2018/dy*/*parquet"

paths_data = "/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/2018/data_*/*parquet"

# paths_ttbar = "/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/2018/ttbar_lep_inclusive/*parquet"
paths_ttbar = "/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/2018/ttbar*/*parquet"
paths_ww = "/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/2018/W*/*parquet"
paths_zz = "/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/2018/Z*/*parquet"

sig_files = glob.glob(paths)
# print(f"sig_files: {sig_files}")
df_temp = dd.read_parquet(sig_files)

data_files = glob.glob(paths_data)
df_data_temp = dd.read_parquet(data_files)

ttbar_files = glob.glob(paths_ttbar)
df_ttbar_temp = dd.read_parquet(ttbar_files)

ww_files = glob.glob(paths_ww)
df_ww_temp = dd.read_parquet(ww_files)

zz_files = glob.glob(paths_zz)
df_zz_temp = dd.read_parquet(zz_files)

df_dy   = df_temp[load_fields]

df_data = df_data_temp[load_fields]
df_ttbar = df_ttbar_temp[load_fields]
df_ww = df_ww_temp[load_fields]
df_zz = df_zz_temp[load_fields]

# frames = [df_ttbar, df_ww, df_zz]
frames = [df_ww, df_zz]


df_bkg = dd.concat(frames)

print("computation complete")

nbjet_cut=0
print(f"nbjet_cut equal to: {nbjet_cut}")
# print(f"nbjet_cut greater than: {nbjet_cut}")

df_dy   = df_dy[(df_dy["r"]==f"{parameters['regions']}") & (df_dy["dilepton_mass"] > 60.) & (df_dy["dilepton_mass"] < 500.) ]
# print(f"len(df_dy) b4 nbjets cut: {len(df_dy)}")
df_dy   = df_dy[(df_dy["nbjets"] > nbjet_cut)]
# print(f"len(df_dy) after nbjets cut: {len(df_dy)}")
# print(f'df_dy["nbjets"]: {df_dy["nbjets"].compute().head()}')

df_data   = df_data[(df_data["r"]==f"{parameters['regions']}") & (df_data["dilepton_mass"] > 60.) & (df_data["dilepton_mass"] < 500.)]
df_data   = df_data[(df_data["nbjets"] == nbjet_cut)]
# print(f"len(df_data) : {len(df_data)}")
df_bkg   = df_bkg[(df_bkg["r"]==f"{parameters['regions']}") & (df_bkg["dilepton_mass"] > 60.) & (df_bkg["dilepton_mass"] < 500.)]
df_bkg   = df_bkg[(df_bkg["nbjets"] == nbjet_cut)]
# print(f"len(df_bkg) : {len(df_bkg)}")
df_ttbar   = df_ttbar[(df_ttbar["r"]==f"{parameters['regions']}") & (df_ttbar["dilepton_mass"] > 60.) & (df_ttbar["dilepton_mass"] < 500.)]
df_ttbar   = df_ttbar[(df_ttbar["nbjets"] == nbjet_cut)]
# print(f"len(df_ttbar) : {len(df_ttbar)}")

#df_dy   = df_dy[(df_dy["r"]==f"{parameters['regions']}") & (df_dy["dilepton_mass"] > 200.) & (df_dy["dilepton_mass_gen"] > 200) & (df_dy["nbjets"] == 0) & (df_dy["bjet1_mb1_dR"] == False) & (df_dy["bjet1_mb2_dR"] == False)]

massBinningMuMu = (
    [j for j in range(60, 500, 5)]
    + [500]
)


print("starting .. ")

dy_mass = df_dy["dilepton_mass"].compute().values
data_mass =  df_data["dilepton_mass"].compute().values 
bkg_mass =  df_bkg["dilepton_mass"].compute().values 
ttbar_mass =  df_ttbar["dilepton_mass"].compute().values 


wgt_dy = df_dy["wgt_nominal"].compute().values
wgt_data = df_data["wgt_nominal"].compute().values
wgt_bkg = df_bkg["wgt_nominal"].compute().values
wgt_ttbar = df_ttbar["wgt_nominal"].compute().values

print("done complete")

h_dy = TH1F("h_dy", "h_dy", len(massBinningMuMu)-1, array('d', massBinningMuMu))
h_data = TH1F("h_data", "h_data", len(massBinningMuMu)-1, array('d', massBinningMuMu))
h_bkg = TH1F("h_bkg", "h_bkg", len(massBinningMuMu)-1, array('d', massBinningMuMu))
h_ttbar = TH1F("h_ttbar", "h_ttbar", len(massBinningMuMu)-1, array('d', massBinningMuMu))

for i in range(len(dy_mass)):
    h_dy.Fill(dy_mass[i], wgt_dy[i])

for i in range(len(data_mass)):
    h_data.Fill(data_mass[i], wgt_data[i])

for i in range(len(bkg_mass)):
    h_bkg.Fill(bkg_mass[i], wgt_bkg[i])

for i in range(len(ttbar_mass)):
    h_ttbar.Fill(ttbar_mass[i], wgt_ttbar[i])

file2 = TFile(f"dy_sys_BB.root","RECREATE")
file2.cd()
h_dy.Write()
h_data.Write()
h_bkg.Write()
h_ttbar.Write()
print(f"total h_data entries: {h_data.Integral()}")
print(f"total h_dy entries: {h_dy.Integral()}")
print(f"total h_bkg entries: {h_bkg.Integral()}")
print(f"total h_ttbar entries: {h_ttbar.Integral()}")
SF_ttbar = (h_data.Integral() - h_dy.Integral() - h_bkg.Integral()) / h_ttbar.Integral()
print(f"SF_ttbar: {SF_ttbar}")
file2.Close()








