import sys
import copy

class Channel:
    name = None
    flavor = None
    inputFile = None
    bJetCat = None
    uncertainties = {}

    def __init__(self, name, flavor, inputFile, bJetCat):
        self.name = name
        self.flavor = flavor
        self.inputFile = inputFile
        self.bJetCat = bJetCat

    def addUncertainty(self, name, shape=False, values = [], correlation = 1):
        self.uncertainties[name] = {}
        if shape:
            self.uncertainties[name]["type"] = "shape" 
            self.uncertainties[name]["values"] = [] 
        else:
            self.uncertainties[name]["type"] = "value" 
            self.uncertainties[name]["values"] = values 
        self.uncertainties[name]["correlation"] = correlation
        # print('self.uncertainties: {0}'.format(self.uncertainties))

uncert_val_dict_mu = {
    "trig" : 1.03,
    "zPeak" : 1.01,
    "ttbarSF" : 1.01,
    "ttbar_dnn" : 1.01,
    "xSecOther" : 1.07,
    "jets" : 1.5,
    "lumi" : 1.016,
    "l1prefiring" : "shape",
    #"lumi" : 1.025,
    "stats" : 0.0,
    "massScale" : "shape",
    "res" : "shape",
    "pdf" : "shape",
    "ttbarUncert" : "shape",
    "ID" :  "shape",
    "ISO" :  "shape",
    "HLT" :  "shape",
    "PU" :  "shape",
    "JEC" : 1.02,
    "JER" : 1.005,
    "reco" : "shape",
    # "btag" : "shape"
    #"btagSF_bc" : "shape", # OneB
    "btagSF_light" : "shape",
    "btagSF_bc_corr" : "shape",
    "btagSF_light_corr" : "shape",
    "btagSF_bc" : "shape", # TwoB
    # "btagSF_light" : 1.04,
    # "btagSF_bc_corr" : 1.10,
    # "btagSF_light_corr" : 1.04,
}
uncert_corr_dict_mu = {
    "trig" : "trg_dimuon",
    "zPeak" : "zp_dimuon",
    "ttbarSF" : "ttbarSF_dimuon",

    "ttbar_dnn" : "ttbar_dnn_dimuon",
    "ttbarUncert" : "ttbarUncert_dimuon",
    


    "xSecOther" : "xso_dilepton",
    "jets" : "jetBkg_dilepton",
    "lumi" : "lumi_dilepton",
    "l1prefiring" : "l1prefiring_prefire_dimuon",
    "stats" : "stat_dimuon",
    "massScale" : "massSc_dimuon",
    "res" : "res_dimuon",
    "pdf" : "pdf_dilepton",
    "ID" : "id_dimuon",
    "ISO" : "iso_dimuon",
    "HLT" : "hlt_dimuon",
    "PU" : "pu_dilepton",
    "JEC" : "jec_dilepton",
    "JER" : "jer_dilepton",
    "reco" : "reco_dimuon",
    # "btag" : "btag_dilepton"
    "btagSF_bc" : "btag_bc_dilepton",
    "btagSF_light" : "btag_light_dilepton",
    "btagSF_bc_corr" : "btag_bc_dilepton",
    "btagSF_light_corr" : "btag_light_dilepton",
}

year_depend_dict_mu = {
    "trig" : True,
    "zPeak" : True,
    "ttbarSF" : True,
    "ttbarUncert" : True, #new

    "ttbar_dnn": True,

    "xSecOther" : False,
    "jets" : True,
    "lumi" : True,
    "l1prefiring": True,
    "stats" : True,
    "massScale" : True,
    "res" : True,
    "pdf" : True,
    "ID" : False,
    "ISO" : False,
    "HLT" : False,
    "PU" : True,
    "JEC" : True,
    "JER" : True,
    "reco" : True,
    # "btag" : True,
    "btagSF_bc" : True,
    "btagSF_light" : True,
    "btagSF_bc_corr" : False,
    "btagSF_light_corr" : False,
}

