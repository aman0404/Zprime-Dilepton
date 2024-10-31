import argparse
import dask
from dask.distributed import Client
from config.variables import variables_lookup
from produceResults.plotter import plotter

# , plotter2D
from produceResults.make_templates import to_templates

__all__ = ["dask"]


parser = argparse.ArgumentParser()
parser.add_argument(
    "-y", "--years", nargs="+", help="Years to process", default=["2018"]
)

parser.add_argument(
    "-f", "--flavor", dest="flavor", help="lepton flavor", default="el"
)

parser.add_argument(
    "-l",
    "--label",
    dest="label",
    default="2018_analyzer_UL",
    action="store",
    help="Unique run label (to create output path)",
)

parser.add_argument(
    "-sl",
    "--slurm",
    dest="slurm_port",
    default=None,
    action="store",
    help="Slurm cluster port (if not specified, will create a local cluster)",
)
args = parser.parse_args()

# Dask client settings
use_local_cluster = args.slurm_port is None
node_ip = "128.211.148.60"

if use_local_cluster:
    ncpus_local = 1
    slurm_cluster_ip = ""
    dashboard_address = f"{node_ip}:34875"
else:
    slurm_cluster_ip = f"{node_ip}:{args.slurm_port}"
    dashboard_address = f"{node_ip}:8787"

# global parameters
parameters = {
    # < general settings >
    "slurm_cluster_ip": slurm_cluster_ip,
    "years": args.years,
    "global_path": "/depot/cms/private/users/kaur214/output/",
    "label": args.label,
    "channels": ["0b", "1b", "2b"],
    "regions": ["bb", "be"],
    "syst_variations": ["nominal"],
    "plot_vars": [
        "dimuon_mass",
    ],  # "d
    "plot_vars_2d": [["dielectron_mass", "met"]],  # "dimuon_mass"],
    "variables_lookup": variables_lookup,
    "save_plots": True,
    "plot_ratio": True,
    "plots_path": "/depot/cms/private/users/kaur214/output/plots/",
    "dnn_models": {},
    "bdt_models": {},
    #
    # < templates and datacards >
    "save_templates": True,
    "templates_vars": [
        "dimuon_mass",
        "dilepton_mass",
        "dielectron_mass",
    ],  # "dielectron_mass"],
}
if args.flavor == "mu":
    parameters["hist_vars"] = [
#        "min_bl_mass",
        "dimuon_mass",
#        "dimuon_mass_gen",
#        "njets",
#        "nbjets",
#        "met",
#        "lb_angle",
#        "bjet1_pt",
#        "mu1_pt",
#        "mu2_pt",
#        "mu1_eta",
#        "mu2_eta",
#        "mu1_phi",
#        "bjet1_eta",

    ]

if args.flavor == "emu":
    parameters["hist_vars"] = [
#        "min_bl_mass",
        "dilepton_mass",
#        "nbjets",
#        "met",
#        "lb_angle",
#        "bjet1_pt",
#        "bjet1_eta",

    ]

if args.flavor == "el":
    parameters["plot_vars"] = [
#        "min_bl_mass",
#        "njets",
#        "nbjets",
#        "met",
#        "lb_angle",
#        "b1l1_dR",
#        "b1l2_dR",
#        "dielectron_dR",
#        "bjet1_pt",
#        "e1_pt",
#        "e2_pt",
#        "e1_eta",
#        "e1_phi",
#        "bjet1_eta",
        "dielectron_mass",
    ]

