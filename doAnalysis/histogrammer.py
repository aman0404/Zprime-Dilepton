import itertools
import pandas as pd

from hist import Hist
from config.variables import Variable
from copperhead.python.io import save_stage2_output_hists
from numpy import array


def calc_binwidth_weight(data, binning):
    weights = []
    for val in data:
        found = False
        val = float(val)
        for i in range(0, len(binning) - 1):
            if val > binning[i] and val <= binning[i + 1]:
                found = True
                weights.append(1.0 / (binning[i + 1] - binning[i]))
        if not found:
            weights.append(1.0)
    return array(weights)


def make_histograms(df, var_name, year, dataset, regions, channels, npart, parameters):
    # try to get binning from config
    if var_name in parameters["variables_lookup"].keys():
        var = parameters["variables_lookup"][var_name]
    else:
        var = Variable(var_name, var_name, 50, 0, 5, 1e-2, 1e8)
    # prepare list of systematic variations
    wgt_variations = [w for w in df.columns if ("wgt_" in w)]
    syst_variations = parameters.get("syst_variations", ["nominal"])
    #print("debugging ", wgt_variations)
    #print("debugging ", syst_variations)
    variations = []
    for w in wgt_variations:
        for v in syst_variations:
            variation = get_variation(w, v)
            if variation:
                variations.append(variation)

    #print("debugging ", variations)
    # prepare multidimensional histogram
    # add axes for (1) mass region, (2) channel, (3) value or sumw2
    hist = (
        Hist.new.StrCat(regions, name="region")
        .StrCat(channels, name="channel")
        .StrCat(["value", "sumw2"], name="val_sumw2")
    )

    # add axis for observable variable
    if ("score" in var.name) and ("mva_bins" in parameters.keys()):
        bins = parameters["mva_bins"][var.name.replace("score_", "")][f"{year}"]
        hist = hist.Var(bins, name=var.name)
    else:
        if len(var.binning) > 0:
            hist = hist.Var(var.binning, name=var.name, label=var.caption)
        else:
            hist = hist.Reg(
                var.nbins, var.xmin, var.xmax, name=var.name, label=var.caption
            )

    # add axis for systematic variation
    hist = hist.StrCat(variations, name="variation")

    # specify container type
    hist = hist.Double()

    # loop over configurations and fill the histogram
    loop_args = {
        "region": regions,
        "w": wgt_variations,
        "v": syst_variations,
        "channel": channels,
    }
    loop_args = [
        dict(zip(loop_args.keys(), values))
        for values in itertools.product(*loop_args.values())
    ]
    hist_info_rows = []
    total_yield = 0
    for loop_arg in loop_args:
        region = loop_arg["region"]
        channel = loop_arg["channel"]
        w = loop_arg["w"]
        v = loop_arg["v"]
        variation = get_variation(w, v)
        if not variation:
            continue

        #print("debugging ", variation)
        var_name = f"{var.name}_{v}"
        if var_name not in df.columns:
            if var.name in df.columns:
                var_name = var.name
            else:
                continue

        #print("debugging ", var_name)
        slicer = (
            (df.dataset == dataset)
            & ((df.r == region) | (region == "inclusive"))
            & (df.year == year)
            #& (df.dimuon_mass > 60)
            #& (df.dimuon_mass < 120)

            & (df.dimuon_mass > 200) # default
            #& (df.dimuon_mass > 200) ##for response matrix
            #& (df.dimuon_mass_gen > 200)  ## for response matrix

            #& (df.dimuon_mass_gen < 400)   #gen level cut for flavor ratio
            #& (df.dimuon_mass_gen > 600)   #gen level cut for flavor ratio


            & ((df["channel"] == channel) | (channel == "inclusive"))

            & (~((df.dataset == "dyInclusive50") & (df.dimuon_mass_gen > 200)))
            & (~((df.dataset == "ttbar_lep_inclusive") & (df.dimuon_mass_gen > 500)))
            & (~((df.dataset == "WWinclusive") & (df.dimuon_mass_gen > 200)))

            #& (~((df.dataset == "dyInclusive50") & (df.dimuon_mass_gen > 200)))
            #& (~((df.dataset == "ttbar_lep_inclusive") & (df.dimuon_mass_gen > 500)))
            #& (~((df.dataset == "WWinclusive") & (df.dimuon_mass_gen > 200)))
            #& (df.bjet1_mb1_dR == True)
            #& (df.bjet1_mb2_dR == True)
            #& (df.bjet2_mb1_dR == True)
            #& (df.bjet2_mb2_dR == True)
        )
        data = df.loc[slicer, var_name]
        weight = df.loc[slicer, w]

        #print(data)

        if var.norm_to_bin_width:
            weight = weight * calc_binwidth_weight(data.to_numpy(), var.binning)

        to_fill = {var.name: data, "region": region, "channel": channel}

        to_fill_value = to_fill.copy()
        to_fill_value["val_sumw2"] = "value"
        to_fill_value["variation"] = variation
        hist.fill(**to_fill_value, weight=weight)

        to_fill_sumw2 = to_fill.copy()
        to_fill_sumw2["val_sumw2"] = "sumw2"
        to_fill_sumw2["variation"] = variation
        hist.fill(**to_fill_sumw2, weight=weight * weight)

        hist_info_row = {
            "year": year,
            "var_name": var.name,
            "dataset": dataset,
            "variation": variation,
            "region": region,
            "channel": channel,
            "yield": weight.sum(),
        }
        if weight.sum() == 0:
            continue
        total_yield += weight.sum()

        if "return_hist" in parameters:
            if parameters["return_hist"]:
                hist_info_row["hist"] = hist
        hist_info_rows.append(hist_info_row)

    if total_yield == 0:
        return None

    # save histogram for this partition to disk
    # (partitions will be joined in stage3)
    save_hists = parameters.get("save_hists", False)
    if save_hists:
        save_stage2_output_hists(hist, var.name, dataset, year, parameters, npart)

    # return info for debugging
    hist_info_rows = pd.DataFrame(hist_info_rows)
    return hist_info_rows


