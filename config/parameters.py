def for_all_years(value):
    out = {k: value for k in ["2016pre", "2016post", "2017", "2018"]}
    #out = {k: value for k in ["2016preVFP","2016postVFP", "2017", "2018"]}
    return out

parameters = {}
# for lumis, the 0th element is golden sample, the 1th element is muonphys
lumis = {"2016pre": [19.12*1000,19.29*1000], "2016post": [16.81*1000, 17.01*1000], "2017": [41.48*1000,42.02*1000], "2018": [59.83*1000,61.31*1000]}
parameters["lumimask_Pre-UL_mu"] = {
    "2016": "data/lumimasks/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON_MuonPhys.txt",
    "2017": "data/lumimasks/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_MuonPhys.txt",
    "2018": "data/lumimasks/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON_MuonPhys.txt",
}


parameters["lumimask_UL_el"] = {
    "2016pre": "data/lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
    "2016post": "data/lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
    "2017": "data/lumimasks/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
    "2018": "data/lumimasks/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
}
parameters["lumimask_UL_mu"] = {
    "2016pre": "data/lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
    "2016post": "data/lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
    "2017": "data/lumimasks/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
    "2018": "data/lumimasks/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
}

parameters["mu_hlt"] = {
    "2016": ["Mu50", "TkMu50"],
    "2017": ["Mu50", "TkMu100", "OldMu100"], # this may have to be changed
    "2018": ["Mu50", "TkMu100", "OldMu100"],
}

parameters["el_hlt"] = {
    #"2016post": ["DoubleEle33_CaloIdL_MW", "DoubleEle33_CaloIdL_GsfTrkIdVL_MW"],
    "2016pre": ["DoubleEle33_CaloIdL_MW", "DoubleEle33_CaloIdL_GsfTrkIdVL", "DoubleEle33_CaloIdL_GsfTrkIdVL_MW"],
    "2016post": ["DoubleEle33_CaloIdL_MW", "DoubleEle33_CaloIdL_GsfTrkIdVL_MW"],
    #"2016post": ["DoubleEle33_CaloIdL_MW", "DoubleEle33_CaloIdL_GsfTrkIdVL", "DoubleEle33_CaloIdL_GsfTrkIdVL_MW"],
    #"2016pre": ["DoubleEle33_CaloIdL_MW","HLT_DoubleEle33_CaloIdL_GsfTrkIdVL"],
#    "2016postVFP": ["DoubleEle33_CaloIdL_MW","HLT_DoubleEle33_CaloIdL_GsfTrkIdVL"],
    "2017": ["DoubleEle33_CaloIdL_MW"],
    "2018": ["DoubleEle25_CaloIdL_MW"],
}


parameters["btag_sf_pre_UL"] = {
    "2016": "data/b-tagging/DeepCSV_2016LegacySF_V1.csv",
    "2017": "data/b-tagging/DeepCSV_94XSF_V5_B_F.csv",
    "2018": "data/b-tagging/DeepJet_102XSF_WP_V1.csv",
}

parameters["btag_sf_UL"] = {
    "2016pre": "data/b-tagging/btagging_UL2016preVFP.json",
    "2016post": "data/b-tagging/btagging_UL2016postVFP.json",
    "2018": "data/b-tagging/btagging_UL18.json",
    "2017": "data/b-tagging/btagging_UL17.json",
}

parameters["btag_sf_eff"] = {
    "2016pre": "data/b-tagging/UL2018_ttbar_eff.pickle",
    "2016post": "data/b-tagging/UL2018_ttbar_eff.pickle",
    "2018": "data/b-tagging/UL2018_ttbar_eff.pickle",
    "2017": "data/b-tagging/UL2018_ttbar_eff.pickle",
}

parameters["pu_file_data"] = {
    "2016pre": "data/pileup/puData2016PreVFP_new.root",
    "2016post": "data/pileup/puData2016PostVFP_new.root",
    "2017": "data/pileup/puData2017_new.root",
    "2018": "data/pileup/puData2018_new.root",
}

