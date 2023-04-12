import numpy as np
import math

from processNano.utils import p4_sum, delta_r, cs_variables
#from processNano.corrections.electronMassScale import electronScaleUncert

def find_dielectron(objs, is_mc=True):

    objs["el_idx"] = objs.index.to_numpy()
    dmass = 20.0
    for i in range(objs.shape[0] - 1):
        for j in range(i + 1, objs.shape[0]):
            px1_ = objs.iloc[i].pt * np.cos(objs.iloc[i].phi)
            py1_ = objs.iloc[i].pt * np.sin(objs.iloc[i].phi)
            pz1_ = objs.iloc[i].pt * np.sinh(objs.iloc[i].eta)
            e1_ = np.sqrt(px1_ ** 2 + py1_ ** 2 + pz1_ ** 2 + objs.iloc[i].mass ** 2)
            px2_ = objs.iloc[j].pt * np.cos(objs.iloc[j].phi)
            py2_ = objs.iloc[j].pt * np.sin(objs.iloc[j].phi)
            pz2_ = objs.iloc[j].pt * np.sinh(objs.iloc[j].eta)
            e2_ = np.sqrt(px2_ ** 2 + py2_ ** 2 + pz2_ ** 2 + objs.iloc[j].mass ** 2)
            m2 = (
                (e1_ + e2_) ** 2
                - (px1_ + px2_) ** 2
                - (py1_ + py2_) ** 2
                - (pz1_ + pz2_) ** 2
            )
            mass = math.sqrt(max(0, m2))
            if abs(mass - 91.1876) < dmass:
                dmass = abs(mass - 91.1876)
                idx1 = objs.iloc[i].el_idx
                idx2 = objs.iloc[j].el_idx
                dielectron_mass = mass
                if is_mc:
                    gpx1_ = objs.iloc[i].pt_gen * np.cos(objs.iloc[i].phi_gen)
                    gpy1_ = objs.iloc[i].pt_gen * np.sin(objs.iloc[i].phi_gen)
                    gpz1_ = objs.iloc[i].pt_gen * np.sinh(objs.iloc[i].eta_gen)
                    ge1_ = np.sqrt(
                        gpx1_ ** 2 + gpy1_ ** 2 + gpz1_ ** 2 + objs.iloc[i].mass ** 2
                    )
                    gpx2_ = objs.iloc[j].pt_gen * np.cos(objs.iloc[j].phi_gen)
                    gpy2_ = objs.iloc[j].pt_gen * np.sin(objs.iloc[j].phi_gen)
                    gpz2_ = objs.iloc[j].pt_gen * np.sinh(objs.iloc[j].eta_gen)
                    ge2_ = np.sqrt(
                        gpx2_ ** 2 + gpy2_ ** 2 + gpz2_ ** 2 + objs.iloc[j].mass ** 2
                    )
                    gm2 = (
                        (ge1_ + ge2_) ** 2
                        - (gpx1_ + gpx2_) ** 2
                        - (gpy1_ + gpy2_) ** 2
                        - (gpz1_ + gpz2_) ** 2
                    )
                    dielectron_mass_gen = math.sqrt(max(0, gm2))

    if dmass == 20:
        objs = objs.sort_values(by="pt")

        obj1 = objs.iloc[-1]
        obj2 = objs.iloc[-2]

        #if is_mc:
        #   obj1 = objs.iloc[-1]
        #   obj2 = objs.iloc[-2]
        #else:
        #   obj1 = objs.iloc[-1]
        #   obj2 = objs.iloc[-2]
           #obj2 = objs.iloc[-3]
 
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
        dielectron_mass = mass
        idx1 = obj1.el_idx
        idx2 = obj2.el_idx
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
            dielectron_mass_gen = math.sqrt(max(0, gm2))
    if is_mc:
        log1 = objs.loc[objs.el_idx == idx1, "idx"].to_numpy()
        log2 = objs.loc[objs.el_idx == idx2, "idx"].to_numpy()
        if log1[0] == -1 or log2[0] == -1:
            dielectron_mass_gen = -999.0
        return [idx1, idx2, dielectron_mass, dielectron_mass_gen]
    else:
        return [idx1, idx2, dielectron_mass]


