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

#parser.add_argument(
#    "-r",
#    "--region",
#    dest="region",
#    default=None,
#    action="store",
#    help="chose region (bb or be)",
#)
#

args = parser.parse_args()


#parameters = {
#"regions" : args.region
#}
#
#print("region is: ", f"{parameters['regions']}") 

node_ip = "128.211.148.61"
client = Client(f"{node_ip}:{args.slurm_port}")

print("connected to cluster")

load_fields = [
        "dimuon_mass",
#        "r",
        "dataset",
        "dimuon_mass_gen",
#        "nbjets",
        "wgt_nominal",
#        "bjet1_mb1_dR",
#        "bjet1_mb2_dR",
    ]


paths = "/depot/cms/users/kaur214/output/test_npdf_weights_raw_test/stage1_output/2018/ttbar_lep*/*.parquet"
paths1 = "/depot/cms/users/kaur214/output/test_npdf_weights_raw_test/stage1_output/2018/tW*/*.parquet"
paths2 = "/depot/cms/users/kaur214/output/test_npdf_weights_raw_test/stage1_output/2018/Wantitop*/*.parquet"
#paths = "/depot/cms/users/kaur214/output/test_npdf_weights/stage1_output/2018/bsll_lambda6TeV_M*/*.parquet"
#paths = "/depot/cms/users/kaur214/output/test_npdf_weights/stage1_output/2018/bbll_22TeV_M*_posLL/*.parquet"



sig_files = glob.glob(paths)
sig_files1 = glob.glob(paths1)
sig_files2 = glob.glob(paths2)

df_temp0 = dd.read_parquet(sig_files)
df_temp1 = dd.read_parquet(sig_files1)
df_temp2 = dd.read_parquet(sig_files2)

frames = [df_temp0, df_temp1, df_temp2]

df_temp = dd.concat(frames)

df_temp = df_temp[(~((df_temp.dataset == "ttbar_lep_inclusive") & (df_temp.dimuon_mass_gen > 500)))]


for i in range(100):
    load_fields.append("pdf_mcreplica"+str(i))
    
df_dy   = df_temp[load_fields]

print("computation complete")

df_dy   = df_dy[(df_dy["dimuon_mass"] > 200.)]

massBinningMuMu = [200, 300, 400,500,700,1100,1900,3500]
#massBinningMuMu = [200, 300, 400,500,700,1100,1900,3500]
#massBinningMuMu = [ 200,  300,  400,  600,  900, 1250, 3500]
#massBinningMuMu = [ 200,  300,  400,  600,  900, 1250, 1610, 2000, 3500]
#massBinningMuMu = [ 200,  300,  400,  600,  900, 1250, 1610, 2000, 2500, 3500]

print("starting .. ")

dy_mass = df_dy["dimuon_mass"].compute().values
lumi_wgt = df_dy["wgt_nominal"].compute().values 

h_dy = TH1F("h_dy", "h_dy", len(massBinningMuMu)-1, array('d', massBinningMuMu))
h_var = TH1F("h_var", "h_var", len(massBinningMuMu)-1, array('d', massBinningMuMu))

h_diff = TH1F("h_diff", "h_diff", len(massBinningMuMu)-1, array('d', massBinningMuMu))
h_final = TH1F("h_final", "h_final", len(massBinningMuMu)-1, array('d', massBinningMuMu))


rows, cols = ((len(massBinningMuMu)-1), 100)
div = [[0 for _ in range(cols)] for _ in range(rows)]

for i in range(1, 100):
    wgt_pdf = "pdf_mcreplica"+str(i)
    wgt_dy  = df_dy[wgt_pdf].compute().values
    wgt_nom  = df_dy["pdf_mcreplica0"].compute().values

    wgt_var = wgt_dy/wgt_nom  

    for j in range(len(dy_mass)):
        h_diff.Fill(dy_mass[j], lumi_wgt[j])
        h_dy.Fill(dy_mass[j], lumi_wgt[j] )
        h_var.Fill(dy_mass[j] , lumi_wgt[j]*wgt_var[j])
    h_diff.Add(h_var, -1)
    norm = []
    for k in range(len(massBinningMuMu)-1):
        norm.append(abs(h_dy.GetBinContent(k+1)))
        vals = abs(h_diff.GetBinContent(k+1))
        div[k][i]= vals*vals 
    

    h_dy.Reset("ICESM");
    h_diff.Reset("ICESM");
    h_var.Reset("ICESM");

   
df = pd.DataFrame(div)
print(df)
df['o'] = df.sum(axis=1)
df['sqrt_o'] = np.sqrt(df['o'])
print(df['sqrt_o'])
print(norm)

#df_sort = df.std(axis=1)
#std_per_row = df.std(axis=1)

#print(df)
#df_sort = df.apply(lambda row: sorted(row), axis=1, result_type='expand')

#std_per_rows = df_sort.std(axis=1)
#print(std_per_rows)
#print(df_sort)

#for k in range(len(massBinningMuMu)-1):
#    #print(df_sort.iloc[k,68])
#    #h_final.SetBinContent(k+1, (df_sort.iloc[k,68]*100))
#    h_final.SetBinContent(k+1, std_per_row[k])
#
#file2 = TFile("test_pdf.root","RECREATE")
#file2.cd()
#h_final.Write()
##h_dy.Write()
##h_var.Write()
#
#file2.Close()

#print("answer is ", df_sort.iloc[:,68])






