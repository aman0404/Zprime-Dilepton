import numpy as np
import math
from processNano.utils import p4_sum, delta_r, cs_variables


def find_dielectron(objs, is_mc=False):
    is_mc = False
    objs1 = objs[objs.charge > 0]
    objs2 = objs[objs.charge < 0]
    objs1["el_idx"] = objs1.index.to_numpy()
    objs2["el_idx"] = objs2.index.to_numpy()
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
                idx1 = objs1.iloc[i].el_idx
                idx2 = objs2.iloc[j].el_idx

                dielectron_mass = mass
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
                    dielectron_mass_gen = math.sqrt(max(0, gm2))

    if dmass == 20:
        objs1 = objs1.sort_values(by="pt")
        objs2 = objs2.sort_values(by="pt")
        obj1 = objs1.iloc[-1]
        obj2 = objs2.iloc[-1]
        #obj1 = objs1.loc[objs1.pt.idxmax()]
        #obj2 = objs2.loc[objs2.pt.idxmax()]
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

        obj1_selected = obj1
        obj2_selected = obj2
        idx1 = objs1.pt.idxmax()
        idx2 = objs2.pt.idxmax()

        log1 = obj1_selected.to_numpy()
        log2 = obj2_selected.to_numpy()
        if log1[0] == -1 or log2[0] == -1:
            dielectron_mass_gen = -999.0

    if obj1_selected.pt > obj2_selected.pt:
        if is_mc:
            return [idx1, idx2, dielectron_mass, dielectron_mass_gen]
        else:
            return [idx1, idx2, dielectron_mass]
    else:
        if is_mc:
            return [idx2, idx1, dielectron_mass, dielectron_mass_gen]
        else:
            return [idx2, idx1, dielectron_mass]


