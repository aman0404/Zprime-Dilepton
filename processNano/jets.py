import numpy as np
import pandas as pd
import awkward as ak
from processNano.utils import p4, p4_sum, delta_r, rapidity, bbangle
import correctionlib
import pickle
from coffea.lookup_tools.dense_lookup import dense_lookup
from coffea.btag_tools import BTagScaleFactor
from config.parameters import parameters


def btagSF(df, year, correction="shape", is_UL=True):

    if is_UL:
        if correction == "wp":
            systs = [
                "central",
                "up",
                "down",
                "up_correlated",
                "up_uncorrelated",
                "down_correlated",
                "down_uncorrelated",
                "up_isr",
                "down_isr",
                "up_fsr",
                "down_fsr",
                "up_hdamp",
                "down_hdamp",
                "up_jes",
                "down_jes",
                "up_jer",
                "down_jer",
                "up_pileup",
                "down_pileup",
                "up_qcdscale",
                "down_qcdscale",
                "up_statistic",
                "down_statistic",
                "up_topmass",
                "down_topmass",
                "up_type3",
                "down_type3",
            ]
        else:
            systs = ["central"]
        cset = correctionlib.CorrectionSet.from_file(parameters["btag_sf_UL"][year])
    else:
        if correction == "wp":
            systs = [
                "central",
                "up",
                "down",
                "up_correlated",
                "up_uncorrelated",
                "down_correlated",
                "down_uncorrelated",
            ]
        else:
            systs = ["central"]

        cset = BTagScaleFactor(parameters["btag_sf_pre_UL"][year], "tight")

    df["pre_selection"] = False
    df.loc[
        #(df.pt > 20.0) & (abs(df.eta) < 2.4) & (df.jetId >= 3), "pre_selection"
        (df.pt > 20.0) & (abs(df.eta) < 2.4) & (df.jetId >= 2), "pre_selection"
    ] = True
    mask = df["pre_selection"]
    print("----------------HELLO---------------")
    for syst in systs:
        if correction == "shape":

            df["btag_sf_shape"] = 1.0
            flavor = df[mask].hadronFlavour.to_numpy()
            eta = np.abs(df[mask].eta.to_numpy())
            pt = df[mask].pt.to_numpy()
            mva = df[mask].btagDeepFlavB.to_numpy()

            if is_UL:
                sf = cset["deepJet_shape"].evaluate(syst, flavor, eta, pt, mva)
            if syst == "central":
                df.loc[mask, "btag_sf_shape"] = sf
            else:
                df.loc[mask, f"btag_sf_shape_{syst}"] = sf

        elif correction == "wp":
            is_bc = df["hadronFlavour"] >= 4
            is_light = df["hadronFlavour"] < 4

            path_eff = parameters["btag_sf_eff"][year]
            wp = parameters["UL_btag_tight"][year]
            with open(path_eff, "rb") as handle:
                eff = pickle.load(handle)

            efflookup = dense_lookup(eff.values(), [ax.edges for ax in eff.axes])
            mask_dict = {0: is_light, 4: is_bc, 5: is_bc}
            for key in mask_dict.keys():

                mask_flavor = mask_dict[key]
                flavor = df[mask & mask_flavor].hadronFlavour.to_numpy()
                eta = np.abs(df[mask & mask_flavor].eta.to_numpy())
                pt = df[mask & mask_flavor].pt.to_numpy()
                mva = df[mask & mask_flavor].btagDeepFlavB.to_numpy()

                if is_UL:
                    if key < 4:
                        corr = "deepJet_incl"
                    else:
                        corr = "deepJet_comb"
                    try:
                        fac = cset[corr].evaluate(syst, "M", flavor, eta, pt)
                    except Exception:
                        fac = cset[corr].evaluate("central", "M", flavor, eta, pt)
                else:
                    try:

                        fac = cset.eval(syst, flavor, eta, pt, wp)
                        print("uncertainty is " + syst)
                    except Exception:
                        fac = cset.eval("central", flavor, eta, pt, wp)

                prob = efflookup(pt, eta, key)
                prob_nosf = np.copy(prob)
                prob_sf = np.copy(prob) * fac
                prob_sf[mva < wp] = 1.0 - prob_sf[mva < wp]
                prob_nosf[mva < wp] = 1.0 - prob_nosf[mva < wp]
                sf = prob_sf / prob_nosf
                if syst == "central":
                    df.loc[mask & mask_flavor, "btag_sf_wp"] = sf
                else:
                    df.loc[mask & mask_flavor, f"btag_sf_wp_{syst}"] = sf
            if syst == "central":
                df["btag_sf_wp"].fillna(1.0)
            else:
                df[f"btag_sf_wp_{syst}"].fillna(1.0)


