"""
Config for dielectron + dimuon case
"""
leptons = "elmu"  
#systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU"]
#systematics = ["lumi",'res','massScale','energyScale',"zPeak","trig","pdf","ID","PU", "JEC", "JER","btag", "reco"]

#systematics = ["lumi",'res','massScale',"zPeak","trig","pdf","ID","PU", "JEC", "JER", "reco","btagSF_bc","btagSF_light","btagSF_bc_corr","btagSF_light_corr",]

systematics = ["lumi",'res','massScale',"zPeak", "ttbarSF" ,"pdf","ID", "ISO", "HLT", "PU", "JEC", "JER", "reco","btagSF_bc","btagSF_light","btagSF_bc_corr","btagSF_light_corr", "l1prefiring", "jets", "ttbar_dnn", "energyScale"]

backgrounds = ['DY','Top','Diboson', 'Jets']

correlate = True

lambdasBBLL = [6,10,14,18,22,26]
#lambdasBBLL = [6, 10, 18, 22, 26] # 14 doesn't exist for chirality LR for 2016
# lambdasBBLL = [6] # 6, 14

lambdasBSLL = [1,2,3,4,5,6]

#interferencesBBLL = ["posLL","posLR","posRL","posRR","negLL","negRL","negLR","negRR"]
interferencesBBLL = ["posLR"]
#interferencesBBLL = ["posLL"]

#interferencesBBLL = ["posLL","posLR","posRL","posRR"]
interferencesBSLL = ["BSLL"] #["default"]

binning_2b = [200, 400, 600, 900, 6000] #my binning for 2b channel
binning_0_1b = [200, 300, 400,500,700,1100,1900,6000] #my binning #for 0b and 1b channel

#binning = [200, 300, 400,500,700,1100,1900,3500,10000]

libraries = []

channels = [
    # "dimuon_2018_BB_AllB",
    "dimuon_2018_BB_ZeroB",
    "dimuon_2018_BB_OneB",
    "dimuon_2018_BB_TwoB",
    # "dimuon_2018_BE_AllB",
    "dimuon_2018_BE_ZeroB",
    "dimuon_2018_BE_OneB",
    "dimuon_2018_BE_TwoB",
    # "dimuon_2017_BB_AllB",
    "dimuon_2017_BB_ZeroB",
    "dimuon_2017_BB_OneB",
    "dimuon_2017_BB_TwoB",
    # # "dimuon_2017_BE_AllB",
    "dimuon_2017_BE_ZeroB",
    "dimuon_2017_BE_OneB",
    "dimuon_2017_BE_TwoB",
    # "dimuon_2016_post_BB_AllB",
    "dimuon_2016_post_BB_ZeroB",
    "dimuon_2016_post_BB_OneB",
    "dimuon_2016_post_BB_TwoB",
    # "dimuon_2016_post_BE_AllB",
    "dimuon_2016_post_BE_ZeroB",
    "dimuon_2016_post_BE_OneB",
    "dimuon_2016_post_BE_TwoB",
    # "dimuon_2016_pre_BB_AllB",
    "dimuon_2016_pre_BB_ZeroB",
    "dimuon_2016_pre_BB_OneB",
    "dimuon_2016_pre_BB_TwoB",
    # "dimuon_2016_pre_BE_AllB",
    "dimuon_2016_pre_BE_ZeroB",
    "dimuon_2016_pre_BE_OneB",
    "dimuon_2016_pre_BE_TwoB",
    
    # "dielectron_2018_BB_AllB",
    "dielectron_2018_BB_ZeroB",
    "dielectron_2018_BB_OneB",
    "dielectron_2018_BB_TwoB",
    # "dielectron_2018_BE_AllB",
    "dielectron_2018_BE_ZeroB",
    "dielectron_2018_BE_OneB",
    "dielectron_2018_BE_TwoB",
    # "dielectron_2017_BB_AllB",
    "dielectron_2017_BB_ZeroB",
    "dielectron_2017_BB_OneB",
    "dielectron_2017_BB_TwoB",
    # # "dielectron_2017_BE_AllB",
    "dielectron_2017_BE_ZeroB",
    "dielectron_2017_BE_OneB",
    "dielectron_2017_BE_TwoB",
    # "dielectron_2016_post_BB_AllB",
    "dielectron_2016_post_BB_ZeroB",
    "dielectron_2016_post_BB_OneB",
    "dielectron_2016_post_BB_TwoB",
    # "dielectron_2016_post_BE_AllB",
    "dielectron_2016_post_BE_ZeroB",
    "dielectron_2016_post_BE_OneB",
    "dielectron_2016_post_BE_TwoB",
    # "dielectron_2016_pre_BB_AllB",
    "dielectron_2016_pre_BB_ZeroB",
    "dielectron_2016_pre_BB_OneB",
    "dielectron_2016_pre_BB_TwoB",
    # "dielectron_2016_pre_BE_AllB",
    "dielectron_2016_pre_BE_ZeroB",
    "dielectron_2016_pre_BE_OneB",
    "dielectron_2016_pre_BE_TwoB"

]
numInt = 100000
numToys = 6
exptToys = 500 # make sure this matches with --nToysExp value in runInterpretation.py
# exptToys = 20
submitTo = "Purdue"
LPCUsername = "kaur214"