def make_histograms2D(
    df, var_name1, var_name2, year, dataset, regions, channels, npart, parameters
):
    # try to get binning from config
    if var_name1 in parameters["variables_lookup"].keys():
        var1 = parameters["variables_lookup"][var_name1]
    else:
        var1 = Variable(var_name1, var_name1, 50, 0, 5, 1e-2, 1e8)

    if var_name2 in parameters["variables_lookup"].keys():
        var2 = parameters["variables_lookup"][var_name2]
    else:
        var2 = Variable(var_name2, var_name2, 50, 0, 5, 1e-2, 1e8)

    # no systematic variations at this point
    # prepare list of systematic variations
    # wgt_variations = [w for w in df.columns if ("wgt_" in w)]
    # syst_variations = parameters.get("syst_variations", ["nominal"])
    # variations = []
    # for w in wgt_variations:
    #    for v in syst_variations:
    #        variation = get_variation(w, v)
    #        if variation:
    #            variations.append(variation)

    # prepare multidimensional histogram
    # add axes for (1) mass region, (2) channel, (3) value or sumw2
    hist = (
        Hist.new.StrCat(regions, name="region")
        .StrCat(channels, name="channel")
        .StrCat(["value1", "value2", "sumw2"], name="val_sumw2")
    )

    # add axis for observable variable
    if len(var1.binning) > 0:
        hist = hist.Var(var1.binning, name=var1.name, label=var1.caption)
    else:
        hist = hist.Reg(
            var1.nbins, var1.xmin, var1.xmax, name=var1.name, label=var1.caption
        )

    if len(var2.binning) > 0:
        hist = hist.Var(var2.binning, name=var2.name, label=var2.caption)
    else:
        hist = hist.Reg(
            var2.nbins, var2.xmin, var2.xmax, name=var2.name, label=var2.caption
        )

    # add axis for systematic variation
    # hist = hist.StrCat(variations, name="variation")

    # specify container type
    hist = hist.Double()

    # loop over configurations and fill the histogram
    loop_args = {
        "region": regions,
        "channel": channels,
    }
    loop_args = [
        dict(zip(loop_args.keys(), values))
        for values in itertools.product(*loop_args.values())
    ]
    hist_info_rows = []
    total_yield = 0
    for loop_arg in loop_args:
        region = loop_arg["region"]
        channel = loop_arg["channel"]
        w = "wgt_nominal"
        #        w = loop_arg["w"]
        #        v = loop_arg["v"]
        #        variation = get_variation(w, v)
        #        if not variation:
        #            continue

        #        var_name = f"{var.name}_{v}"
        #        if var_name not in df.columns:
        #            if var.name in df.columns:
        #                var_name = var.name
        #            else:
        #                continue

        slicer = (
            (df.dataset == dataset)
            & (df.r == region)
            & (df.year == year)
            & (df.dimuon_mass > 200)
#            & (df.dimuon_mass_gen > 400)   #gen level cut for flavor ratio
            & ((df["channel"] == channel) | (channel == "inclusive"))
            & (~((df.dataset == "ttbar_lep_inclusive") & (df.dimuon_mass_gen > 500)))
            & (~((df.dataset == "WWinclusive") & (df.dimuon_mass_gen > 200)))
            #& (df.bjet1_mb1_dR == False)
            #& (df.bjet1_mb2_dR == False)
        )

        data1 = df.loc[slicer, var_name1]
        data2 = df.loc[slicer, var_name2]
        weight = df.loc[slicer, w]
#        print("weight", weight)
        to_fill = {
            var1.name: data1,
            var2.name: data2,
            "region": region,
            "channel": channel,
        }

        to_fill_value = to_fill.copy()
        to_fill_value["val_sumw2"] = "value"
        hist.fill(**to_fill_value, weight=weight)

        to_fill_sumw2 = to_fill.copy()
        to_fill_sumw2["val_sumw2"] = "sumw2"
        hist.fill(**to_fill_sumw2, weight=weight * weight)

        hist_info_row = {
            "year": year,
            "var_name1": var1.name,
            "var_name2": var2.name,
            "dataset": dataset,
            "variation": "nominal",
            "region": region,
            "channel": channel,
            "yield": weight.sum(),
        }
        if weight.sum() == 0:
            continue
        total_yield += weight.sum()
        if "return_hist" in parameters:
            if parameters["return_hist"]:
                hist_info_row["hist"] = hist
        hist_info_rows.append(hist_info_row)

    if total_yield == 0:
        return None

    # save histogram for this partition to disk
    # (partitions will be joined in stage3)
    save_hists = parameters.get("save_hists", False)
    if save_hists:
        save_stage2_output_hists(
            hist, var1.name + "_" + var2.name, dataset, year, parameters, npart
        )

    # return info for debugging
    hist_info_rows = pd.DataFrame(hist_info_rows)
    return hist_info_rows


def get_variation(wgt_variation, sys_variation):
    if "nominal" in wgt_variation:
        if "nominal" in sys_variation:
            return "nominal"
        else:
            return sys_variation
    else:
        if "nominal" in sys_variation:
            return wgt_variation
        else:
            return None