parameters["grouping"] = {
    "data_A": "Data",
    "data_B": "Data",
    "data_Bv1": "Data",
    "data_Bv2": "Data",
    "data_C": "Data",
    "data_D": "Data",
    "data_E": "Data",
    "data_F": "Data",
    "data_G": "Data",
    "data_H": "Data",

    "dy0J_M200to400": "DYJets",
    "dy0J_M400to800": "DYJets",
    "dy0J_M800to1400": "DYJets",
    "dy0J_M1400to2300": "DYJets",
    "dy0J_M2300to3500": "DYJets",
    "dy0J_M3500to4500": "DYJets",
    "dy0J_M4500to6000": "DYJets",
    "dy0J_M6000toInf": "DYJets",

    "dy1J_M200to400": "DYJets",
    "dy1J_M400to800": "DYJets",
    "dy1J_M800to1400": "DYJets",
    "dy1J_M1400to2300": "DYJets",
    "dy1J_M2300to3500": "DYJets",
    "dy1J_M3500to4500": "DYJets",
    "dy1J_M4500to6000": "DYJets",
    "dy1J_M6000toInf": "DYJets",

    "dy2J_M200to400": "DYJets",
    "dy2J_M400to800": "DYJets",
    "dy2J_M800to1400": "DYJets",
    "dy2J_M1400to2300": "DYJets",
    "dy2J_M2300to3500": "DYJets",
    "dy2J_M3500to4500": "DYJets",
    "dy2J_M4500to6000": "DYJets",
    "dy2J_M6000toInf": "DYJets",

    "ttbar_lep_inclusive": "Top",
    "ttbar_lep_M500to800": "Top",
    "ttbar_lep_M800to1200": "Top",
    "ttbar_lep_M1200to1800": "Top",
    "ttbar_lep_M1800toInf": "Top",
    "tW": "Top",
    "Wantitop": "Top",

     "ttWjets" : "Top",
     "ttZ" : "Top",
     "ttZQQ" : "Top",
     "ttGJets" : "Top",
     "ttWQQ" : "Top",
     "ttH" : "Top",
     "ZG" : "Top",

     "WWW" : "Diboson",
     "WZZ" : "Diboson",
     "ZZZ" : "Diboson",
     "WWZ" : "Diboson",


    "WWinclusive": "Diboson",
    "WW200to600": "Diboson",
    "WW600to1200": "Diboson",
    "WW1200to2500": "Diboson",
    "WW2500": "Diboson",
    "WZ2L2Q": "Diboson",
    "WZ3LNu": "Diboson",
    "ZZ2L2Nu": "Diboson",
    "ZZ4L":  "Diboson",

    "bsll_lambda1TeV_M200to500" : "bsll_lambda1TeV",
    "bsll_lambda1TeV_M500to1000" : "bsll_lambda1TeV",
    "bsll_lambda1TeV_M1000to2000" : "bsll_lambda1TeV",
    "bsll_lambda1TeV_M2000toInf" : "bsll_lambda1TeV",

    "bsll_lambda2TeV_M200to500" : "bsll_lambda2TeV",
    "bsll_lambda2TeV_M500to1000" : "bsll_lambda2TeV",
    "bsll_lambda2TeV_M1000to2000" : "bsll_lambda2TeV",
    "bsll_lambda2TeV_M2000toInf" : "bsll_lambda2TeV",

  
    "bsll_lambda3TeV_M200to500" : "bsll_lambda3TeV",
    "bsll_lambda3TeV_M500to1000" : "bsll_lambda3TeV",
    "bsll_lambda3TeV_M1000to2000" : "bsll_lambda3TeV",
    "bsll_lambda3TeV_M2000toInf" : "bsll_lambda3TeV",


    "bsll_lambda4TeV_M200to500" : "bsll_lambda4TeV",
    "bsll_lambda4TeV_M500to1000" : "bsll_lambda4TeV",
    "bsll_lambda4TeV_M1000to2000" : "bsll_lambda4TeV",
    "bsll_lambda4TeV_M2000toInf" : "bsll_lambda4TeV",

    "bsll_lambda5TeV_M200to500" : "bsll_lambda5TeV",
    "bsll_lambda5TeV_M500to1000" : "bsll_lambda5TeV",
    "bsll_lambda5TeV_M1000to2000" : "bsll_lambda5TeV",
    "bsll_lambda5TeV_M2000toInf" : "bsll_lambda5TeV",


    "bsll_lambda6TeV_M200to500" : "bsll_lambda6TeV",
    "bsll_lambda6TeV_M500to1000" : "bsll_lambda6TeV",
    "bsll_lambda6TeV_M1000to2000" : "bsll_lambda6TeV",
    "bsll_lambda6TeV_M2000toInf" : "bsll_lambda6TeV",

    "bbll_6TeV_M300To800_posLL"  : "bbll_lambda6TeV_posLL",
    "bbll_6TeV_M800To1300_posLL" : "bbll_lambda6TeV_posLL",
    "bbll_6TeV_M1300To2000_posLL": "bbll_lambda6TeV_posLL",
    "bbll_6TeV_M2000ToInf_posLL" : "bbll_lambda6TeV_posLL",

    "bbll_10TeV_M300To800_posLL"  : "bbll_lambda10TeV_posLL",
    "bbll_10TeV_M800To1300_posLL" : "bbll_lambda10TeV_posLL",
    "bbll_10TeV_M1300To2000_posLL": "bbll_lambda10TeV_posLL",
    "bbll_10TeV_M2000ToInf_posLL" : "bbll_lambda10TeV_posLL",

    "bbll_14TeV_M300To800_posLL"  : "bbll_lambda14TeV_posLL",
    "bbll_14TeV_M800To1300_posLL" : "bbll_lambda14TeV_posLL",
    "bbll_14TeV_M1300To2000_posLL": "bbll_lambda14TeV_posLL",
    "bbll_14TeV_M2000ToInf_posLL" : "bbll_lambda14TeV_posLL",


    "bbll_18TeV_M300To800_posLL"  : "bbll_lambda18TeV_posLL",
    "bbll_18TeV_M800To1300_posLL" : "bbll_lambda18TeV_posLL",
    "bbll_18TeV_M1300To2000_posLL": "bbll_lambda18TeV_posLL",
    "bbll_18TeV_M2000ToInf_posLL" : "bbll_lambda18TeV_posLL",


    "bbll_22TeV_M300To800_posLL"  : "bbll_lambda22TeV_posLL",
    "bbll_22TeV_M800To1300_posLL" : "bbll_lambda22TeV_posLL",
    "bbll_22TeV_M1300To2000_posLL": "bbll_lambda22TeV_posLL",
    "bbll_22TeV_M2000ToInf_posLL" : "bbll_lambda22TeV_posLL",


    "bbll_26TeV_M300To800_posLL"  : "bbll_lambda26TeV_posLL",
    "bbll_26TeV_M800To1300_posLL" : "bbll_lambda26TeV_posLL",
    "bbll_26TeV_M1300To2000_posLL": "bbll_lambda26TeV_posLL",
    "bbll_26TeV_M2000ToInf_posLL" : "bbll_lambda26TeV_posLL",


    "bbll_6TeV_M300To800_posLR"  : "bbll_lambda6TeV_posLR",
    "bbll_6TeV_M800To1300_posLR" : "bbll_lambda6TeV_posLR",
    "bbll_6TeV_M1300To2000_posLR": "bbll_lambda6TeV_posLR",
    "bbll_6TeV_M2000ToInf_posLR" : "bbll_lambda6TeV_posLR",

    "bbll_10TeV_M300To800_posLR"  : "bbll_lambda10TeV_posLR",
    "bbll_10TeV_M800To1300_posLR" : "bbll_lambda10TeV_posLR",
    "bbll_10TeV_M1300To2000_posLR": "bbll_lambda10TeV_posLR",
    "bbll_10TeV_M2000ToInf_posLR" : "bbll_lambda10TeV_posLR",

    "bbll_14TeV_M300To800_posLR"  : "bbll_lambda14TeV_posLR",
    "bbll_14TeV_M800To1300_posLR" : "bbll_lambda14TeV_posLR",
    "bbll_14TeV_M1300To2000_posLR": "bbll_lambda14TeV_posLR",
    "bbll_14TeV_M2000ToInf_posLR" : "bbll_lambda14TeV_posLR",


    "bbll_18TeV_M300To800_posLR"  : "bbll_lambda18TeV_posLR",
    "bbll_18TeV_M800To1300_posLR" : "bbll_lambda18TeV_posLR",
    "bbll_18TeV_M1300To2000_posLR": "bbll_lambda18TeV_posLR",
    "bbll_18TeV_M2000ToInf_posLR" : "bbll_lambda18TeV_posLR",


    "bbll_22TeV_M300To800_posLR"  : "bbll_lambda22TeV_posLR",
    "bbll_22TeV_M800To1300_posLR" : "bbll_lambda22TeV_posLR",
    "bbll_22TeV_M1300To2000_posLR": "bbll_lambda22TeV_posLR",
    "bbll_22TeV_M2000ToInf_posLR" : "bbll_lambda22TeV_posLR",


    "bbll_26TeV_M300To800_posLR"  : "bbll_lambda26TeV_posLR",
    "bbll_26TeV_M800To1300_posLR" : "bbll_lambda26TeV_posLR",
    "bbll_26TeV_M1300To2000_posLR": "bbll_lambda26TeV_posLR",
    "bbll_26TeV_M2000ToInf_posLR" : "bbll_lambda26TeV_posLR",


    "bbll_6TeV_M300To800_posRL"  : "bbll_lambda6TeV_posRL",
    "bbll_6TeV_M800To1300_posRL" : "bbll_lambda6TeV_posRL",
    "bbll_6TeV_M1300To2000_posRL": "bbll_lambda6TeV_posRL",
    "bbll_6TeV_M2000ToInf_posRL" : "bbll_lambda6TeV_posRL",

    "bbll_10TeV_M300To800_posRL"  : "bbll_lambda10TeV_posRL",
    "bbll_10TeV_M800To1300_posRL" : "bbll_lambda10TeV_posRL",
    "bbll_10TeV_M1300To2000_posRL": "bbll_lambda10TeV_posRL",
    "bbll_10TeV_M2000ToInf_posRL" : "bbll_lambda10TeV_posRL",

    "bbll_14TeV_M300To800_posRL"  : "bbll_lambda14TeV_posRL",
    "bbll_14TeV_M800To1300_posRL" : "bbll_lambda14TeV_posRL",
    "bbll_14TeV_M1300To2000_posRL": "bbll_lambda14TeV_posRL",
    "bbll_14TeV_M2000ToInf_posRL" : "bbll_lambda14TeV_posRL",


    "bbll_18TeV_M300To800_posRL"  : "bbll_lambda18TeV_posRL",
    "bbll_18TeV_M800To1300_posRL" : "bbll_lambda18TeV_posRL",
    "bbll_18TeV_M1300To2000_posRL": "bbll_lambda18TeV_posRL",
    "bbll_18TeV_M2000ToInf_posRL" : "bbll_lambda18TeV_posRL",


    "bbll_22TeV_M300To800_posRL"  : "bbll_lambda22TeV_posRL",
    "bbll_22TeV_M800To1300_posRL" : "bbll_lambda22TeV_posRL",
    "bbll_22TeV_M1300To2000_posRL": "bbll_lambda22TeV_posRL",
    "bbll_22TeV_M2000ToInf_posRL" : "bbll_lambda22TeV_posRL",


    "bbll_26TeV_M300To800_posRL"  : "bbll_lambda26TeV_posRL",
    "bbll_26TeV_M800To1300_posRL" : "bbll_lambda26TeV_posRL",
    "bbll_26TeV_M1300To2000_posRL": "bbll_lambda26TeV_posRL",
    "bbll_26TeV_M2000ToInf_posRL" : "bbll_lambda26TeV_posRL",


    "bbll_6TeV_M300To800_posRR"  : "bbll_lambda6TeV_posRR",
    "bbll_6TeV_M800To1300_posRR" : "bbll_lambda6TeV_posRR",
    "bbll_6TeV_M1300To2000_posRR": "bbll_lambda6TeV_posRR",
    "bbll_6TeV_M2000ToInf_posRR" : "bbll_lambda6TeV_posRR",

    "bbll_10TeV_M300To800_posRR"  : "bbll_lambda10TeV_posRR",
    "bbll_10TeV_M800To1300_posRR" : "bbll_lambda10TeV_posRR",
    "bbll_10TeV_M1300To2000_posRR": "bbll_lambda10TeV_posRR",
    "bbll_10TeV_M2000ToInf_posRR" : "bbll_lambda10TeV_posRR",

    "bbll_14TeV_M300To800_posRR"  : "bbll_lambda14TeV_posRR",
    "bbll_14TeV_M800To1300_posRR" : "bbll_lambda14TeV_posRR",
    "bbll_14TeV_M1300To2000_posRR": "bbll_lambda14TeV_posRR",
    "bbll_14TeV_M2000ToInf_posRR" : "bbll_lambda14TeV_posRR",


    "bbll_18TeV_M300To800_posRR"  : "bbll_lambda18TeV_posRR",
    "bbll_18TeV_M800To1300_posRR" : "bbll_lambda18TeV_posRR",
    "bbll_18TeV_M1300To2000_posRR": "bbll_lambda18TeV_posRR",
    "bbll_18TeV_M2000ToInf_posRR" : "bbll_lambda18TeV_posRR",


    "bbll_22TeV_M300To800_posRR"  : "bbll_lambda22TeV_posRR",
    "bbll_22TeV_M800To1300_posRR" : "bbll_lambda22TeV_posRR",
    "bbll_22TeV_M1300To2000_posRR": "bbll_lambda22TeV_posRR",
    "bbll_22TeV_M2000ToInf_posRR" : "bbll_lambda22TeV_posRR",


    "bbll_26TeV_M300To800_posRR"  : "bbll_lambda26TeV_posRR",
    "bbll_26TeV_M800To1300_posRR" : "bbll_lambda26TeV_posRR",
    "bbll_26TeV_M1300To2000_posRR": "bbll_lambda26TeV_posRR",
    "bbll_26TeV_M2000ToInf_posRR" : "bbll_lambda26TeV_posRR",



    "bbll_100000TeV_M1300To2000_negLL" : "bbll_100000TeV_negLL",
    "bbll_100000TeV_M2000ToInf_negLL"  : "bbll_100000TeV_negLL",
    "bbll_100000TeV_M300To800_negLL"   : "bbll_100000TeV_negLL",
    "bbll_100000TeV_M800To1300_negLL"  : "bbll_100000TeV_negLL",

    "bbll_4TeV_M1300To2000_negLL" : "bbll_lambda4TeV_negLL",
    "bbll_4TeV_M2000ToInf_negLL"  : "bbll_lambda4TeV_negLL",
    "bbll_4TeV_M300To800_negLL"   : "bbll_lambda4TeV_negLL",
    "bbll_4TeV_M800To1300_negLL"  : "bbll_lambda4TeV_negLL",

    "bbll_6TeV_M1300To2000_negLL" : "bbll_lambda6TeV_negLL",
    "bbll_6TeV_M2000ToInf_negLL"  : "bbll_lambda6TeV_negLL",
    "bbll_6TeV_M300To800_negLL"   : "bbll_lambda6TeV_negLL",
    "bbll_6TeV_M800To1300_negLL"  : "bbll_lambda6TeV_negLL",

    "bbll_8TeV_M1300To2000_negLL" : "bbll_lambda8TeV_negLL",
    "bbll_8TeV_M2000ToInf_negLL"  : "bbll_lambda8TeV_negLL",
    "bbll_8TeV_M300To800_negLL"   : "bbll_lambda8TeV_negLL",
    "bbll_8TeV_M800To1300_negLL"  : "bbll_lambda8TeV_negLL",

    "bbll_10TeV_M1300To2000_negLL" : "bbll_lambda10TeV_negLL",
    "bbll_10TeV_M2000ToInf_negLL"  : "bbll_lambda10TeV_negLL",
    "bbll_10TeV_M300To800_negLL"   : "bbll_lambda10TeV_negLL",
    "bbll_10TeV_M800To1300_negLL"  : "bbll_lambda10TeV_negLL",

    "bbll_14TeV_M1300To2000_negLL" : "bbll_lambda14TeV_negLL",
    "bbll_14TeV_M2000ToInf_negLL"  : "bbll_lambda14TeV_negLL",
    "bbll_14TeV_M300To800_negLL"   : "bbll_lambda14TeV_negLL",
    "bbll_14TeV_M800To1300_negLL"  : "bbll_lambda14TeV_negLL",

    "bbll_18TeV_M1300To2000_negLL" : "bbll_lambda18TeV_negLL",
    "bbll_18TeV_M2000ToInf_negLL"  : "bbll_lambda18TeV_negLL",
    "bbll_18TeV_M300To800_negLL"   : "bbll_lambda18TeV_negLL",
    "bbll_18TeV_M800To1300_negLL"  : "bbll_lambda18TeV_negLL",

    "bbll_4TeV_M1300To2000_negLR" : "bbll_lambda4TeV_negLR",
    "bbll_4TeV_M2000ToInf_negLR"  : "bbll_lambda4TeV_negLR",
    "bbll_4TeV_M300To800_negLR"   : "bbll_lambda4TeV_negLR",
    "bbll_4TeV_M800To1300_negLR"  : "bbll_lambda4TeV_negLR",

    "bbll_6TeV_M1300To2000_negLR" : "bbll_lambda6TeV_negLR",
    "bbll_6TeV_M2000ToInf_negLR"  : "bbll_lambda6TeV_negLR",
    "bbll_6TeV_M300To800_negLR"   : "bbll_lambda6TeV_negLR",
    "bbll_6TeV_M800To1300_negLR"  : "bbll_lambda6TeV_negLR",

    "bbll_8TeV_M1300To2000_negLR" : "bbll_lambda8TeV_negLR",
    "bbll_8TeV_M2000ToInf_negLR"  : "bbll_lambda8TeV_negLR",
    "bbll_8TeV_M300To800_negLR"   : "bbll_lambda8TeV_negLR",
    "bbll_8TeV_M800To1300_negLR"  : "bbll_lambda8TeV_negLR",

    "bbll_10TeV_M1300To2000_negLR" : "bbll_lambda10TeV_negLR",
    "bbll_10TeV_M2000ToInf_negLR"  : "bbll_lambda10TeV_negLR",
    "bbll_10TeV_M300To800_negLR"   : "bbll_lambda10TeV_negLR",
    "bbll_10TeV_M800To1300_negLR"  : "bbll_lambda10TeV_negLR",

    "bbll_14TeV_M1300To2000_negLR" : "bbll_lambda14TeV_negLR",
    "bbll_14TeV_M2000ToInf_negLR"  : "bbll_lambda14TeV_negLR",
    "bbll_14TeV_M300To800_negLR"   : "bbll_lambda14TeV_negLR",
    "bbll_14TeV_M800To1300_negLR"  : "bbll_lambda14TeV_negLR",

    "bbll_18TeV_M1300To2000_negLR" : "bbll_lambda18TeV_negLR",
    "bbll_18TeV_M2000ToInf_negLR"  : "bbll_lambda18TeV_negLR",
    "bbll_18TeV_M300To800_negLR"   : "bbll_lambda18TeV_negLR",
    "bbll_18TeV_M800To1300_negLR"  : "bbll_lambda18TeV_negLR",


    "bbll_4TeV_M1300To2000_negRL" : "bbll_lambda4TeV_negRL",
    "bbll_4TeV_M2000ToInf_negRL"  : "bbll_lambda4TeV_negRL",
    "bbll_4TeV_M300To800_negRL"   : "bbll_lambda4TeV_negRL",
    "bbll_4TeV_M800To1300_negRL"  : "bbll_lambda4TeV_negRL",

    "bbll_6TeV_M1300To2000_negRL" : "bbll_lambda6TeV_negRL",
    "bbll_6TeV_M2000ToInf_negRL"  : "bbll_lambda6TeV_negRL",
    "bbll_6TeV_M300To800_negRL"   : "bbll_lambda6TeV_negRL",
    "bbll_6TeV_M800To1300_negRL"  : "bbll_lambda6TeV_negRL",

    "bbll_8TeV_M1300To2000_negRL" : "bbll_lambda8TeV_negRL",
    "bbll_8TeV_M2000ToInf_negRL"  : "bbll_lambda8TeV_negRL",
    "bbll_8TeV_M300To800_negRL"   : "bbll_lambda8TeV_negRL",
    "bbll_8TeV_M800To1300_negRL"  : "bbll_lambda8TeV_negRL",

    "bbll_10TeV_M1300To2000_negRL" : "bbll_lambda10TeV_negRL",
    "bbll_10TeV_M2000ToInf_negRL"  : "bbll_lambda10TeV_negRL",
    "bbll_10TeV_M300To800_negRL"   : "bbll_lambda10TeV_negRL",
    "bbll_10TeV_M800To1300_negRL"  : "bbll_lambda10TeV_negRL",

    "bbll_14TeV_M1300To2000_negRL" : "bbll_lambda14TeV_negRL",
    "bbll_14TeV_M2000ToInf_negRL"  : "bbll_lambda14TeV_negRL",
    "bbll_14TeV_M300To800_negRL"   : "bbll_lambda14TeV_negRL",
    "bbll_14TeV_M800To1300_negRL"  : "bbll_lambda14TeV_negRL",

    "bbll_18TeV_M1300To2000_negRL" : "bbll_lambda18TeV_negRL",
    "bbll_18TeV_M2000ToInf_negRL"  : "bbll_lambda18TeV_negRL",
    "bbll_18TeV_M300To800_negRL"   : "bbll_lambda18TeV_negRL",
    "bbll_18TeV_M800To1300_negRL"  : "bbll_lambda18TeV_negRL",

    "bbll_4TeV_M1300To2000_negRR" : "bbll_lambda4TeV_negRR",
    "bbll_4TeV_M2000ToInf_negRR"  : "bbll_lambda4TeV_negRR",
    "bbll_4TeV_M300To800_negRR"   : "bbll_lambda4TeV_negRR",
    "bbll_4TeV_M800To1300_negRR"  : "bbll_lambda4TeV_negRR",

    "bbll_6TeV_M1300To2000_negRR" : "bbll_lambda6TeV_negRR",
    "bbll_6TeV_M2000ToInf_negRR"  : "bbll_lambda6TeV_negRR",
    "bbll_6TeV_M300To800_negRR"   : "bbll_lambda6TeV_negRR",
    "bbll_6TeV_M800To1300_negRR"  : "bbll_lambda6TeV_negRR",

    "bbll_8TeV_M1300To2000_negRR" : "bbll_lambda8TeV_negRR",
    "bbll_8TeV_M2000ToInf_negRR"  : "bbll_lambda8TeV_negRR",
    "bbll_8TeV_M300To800_negRR"   : "bbll_lambda8TeV_negRR",
    "bbll_8TeV_M800To1300_negRR"  : "bbll_lambda8TeV_negRR",

    "bbll_10TeV_M1300To2000_negRR" : "bbll_lambda10TeV_negRR",
    "bbll_10TeV_M2000ToInf_negRR"  : "bbll_lambda10TeV_negRR",
    "bbll_10TeV_M300To800_negRR"   : "bbll_lambda10TeV_negRR",
    "bbll_10TeV_M800To1300_negRR"  : "bbll_lambda10TeV_negRR",

    "bbll_14TeV_M1300To2000_negRR" : "bbll_lambda14TeV_negRR",
    "bbll_14TeV_M2000ToInf_negRR"  : "bbll_lambda14TeV_negRR",
    "bbll_14TeV_M300To800_negRR"   : "bbll_lambda14TeV_negRR",
    "bbll_14TeV_M800To1300_negRR"  : "bbll_lambda14TeV_negRR",

    "bbll_18TeV_M1300To2000_negRR" : "bbll_lambda18TeV_negRR",
    "bbll_18TeV_M2000ToInf_negRR"  : "bbll_lambda18TeV_negRR",
    "bbll_18TeV_M300To800_negRR"   : "bbll_lambda18TeV_negRR",
    "bbll_18TeV_M800To1300_negRR"  : "bbll_lambda18TeV_negRR",

}

