import numpy as np
import math
from processNano.utils import p4_sum, delta_r, cs_variables, p4, rapidity
from processNano.corrections.muonMassResolution import smearMass
from processNano.corrections.muonMassScale import muonScaleUncert
from processNano.corrections.muonRecoUncert import muonRecoUncert

def get_pair_inv_mass(mu_mass, el_mass, mu_pt, el_pt, mu_eta, el_eta, mu_phi, el_phi):
    """
    take the four vectors of the muon + electron pair and calculate their invariant mass
    """
    px1_ = mu_pt * np.cos(mu_phi)
    py1_ = mu_pt * np.sin(mu_phi)
    pz1_ = mu_pt * np.sinh(mu_eta)
    e1_ = np.sqrt(px1_ ** 2 + py1_ ** 2 + pz1_ ** 2 + mu_mass ** 2)
    px2_ = el_pt * np.cos(el_phi)
    py2_ = el_pt * np.sin(el_phi)
    pz2_ = el_pt * np.sinh(el_eta)
    e2_ = np.sqrt(px2_ ** 2 + py2_ ** 2 + pz2_ ** 2 + el_mass ** 2)
    m2 = (
        (e1_ + e2_) ** 2
        - (px1_ + px2_) ** 2
        - (py1_ + py2_) ** 2
        - (pz1_ + pz2_) ** 2
    )
    m2[m2 < 0] = 0 # override negative values as zero
    mass = np.sqrt(m2)
    return mass