def prepare_jets(df, is_mc):
    # Initialize missing fields (needed for JEC)
    df["Jet", "pt_raw"] = (1 - df.Jet.rawFactor) * df.Jet.pt
    df["Jet", "mass_raw"] = (1 - df.Jet.rawFactor) * df.Jet.mass
    df["Jet", "rho"] = ak.broadcast_arrays(df.fixedGridRhoFastjetAll, df.Jet.pt)[0]

    if is_mc:
        df["Jet", "pt_gen"] = ak.values_astype(
            ak.fill_none(df.Jet.matched_gen.pt, 0), np.float32
        )


def fill_jets(output, variables, jets, flavor="mu", is_mc=True):
    variable_names = [
        #"overlap",        
        "jet1_pt",
        "jet1_eta",
        "jet1_rap",
        "jet1_phi",
        "jet1_qgl",
        "jet1_jetId",
        "jet1_puId",
        "jet1_btagDeepB",
        "jet2_pt",
        "jet2_eta",
        "jet2_rap",
        "jet2_phi",
        "jet2_qgl",
        "jet2_jetId",
        "jet2_puId",
        "jet2_btagDeepB",
        "jet1_sf",
        "jet2_sf",
        "jj_mass",
        "jj_mass_log",
        "jj_pt",
        "jj_eta",
        "jj_phi",
        "jj_dEta",
        "jj_dPhi",
        "mmj1_dEta",
        "mmj1_dPhi",
        "mmj1_dR",
        "mmj2_dEta",
        "mmj2_dPhi",
        "mmj2_dR",
        "mmj_min_dEta",
        "mmj_min_dPhi",
        "mmjj_pt",
        "mmjj_eta",
        "mmjj_phi",
        "mmjj_mass",
        "rpt",
        "zeppenfeld",
        "ll_zstar_log",
        "nsoftjets2",
        "nsoftjets5",
        "htsoft2",
        "htsoft5",
        "selection",
    ]

    for v in variable_names:
        variables[v] = -999.0
    njet = len(jets)

    jet1 = jets[0]
    jet2 = jets[1]
    # Fill single jet variables
    for v in [
        "pt",
        "eta",
        "phi",
        "mass",
        "pt_gen",
        "eta_gen",
        "phi_gen",
        "qgl",
        "btagDeepB",
        "btagDeepFlavB",
    ]:
        try:
            variables[f"jet1_{v}"] = jet1[v]
            variables[f"jet2_{v}"] = jet2[v]
        except Exception:
            variables[f"jet1_{v}"] = -999.0
            variables[f"jet2_{v}"] = -999.0
    variables.jet1_rap = rapidity(jet1)

    if njet > 1:
        variables.jet2_rap = rapidity(jet2)
        # Fill dijet variables
        jj = p4_sum(jet1, jet2, is_mc=is_mc)

        for v in [
            "pt",
            "eta",
            "phi",
            "mass",
            "pt_gen",
            "eta_gen",
            "phi_gen",
            "mass_gen",
        ]:
            try:
                variables[f"jj_{v}"] = jj[v]
            except Exception:
                variables[f"jj_{v}"] = -999.0

        variables.jj_mass_log = np.log(variables.jj_mass)

        variables.jj_dEta, variables.jj_dPhi, _ = delta_r(
            variables.jet1_eta,
            variables.jet2_eta,
            variables.jet1_phi,
            variables.jet2_phi,
        )

        # Fill dimuon-dijet system variables
        if flavor == "mu":
            mm_columns = [
                "dimuon_pt",
                "dimuon_eta",
                "dimuon_phi",
                "dimuon_mass",
                "dimuon_pt_gen",
                "dimuon_eta_gen",
                "dimuon_phi_gen",
                "dimuon_mass_gen",
            ]
        else:
            mm_columns = [
                "dielectron_pt",
                "dielectron_eta",
                "dielectron_phi",
                "dielectron_mass",
                "dielectron_pt_gen",
                "dielectron_eta_gen",
                "dielectron_phi_gen",
                "dielectron_mass_gen",
            ]
        jj_columns = [
            "jj_pt",
            "jj_eta",
            "jj_phi",
            "jj_mass",
            "jj_pt_gen",
            "jj_eta_gen",
            "jj_phi_gen",
            "jj_mass_gen",
        ]

        dileptons = output.loc[:, mm_columns]
        dijets = variables.loc[:, jj_columns]

        # careful with renaming
        dileptons.columns = [
            "mass",
            "pt",
            "eta",
            "phi",
            "mass_gen",
            "pt_gen",
            "eta_gen",
            "phi_gen",
        ]
        dijets.columns = [
            "pt",
            "eta",
            "phi",
            "mass",
            "mass_gen",
            "pt_gen",
            "eta_gen",
            "phi_gen",
        ]

        mmjj = p4_sum(dileptons, dijets, is_mc=is_mc)
        for v in [
            "pt",
            "eta",
            "phi",
            "mass",
            "mass_gen",
            "pt_gen",
            "eta_gen",
            "phi_gen",
        ]:
            try:
                variables[f"mmjj_{v}"] = mmjj[v]
            except Exception:
                variables[f"mmjj_{v}"] = -999.0

        if flavor == "mu":
            dilepton_pt, dilepton_eta, dilepton_phi, dilepton_rap = (
                output.dimuon_pt,
                output.dimuon_eta,
                output.dimuon_phi,
                output.dimuon_rap,
            )
        else:
            dilepton_pt, dilepton_eta, dilepton_phi, dilepton_rap = (
                output.dielectron_pt,
                output.dielectron_eta,
                output.dielectron_phi,
                output.dielectron_rap,
            )

        variables.zeppenfeld = dilepton_eta - 0.5 * (
            variables.jet1_eta + variables.jet2_eta
        )

        variables.rpt = variables.mmjj_pt / (
            dilepton_pt + variables.jet1_pt + variables.jet2_pt
        )

        ll_ystar = dilepton_rap - (variables.jet1_rap + variables.jet2_rap) / 2

        ll_zstar = abs(ll_ystar / (variables.jet1_rap - variables.jet2_rap))

        variables.ll_zstar_log = np.log(ll_zstar)

        variables.mmj1_dEta, variables.mmj1_dPhi, variables.mmj1_dR = delta_r(
            dilepton_eta, variables.jet1_eta, dilepton_phi, variables.jet1_phi
        )

        variables.mmj2_dEta, variables.mmj2_dPhi, variables.mmj2_dR = delta_r(
            dilepton_eta, variables.jet2_eta, dilepton_phi, variables.jet2_phi
        )

        variables.mmj_min_dEta = np.where(
            variables.mmj1_dEta,
            variables.mmj2_dEta,
            (variables.mmj1_dEta < variables.mmj2_dEta),
        )

        variables.mmj_min_dPhi = np.where(
            variables.mmj1_dPhi,
            variables.mmj2_dPhi,
            (variables.mmj1_dPhi < variables.mmj2_dPhi),
        )