parameters["pu_file_mc"] = {
    "2016pre": "data/pileup/puMC2016PreVFP_new.root",
    "2016post": "data/pileup/puMC2016PostVFP_new.root",
    "2017": "data/pileup/puMC2017_new.root",
    "2018": "data/pileup/puMC2018_new.root",
}

parameters["muSFFileList"] = {
    "2016": [
        {
            "id": (
                "data/muon_sf/year2016/RunBCDEF_SF_ID.root",
                "NUM_MediumID_DEN_genTracks_eta_pt",
            ),
            "iso": (
                "data/muon_sf/year2016/RunBCDEF_SF_ISO.root",
                "NUM_TightRelIso_DEN_MediumID_eta_pt",
            ),
            "trig": (
                "data/muon_sf/mu2016/EfficienciesStudies_2016_trigger_EfficienciesAndSF_RunBtoF.root",
                "IsoMu24_OR_IsoTkMu24_PtEtaBins/efficienciesDATA/abseta_pt_DATA",
                "IsoMu24_OR_IsoTkMu24_PtEtaBins/efficienciesMC/abseta_pt_MC",
            ),
            "scale": 20.1 / 36.4,
        },
        {
            "id": (
                "data/muon_sf/year2016/RunGH_SF_ID.root",
                "NUM_MediumID_DEN_genTracks_eta_pt",
            ),
            "iso": (
                "data/muon_sf/year2016/RunGH_SF_ISO.root",
                "NUM_TightRelIso_DEN_MediumID_eta_pt",
            ),
            "trig": (
                "data/muon_sf/mu2016/EfficienciesStudies_2016_trigger_EfficienciesAndSF_RunGtoH.root",
                "IsoMu24_OR_IsoTkMu24_PtEtaBins/efficienciesDATA/abseta_pt_DATA",
                "IsoMu24_OR_IsoTkMu24_PtEtaBins/efficienciesMC/abseta_pt_MC",
            ),
            "scale": 16.3 / 36.4,
        },
    ],
    "2017": [
        {
            "id": (
                "data/muon_sf/year2017/RunBCDEF_SF_ID.root",
                "NUM_MediumID_DEN_genTracks_pt_abseta",
            ),
            "iso": (
                "data/muon_sf/year2017/RunBCDEF_SF_ISO.root",
                "NUM_TightRelIso_DEN_MediumID_pt_abseta",
            ),
            "trig": (
                "data/muon_sf/mu2017/EfficienciesAndSF_RunBtoF_Nov17Nov2017.root",
                "IsoMu27_PtEtaBins/efficienciesDATA/abseta_pt_DATA",
                "IsoMu27_PtEtaBins/efficienciesMC/abseta_pt_MC",
            ),
            "scale": 1.0,
        }
    ],
    "2018": [
        {
            "id": (
                "data/muon_sf/year2018/RunABCD_SF_ID.root",
                "NUM_MediumID_DEN_genTracks_pt_abseta",
            ),
            "iso": (
                "data/muon_sf/year2018/RunABCD_SF_ISO.root",
                "NUM_TightRelIso_DEN_MediumID_pt_abseta",
            ),
            "trig": (
                "data/muon_sf/mu2018/EfficienciesStudies_2018_trigger_EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root",
                "IsoMu24_PtEtaBins/efficienciesDATA/abseta_pt_DATA",
                "IsoMu24_PtEtaBins/efficienciesMC/abseta_pt_MC",
            ),
            "scale": 8.95 / 59.74,
        },
        {
            "id": (
                "data/muon_sf/year2018/RunABCD_SF_ID.root",
                "NUM_MediumID_DEN_genTracks_pt_abseta",
            ),
            "iso": (
                "data/muon_sf/year2018/RunABCD_SF_ISO.root",
                "NUM_TightRelIso_DEN_MediumID_pt_abseta",
            ),
            "trig": (
                "data/muon_sf/mu2018/EfficienciesStudies_2018_trigger_EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root",
                "IsoMu24_PtEtaBins/efficienciesDATA/abseta_pt_DATA",
                "IsoMu24_PtEtaBins/efficienciesMC/abseta_pt_MC",
            ),
            "scale": 50.79 / 59.74,
        },
    ],
}