def find_dimuon(objs, is_mc=False):
    is_mc = False

    objs1 = objs[objs.charge > 0]
    objs2 = objs[objs.charge < 0]
    # objs1["mu_idx"] = objs1.index.to_numpy()
    # objs2["mu_idx"] = objs2.index.to_numpy()
    # dmass = 20.0

    # for i in range(objs1.shape[0]):
    #     for j in range(objs2.shape[0]):
    #         px1_ = objs1.iloc[i].pt * np.cos(objs1.iloc[i].phi)
    #         py1_ = objs1.iloc[i].pt * np.sin(objs1.iloc[i].phi)
    #         pz1_ = objs1.iloc[i].pt * np.sinh(objs1.iloc[i].eta)
    #         e1_ = np.sqrt(px1_ ** 2 + py1_ ** 2 + pz1_ ** 2 + objs1.iloc[i].mass ** 2)
    #         px2_ = objs2.iloc[j].pt * np.cos(objs2.iloc[j].phi)
    #         py2_ = objs2.iloc[j].pt * np.sin(objs2.iloc[j].phi)
    #         pz2_ = objs2.iloc[j].pt * np.sinh(objs2.iloc[j].eta)
    #         e2_ = np.sqrt(px2_ ** 2 + py2_ ** 2 + pz2_ ** 2 + objs2.iloc[j].mass ** 2)
    #         m2 = (
    #             (e1_ + e2_) ** 2
    #             - (px1_ + px2_) ** 2
    #             - (py1_ + py2_) ** 2
    #             - (pz1_ + pz2_) ** 2
    #         )
    #         mass = math.sqrt(max(0, m2))

    #         if abs(mass - 91.1876) < dmass:
    #             dmass = abs(mass - 91.1876)
    #             obj1_selected = objs1.iloc[i]
    #             obj2_selected = objs2.iloc[j]
    #             idx1 = objs1.iloc[i].mu_idx
    #             idx2 = objs2.iloc[j].mu_idx

    #             dilepton_mass = mass
    #             if is_mc:
    #                 gpx1_ = objs1.iloc[i].pt_gen * np.cos(objs1.iloc[i].phi_gen)
    #                 gpy1_ = objs1.iloc[i].pt_gen * np.sin(objs1.iloc[i].phi_gen)
    #                 gpz1_ = objs1.iloc[i].pt_gen * np.sinh(objs1.iloc[i].eta_gen)
    #                 ge1_ = np.sqrt(
    #                     gpx1_ ** 2 + gpy1_ ** 2 + gpz1_ ** 2 + objs1.iloc[i].mass ** 2
    #                 )
    #                 gpx2_ = objs2.iloc[j].pt_gen * np.cos(objs2.iloc[j].phi_gen)
    #                 gpy2_ = objs2.iloc[j].pt_gen * np.sin(objs2.iloc[j].phi_gen)
    #                 gpz2_ = objs2.iloc[j].pt_gen * np.sinh(objs2.iloc[j].eta_gen)
    #                 ge2_ = np.sqrt(
    #                     gpx2_ ** 2 + gpy2_ ** 2 + gpz2_ ** 2 + objs2.iloc[j].mass ** 2
    #                 )
    #                 gm2 = (
    #                     (ge1_ + ge2_) ** 2
    #                     - (gpx1_ + gpx2_) ** 2
    #                     - (gpy1_ + gpy2_) ** 2
    #                     - (gpz1_ + gpz2_) ** 2
    #                 )
    #                 dilepton_mass_gen = math.sqrt(max(0, gm2))

    if dmass == 20:
        objs1["lepton_idx"] = objs1.index.to_numpy()
        objs2["lepton_idx"] = objs2.index.to_numpy()

        # print(f"type(objs1): {type(objs1)}")
        # print(f"objs1: {objs1}")
        obj1 = objs1.loc[objs1.pt.idxmax()]
        obj2 = objs2.loc[objs2.pt.idxmax()]
        px1_ = obj1.pt * np.cos(obj1.phi)
        py1_ = obj1.pt * np.sin(obj1.phi)
        pz1_ = obj1.pt * np.sinh(obj1.eta)
        e1_ = np.sqrt(px1_ ** 2 + py1_ ** 2 + pz1_ ** 2 + obj1.mass ** 2)
        px2_ = obj2.pt * np.cos(obj2.phi)
        py2_ = obj2.pt * np.sin(obj2.phi)
        pz2_ = obj2.pt * np.sinh(obj2.eta)
        e2_ = np.sqrt(px2_ ** 2 + py2_ ** 2 + pz2_ ** 2 + obj2.mass ** 2)
        m2 = (
            (e1_ + e2_) ** 2
            - (px1_ + px2_) ** 2
            - (py1_ + py2_) ** 2
            - (pz1_ + pz2_) ** 2
        )
        mass = math.sqrt(max(0, m2))
        dilepton_mass = mass

        if is_mc:
            gpx1_ = obj1.pt_gen * np.cos(obj1.phi_gen)
            gpy1_ = obj1.pt_gen * np.sin(obj1.phi_gen)
            gpz1_ = obj1.pt_gen * np.sinh(obj1.eta_gen)
            ge1_ = np.sqrt(gpx1_ ** 2 + gpy1_ ** 2 + gpz1_ ** 2 + obj1.mass ** 2)
            gpx2_ = obj2.pt_gen * np.cos(obj2.phi_gen)
            gpy2_ = obj2.pt_gen * np.sin(obj2.phi_gen)
            gpz2_ = obj2.pt_gen * np.sinh(obj2.eta_gen)
            ge2_ = np.sqrt(gpx2_ ** 2 + gpy2_ ** 2 + gpz2_ ** 2 + obj2.mass ** 2)
            gm2 = (
                (ge1_ + ge2_) ** 2
                - (gpx1_ + gpx2_) ** 2
                - (gpy1_ + gpy2_) ** 2
                - (gpz1_ + gpz2_) ** 2
            )
            dilepton_mass_gen = math.sqrt(max(0, gm2))


        obj1_selected = obj1
        obj2_selected = obj2
        idx1 = objs1.pt.idxmax()
        idx2 = objs2.pt.idxmax()

        log1 = obj1_selected.to_numpy()
        log2 = obj2_selected.to_numpy()
        if log1[0] == -1 or log2[0] == -1:
            dilepton_mass_gen = -999.0

    if obj1_selected.pt > obj2_selected.pt:
        if is_mc:
            return [idx1, idx2, dilepton_mass, dilepton_mass_gen]
        else:
            return [idx1, idx2, dilepton_mass]
    else:
        if is_mc:
            return [idx2, idx1, dilepton_mass, dilepton_mass_gen]
        else:
            return [idx2, idx1, dilepton_mass]