def fill_bjets(output, variables, jets, leptons, flavor="mu", is_mc=True):
    variable_names = [
        "bjet1_pt",
        "bjet1_eta",
        "bjet1_rap",
        "bjet1_phi",
        "bjet1_qgl",
        "bjet1_jetId",
        "bjet1_puId",
        "bjet1_btagDeepB",
        "bjet2_pt",
        "bjet2_eta",
        "bjet2_rap",
        "bjet2_phi",
        "bjet2_qgl",
        "bjet2_jetId",
        "bjet2_puId",
        "bjet2_btagDeepB",
        "bjet1_sf",
        "bjet2_sf",
        "bjj_mass",
        "bjj_mass_log",
        "bjj_pt",
        "bjj_eta",
        "bjj_phi",
        "bjj_dEta",
        "bjj_dPhi",
        "bllj1_dEta",
        "bllj1_dPhi",
        "bllj1_dR",
       
        "b1l1_dEta",
        "b1l1_dPhi",
        "b1l1_dR",

        "b1l2_dEta",
        "b1l2_dPhi",
        "b1l2_dR",


        "bllj2_dEta",
        "bllj2_dPhi",
        "bllj2_dR",
        "bllj_min_dEta",
        "bllj_min_dPhi",
        "blljj_pt",
        "blljj_eta",
        "blljj_phi",
        "blljj_mass",
        "bllj1_pt",
        "bllj1_eta",
        "bllj1_phi",
        "bllj1_mass",
        "b1l1_mass",
        "b1l2_mass",
        "b2l1_mass",
        "b2l2_mass",
        "min_bl_mass",
        "min_b1l_mass",
        "min_b2l_mass",
        "bselection",
        "lb_angle11",
        "lb_angle21",
        "lb_angle",
    ]

    for v in variable_names:
        variables[v] = -999.0
    njet = len(jets)

    jet1 = jets[0]
    jet2 = jets[1]
    lepton1 = leptons[0]
    lepton2 = leptons[1]



    _,_,dR_mb1 = delta_r(jet1["eta"], lepton1["eta"], jet1["phi"], lepton1["phi"])

    jet1["dR_mb1"] = dR_mb1 < 0.4

    jet1["dR_mb1"] = jet1["dR_mb1"].fillna(False)

    _,_,dR_mb2 = delta_r(jet1["eta"], lepton2["eta"], jet1["phi"], lepton2["phi"])

    jet1["dR_mb2"] = dR_mb2 < 0.4

    jet1["dR_mb2"] = jet1["dR_mb2"].fillna(False)


    # Fill single jet variables
    for v in [
        "pt",
        "eta",
        "phi",
        "pt_gen",
        "eta_gen",
        "phi_gen",
        "qgl",
        "btagDeepB",
        "sf",
    ]:
        try:
            variables[f"bjet1_{v}"] = jet1[v]
            variables[f"bjet2_{v}"] = jet2[v]
        except Exception:
            variables[f"bjet1_{v}"] = -999.0
            variables[f"bjet2_{v}"] = -999.0
    variables.bjet1_rap = rapidity(jet1)

        
    variables[f"bjet1_mb1_dR"] =  jet1["dR_mb1"]
    variables[f"bjet1_mb2_dR"] =  jet1["dR_mb2"]


    if flavor == "mu":
        mm_columns = [
            "dimuon_mass",
            "dimuon_pt",
            "dimuon_eta",
            "dimuon_phi",
            "dimuon_mass_gen",
            "dimuon_pt_gen",
            "dimuon_eta_gen",
            "dimuon_phi_gen",
        ]
    else:
        mm_columns = [
            "dielectron_mass",
            "dielectron_pt",
            "dielectron_eta",
            "dielectron_phi",
            "dielectron_mass_gen",
            "dielectron_pt_gen",
            "dielectron_eta_gen",
            "dielectron_phi_gen",
        ]

    dileptons = output.loc[:, mm_columns]
    dileptons.columns = [
        "mass",
        "pt",
        "eta",
        "phi",
        "mass_gen",
        "pt_gen",
        "eta_gen",
        "phi_gen",
    ]

    if njet > 0:
        bjet = p4(jet1, is_mc=is_mc)
        mmj = p4_sum(dileptons, bjet, is_mc=is_mc)
        for v in [
            "pt",
            "eta",
            "phi",
            "mass",
            "mass_gen",
            "pt_gen",
            "eta_gen",
            "phi_gen",
        ]:
            try:
                variables[f"bmmj1_{v}"] = mmj[v]
            except Exception:
                variables[f"bmmj1_{v}"] = -999.0

        lep1 = p4(lepton1, is_mc=is_mc)
        lep2 = p4(lepton2, is_mc=is_mc)

        ml1 = p4_sum(jet1, lepton1, is_mc=is_mc)
        ml2 = p4_sum(jet1, lepton2, is_mc=is_mc)
        try:
            variables["b1l1_mass"] = ml1["mass"]
        except Exception:
            variables["b1l1_mass"] = 100000
        try:
            variables["b1l2_mass"] = ml2["mass"]
        except Exception:
            variables["b1l2_mass"] = 100000

        variables["min_b1l_mass"] = variables[["b1l1_mass", "b1l2_mass"]].min(axis=1)
        variables["min_bl_mass"] = variables[["b1l1_mass", "b1l2_mass"]].min(axis=1)

        lbangle11 = bbangle(lepton1, jet1)
        lbangle21 = bbangle(lepton2, jet1)

        try:
            variables["lb_angle11"] = lbangle11

        except Exception:
            variables["lb_angle11"] = 100000

        try:
            variables["lb_angle21"] = lbangle21

        except Exception:
            variables["lb_angle21"] = 100000

        
        variables["lb_angle"] = variables[["lb_angle11", "lb_angle21"]].min(axis=1)

        dilepton_pt, dilepton_eta, dilepton_phi, dilepton_rap = (
            output.dielectron_pt,
            output.dielectron_eta,
            output.dielectron_phi,
            output.dielectron_rap,
        )



        variables.bllj1_dEta, variables.bllj1_dPhi, variables.bllj1_dR = delta_r(
            dilepton_eta, variables.bjet1_eta, dilepton_phi, variables.bjet1_phi
        )

        variables.b1l1_dEta, variables.b1l1_dPhi, variables.b1l1_dR = delta_r(
            output.e1_eta, variables.bjet1_eta, output.e1_phi, variables.bjet1_phi
        )

        variables.b1l2_dEta, variables.b1l2_dPhi, variables.b1l2_dR = delta_r(
            output.e2_eta, variables.bjet1_eta, output.e2_phi, variables.bjet1_phi
        )



    if njet > 1:
        bjet2 = p4(jet1, is_mc=is_mc)
        mmj2 = p4_sum(dileptons, bjet2, is_mc=is_mc)
        for v in [
            "pt",
            "eta",
            "phi",
            "mass",
            "mass_gen",
            "pt_gen",
            "eta_gen",
            "phi_gen",
        ]:
            try:
                variables[f"bmmj2_{v}"] = mmj[v]
            except Exception:
                variables[f"bmmj2_{v}"] = -999.0

        lep1 = p4(lepton1, is_mc=is_mc)
        lep2 = p4(lepton2, is_mc=is_mc)

        ml1 = p4_sum(jet2, lepton1, is_mc=is_mc)
        ml2 = p4_sum(jet2, lepton2, is_mc=is_mc)
        try:
            variables["b2l1_mass"] = ml1["mass"]
        except Exception:
            variables["b2l1_mass"] = 100000
        try:
            variables["b2l2_mass"] = ml2["mass"]
        except Exception:
            variables["b2l2_mass"] = 100000

        variables["min_b2l_mass"] = variables[["b2l1_mass", "b2l2_mass"]].min(axis=1)
        variables["min_bl_mass"] = variables[
            ["b1l1_mass", "b1l2_mass", "b2l1_mass", "b2l2_mass"]
        ].min(axis=1)

        variables.bjet2_rap = rapidity(jet2)
        # Fill dijet variables
        jj = p4_sum(jet1, jet2, is_mc=is_mc)
        for v in [
            "pt",
            "eta",
            "phi",
            "mass",
            "pt_gen",
            "eta_gen",
            "phi_gen",
            "mass_gen",
        ]:
            try:
                variables[f"bjj_{v}"] = jj[v]
            except Exception:
                variables[f"bjj_{v}"] = -999.0

        variables.bjj_mass_log = np.log(variables.bjj_mass)

        variables.bjj_dEta, variables.bjj_dPhi, _ = delta_r(
            variables.bjet1_eta,
            variables.bjet2_eta,
            variables.bjet1_phi,
            variables.bjet2_phi,
        )

        # Fill dimuon-dibjet system variables
        jj_columns = [
            "bjj_pt",
            "bjj_eta",
            "bjj_phi",
            "bjj_mass",
            "bjj_pt_gen",
            "bjj_eta_gen",
            "bjj_phi_gen",
            "bjj_mass_gen",
        ]

        dijets = variables.loc[:, jj_columns]

        # careful with renaming
        dijets.columns = [
            "pt",
            "eta",
            "phi",
            "mass",
            "mass_gen",
            "pt_gen",
            "eta_gen",
            "phi_gen",
        ]

        mmjj = p4_sum(dileptons, dijets, is_mc=is_mc)
        for v in [
            "pt",
            "eta",
            "phi",
            "mass",
            "mass_gen",
            "pt_gen",
            "eta_gen",
            "phi_gen",
        ]:
            try:
                variables[f"bmmjj_{v}"] = mmjj[v]
            except Exception:
                variables[f"bmmjj_{v}"] = -999.0


