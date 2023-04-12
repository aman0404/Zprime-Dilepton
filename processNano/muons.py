import numpy as np
import math
from processNano.utils import p4_sum, delta_r, cs_variables
from processNano.corrections.muonMassResolution import smearMass
from processNano.corrections.muonMassScale import muonScaleUncert
from processNano.corrections.muonRecoUncert import muonRecoUncert


def find_dimuon(objs, is_mc=False):
    is_mc = False
    objs1 = objs[objs.charge > 0]
    objs2 = objs[objs.charge < 0]
    objs1["mu_idx"] = objs1.index.to_numpy()
    objs2["mu_idx"] = objs2.index.to_numpy()
    dmass = 20.0

    for i in range(objs1.shape[0]):
        for j in range(objs2.shape[0]):
            px1_ = objs1.iloc[i].pt * np.cos(objs1.iloc[i].phi)
            py1_ = objs1.iloc[i].pt * np.sin(objs1.iloc[i].phi)
            pz1_ = objs1.iloc[i].pt * np.sinh(objs1.iloc[i].eta)
            e1_ = np.sqrt(px1_ ** 2 + py1_ ** 2 + pz1_ ** 2 + objs1.iloc[i].mass ** 2)
            px2_ = objs2.iloc[j].pt * np.cos(objs2.iloc[j].phi)
            py2_ = objs2.iloc[j].pt * np.sin(objs2.iloc[j].phi)
            pz2_ = objs2.iloc[j].pt * np.sinh(objs2.iloc[j].eta)
            e2_ = np.sqrt(px2_ ** 2 + py2_ ** 2 + pz2_ ** 2 + objs2.iloc[j].mass ** 2)
            m2 = (
                (e1_ + e2_) ** 2
                - (px1_ + px2_) ** 2
                - (py1_ + py2_) ** 2
                - (pz1_ + pz2_) ** 2
            )
            mass = math.sqrt(max(0, m2))

            if abs(mass - 91.1876) < dmass:
                dmass = abs(mass - 91.1876)
                obj1_selected = objs1.iloc[i]
                obj2_selected = objs2.iloc[j]
                idx1 = objs1.iloc[i].mu_idx
                idx2 = objs2.iloc[j].mu_idx

                dimuon_mass = mass
                if is_mc:
                    gpx1_ = objs1.iloc[i].pt_gen * np.cos(objs1.iloc[i].phi_gen)
                    gpy1_ = objs1.iloc[i].pt_gen * np.sin(objs1.iloc[i].phi_gen)
                    gpz1_ = objs1.iloc[i].pt_gen * np.sinh(objs1.iloc[i].eta_gen)
                    ge1_ = np.sqrt(
                        gpx1_ ** 2 + gpy1_ ** 2 + gpz1_ ** 2 + objs1.iloc[i].mass ** 2
                    )
                    gpx2_ = objs2.iloc[j].pt_gen * np.cos(objs2.iloc[j].phi_gen)
                    gpy2_ = objs2.iloc[j].pt_gen * np.sin(objs2.iloc[j].phi_gen)
                    gpz2_ = objs2.iloc[j].pt_gen * np.sinh(objs2.iloc[j].eta_gen)
                    ge2_ = np.sqrt(
                        gpx2_ ** 2 + gpy2_ ** 2 + gpz2_ ** 2 + objs2.iloc[j].mass ** 2
                    )
                    gm2 = (
                        (ge1_ + ge2_) ** 2
                        - (gpx1_ + gpx2_) ** 2
                        - (gpy1_ + gpy2_) ** 2
                        - (gpz1_ + gpz2_) ** 2
                    )
                    dimuon_mass_gen = math.sqrt(max(0, gm2))

    if dmass == 20:
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
        dimuon_mass = mass

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
            dimuon_mass_gen = math.sqrt(max(0, gm2))

        obj1_selected = obj1
        obj2_selected = obj2
        idx1 = objs1.pt.idxmax()
        idx2 = objs2.pt.idxmax()

        log1 = obj1_selected.to_numpy()
        log2 = obj2_selected.to_numpy()
        if log1[0] == -1 or log2[0] == -1:
            dimuon_mass_gen = -999.0

    if obj1_selected.pt > obj2_selected.pt:
        if is_mc:
            return [idx1, idx2, dimuon_mass, dimuon_mass_gen]
        else:
            return [idx1, idx2, dimuon_mass]
    else:
        if is_mc:
            return [idx2, idx1, dimuon_mass, dimuon_mass_gen]
        else:
            return [idx2, idx1, dimuon_mass]


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
    dimuon_variable_names = [
        "dimuon_mass",
        # "dimuon_mass_gen",
        "dimuon_mass_res",
        "dimuon_mass_res_rel",
        "dimuon_ebe_mass_res",
        "dimuon_ebe_mass_res_rel",
        "dimuon_pt",
        "dimuon_pt_log",
        "dimuon_eta",
        "dimuon_phi",
        # "dimuon_pt_gen",
        # "dimuon_eta_gen",
        # "dimuon_phi_gen",
        "dimuon_dEta",
        "dimuon_dPhi",
        "dimuon_dR",
        "dimuon_rap",
        "bbangle",
        "dimuon_cos_theta_cs",
        "dimuon_phi_cs",
        "wgt_nominal",
    ]
    v_names = mu1_variable_names + mu2_variable_names + dimuon_variable_names

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
        name = f"dimuon_{v}"
        try:
            output[name] = mm[v]
            output[name] = output[name].fillna(-999.0)
        except Exception:
            output[name] = -999.0

    # create numpy arrays for reco and gen mass needed for mass variations
    recoMassBB = output.loc[
        ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))), "dimuon_mass"
    ].to_numpy()
    recoMassBE = output.loc[
        ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))), "dimuon_mass"
    ].to_numpy()
    genMassBB = output.loc[
        ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))), "dimuon_mass_gen"
    ].to_numpy()
    genMassBE = output.loc[
        ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))), "dimuon_mass_gen"
    ].to_numpy()

    # apply additional mass smearing for MC events in the BE category
    if is_mc:
        output.loc[
            ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))), "dimuon_mass"
        ] = (
            output.loc[
                ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
                "dimuon_mass",
            ]
            * smearMass(genMassBE, year, bb=False, forUnc=False)
        ).values

    # calculate mass values smeared by mass resolution uncertainty
    output["dimuon_mass_resUnc"] = output.dimuon_mass.values
    if is_mc:

        output.loc[
            ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
            "dimuon_mass_resUnc",
        ] = (
            output.loc[
                ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
                "dimuon_mass_resUnc",
            ]
            * smearMass(genMassBB, year, bb=True)
        ).values
        output.loc[
            ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
            "dimuon_mass_resUnc",
        ] = (
            output.loc[
                ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
                "dimuon_mass_resUnc",
            ]
            * smearMass(genMassBE, year, bb=False)
        ).values

    # calculate mass values shifted by mass scale uncertainty
    output["dimuon_mass_scaleUncUp"] = output.dimuon_mass.values
    output["dimuon_mass_scaleUncDown"] = output.dimuon_mass.values
    if is_mc:
        output.loc[
            ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
            "dimuon_mass_scaleUncUp",
        ] = (
            output.loc[
                ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
                "dimuon_mass_scaleUncUp",
            ]
            * muonScaleUncert(recoMassBB, True, year)
        ).values
        output.loc[
            ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
            "dimuon_mass_scaleUncUp",
        ] = (
            output.loc[
                ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
                "dimuon_mass_scaleUncUp",
            ]
            * muonScaleUncert(recoMassBE, False, year)
        ).values
        output.loc[
            ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
            "dimuon_mass_scaleUncDown",
        ] = (
            output.loc[
                ((abs(output.mu1_eta < 1.2)) & (abs(output.mu2_eta < 1.2))),
                "dimuon_mass_scaleUncDown",
            ]
            * muonScaleUncert(recoMassBB, True, year, up=False)
        ).values
        output.loc[
            ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
            "dimuon_mass_scaleUncDown",
        ] = (
            output.loc[
                ((abs(output.mu1_eta > 1.2)) | (abs(output.mu2_eta > 1.2))),
                "dimuon_mass_scaleUncDown",
            ]
            * muonScaleUncert(recoMassBE, False, year, up=False)
        ).values

    # calculate event weights for muon reconstruction efficiency uncertainty
    eta1 = output["mu1_eta"].to_numpy()
    eta2 = output["mu2_eta"].to_numpy()
    pT1 = output["mu1_pt"].to_numpy()
    pT2 = output["mu2_pt"].to_numpy()
    mass = output["dimuon_mass"].to_numpy()
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

    output["mu1_pt_over_mass"] = output.mu1_pt.values / output.dimuon_mass.values
    output["mu2_pt_over_mass"] = output.mu2_pt.values / output.dimuon_mass.values
    output["dimuon_pt_log"] = np.log(output.dimuon_pt[output.dimuon_pt > 0])
    output.loc[output.dimuon_pt < 0, "dimuon_pt_log"] = -999.0

    mm_deta, mm_dphi, mm_dr = delta_r(mu1.eta, mu2.eta, mu1.phi, mu2.phi)
    output["dimuon_pt"] = mm.pt
    output["dimuon_eta"] = mm.eta
    output["dimuon_phi"] = mm.phi
    output["dimuon_dEta"] = mm_deta
    output["dimuon_dPhi"] = mm_dphi
    output["dimuon_dR"] = mm_dr

    # output["dimuon_ebe_mass_res"] = mass_resolution(
    #    is_mc, processor.evaluator, output, processor.year
    # )
    # output["dimuon_ebe_mass_res_rel"] = output.dimuon_ebe_mass_res / output.dimuon_mass
    output["dimuon_cos_theta_cs"], output["dimuon_phi_cs"] = cs_variables(mu1, mu2)


def mass_resolution(is_mc, evaluator, df, year):
    # Returns absolute mass resolution!
    dpt1 = (df.mu1_ptErr * df.dimuon_mass) / (2 * df.mu1_pt)
    dpt2 = (df.mu2_ptErr * df.dimuon_mass) / (2 * df.mu2_pt)

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
