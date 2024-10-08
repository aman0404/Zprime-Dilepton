from doAnalysis.dnn_eval_vtest import model_eval
#from doAnalysis.dnn_eval_v7 import model_eval
#from doAnalysis.dnn_eval import model_eval


def split_into_channels(df, v=""):
    #if v is None:
    #    # this was used for Delphes datasets
    #    cuts = {
    #        "vbf": (df.jj_mass > 400) & (df.jj_dEta > 2.5) & (df.jet1_pt > 35),
    #        "ggh_0jets": (df.njets == 0),
    #        "ggh_1jet": (df.njets == 1)
    #        & ((df.jj_mass <= 400) | (df.jj_dEta <= 2.5) | (df.jet1_pt < 35)),
    #        "ggh_2orMoreJets": (df.njets >= 2)
    #        & ((df.jj_mass <= 400) | (df.jj_dEta <= 2.5) | (df.jet1_pt < 35)),
    #    }

    #    for cname, cut in cuts.items():
    #        df.loc[cut, "channel"] = cname
    #else:

    scores = model_eval(df)

    #print("lenght is : ", len(scores), len(df))
    df["scores"] = scores

    df["nbjets"].fillna(0, inplace=True)
    df.loc[:, "channel"] = "none"
    df.loc[(df["nbjets"] == 0), "channel"] = "0b"
    
    #df.loc[(df["nbjets"] == 1), "channel"] = "1b"
    #df.loc[((df["nbjets"] == 1) & (df["min_bl_mass"] > 175.) &  (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True)), "channel"] = "1b"
    #df.loc[((df["nbjets"] == 1) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True)), "channel"] = "1b"
    #df.loc[((df["nbjets"] == 1) & (df["scores"] < 0.5) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True)), "channel"] = "1b"
    #df.loc[((df["nbjets"] == 1) & (df["scores"] > 0.6) & (df["scores"] < 0.8)  & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True)), "channel"] = "1b"

    #df.loc[((df["nbjets"] == 1) & (df["scores"] > 0.8) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True)), "channel"] = "1b"
    #df.loc[((df["nbjets"] == 1) & (df["scores"] > 0.7) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True)), "channel"] = "1b"
    df.loc[((df["nbjets"] == 1) & (df["scores"] > 0.6) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True)), "channel"] = "1b"


    #df.loc[((df["nbjets"] >= 2)), "channel"] = "2b"
    #df.loc[((df["nbjets"] >= 2) & (df["min_bl_mass"] > 175.) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True) & (df.bjet2_mb1_dR == True) & (df.bjet2_mb2_dR == True)), "channel"] = "2b"
    
    #df.loc[((df["nbjets"] >= 2) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True) & (df.bjet2_mb1_dR == True) & (df.bjet2_mb2_dR == True)), "channel"] = "2b"
    #df.loc[((df["nbjets"] >= 2) & (df["scores"] < 0.5) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True) & (df.bjet2_mb1_dR == True) & (df.bjet2_mb2_dR == True)), "channel"] = "2b"
    #df.loc[((df["nbjets"] >= 2) & (df["scores"] > 0.6) & (df["scores"] < 0.8) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True) & (df.bjet2_mb1_dR == True) & (df.bjet2_mb2_dR == True)), "channel"] = "2b"

    #df.loc[((df["nbjets"] >= 2) & (df["scores"] > 0.8) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True) & (df.bjet2_mb1_dR == True) & (df.bjet2_mb2_dR == True)), "channel"] = "2b"
    #df.loc[((df["nbjets"] >= 2) & (df["scores"] > 0.7) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True) & (df.bjet2_mb1_dR == True) & (df.bjet2_mb2_dR == True)), "channel"] = "2b"
    df.loc[((df["nbjets"] >= 2) & (df["scores"] > 0.6) & (df.bjet1_mb1_dR == True) & (df.bjet1_mb2_dR == True) & (df.bjet2_mb1_dR == True) & (df.bjet2_mb2_dR == True)), "channel"] = "2b"


    #df.loc[((df["nbjets"] == 1) & (df["min_bl_mass"] > 175)), "channel"] = "1b"
    #df.loc[((df["nbjets"] >= 2) & (df["min_bl_mass"] > 175)), "channel"] = "2b"


def categorize_by_score(df, scores, mode="uniform", **kwargs):
    nbins = kwargs.pop("nbins", 4)
    for channel, score_name in scores.items():
        score = df.loc[df.channel == channel, score_name]
        if mode == "uniform":
            for i in range(nbins):
                cat_name = f"{score_name}_cat{i}"
                cut_lo = score.quantile(i / nbins)
                cut_hi = score.quantile((i + 1) / nbins)
                cut = (df.channel == channel) & (score > cut_lo) & (score < cut_hi)
                df.loc[cut, "category"] = cat_name