def jet_id(jets, parameters, year):
    pass_jet_id = np.ones_like(jets.jetId, dtype=bool)
    if "loose" in parameters["jet_id"]:
        pass_jet_id = jets.jetId >= 1
    elif "tight" in parameters["jet_id"]:
        if "2016" in year:
            pass_jet_id = jets.jetId >= 3
        else:
            pass_jet_id = jets.jetId >= 2
    return pass_jet_id


def jet_puid(jets, parameters, year):
    jet_puid_opt = parameters["jet_puid"]
    puId = jets.puId17 if year == "2017" else jets.puId
    jet_puid_wps = {
        "loose": (puId >= 4) | (jets.pt > 50),
        "medium": (puId >= 6) | (jets.pt > 50),
        "tight": (puId >= 7) | (jets.pt > 50),
    }
    pass_jet_puid = np.ones_like(jets.pt.values)
    if jet_puid_opt in ["loose", "medium", "tight"]:
        pass_jet_puid = jet_puid_wps[jet_puid_opt]
    elif "2017corrected" in jet_puid_opt:
        eta_window = (abs(jets.eta) > 2.6) & (abs(jets.eta) < 3.0)
        pass_jet_puid = (eta_window & (puId >= 7)) | (
            (~eta_window) & jet_puid_wps["loose"]
        )
    return pass_jet_puid