parameters["zpt_weights_file"] = for_all_years("data/zpt/zpt_weights.histo.json")
parameters["res_calib_path"] = for_all_years("data/res_calib/")

parameters.update(
    {
        "event_flags": for_all_years(
            [
                "BadPFMuonDzFilter",
                "BadPFMuonFilter",
                "EcalDeadCellTriggerPrimitiveFilter",
                "HBHENoiseFilter",
                "HBHENoiseIsoFilter",
                "globalSuperTightHalo2016Filter",
                "goodVertices",
                "BadChargedCandidateFilter",
                "eeBadScFilter",
                "ecalBadCalibFilter",

            ]
        ),
        "do_l1prefiring_wgts": {"2016pre": True,"2016post":True,  "2017": True, "2018": False},
        "3dangle": for_all_years(-0.9998),
    }
)

parameters.update(
    {
        "muon_pt_cut": for_all_years(53.0),
        "muon_eta_cut": for_all_years(2.4),
        "muon_iso_cut": for_all_years(0.15),  # medium iso
        "muon_id": for_all_years("looseId"),
        "muon_dxy": for_all_years(0.2),
        "muon_ptErr/pt": for_all_years(0.3),
        # "muon_flags": for_all_years(["isGlobal", "isTracker"]),
        "muon_flags": for_all_years([]),
        "electron_flags": for_all_years([]),
        "muon_leading_pt": {"2016pre": 53.0,"2016post":53.0, "2017": 53.0, "2018": 53.0},
        "muon_trigmatch_iso": for_all_years(0.15),  # tight iso
        "muon_trigmatch_dr": for_all_years(0.1),
        "muon_trigmatch_id": for_all_years("tightId"),
        "electron_pt_cut": for_all_years(35.0),
        "electron_eta_cut": for_all_years(2.5),
        "electron_id": for_all_years("cutBased_HEEP"),

        "UL_btag_loose":  {"2016pre": 0.0508, "2016post": 0.0480, "2017": 0.0532, "2018": 0.0490},
        "UL_btag_medium": {"2016pre": 0.2598, "2016post": 0.2489, "2017": 0.3040, "2018": 0.2783},
        "UL_btag_tight":  {"2016pre": 0.6502, "2016post": 0.6377, "2017": 0.7476, "2018": 0.7100},

        "2018HEM_veto" : {"2016pre": 0, "2016post": 0,"2017": 0, "2018": 1},

    }
)

bins = [
    120.0,
    129.95474058,
    140.73528833,
    152.41014904,
    165.0535115,
    178.74571891,
    193.57377942,
    209.63191906,
    227.02218049,
    245.85507143,
    266.2502669,
    288.3373697,
    312.25673399,
    338.16035716,
    366.21284574,
    396.59246138,
    429.49225362,
    465.12128666,
    503.70596789,
    545.49148654,
    590.74337185,
    639.74918031,
    692.82032303,
    750.29404456,
    812.53556599,
    879.94040575,
    952.93689296,
    1031.98888927,
    1117.59873655,
    1210.310449,
    1310.71317017,
    1419.4449167,
    1537.19663264,
    1664.71658012,
    1802.81509423,
    1952.36973236,
    2114.3308507,
    2289.72764334,
    2479.6746824,
    2685.37900061,
    2908.14776151,
    3149.39656595,
    3410.65844758,
    3693.59361467,
    4000.0,
    4500,
    5200,
    6000,
    7000,
    8000,
]