parameters["plot_groups"] = {
    "stack": ["DYJets", "Top", "Diboson"],
    "step": ["bsll_lambda1TeV", "bsll_lambda2TeV", "bsll_lambda4TeV", "bsll_lambda8TeV"],
    "errorbar": ["Data"],
}
# ways to specificy colors for matplotlib are here: https://matplotlib.org/3.5.0/tutorials/colors/colors.html Using the xkcd color survey for now: https://xkcd.com/color/rgb/
parameters["color_dict"] = {
    "DYJets": "xkcd:water blue",
    "Top": "xkcd:pastel orange",
    "Topinc": "xkcd:orange",
    "Diboson": "xkcd:red",

    "Data": "xkcd:black",

    "bsll_lambda1TeV":"xkcd:blue",
    "bsll_lambda2TeV":"xkcd:blue",
    "bsll_lambda4TeV":"xkcd:blue",
    "bsll_lambda8TeV":"xkcd:blue",

}

if __name__ == "__main__":
    if use_local_cluster:
        print(
            f"Creating local cluster with {ncpus_local} workers."
            f" Dashboard address: {dashboard_address}"
        )
        client = Client(
            processes=True,
            # dashboard_address=dashboard_address,
            n_workers=1,
            threads_per_worker=1,
            memory_limit="40GB",
        )
    else:
        print(
            f"Connecting to Slurm cluster at {slurm_cluster_ip}."
            f" Dashboard address: {dashboard_address}"
        )
        client = Client(parameters["slurm_cluster_ip"])
    parameters["ncpus"] = len(client.scheduler_info()["workers"])
    print(f"Connected to cluster! #CPUs = {parameters['ncpus']}")

    # add MVA scores to the list of variables to plot
    dnn_models = list(parameters["dnn_models"].values())
    bdt_models = list(parameters["bdt_models"].values())
    for models in dnn_models + bdt_models:
        for model in models:
            parameters["plot_vars"] += ["score_" + model]
            parameters["templates_vars"] += ["score_" + model]

    parameters["datasets"] = parameters["grouping"].keys()

    ## make 1D plots
    yields = plotter(client, parameters)

    # make 2D plots
    # yields2D = plotter2D(client, parameters)

    # save templates to ROOT files
    if parameters["save_templates"] ==  True:
        yield_df = to_templates(client, parameters)

    # make datacards
    # build_datacards("score_pytorch_test", yield_df, parameters)