def gen_jet_pair_mass(df):
    gjmass = None
    gjets = df.GenJet
    gleptons = df.GenPart[
        (abs(df.GenPart.pdgId) == 13)
        | (abs(df.GenPart.pdgId) == 11)
        | (abs(df.GenPart.pdgId) == 15)
    ]
    gl_pair = ak.cartesian({"jet": gjets, "lepton": gleptons}, axis=1, nested=True)
    _, _, dr_gl = delta_r(
        gl_pair["jet"].eta,
        gl_pair["lepton"].eta,
        gl_pair["jet"].phi,
        gl_pair["lepton"].phi,
    )
    isolated = ak.all((dr_gl > 0.3), axis=-1)
    if ak.count(gjets[isolated], axis=None) > 0:
        # TODO: convert only relevant fields!
        gjet1 = ak.to_pandas(gjets[isolated]).loc[
            pd.IndexSlice[:, 0], ["pt", "eta", "phi", "mass"]
        ]
        gjet2 = ak.to_pandas(gjets[isolated]).loc[
            pd.IndexSlice[:, 1], ["pt", "eta", "phi", "mass"]
        ]
        gjet1.index = gjet1.index.droplevel("subentry")
        gjet2.index = gjet2.index.droplevel("subentry")

        gjsum = p4_sum(gjet1, gjet2)
        gjmass = gjsum.mass
    return gjmass