def fill_muons(processor, output, mu1, mu2, is_mc, year, weights):
    mu1_variable_names = [
        "mu1_pt",
        "mu1_pt_gen",
        "mu1_pt_over_mass",
        "mu1_ptErr",
        "mu1_eta",
        "mu1_eta_gen",
        "mu1_phi",
        "mu1_phi_gen",
        "mu1_iso",
        "mu1_dxy",
        "mu1_dz",
        "mu1_genPartFlav",
        "mu1_ip3d",
        "mu1_sip3d",
    ]
    mu2_variable_names = [
        "mu2_pt",
        "mu2_pt_gen",
        "mu2_pt_over_mass",
        "mu2_ptErr",
        "mu2_eta",
        "mu2_eta_gen",
        "mu2_phi",
        "mu2_phi_gen",
        "mu2_iso",
        "mu2_dxy",
        "mu2_dz",
        "mu2_genPartFlav",
        "mu2_ip3d",
        "mu2_sip3d",
    ]
    dilepton_variable_names = [
        "dilepton_mass",
       "dilepton_mass_gen",
        "dilepton_mass_res",
        "dilepton_mass_res_rel",
        "dilepton_ebe_mass_res",
        "dilepton_ebe_mass_res_rel",
        "dilepton_pt",
        "dilepton_pt_log",
        "dilepton_eta",
        "dilepton_phi",
        "dilepton_pt_gen",
        "dilepton_eta_gen",
        "dilepton_phi_gen",
        "dilepton_dEta",
        "dilepton_dPhi",
        "dilepton_dR",
        "dilepton_rap",
        "bbangle",
        "dilepton_cos_theta_cs",
        "dilepton_phi_cs",
        "wgt_nominal",
    ]
    v_names = mu1_variable_names + mu2_variable_names + dilepton_variable_names

    # Initialize columns for muon variables

    for n in v_names:
        output[n] = 0.0

    # Fill single muon variables
    mm = p4_sum(mu1, mu2, is_mc)
    for v in [
        "pt",
        "pt_gen",
        "ptErr",
        "eta",
        "eta_gen",
        "phi",
        "phi_gen",
        "dxy",
        "dz",
        "genPartFlav",
        "ip3d",
        "sip3d",
        "tkRelIso",
        "charge",
    ]:

        try:
            output[f"mu1_{v}"] = mu1[v]
            output[f"mu2_{v}"] = mu2[v]
        except Exception:
            output[f"mu1_{v}"] = -999.0
            output[f"mu2_{v}"] = -999.0

    for v in [
        "pt",
        "eta",
        "phi",
        "mass",
        "rap",
    ]:
        name = f"dilepton_{v}"
        try:
            output[name] = mm[v]
            output[name] = output[name].fillna(-999.0)
        except Exception:
            output[name] = -999.0

    # create numpy arrays for reco and gen mass needed for mass variations
    recoMassBB = output.loc[
        ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))), "dilepton_mass"
    ].to_numpy()
    recoMassBE = output.loc[
        ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))), "dilepton_mass"
    ].to_numpy()
    genMassBB = output.loc[
        ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))), "dilepton_mass_gen"
    ].to_numpy()
    genMassBE = output.loc[
        ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))), "dilepton_mass_gen"
    ].to_numpy()

    # apply additional mass smearing for MC events in the BE category
    if is_mc:
        output.loc[
            ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))), "dilepton_mass"
        ] = (
            output.loc[
                ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
                "dilepton_mass",
            ]
            * smearMass(genMassBE, year, bb=False, forUnc=False)
        ).values

    # calculate mass values smeared by mass resolution uncertainty
    output["dilepton_mass_resUnc"] = output.dilepton_mass.values
    if is_mc:

        output.loc[
            ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
            "dilepton_mass_resUnc",
        ] = (
            output.loc[
                ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
                "dilepton_mass_resUnc",
            ]
            * smearMass(genMassBB, year, bb=True)
        ).values
        output.loc[
            ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
            "dilepton_mass_resUnc",
        ] = (
            output.loc[
                ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
                "dilepton_mass_resUnc",
            ]
            * smearMass(genMassBE, year, bb=False)
        ).values

    # calculate mass values shifted by mass scale uncertainty
    output["dilepton_mass_scaleUncUp"] = output.dilepton_mass.values
    output["dilepton_mass_scaleUncDown"] = output.dilepton_mass.values
    if is_mc:
        output.loc[
            ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
            "dilepton_mass_scaleUncUp",
        ] = (
            output.loc[
                ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
                "dilepton_mass_scaleUncUp",
            ]
            * muonScaleUncert(recoMassBB, True, year)
        ).values
        output.loc[
            ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
            "dilepton_mass_scaleUncUp",
        ] = (
            output.loc[
                ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
                "dilepton_mass_scaleUncUp",
            ]
            * muonScaleUncert(recoMassBE, False, year)
        ).values
        output.loc[
            ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
            "dilepton_mass_scaleUncDown",
        ] = (
            output.loc[
                ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
                "dilepton_mass_scaleUncDown",
            ]
            * muonScaleUncert(recoMassBB, True, year, up=False)
        ).values
        output.loc[
            ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
            "dilepton_mass_scaleUncDown",
        ] = (
            output.loc[
                ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
                "dilepton_mass_scaleUncDown",
            ]
            * muonScaleUncert(recoMassBE, False, year, up=False)
        ).values

    # calculate event weights for muon reconstruction efficiency uncertainty
    eta1 = output["mu1_eta"].to_numpy()
    eta2 = output["mu2_eta"].to_numpy()
    pT1 = output["mu1_pt"].to_numpy()
    pT2 = output["mu2_pt"].to_numpy()
    mass = output["dilepton_mass"].to_numpy()
    isDimuon = output["two_muons"].to_numpy()

    recowgts = {}
    recowgts["nom"] = muonRecoUncert(
        mass, pT1, pT2, eta1, eta2, isDimuon, year, how="nom"
    )
    recowgts["up"] = muonRecoUncert(
        mass, pT1, pT2, eta1, eta2, isDimuon, year, how="up"
    )
    recowgts["down"] = muonRecoUncert(
        mass, pT1, pT2, eta1, eta2, isDimuon, year, how="down"
    )
    weights.add_weight("recowgt", recowgts, how="all")

    output["mu1_pt_over_mass"] = output.mu1_pt.values / output.dilepton_mass.values
    output["mu2_pt_over_mass"] = output.mu2_pt.values / output.dilepton_mass.values
    output["dilepton_pt_log"] = np.log(output.dilepton_pt[output.dilepton_pt > 0])
    output.loc[output.dilepton_pt < 0, "dilepton_pt_log"] = -999.0

    mm_deta, mm_dphi, mm_dr = delta_r(mu1.eta, mu2.eta, mu1.phi, mu2.phi)
    output["dilepton_pt"] = mm.pt
    output["dilepton_eta"] = mm.eta
    output["dilepton_phi"] = mm.phi
    output["dilepton_dEta"] = mm_deta
    output["dilepton_dPhi"] = mm_dphi
    output["dilepton_dR"] = mm_dr

    # output["dilepton_ebe_mass_res"] = mass_resolution(
    #    is_mc, processor.evaluator, output, processor.year
    # )
    # output["dilepton_ebe_mass_res_rel"] = output.dilepton_ebe_mass_res / output.dilepton_mass
    output["dilepton_cos_theta_cs"], output["dilepton_phi_cs"] = cs_variables(mu1, mu2)


