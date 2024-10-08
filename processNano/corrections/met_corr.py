import numpy as np


def corrMet(met, obj):
    
    metpt   = met.pt
    meteta  = 0
    metphi  = met.phi
    met_m   = met.pt

    met_px  = metpt * np.cos(metphi)    
    met_py  = metpt * np.sin(metphi)    

    muon_pt_raw = obj.pt_raw
    muon_eta    = obj.eta
    muon_phi    = obj.phi

    muon_px = muon_pt_raw * np.cos(muon_phi)
    muon_py = muon_pt_raw * np.sin(muon_phi)

#    sum_mupt_raw = [np.sum(inner_array) if len(inner_array) > 0 else 0 for inner_array in muon_pt_raw]
    muon_pxx = muon_px.groupby("entry").sum()
    muon_pyy = muon_py.groupby("entry").sum()

    muon_pxx_reindexed = muon_pxx.reindex(met_px.index,  fill_value=0)
    muon_pyy_reindexed = muon_pyy.reindex(met_py.index,  fill_value=0)

    muon_tunePt = obj.pt

    mu_tunePx = muon_tunePt * np.cos(muon_phi)
    mu_tunePy = muon_tunePt * np.sin(muon_phi)

    mu_tunePxx = mu_tunePx.groupby("entry").sum()
    mu_tunePyy = mu_tunePy.groupby("entry").sum()

    mu_tunePxx_reindexed  = mu_tunePxx.reindex(met_px.index,  fill_value=0)
    mu_tunePyy_reindexed  = mu_tunePyy.reindex(met_py.index,  fill_value=0)


    met_corrPx = met_px - muon_pxx_reindexed + mu_tunePxx_reindexed
    met_corrPy = met_py - muon_pyy_reindexed + mu_tunePyy_reindexed

#    sum_mupt_tunep = [np.sum(inner_array) if len(inner_array) > 0 else 0 for inner_array in muon_tunePt]


    met_corrPt = np.sqrt(met_corrPx ** 2 + met_corrPy ** 2)
    #print(met_corrPt, met.pt)
    return met_corrPt

    

   


   
     