# branches are important only for Spark executor
event_branches = ["run", "event", "luminosityBlock", "genWeight"]
muon_branches = [
    "pt_raw",
    "pt",
    "eta",
    "eta_raw",
    "phi",
    "phi_raw",
    "charge",
    "ptErr",
    "looseId",
    "highPtId",
    "tkRelIso",
    "mass",
    "dxy",
    "dz",
    "ip3d",
    "sip3d",
]
fsr_branches = [
    "nFsrPhoton",
    "FsrPhoton_pt",
    "FsrPhoton_eta",
    "FsrPhoton_phi",
    "FsrPhoton_relIso03",
    "FsrPhoton_dROverEt2",
]
jet_branches = [
    "pt",
    "eta",
    "phi",
    "jetId",
    "qgl",
    "puId",
    "mass",
    "btagDeepB",
    "btagDeepFlavB",
]
genjet_branches = [
    "nGenJet",
    "GenJet_pt",
    "GenJet_eta",
    "GenJet_phi",
    "GenJet_mass",
    "GenJet_partonFlavour",
]
genpart_branches = [
    "GenPart_eta",
    "GenPart_genPartIdxMother",
    "GenPart_mass",
    "GenPart_pdgId",
    "GenPart_phi",
    "GenPart_pt",
    "GenPart_status",
    "GenPart_statusFlags",
    "nGenPart",
]
sajet_branches = [
    "nSoftActivityJet",
    "SoftActivityJet_pt",
    "SoftActivityJet_eta",
    "SoftActivityJet_phi",
    "SoftActivityJetNjets2",
    "SoftActivityJetNjets5",
    "SoftActivityJetHT2",
    "SoftActivityJetHT5",
]
vtx_branches = ["Pileup_nTrueInt", "PV_npvsGood", "PV_npvs"]
genpart_branches = [
    "nGenPart",
    "GenPart_pt",
    "GenPart_eta",
    "GenPart_phi",
    "GenPart_pdgId",
]
trigobj_branches = [
    "nTrigObj",
    "TrigObj_pt",
    "TrigObj_l1pt",
    "TrigObj_l1pt_2",
    "TrigObj_l2pt",
    "TrigObj_eta",
    "TrigObj_phi",
    "TrigObj_id",
    "TrigObj_l1iso",
    "TrigObj_l1charge",
    "TrigObj_filterBits",
]
ele_branches = [
    "pt_raw",
    "pt",
    "scEtOverPt",
    "eta",
    "deltaEtaSC",
    "eta_raw",
    "phi",
    "phi_raw",
    "mass",
    "cutBased_HEEP",
    "charge",
]
other_branches = [
    "MET_pt",
    "MET_phi",
    "HTXS_stage1_1_fine_cat_pTjet30GeV",
    "fixedGridRhoFastjetAll",
    "nLHEScaleWeight",
    "nLHEPdfWeight",
    "LHEPdfWeight",
]

event_flags = [
    "Flag_BadPFMuonDzFilter",
    "Flag_BadPFMuonFilter",
    "Flag_EcalDeadCellTriggerPrimitiveFilter",
    "Flag_HBHENoiseFilter",
    "Flag_HBHENoiseIsoFilter",
    "Flag_globalSuperTightHalo2016Filter",
    "Flag_goodVertices",
    "Flag_BadChargedCandidateFilter",
    "Flag_eeBadScFilter",
    "Flag_ecalBadCalibFilter",
]


branches_2016 = [
    "Mu50",
    "TkMu50",
    "L1PreFiringWeight_Nom",
    "L1PreFiringWeight_Up",
    "L1PreFiringWeight_Dn",
]
branches_2017 = [
    "Mu50",
    "TkMu100",
    "OldMu100",
    "L1PreFiringWeight_Nom",
    "L1PreFiringWeight_Up",
    "L1PreFiringWeight_Dn",
]
branches_2018 = [
    "Mu50",
    "TkMu100",
    "OldMu100",
    "L1PreFiringWeight_Nom",
    "L1PreFiringWeight_Up",
    "L1PreFiringWeight_Dn",
]


proc_columns = (
    event_branches
    + muon_branches
    + fsr_branches
    + jet_branches
    + genjet_branches
    + genpart_branches
    + sajet_branches
    + vtx_branches
    + genpart_branches
    + trigobj_branches
    + ele_branches
    + other_branches
    + event_flags
)
parameters["proc_columns"] = {
    "2016pre": proc_columns + branches_2016,
    "2016post": proc_columns + branches_2016,
    "2017": proc_columns + branches_2017,
    "2018": proc_columns + branches_2018,
}