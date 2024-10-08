from config.parameters import parameters
import correctionlib
import numpy as np
import pandas as pd
import awkward  as ak


def musf_iso_evaluator(parameters, year, mu1, mu2):


    scaleFactors = parameters["muSFFileList"]
    id_file = scaleFactors[0]['iso']

    muon_correctionset = correctionlib.CorrectionSet.from_file(
        id_file[0]
    )
    print(id_file) 
    
    sf = pd.DataFrame(
        index=mu1.index,
        columns=[
            "muISO_nom",
            "muISO_up",
            "muISO_down",
        ],
    )
    sf = sf.fillna(1.0)  

    for mu in [mu1, mu2]:
        pt = mu.pt.values
        eta = mu.eta_raw.values
        abs_eta = abs(mu.eta_raw.values)

    muID_ = muon_correctionset[id_file[1]].evaluate(
         np.abs(eta), np.abs(pt), "nominal"
    )
    muIDUp_ = muon_correctionset[id_file[1]].evaluate(
         np.abs(eta), np.abs(pt), "systup"
    )
    muIDDown_ = muon_correctionset[id_file[1]].evaluate(
         np.abs(eta), np.abs(pt), "systdown"
    )

    sf["muISO_nom"] *= ak.to_numpy(muID_)
    sf["muISO_up"] *= ak.to_numpy(muIDUp_)
    sf["muISO_down"] *= ak.to_numpy(muIDDown_)

    muID = {"nom": sf["muISO_nom"], "up": sf["muISO_up"], "down": sf["muISO_down"]}

    return muID
    