# uncert_val_dict_el = {
#     "trig" : 1.04,
#     "zPeak" : 1.01,
#     "xSecOther" : 1.07,
#     "jets" : 1.5,
#     "lumi" : 1.025,
#     "stats" : 0.0,
#     "energyScale" : "shape",
#     "res" : "shape",
#     "pdf" : "shape",
#     "ID" : 1.01,
#     "PU" : "shape",
#     "JEC" : 1.02,
#     "JER" : 1.005,
#     "reco" : "shape",
#     # "btag" : "shape"
#     "btagSF_bc" : 1.10,
#     "btagSF_light" : 1.04,
#     "btagSF_bc_corr" : 1.10,
#     "btagSF_light_corr" : 1.04,
# }

uncert_val_dict_el = copy.deepcopy(uncert_val_dict_mu)
del uncert_val_dict_el['massScale'] 
del uncert_val_dict_el['ISO'] 
del uncert_val_dict_el['HLT'] 
uncert_val_dict_el['energyScale'] = "shape" # el has energyScale instead of massScale

uncert_corr_dict_el = {
    "trig" : "trg_dielectron",
    "zPeak" : "zp_dielectron",

    "ttbarSF" : "ttbarSF_dielectron",
    "ttbar_dnn" : "ttbar_dnn_dielectron",
    "ttbarUncert" : "ttbarUncert_dielectron",
    "xSecOther" : "xso_dilepton",
    "jets" : "jetBkg_dilepton",
    "lumi" : "lumi_dilepton",
    "l1prefiring": "l1prefiring_dielectron",
    "stats" : "stat_dielectron",
    "energyScale" : "energySc_dielectron",
    "res" : "res_dielectron",
    "pdf" : "pdf_dilepton",
    "ID" : "id_dielectron",
    "PU" : "pu_dielectron",
    "JEC" : "jec_dilepton",
    "JER" : "jer_dilepton",
    "reco" : "reco_dielectron",
    # "btag" : "btag_dilepton"
    "btagSF_bc" : "btag_bc_dilepton",
    "btagSF_light" : "btag_light_dilepton",
    "btagSF_bc_corr" : "btag_bc_dilepton",
    "btagSF_light_corr" : "btag_light_dilepton",
}

year_depend_dict_el = {
    "trig" : True,
    "zPeak" : True,
    "ttbarSF" : True,
    "ttbar_dnn": True,
    "ttbarUncert" : True,
    
    "xSecOther" : False,
    "jets" : True,
    "lumi" : True,
    "l1prefiring" : True,
    "stats" : True,
    "energyScale" : True,
    "res" : True,
    "pdf" : True,
    "ID" : False,
    "PU" : True,
    "JEC" : True,
    "JER" : True,
    "reco" : True,
    # "btag" : True,
    "btagSF_bc" : True,
    "btagSF_light" : True,
    "btagSF_bc_corr" : False,
    "btagSF_light_corr" : False,
}