def mass_resolution(is_mc, evaluator, df, year):
    # Returns absolute mass resolution!
    dpt1 = (df.mu1_ptErr * df.dilepton_mass) / (2 * df.mu1_pt)
    dpt2 = (df.mu2_ptErr * df.dilepton_mass) / (2 * df.mu2_pt)

    if is_mc:
        label = f"res_calib_MC_{year}"
    else:
        label = f"res_calib_Data_{year}"
    calibration = np.array(
        evaluator[label](
            df.mu1_pt.values, abs(df.mu1_eta.values), abs(df.mu2_eta.values)
        )
    )

    return np.sqrt(dpt1 * dpt1 + dpt2 * dpt2) * calibration


def fill_bjets(output, variables, jets, leptons, is_mc=True):
    variable_names = [
        "bjet1_pt",
        "bjet1_eta",
        "bjet1_rap",
        "bjet1_phi",
        # "bjet1_qgl",
        # "bjet1_jetId",
        # "bjet1_puId",
        # "bjet1_btagDeepB",
        "bjet2_pt",
        "bjet2_eta",
        "bjet2_rap",
        "bjet2_phi",
        # "bjet2_qgl",
        # "bjet2_jetId",
        # "bjet2_puId",
        # "bjet2_btagDeepB",
        # "bjet1_sf",
        # "bjet2_sf",
        # "bjj_mass",
        # "bjj_mass_log",
        # "bjj_pt",
        # "bjj_eta",
        # "bjj_phi",
        # "bjj_dEta",
        # "bjj_dPhi",
        # "bllj1_dEta",
        # "bllj1_dPhi",
        # "bllj1_dR",
        # "bllj2_dEta",
        # "bllj2_dPhi",
        # "bllj2_dR",
        # "bllj_min_dEta",
        # "bllj_min_dPhi",
        # "blljj_pt",
        # "blljj_eta",
        # "blljj_phi",
        # "blljj_mass",
        # "bllj1_pt",
        # "bllj1_eta",
        # "bllj1_phi",
        # "bllj1_mass",
        # "b1l1_mass",
        # "b1l2_mass",
        # "b2l1_mass",
        # "b2l2_mass",
        "min_bl_mass",
        "min_b1l_mass",
        "min_b2l_mass",
        # "bselection",
        "dilepton_mass",
        "dilepton_pt",
        "dilepton_eta",
        "dilepton_phi",
        "dilepton_mass_gen",
        "dilepton_pt_gen",
        "dilepton_eta_gen",
        "dilepton_phi_gen",
    ]
    for v in variable_names:
        variables[v] = -999.0
    njet = len(jets)

    
    lepton1 = leptons[0] # muon
    lepton2 = leptons[1] # electron
    jet1 = jets[0] # leading bjet
    jet2 = jets[1] # subleading b jet

    _,_,dR_mb1 = delta_r(jet1["eta"], lepton1["eta"], jet1["phi"], lepton1["phi"])

    jet1["dR_mb1"] = dR_mb1 > 0.4


    _,_,dR_eb1 = delta_r(jet1["eta"], lepton2["eta"], jet1["phi"], lepton2["phi"])

    jet1["dR_eb1"] = dR_eb1 > 0.4



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
    
    variables[f"bjet1_ll_dR"] =  jet1["dR_mb1"] & jet1["dR_eb1"]
    variables[f"bjet1_ll_dR"].fillna(True, inplace=True) # NaN exists for nbjets ==0, in which case, we don't need to worry about min dR
    # variables[f"bjet1_mb2_dR"] =  jet1["dR_eb1"]
    dileptons = p4_sum(lepton1, lepton2, is_mc=is_mc)

    ll_columns = [
        "dilepton_mass",
        "dilepton_pt",
        "dilepton_eta",
        "dilepton_phi",
        "dilepton_mass_gen",
        "dilepton_pt_gen",
        "dilepton_eta_gen",
        "dilepton_phi_gen",
    ]
    for col in ll_columns:
        dilep_col = col[len("dilepton_"):]
        variables[col] = dileptons[dilep_col]
    # dileptons = output.loc[:, ll_columns]
    # dileptons.columns = [
    #     "mass",
    #     "pt",
    #     "eta",
    #     "phi",
    #     "mass_gen",
    #     "pt_gen",
    #     "eta_gen",
    #     "phi_gen",
    # ]

    if njet > 0:
        bjet = p4(jet1, is_mc=is_mc)
        llj = p4_sum(dileptons, bjet, is_mc=is_mc)
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
                variables[f"bllj1_{v}"] = llj[v]
            except Exception:
                variables[f"bllj1_{v}"] = -999.0

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
        variables["min_b1l_mass"].fillna(0, inplace=True)
        variables["min_bl_mass"] = variables[["b1l1_mass", "b1l2_mass"]].min(axis=1)
        variables["min_bl_mass"].fillna(0, inplace=True)
    if njet > 1:
        bjet2 = p4(jet2, is_mc=is_mc) # NOTE: this line is sus -> need confirmation
        llj2 = p4_sum(dileptons, bjet2, is_mc=is_mc)
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
                variables[f"bllj2_{v}"] = llj[v]
            except Exception:
                variables[f"bllj2_{v}"] = -999.0

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
        variables["min_b2l_mass"].fillna(0, inplace=True)
        variables["min_bl_mass"] = variables[
            ["b1l1_mass", "b1l2_mass", "b2l1_mass", "b2l2_mass"]
        ].min(axis=1)
        variables["min_bl_mass"].fillna(0, inplace=True)
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
        # Fill dilepton-dibjet system variables
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

        lljj = p4_sum(dileptons, dijets, is_mc=is_mc)
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
                variables[f"blljj_{v}"] = lljj[v]
            except Exception:
                variables[f"blljj_{v}"] = -999.0