def fill_softjets(df, output, variables, cutoff):
    saj_df = ak.to_pandas(df.SoftActivityJet)
    saj_df["mass"] = 0.0
    nj_name = f"SoftActivityJetNjets{cutoff}"
    ht_name = f"SoftActivityJetHT{cutoff}"
    res = ak.to_pandas(df[[nj_name, ht_name]])

    res["to_correct"] = output.two_muons | (variables.njets > 0)
    _, _, dR_m1 = delta_r(saj_df.eta, output.mu1_eta, saj_df.phi, output.mu1_phi)
    _, _, dR_m2 = delta_r(saj_df.eta, output.mu2_eta, saj_df.phi, output.mu2_phi)
    _, _, dR_j1 = delta_r(
        saj_df.eta, variables.jet1_eta, saj_df.phi, variables.jet1_phi
    )
    _, _, dR_j2 = delta_r(
        saj_df.eta, variables.jet2_eta, saj_df.phi, variables.jet2_phi
    )
    saj_df["dR_m1"] = dR_m1 < 0.4
    saj_df["dR_m2"] = dR_m2 < 0.4
    saj_df["dR_j1"] = dR_j1 < 0.4
    saj_df["dR_j2"] = dR_j2 < 0.4
    dr_cols = ["dR_m1", "dR_m2", "dR_j1", "dR_j2"]
    saj_df[dr_cols] = saj_df[dr_cols].fillna(False)
    saj_df["to_remove"] = saj_df[dr_cols].sum(axis=1).astype(bool)

    saj_df_filtered = saj_df[(~saj_df.to_remove) & (saj_df.pt > cutoff)]
    footprint = saj_df[(saj_df.to_remove) & (saj_df.pt > cutoff)]
    res["njets_corrected"] = (
        saj_df_filtered.reset_index().groupby("entry")["subentry"].nunique()
    )
    res["njets_corrected"] = res["njets_corrected"].fillna(0).astype(int)
    res["footprint"] = footprint.pt.groupby(level=[0]).sum()
    res["footprint"] = res["footprint"].fillna(0.0)
    res["ht_corrected"] = res[ht_name] - res.footprint
    res.loc[res.ht_corrected < 0, "ht_corrected"] = 0.0

    res.loc[res.to_correct, nj_name] = res.loc[res.to_correct, "njets_corrected"]

    res.loc[res.to_correct, ht_name] = res.loc[res.to_correct, "ht_corrected"]

    variables[f"nsoftjets{cutoff}"] = res[f"SoftActivityJetNjets{cutoff}"]
    variables[f"htsoft{cutoff}"] = res[f"SoftActivityJetHT{cutoff}"]