# dimuon decay mode
dimuon_2018_ZeroB = Channel("dimuon_2018_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2017_ZeroB = Channel("dimuon_2017_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_ZeroB = Channel("dimuon_2016_pre_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2016_post_ZeroB = Channel("dimuon_2016_post_ZeroB","mu", "inputs.root", "inclusive")

dimuon_2018_OneB = Channel("dimuon_2018_OneB","mu", "inputs.root", "inclusive")
dimuon_2017_OneB = Channel("dimuon_2017_OneB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_OneB = Channel("dimuon_2016_pre_OneB","mu", "inputs.root", "inclusive")
dimuon_2016_post_OneB = Channel("dimuon_2016_post_OneB","mu", "inputs.root", "inclusive")

dimuon_2018_BB_ZeroB = Channel("dimuon_2018_BB_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2018_BB_AllB = Channel("dimuon_2018_BB_allB","mu", "inputs.root", "inclusive")
dimuon_2018_BB_ZeroB = Channel("dimuon_2018_BB_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2018_BB_OneB = Channel("dimuon_2018_BB_OneB","mu", "inputs.root", "inclusive")
dimuon_2018_BB_TwoB = Channel("dimuon_2018_BB_TwoB","mu", "inputs.root", "inclusive")
dimuon_2018_BE_AllB = Channel("dimuon_2018_BE_allB","mu", "inputs.root", "inclusive")
dimuon_2018_BE_ZeroB = Channel("dimuon_2018_BE_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2018_BE_OneB = Channel("dimuon_2018_BE_OneB","mu", "inputs.root", "inclusive")
dimuon_2018_BE_TwoB = Channel("dimuon_2018_BE_TwoB","mu", "inputs.root", "inclusive")
dimuon_2017_BB_AllB = Channel("dimuon_2017_BB_allB","mu", "inputs.root", "inclusive")
dimuon_2017_BB_ZeroB = Channel("dimuon_2017_BB_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2017_BB_OneB = Channel("dimuon_2017_BB_OneB","mu", "inputs.root", "inclusive")
dimuon_2017_BB_TwoB = Channel("dimuon_2017_BB_TwoB","mu", "inputs.root", "inclusive")
dimuon_2017_BE_AllB = Channel("dimuon_2017_BE_allB","mu", "inputs.root", "inclusive")
dimuon_2017_BE_ZeroB = Channel("dimuon_2017_BE_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2017_BE_OneB = Channel("dimuon_2017_BE_OneB","mu", "inputs.root", "inclusive")
dimuon_2017_BE_TwoB = Channel("dimuon_2017_BE_TwoB","mu", "inputs.root", "inclusive")
dimuon_2016_post_BB_AllB = Channel("dimuon_2016_post_BB_allB","mu", "inputs.root", "inclusive")
dimuon_2016_post_BB_ZeroB = Channel("dimuon_2016_post_BB_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2016_post_BB_OneB = Channel("dimuon_2016_post_BB_OneB","mu", "inputs.root", "inclusive")
dimuon_2016_post_BB_TwoB = Channel("dimuon_2016_post_BB_TwoB","mu", "inputs.root", "inclusive")
dimuon_2016_post_BE_AllB = Channel("dimuon_2016_post_BE_allB","mu", "inputs.root", "inclusive")
dimuon_2016_post_BE_ZeroB = Channel("dimuon_2016_post_BE_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2016_post_BE_OneB = Channel("dimuon_2016_post_BE_OneB","mu", "inputs.root", "inclusive")
dimuon_2016_post_BE_TwoB = Channel("dimuon_2016_post_BE_TwoB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_BB_AllB = Channel("dimuon_2016_pre_BB_allB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_BB_ZeroB = Channel("dimuon_2016_pre_BB_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_BB_OneB = Channel("dimuon_2016_pre_BB_OneB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_BB_TwoB = Channel("dimuon_2016_pre_BB_TwoB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_BE_AllB = Channel("dimuon_2016_pre_BE_allB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_BE_ZeroB = Channel("dimuon_2016_pre_BE_ZeroB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_BE_OneB = Channel("dimuon_2016_pre_BE_OneB","mu", "inputs.root", "inclusive")
dimuon_2016_pre_BE_TwoB = Channel("dimuon_2016_pre_BE_TwoB","mu", "inputs.root", "inclusive")

# dielectron

dielectron_2018_ZeroB = Channel("dielectron_2018_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2017_ZeroB = Channel("dielectron_2017_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_ZeroB = Channel("dielectron_2016_pre_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2016_post_ZeroB = Channel("dielectron_2016_post_ZeroB","mu", "inputs.root", "inclusive")

dielectron_2018_OneB = Channel("dielectron_2018_OneB","mu", "inputs.root", "inclusive")
dielectron_2017_OneB = Channel("dielectron_2017_OneB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_OneB = Channel("dielectron_2016_pre_OneB","mu", "inputs.root", "inclusive")
dielectron_2016_post_OneB = Channel("dielectron_2016_post_OneB","mu", "inputs.root", "inclusive")





dielectron_2018_BB_AllB = Channel("dielectron_2018_BB_allB","mu", "inputs.root", "inclusive")
dielectron_2018_BB_ZeroB = Channel("dielectron_2018_BB_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2018_BB_OneB = Channel("dielectron_2018_BB_OneB","mu", "inputs.root", "inclusive")
dielectron_2018_BB_TwoB = Channel("dielectron_2018_BB_TwoB","mu", "inputs.root", "inclusive")
dielectron_2018_BE_AllB = Channel("dielectron_2018_BE_allB","mu", "inputs.root", "inclusive")
dielectron_2018_BE_ZeroB = Channel("dielectron_2018_BE_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2018_BE_OneB = Channel("dielectron_2018_BE_OneB","mu", "inputs.root", "inclusive")
dielectron_2018_BE_TwoB = Channel("dielectron_2018_BE_TwoB","mu", "inputs.root", "inclusive")
dielectron_2017_BB_AllB = Channel("dielectron_2017_BB_allB","mu", "inputs.root", "inclusive")
dielectron_2017_BB_ZeroB = Channel("dielectron_2017_BB_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2017_BB_OneB = Channel("dielectron_2017_BB_OneB","mu", "inputs.root", "inclusive")
dielectron_2017_BB_TwoB = Channel("dielectron_2017_BB_TwoB","mu", "inputs.root", "inclusive")
dielectron_2017_BE_AllB = Channel("dielectron_2017_BE_allB","mu", "inputs.root", "inclusive")
dielectron_2017_BE_ZeroB = Channel("dielectron_2017_BE_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2017_BE_OneB = Channel("dielectron_2017_BE_OneB","mu", "inputs.root", "inclusive")
dielectron_2017_BE_TwoB = Channel("dielectron_2017_BE_TwoB","mu", "inputs.root", "inclusive")
dielectron_2016_post_BB_AllB = Channel("dielectron_2016_post_BB_allB","mu", "inputs.root", "inclusive")
dielectron_2016_post_BB_ZeroB = Channel("dielectron_2016_post_BB_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2016_post_BB_OneB = Channel("dielectron_2016_post_BB_OneB","mu", "inputs.root", "inclusive")
dielectron_2016_post_BB_TwoB = Channel("dielectron_2016_post_BB_TwoB","mu", "inputs.root", "inclusive")
dielectron_2016_post_BE_AllB = Channel("dielectron_2016_post_BE_allB","mu", "inputs.root", "inclusive")
dielectron_2016_post_BE_ZeroB = Channel("dielectron_2016_post_BE_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2016_post_BE_OneB = Channel("dielectron_2016_post_BE_OneB","mu", "inputs.root", "inclusive")
dielectron_2016_post_BE_TwoB = Channel("dielectron_2016_post_BE_TwoB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_BB_AllB = Channel("dielectron_2016_pre_BB_allB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_BB_ZeroB = Channel("dielectron_2016_pre_BB_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_BB_OneB = Channel("dielectron_2016_pre_BB_OneB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_BB_TwoB = Channel("dielectron_2016_pre_BB_TwoB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_BE_AllB = Channel("dielectron_2016_pre_BE_allB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_BE_ZeroB = Channel("dielectron_2016_pre_BE_ZeroB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_BE_OneB = Channel("dielectron_2016_pre_BE_OneB","mu", "inputs.root", "inclusive")
dielectron_2016_pre_BE_TwoB = Channel("dielectron_2016_pre_BE_TwoB","mu", "inputs.root", "inclusive")


channel_l = [
    # dimuon
    dimuon_2018_OneB,
    dimuon_2017_OneB,
    dimuon_2016_pre_OneB,
    dimuon_2016_post_OneB,

    dimuon_2018_ZeroB,
    dimuon_2017_ZeroB,
    dimuon_2016_pre_ZeroB,
    dimuon_2016_post_ZeroB,

    dimuon_2018_BB_AllB,
    dimuon_2018_BB_ZeroB,
    dimuon_2018_BB_OneB,
    dimuon_2018_BB_TwoB,
    dimuon_2018_BE_AllB,
    dimuon_2018_BE_ZeroB,
    dimuon_2018_BE_OneB,
    dimuon_2018_BE_TwoB,
    dimuon_2017_BB_AllB,
    dimuon_2017_BB_ZeroB,
    dimuon_2017_BB_OneB,
    dimuon_2017_BB_TwoB,
    dimuon_2017_BE_AllB,
    dimuon_2017_BE_ZeroB,
    dimuon_2017_BE_OneB,
    dimuon_2017_BE_TwoB,
    dimuon_2016_post_BB_AllB,
    dimuon_2016_post_BB_ZeroB,
    dimuon_2016_post_BB_OneB,
    dimuon_2016_post_BB_TwoB,
    dimuon_2016_post_BE_AllB,
    dimuon_2016_post_BE_ZeroB,
    dimuon_2016_post_BE_OneB,
    dimuon_2016_post_BE_TwoB,
    dimuon_2016_pre_BB_AllB,
    dimuon_2016_pre_BB_ZeroB,
    dimuon_2016_pre_BB_OneB,
    dimuon_2016_pre_BB_TwoB,
    dimuon_2016_pre_BE_AllB,
    dimuon_2016_pre_BE_ZeroB,
    dimuon_2016_pre_BE_OneB,
    dimuon_2016_pre_BE_TwoB,
    # dielectron

    dielectron_2018_OneB,
    dielectron_2017_OneB,
    dielectron_2016_pre_OneB,
    dielectron_2016_post_OneB,

    dielectron_2018_ZeroB,
    dielectron_2017_ZeroB,
    dielectron_2016_pre_ZeroB,
    dielectron_2016_post_ZeroB,

    dielectron_2018_BB_AllB,
    dielectron_2018_BB_ZeroB,
    dielectron_2018_BB_OneB,
    dielectron_2018_BB_TwoB,
    dielectron_2018_BE_AllB,
    dielectron_2018_BE_ZeroB,
    dielectron_2018_BE_OneB,
    dielectron_2018_BE_TwoB,
    dielectron_2017_BB_AllB,
    dielectron_2017_BB_ZeroB,
    dielectron_2017_BB_OneB,
    dielectron_2017_BB_TwoB,
    dielectron_2017_BE_AllB,
    dielectron_2017_BE_ZeroB,
    dielectron_2017_BE_OneB,
    dielectron_2017_BE_TwoB,
    dielectron_2016_post_BB_AllB,
    dielectron_2016_post_BB_ZeroB,
    dielectron_2016_post_BB_OneB,
    dielectron_2016_post_BB_TwoB,
    dielectron_2016_post_BE_AllB,
    dielectron_2016_post_BE_ZeroB,
    dielectron_2016_post_BE_OneB,
    dielectron_2016_post_BE_TwoB,
    dielectron_2016_pre_BB_AllB,
    dielectron_2016_pre_BB_ZeroB,
    dielectron_2016_pre_BB_OneB,
    dielectron_2016_pre_BB_TwoB,
    dielectron_2016_pre_BE_AllB,
    dielectron_2016_pre_BE_ZeroB,
    dielectron_2016_pre_BE_OneB,
    dielectron_2016_pre_BE_TwoB,
]

for channel in channel_l:
    if "mu" in channel.name :
        # print("mu channel.name: {0}".format(channel.name))
        uncert_val_dict = uncert_val_dict_mu
        uncert_corr_dict = uncert_corr_dict_mu
        year_depend_dict = year_depend_dict_mu
    else: # dielectron
        # print("e channel.name: {0}".format(channel.name))
        uncert_val_dict = uncert_val_dict_el
        uncert_corr_dict = uncert_corr_dict_el
        year_depend_dict = year_depend_dict_el


    if "2018" in channel.name :
        year = "18"
    elif "2017" in channel.name :
        year = "17"    
    elif "2016" in channel.name :
        if "post" in channel.name :
            year = "16_post"   
        else: 
            year = "16_pre"  
    else:
        print("invalid channel year")
        raise ValueError

    # print("uncert_corr_dictL {0}".format(uncert_corr_dict))
    for uncert in uncert_corr_dict.keys():
        val = uncert_val_dict[uncert]
        if year_depend_dict[uncert] == True:
            correlation = uncert_corr_dict[uncert] + year
        else:
            correlation = uncert_corr_dict[uncert]

        # print("uncert: {0}".format(uncert))
        # print("correlation: {0}".format(correlation))
        if val == "shape":
            channel.addUncertainty(uncert, shape = True, correlation = correlation)
        else:
            channel.addUncertainty(uncert, values = [val], correlation = correlation)
        # print("uncert: {0}, correlation: {1}".format(uncert,correlation))



channels = {
    # dimuon
#    "dimuon_2018_ZeroB": dimuon_2018_ZeroB,
#    "dimuon_2017_ZeroB": dimuon_2017_ZeroB,
#    "dimuon_2016_pre_ZeroB": dimuon_2016_pre_ZeroB,
#    "dimuon_2016_post_ZeroB": dimuon_2016_post_ZeroB,

#    "dimuon_2018_OneB": dimuon_2018_OneB,
#    "dimuon_2017_OneB": dimuon_2017_OneB,
#    "dimuon_2016_pre_OneB": dimuon_2016_pre_OneB,
#    "dimuon_2016_post_OneB": dimuon_2016_post_OneB,

    "dimuon_2018_BB_ZeroB": dimuon_2018_BB_ZeroB,
    "dimuon_2018_BE_ZeroB": dimuon_2018_BE_ZeroB, 
    "dimuon_2017_BB_ZeroB": dimuon_2017_BB_ZeroB,
    "dimuon_2017_BE_ZeroB": dimuon_2017_BE_ZeroB, 
    "dimuon_2016_post_BB_ZeroB": dimuon_2016_post_BB_ZeroB,
    "dimuon_2016_post_BE_ZeroB": dimuon_2016_post_BE_ZeroB, 
    "dimuon_2016_pre_BB_ZeroB": dimuon_2016_pre_BB_ZeroB,
    "dimuon_2016_pre_BE_ZeroB": dimuon_2016_pre_BE_ZeroB, 

    "dimuon_2018_BB_OneB": dimuon_2018_BB_OneB,
    "dimuon_2018_BE_OneB": dimuon_2018_BE_OneB,
    "dimuon_2017_BB_OneB": dimuon_2017_BB_OneB,
    "dimuon_2017_BE_OneB": dimuon_2017_BE_OneB,
    "dimuon_2016_post_BB_OneB": dimuon_2016_post_BB_OneB,
    "dimuon_2016_post_BE_OneB": dimuon_2016_post_BE_OneB,
    "dimuon_2016_pre_BB_OneB": dimuon_2016_pre_BB_OneB,
    "dimuon_2016_pre_BE_OneB": dimuon_2016_pre_BE_OneB,

    "dimuon_2018_BB_TwoB": dimuon_2018_BB_TwoB,
    "dimuon_2018_BE_TwoB": dimuon_2018_BE_TwoB,
    "dimuon_2017_BB_TwoB": dimuon_2017_BB_TwoB,
    "dimuon_2017_BE_TwoB": dimuon_2017_BE_TwoB,
    "dimuon_2016_post_BB_TwoB": dimuon_2016_post_BB_TwoB,
    "dimuon_2016_post_BE_TwoB": dimuon_2016_post_BE_TwoB,
    "dimuon_2016_pre_BB_TwoB": dimuon_2016_pre_BB_TwoB,
    "dimuon_2016_pre_BE_TwoB": dimuon_2016_pre_BE_TwoB,

# dielectron

    #"dielectron_2018_ZeroB": dielectron_2018_ZeroB,
    #"dielectron_2017_ZeroB": dielectron_2017_ZeroB,
    #"dielectron_2016_pre_ZeroB": dielectron_2016_pre_ZeroB,
    #"dielectron_2016_post_ZeroB": dielectron_2016_post_ZeroB,

    #"dielectron_2018_OneB": dielectron_2018_OneB,
    #"dielectron_2017_OneB": dielectron_2017_OneB,
    #"dielectron_2016_pre_OneB": dielectron_2016_pre_OneB,
    #"dielectron_2016_post_OneB": dielectron_2016_post_OneB,



#    "dielectron_2018_BB_AllB": dielectron_2018_BB_AllB, 
    "dielectron_2018_BB_ZeroB": dielectron_2018_BB_ZeroB,
#    "dielectron_2018_BB_OneB": dielectron_2018_BB_OneB, 
#    "dielectron_2018_BB_TwoB": dielectron_2018_BB_TwoB, 
#    "dielectron_2018_BE_AllB": dielectron_2018_BE_AllB, 
    "dielectron_2018_BE_ZeroB": dielectron_2018_BE_ZeroB, 
#    "dielectron_2018_BE_OneB": dielectron_2018_BE_OneB, 
#    "dielectron_2018_BE_TwoB": dielectron_2018_BE_TwoB,
#    "dielectron_2017_BB_AllB": dielectron_2017_BB_AllB, 
#    "dielectron_2017_BB_ZeroB": dielectron_2017_BB_ZeroB,
#    "dielectron_2017_BB_OneB": dielectron_2017_BB_OneB, 
#    "dielectron_2017_BB_TwoB": dielectron_2017_BB_TwoB, 
##    "dielectron_2017_BE_AllB": dielectron_2017_BE_AllB, 
#    "dielectron_2017_BE_ZeroB": dielectron_2017_BE_ZeroB, 
#    "dielectron_2017_BE_OneB": dielectron_2017_BE_OneB, 
#    "dielectron_2017_BE_TwoB": dielectron_2017_BE_TwoB,
##    "dielectron_2016_post_BB_AllB": dielectron_2016_post_BB_AllB, 
#    "dielectron_2016_post_BB_ZeroB": dielectron_2016_post_BB_ZeroB,
#    "dielectron_2016_post_BB_OneB": dielectron_2016_post_BB_OneB, 
#    "dielectron_2016_post_BB_TwoB": dielectron_2016_post_BB_TwoB, 
##    "dielectron_2016_post_BE_AllB": dielectron_2016_post_BE_AllB, 
#    "dielectron_2016_post_BE_ZeroB": dielectron_2016_post_BE_ZeroB, 
#    "dielectron_2016_post_BE_OneB": dielectron_2016_post_BE_OneB, 
#    "dielectron_2016_post_BE_TwoB": dielectron_2016_post_BE_TwoB,
##    "dielectron_2016_pre_BB_AllB" : dielectron_2016_pre_BB_AllB,
#    "dielectron_2016_pre_BB_ZeroB" : dielectron_2016_pre_BB_ZeroB,
#    "dielectron_2016_pre_BB_OneB" : dielectron_2016_pre_BB_OneB,
#    "dielectron_2016_pre_BB_TwoB" : dielectron_2016_pre_BB_TwoB,
##    "dielectron_2016_pre_BE_AllB" : dielectron_2016_pre_BE_AllB,
#    "dielectron_2016_pre_BE_ZeroB" : dielectron_2016_pre_BE_ZeroB,
#    "dielectron_2016_pre_BE_OneB" : dielectron_2016_pre_BE_OneB,
#    "dielectron_2016_pre_BE_TwoB" : dielectron_2016_pre_BE_TwoB,

}

def getChannelConfig(name):
        if not name in channels:
                print ("unknown channel '%s, exiting'"%name)
                sys.exit()
        else:
                return copy.copy(channels[name])