# skip fill jets
def fill_jets(output, variables, jets, is_mc=True):
    variable_names = [
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
        "llj1_dEta",
        "llj1_dPhi",
        "llj1_dR",
        "llj2_dEta",
        "llj2_dPhi",
        "llj2_dR",
        "llj_min_dEta",
        "llj_min_dPhi",
        "lljj_pt",
        "lljj_eta",
        "lljj_phi",
        "lljj_mass",
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

        # Fill dilepton-dijet system variables
        # ll_columns = [
        #    "dilepton_pt",
        #    "dilepton_eta",
        #    "dilepton_phi",
        #    "dilepton_mass",
        #    "dilepton_pt_gen",
        #    "dilepton_eta_gen",
        #    "dilepton_phi_gen",
        #    "dilepton_mass_gen",
        # ]
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

        # dileptons = output.loc[:, ll_columns]
        dijets = variables.loc[:, jj_columns]

        # careful with renaming
        # dileptons.columns = [
        #     "mass",
        #     "pt",
        #     "eta",
        #     "phi",
        #     "mass_gen",
        #     "pt_gen",
        #     "eta_gen",
        #     "phi_gen",
        # ]
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

        # lljj = p4_sum(dileptons, dijets, is_mc=is_mc)
        # for v in [
        #     "pt",
        #     "eta",
        #     "phi",
        #     "mass",
        #     "mass_gen",
        #     "pt_gen",
        #     "eta_gen",
        #     "phi_gen",
        # ]:
        #     try:
        #         variables[f"lljj_{v}"] = lljj[v]
        #     except Exception:
        #         variables[f"lljj_{v}"] = -999.0

        # dilepton_pt, dilepton_eta, dilepton_phi, dilepton_rap = (
        #     output.dilepton_pt,
        #     output.dilepton_eta,
        #     output.dilepton_phi,
        #     output.dilepton_rap,
        # )

        # variables.zeppenfeld = dilepton_eta - 0.5 * (
        #     variables.jet1_eta + variables.jet2_eta
        # )

        # variables.rpt = variables.lljj_pt / (
        #     dilepton_pt + variables.jet1_pt + variables.jet2_pt
        # )

        # ll_ystar = dilepton_rap - (variables.jet1_rap + variables.jet2_rap) / 2

        # ll_zstar = abs(ll_ystar / (variables.jet1_rap - variables.jet2_rap))

        # variables.ll_zstar_log = np.log(ll_zstar)

        # variables.llj1_dEta, variables.llj1_dPhi, variables.llj1_dR = delta_r(
        #     dilepton_eta, variables.jet1_eta, dilepton_phi, variables.jet1_phi
        # )

        # variables.llj2_dEta, variables.llj2_dPhi, variables.llj2_dR = delta_r(
        #     dilepton_eta, variables.jet2_eta, dilepton_phi, variables.jet2_phi
        # )

        # variables.llj_min_dEta = np.where(
        #     variables.llj1_dEta,
        #     variables.llj2_dEta,
        #     (variables.llj1_dEta < variables.llj2_dEta),
        # )

        # variables.llj_min_dPhi = np.where(
        #     variables.llj1_dPhi,
        #     variables.llj2_dPhi,
        #     (variables.llj1_dPhi < variables.llj2_dPhi),
        # )