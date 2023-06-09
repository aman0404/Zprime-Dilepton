import pandas as pd
import pickle
import glob


def load_stage2_output_hists_2D(argset, parameters):
    year = argset["year"]
    var_name1 = argset["var_names"][0]
    var_name2 = argset["var_names"][1]
    dataset = argset["dataset"]
    global_path = parameters.get("global_path", None)
    label = parameters.get("label", None)

    if (global_path is None) or (label is None):
        return

    path = f"{global_path}/{label}//stage2_histograms/{var_name1}_{var_name2}/{year}/"
    paths = glob.glob(f"{path}/{dataset}_*.pickle") + glob.glob(f"{path}.pickle")
    hist_df = pd.DataFrame()
    for path in paths:
        try:
            with open(path, "rb") as handle:
                hist = pickle.load(handle)
                new_row = {
                    "year": year,
                    "var_name1": var_name1,
                    "var_name2": var_name2,
                    "dataset": dataset,
                    "hist": hist,
                }
                hist_df = pd.concat([hist_df, pd.DataFrame([new_row])])
                hist_df.reset_index(drop=True, inplace=True)
        except Exception:
            pass
    return hist_df