def fill_electrons(output, e1, e2, is_mc=True):
    e1_variable_names = [
        "e1_pt",
        "e1_pt_gen",
        "e1_pt_over_mass",
        "e1_ptErr",
        "e1_eta",
        "e1_eta_gen",
        "e1_phi",
        "e1_phi_gen",
        "e1_iso",
        "e1_dxy",
        "e1_dz",
        "e1_genPartFlav",
        "e1_ip3d",
        "e1_sip3d",
    ]
    e2_variable_names = [
        "e2_pt",
        "e2_pt_gen",
        "e2_pt_over_mass",
        "e2_ptErr",
        "e2_eta",
        "e2_eta_gen",
        "e2_phi",
        "e2_phi_gen",
        "e2_iso",
        "e2_dxy",
        "e2_dz",
        "e2_genPartFlav",
        "e2_ip3d",
        "e2_sip3d",
    ]

    dielectron_variable_names = [
        "dielectron_mass",
        "dielectron_mass_gen",
        "dielectron_mass_res",
        "dielectron_mass_res_rel",
        "dielectron_ebe_mass_res",
        "dielectron_ebe_mass_res_rel",
        "dielectron_pt",
        "dielectron_pt_log",
        "dielectron_eta",
        "dielectron_phi",
        "dielectron_pt_gen",
        "dielectron_eta_gen",
        "dielectron_phi_gen",
        "dielectron_dEta",
        "dielectron_dPhi",
        "dielectron_dR",
        "dielectron_rap",
        "dielectron_cos_theta_cs",
        "dielectron_phi_cs",
        "wgt_nominal",
        "pu_wgt",
    ]
    v_names = e1_variable_names + e2_variable_names + dielectron_variable_names

    # Initialize columns for electron variables
    for n in v_names:
        output[n] = 0.0

    # Fill single electron variables
    for v in [
        "pt",
        "eta",
        "phi",
        "pt_raw",
        "eta_raw",
        "phi_raw",
        "pt_gen",
        "eta_gen",
        "phi_gen",
    ]:
        try:
            output[f"e1_{v}"] = e1[v]
            output[f"e2_{v}"] = e2[v]
        except Exception:
            output[f"e1_{v}"] = -999.0
            output[f"e2_{v}"] = -999.0

    # Fill dielectron variables

    ee = p4_sum(e1, e2, is_mc)
    for v in [
        "pt",
        "eta",
        "phi",
        "mass",
        "pt_gen",
        "eta_gen",
        "phi_gen",
        "mass_gen",
        "rap",
    ]:
        name = f"dielectron_{v}"
        try:
            output[name] = ee[v]
            output[name] = output[name].fillna(-999.0)
        except Exception:
            output[name] = -999.0

    output["dielectron_pt_log"] = np.log(output.dielectron_pt[output.dielectron_pt > 0])
    output.loc[output.dielectron_pt < 0, "dielectron_pt_log"] = -999.0

    ee_deta, ee_dphi, ee_dr = delta_r(e1.eta, e2.eta, e1.phi, e2.phi)
    output["dielectron_pt"] = ee.pt
    output["dielectron_eta"] = ee.eta
    output["dielectron_phi"] = ee.phi
    output["dielectron_dEta"] = ee_deta
    output["dielectron_dPhi"] = ee_dphi
    output["dielectron_dR"] = ee_dr
    output["dielectron_cos_theta_cs"], output["dielectron_phi_cs"] = cs_variables(
        e1, e2
    )


    ee = p4_sum(e1, e2, is_mc,eScale="Up")
    for v in [
        "mass_scaleUncUp",
    ]:
        name = f"dielectron_{v}"
        try:
            output[name] = ee[v]
            output[name] = output[name].fillna(-999.0)
        except Exception:
            output[name] = -999.0

    ee = p4_sum(e1, e2, is_mc,eScale="Down")
    for v in [
        "mass_scaleUncDown",
    ]:
        name = f"dielectron_{v}"
        try:
            output[name] = ee[v]
            output[name] = output[name].fillna(-999.0)
        except Exception:
            output[name] = -999.0
