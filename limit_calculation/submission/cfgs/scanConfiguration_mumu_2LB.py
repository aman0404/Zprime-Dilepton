"""
Config for dimuon case
"""

leptons = "mumu"
systematics = ["lumi",'res','massScale',"zPeak", "ttbarSF" ,"pdf","ID", "ISO", "HLT", "PU", "JEC", "JER", "reco","btagSF_bc","btagSF_light","btagSF_bc_corr","btagSF_light_corr", "l1prefiring", "jets", "ttbar_dnn", "ttbarUncert"]


backgrounds = ['DY','Top','Diboson', 'Jets']
#backgrounds = ['DY','Top','Diboson']

correlate = True

lambdasBBLL = [6]
#lambdasBBLL = [6,10,14,18]
#lambdasBBLL = [6,10,14,18,22,26]
# lambdasBBLL = [6, 10, 14, 18, 22, 26] # 14 doesn't exist for chirality LR for 2016
#lambdasBBLL = [6, 10, 14, 18, 22, 26] # 14 doesn't exist for chirality LR for 2016
#lambdasBBLL = [6] # 14 doesn't exist for chirality LR for 2016


# lambdasBBLL = [6] # 6, 14

#lambdasBSLL = [1]
lambdasBSLL = [1,2,3,4,5,6]

#interferencesBBLL = ["posLL","posLR","posRL","posRR","negLL","negRL","negLR","negRR"]
#interferencesBBLL = ["posLL"]

interferencesBBLL = ["negLL"]
interferencess = ["negLL"]
interferences = ["negLL"]
#interferencesBBLL = ["posLR"]
#interferencesBBLL = ["posLL","posRL","posRR"]
interferencesBSLL = ["BSLL"] #["default"]



#binning for 2b channel
#binning = [200, 500 ,1100,1900,3500,10000]

#binning = [200, 400, 600, 900, 1300, 10000] #for 2b channel

#binning = [200, 400, 600, 900, 1300, 1800, 10000]

binning_2b = [300, 400, 600, 900, 6000] #my binning for 2b channel
binning_0_1b = [300, 400,500,700,1100,1900,6000] #my binning #for 0b and 1b channel

#binning = [200, 300, 400,500,700, 800, 900, 1100, 1900,3500] #test binning case2

#binning = [200, 300, 400,500,700, 800, 900, 1100, 1500, 1900,3500] #test binning case3

#binning = [200, 300, 400,500,700, 1100, 1500, 1900, 2500, 3500] #test binning case4

#binning = [200, 300, 400,500,700, 800, 900, 1100, 1500, 1900, 2500, 3500] #test binning case5


#binning = [200, 300, 400,500,700,1100,1900,3500,10000] #my binning

#masses = [[50,200,1800]]
masses = [[4,6,10]]
massesExp = [[4,6,10,10,10,50000]]

libraries = []

#channels = [
#    "dimuon_2018_BB_ZeroB",
#    "dimuon_2018_BB_OneB",
#    "dimuon_2018_BB_TwoB",
#    "dimuon_2018_BE_ZeroB",
#    "dimuon_2018_BE_OneB",
#    "dimuon_2018_BE_TwoB",
#    "dimuon_2017_BB_ZeroB",
#    "dimuon_2017_BB_OneB",
#    "dimuon_2017_BB_TwoB",
#    "dimuon_2017_BE_ZeroB",
#    "dimuon_2017_BE_OneB",
#    "dimuon_2017_BE_TwoB",
#    "dimuon_2016_post_BB_ZeroB",
#    "dimuon_2016_post_BB_OneB",
#    "dimuon_2016_post_BB_TwoB",
#    "dimuon_2016_post_BE_ZeroB",
#    "dimuon_2016_post_BE_OneB",
#    "dimuon_2016_post_BE_TwoB",
#    "dimuon_2016_pre_BB_ZeroB",
#    "dimuon_2016_pre_BB_OneB",
#    "dimuon_2016_pre_BB_TwoB",
#    "dimuon_2016_pre_BE_ZeroB",
#    "dimuon_2016_pre_BE_OneB",
#    "dimuon_2016_pre_BE_TwoB"
#
#]

#channels = [
#    "dimuon_2018_ZeroB",
#    "dimuon_2017_ZeroB",
#    "dimuon_2016_pre_ZeroB",
#    "dimuon_2016_post_ZeroB",
#]

#channels = [
#    "dimuon_2018_OneB",
#    "dimuon_2017_OneB",
#    "dimuon_2016_pre_OneB",
#    "dimuon_2016_post_OneB",
#]

#channels = [
#    "dimuon_2018_BB_ZeroB",
#    "dimuon_2018_BE_ZeroB",
#    "dimuon_2017_BB_ZeroB",
#    "dimuon_2017_BE_ZeroB",
#    "dimuon_2016_post_BB_ZeroB",
#    "dimuon_2016_post_BE_ZeroB",
#    "dimuon_2016_pre_BB_ZeroB",
#    "dimuon_2016_pre_BE_ZeroB",
#
#]

#channels = [
#    "dimuon_2018_BB_OneB",
#    "dimuon_2018_BE_OneB",
#    "dimuon_2017_BB_OneB",
#    "dimuon_2017_BE_OneB",
#    "dimuon_2016_post_BB_OneB",
#    "dimuon_2016_post_BE_OneB",
#    "dimuon_2016_pre_BB_OneB",
#    "dimuon_2016_pre_BE_OneB",
#
#]

channels = [
    "dimuon_2018_BB_TwoB",
    "dimuon_2018_BE_TwoB",
    "dimuon_2017_BB_TwoB",
    "dimuon_2017_BE_TwoB",
    "dimuon_2016_post_BB_TwoB",
    "dimuon_2016_post_BE_TwoB",
    "dimuon_2016_pre_BB_TwoB",
    "dimuon_2016_pre_BE_TwoB"

]

#numInt = 5000000
numInt =  50000
numToys = 10
exptToys = 500 # make sure this matches with --nToysExp value in runInterpretation.py
#exptToys = 10
submitTo = "Purdue"
LPCUsername = "kaur214"
