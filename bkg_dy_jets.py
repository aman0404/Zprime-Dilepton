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
import copy

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
    help="choose region (bb or be)",
)

parser.add_argument(
    "-nbj",
    "--nbjets",
    dest="nbjets",
    default=None,
    action="store",
    help="specify nbjets cut",
)

parser.add_argument(
    "-yr",
    "--year",
    dest="year",
    default=None,
    action="store",
    help="specify era",
)

args = parser.parse_args()

if __name__ == '__main__':
    parameters = {
    "regions" : args.region
    }

    print(f"region is: {parameters['regions']}") 

    print(f"nbjet cut is: {args.nbjets}")
    year = args.year
    print(f"year is : {year}")
    
    # Dask client settings
    use_local_cluster = args.slurm_port is None
    node_ip = "128.211.148.60"

    if use_local_cluster:
        ncpus_local = 40
        slurm_cluster_ip = ""
        client = Client(
                processes=True,
                n_workers=50,
                threads_per_worker=1,
                memory_limit="6GB",
            )
    else:
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






    paths_data = f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/data_*/*parquet"

    paths_dy_incl = f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/dyInclusive50/*parquet"
    paths_dy_rest = f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/dy*/*parquet"


    paths_ttbar_incl = f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/ttbar_lep_inclusive/*parquet"
    paths_ttbar_rest = f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/ttbar*/*parquet"


    paths_w_incl = f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/WWinclusive/*parquet"
    paths_w_rest = f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/W*/*parquet" 

    #other bkdgs with no need for inclusive data cut
    paths_z = f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/Z*/*parquet" # they are ZZZ, ZH_HToZZ, ZH_HToBB_ZToLL, ZZ2L2Nu, ZZ2L2Q, ZZ4L

    paths_Higgs = list(set(glob.glob(f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/TT*/*parquet")))
    paths_Higgs += list(set(glob.glob(f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/ttH*/*parquet")))
    paths_Higgs += list(set(glob.glob(f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/ggZH_HToBB/*parquet")))
    paths_Higgs += list(set(glob.glob(f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/GluGlu*/*parquet")))
    paths_Higgs += list(set(glob.glob(f"/depot/cms/users/yun79/Zprime-Dilepton/output/test2023june_golden_data/stage1_output_emu/{year}/VBF_HToZZTo4L/*parquet")))

    data_files = glob.glob(paths_data)
    df_data_temp = dd.read_parquet(data_files)


    dy_incl_files = glob.glob(paths_dy_incl)
    df_dy_incl_temp = dd.read_parquet(dy_incl_files)

    dy_rest_files = list(set(glob.glob(paths_dy_rest)) - set(glob.glob(paths_dy_incl)))
    # print(f"dy_rest_files: {dy_rest_files}")
    df_dy_rest_temp = dd.read_parquet(dy_rest_files)

    ttbar_incl_files = glob.glob(paths_ttbar_incl)
    df_ttbar_incl_temp = dd.read_parquet(ttbar_incl_files)

    ttbar_rest_files = list(set(glob.glob(paths_ttbar_rest)) - set(glob.glob(paths_ttbar_incl)))
    # print(f"ttbar_rest_files: {ttbar_rest_files}")
    df_ttbar_rest_temp = dd.read_parquet(ttbar_rest_files)

    w_incl_files = glob.glob(paths_w_incl)
    df_w_incl_temp = dd.read_parquet(w_incl_files)

    w_rest_files = list(set(glob.glob(paths_w_rest)) - set(glob.glob(paths_w_incl)))
    # print(f"w_rest_files: {w_rest_files}")
    df_w_rest_temp = dd.read_parquet(w_rest_files)

    z_files = glob.glob(paths_z)
    # print(f"z_files: {z_files}")
    df_z_temp = dd.read_parquet(z_files)

    Higgs_files = paths_Higgs
    # print(f"Higgs_files: {Higgs_files}")
    df_Higgs_temp = dd.read_parquet(Higgs_files)

    #check if we are double counting any files
    print("checking for double counting")
    double_count_suspects = [
        z_files, 
        Higgs_files,
        dy_incl_files,
        dy_rest_files,
        ttbar_incl_files,
        ttbar_rest_files,
        w_incl_files,
        w_rest_files,
    ]
    for file_idx in range(len(double_count_suspects)):
        suspect = double_count_suspects[file_idx]
        comp_files = copy.deepcopy(double_count_suspects)
        comp_files.pop(file_idx)
        # print(f"suspect: {suspect}")
        # print(f"comp_files: {comp_files}")
        for comp_file in comp_files :
            overlap = list(set(suspect) & set(comp_file))
            if len(overlap) != 0 :
                print(f"overlap by : {len(overlap)}")


    df_data = df_data_temp[load_fields]
    df_dy_incl  = df_dy_incl_temp[load_fields]
    df_dy_rest  = df_dy_rest_temp[load_fields]

    df_ttbar_incl = df_ttbar_incl_temp[load_fields]
    df_ttbar_rest = df_ttbar_rest_temp[load_fields]

    df_w_incl = df_w_incl_temp[load_fields]
    df_w_rest = df_w_rest_temp[load_fields]

    df_z = df_z_temp[load_fields]
    df_Higgs = df_Higgs_temp[load_fields]

    # bkg_l = [df_z, df_Higgs]
    bkg_l = [df_z]
    df_bkg = dd.concat(bkg_l)

    print("computation complete")

    df_data   = df_data[(df_data["r"]==f"{parameters['regions']}")]

    df_dy_incl   = df_dy_incl[(df_dy_incl["r"]==f"{parameters['regions']}") & (df_dy_incl["dilepton_mass_gen"] < 200.) ] # 200 GeV cut
    df_dy_rest   = df_dy_rest[(df_dy_rest["r"]==f"{parameters['regions']}") & (df_dy_rest["dilepton_mass_gen"] > 200.)]
    df_dy = dd.concat([df_dy_incl, df_dy_rest])


    df_ttbar_incl   = df_ttbar_incl[(df_ttbar_incl["r"]==f"{parameters['regions']}") & (df_ttbar_incl["dilepton_mass_gen"] < 500.)] # 500 GeV cut
    df_ttbar_rest   = df_ttbar_rest[(df_ttbar_rest["r"]==f"{parameters['regions']}") & (df_ttbar_rest["dilepton_mass_gen"] > 500.)]
    df_ttbar = dd.concat([df_ttbar_incl, df_ttbar_rest])

    df_w_incl   = df_w_incl[(df_w_incl["r"]==f"{parameters['regions']}") & (df_w_incl["dilepton_mass_gen"] < 200.)] # 200 GeV cut
    df_w_rest   = df_w_rest[(df_w_rest["r"]==f"{parameters['regions']}") & (df_w_rest["dilepton_mass_gen"] > 200.)]

    df_bkg = df_bkg[(df_bkg["r"]==f"{parameters['regions']}")]
    df_bkg = dd.concat([df_bkg, df_w_incl, df_w_rest]) # df_w_incl and df_w_rest is part of other bkg


    # apply nbjet cut:
    nbjet_cut= int(args.nbjets)
    if nbjet_cut <= 1:
        print(f"nbjet_cut equal to: {nbjet_cut}")
        df_dy   = df_dy[(df_dy["nbjets"] == nbjet_cut)]
        df_data   = df_data[(df_data["nbjets"] == nbjet_cut)]
        df_bkg   = df_bkg[(df_bkg["nbjets"] == nbjet_cut)]
        df_ttbar   = df_ttbar[(df_ttbar["nbjets"] == nbjet_cut)]
    else:
        print(f"nbjet_cut greater or equal than: {nbjet_cut}")
        df_dy   = df_dy[(df_dy["nbjets"] >= nbjet_cut)]
        df_data   = df_data[(df_data["nbjets"] >= nbjet_cut)]
        df_bkg   = df_bkg[(df_bkg["nbjets"] >= nbjet_cut)]
        df_ttbar   = df_ttbar[(df_ttbar["nbjets"] >= nbjet_cut)]

    # apply the dr cut:
    df_dy   = df_dy[(df_dy["bjet1_ll_dR"])]
    df_data   = df_data[(df_data["bjet1_ll_dR"])]
    df_bkg   = df_bkg[(df_bkg["bjet1_ll_dR"])]
    df_ttbar   = df_ttbar[(df_ttbar["bjet1_ll_dR"])]

        

    #df_dy   = df_dy[(df_dy["r"]==f"{parameters['regions']}") & (df_dy["dilepton_mass"] > 200.) & (df_dy["dilepton_mass_gen"] > 200) & (df_dy["nbjets"] == 0) & (df_dy["bjet1_mb1_dR"] == False) & (df_dy["bjet1_mb2_dR"] == False)]

    massBinning = (
        [j for j in range(100, 4000, 10)]
        + [4000]
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

    h_dy = TH1F("h_dy", "h_dy", len(massBinning)-1, array('d', massBinning))
    h_data = TH1F("h_data", "h_data", len(massBinning)-1, array('d', massBinning))
    h_bkg = TH1F("h_bkg", "h_bkg", len(massBinning)-1, array('d', massBinning))
    h_ttbar = TH1F("h_ttbar", "h_ttbar", len(massBinning)-1, array('d', massBinning))

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








