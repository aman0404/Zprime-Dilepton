#from coffea.jetmet_tools import CorrectedJetsFactory, JECStack
import awkward as ak
from coffea.lookup_tools import extractor
from config.jec_parameters import jec_parameters

from coffea.jetmet_tools import FactorizedJetCorrector, JetCorrectionUncertainty
from coffea.jetmet_tools import JECStack, CorrectedJetsFactory

def apply_jec(
    df,
    jets,
    dataset,
    is_mc,
    year,
    do_jec,
    do_jecunc,
    do_jerunc,
    jec_factories,
    jec_factories_data,
):
    cache = df.caches[0]

    # Correct jets (w/o uncertainties)
    if do_jec:
        #print('old columns:', set(ak.fields(jets)))
        if is_mc:
            factory = jec_factories["jec"]
        else:
            for run in jec_parameters["runs"][year]:
                if run in dataset:
                    factory = jec_factories_data[run]

        jets = factory.build(jets, lazy_cache=cache)

        #print('new columns:', set(ak.fields(jets)))

    # TODO: only consider nuisances that are defined in run parameters
    # Compute JEC uncertainties
    if is_mc and do_jecunc:
        jets = jec_factories["junc"].build(jets, lazy_cache=cache)

#        print("JES UP pt ratio", jets.JES_jes.up.pt/jets.pt)
#        print("JES Down pt ratio", jets.JES_jes.down.pt/jets.pt_raw)

    # Compute JER uncertainties
    if is_mc and do_jerunc:
        jets = jec_factories["jer"].build(jets, lazy_cache=cache)

        #print('new columns:', set(ak.fields(jets)))


        
        #print("JER UP pt ratio", jets.JER.up.pt/jets.pt_raw)
        #print("JER Down pt ratio", jets.JER.down.pt/jets.pt_raw)

    # TODO: JER nuisances


    return jets


def jec_names_and_sources(jec_pars, year):
    names = {}
    suffix = {
        "jec_names": [f"_{level}_AK4PFchs" for level in jec_pars["jec_levels_mc"]],
        "jec_names_data": [
            f"_{level}_AK4PFchs" for level in jec_pars["jec_levels_data"]
        ],
        "junc_names": ["_Uncertainty_AK4PFchs"],
        "junc_names_data": ["_Uncertainty_AK4PFchs"],
        "junc_sources": ["_UncertaintySources_AK4PFchs"],
        "junc_sources_data": ["_UncertaintySources_AK4PFchs"],
        "jer_names": ["_PtResolution_AK4PFchs"],
        "jersf_names": ["_SF_AK4PFchs"],
    }

    for key, suff in suffix.items():
        if "data" in key:
            names[key] = {}
            for run in jec_pars["runs"]:
                for tag, iruns in jec_pars["jec_data_tags"].items():
                    if run in iruns:
                        names[key].update({run: [f"{tag}{s}" for s in suff]})
        else:
            tag = jec_pars["jer_tags"] if "jer" in key else jec_pars["jec_tags"]
            names[key] = [f"{tag}{s}" for s in suff]

    return names


def jec_weight_sets(jec_pars, year):
    weight_sets = {}
    names = jec_names_and_sources(jec_pars, year)

    extensions = {
        "jec_names": "jec",
        "jer_names": "jr",
        "jersf_names": "jersf",
        "junc_names": "junc",
        "junc_sources": "junc",
    }

    weight_sets["jec_weight_sets"] = []
    weight_sets["jec_weight_sets_data"] = []

    for opt, ext in extensions.items():
        # MC
        weight_sets["jec_weight_sets"].extend(
            #[f"* * data/jec/{name}.txt" for name in names[opt]]
            [f"* * data/jec/{name}.{ext}.txt" for name in names[opt]]
        )
        # Data
        if "jer" in opt:
            continue
        data = []
        for run, items in names[f"{opt}_data"].items():
            data.extend(items)
        data = list(set(data))
        weight_sets["jec_weight_sets_data"].extend(
            #[f"* * data/jec/{name}.txt" for name in data]
            [f"* * data/jec/{name}.{ext}.txt" for name in data]
        )
    return weight_sets


def get_name_map(stack):
    name_map = stack.blank_name_map
    name_map["JetPt"] = "pt"
    name_map["JetMass"] = "mass"
    name_map["JetEta"] = "eta"
    name_map["JetA"] = "area"
    name_map["ptGenJet"] = "pt_gen"
    name_map["ptRaw"] = "pt_raw"
    name_map["massRaw"] = "mass_raw"
    name_map["Rho"] = "rho"
    return name_map


def jec_factories(year):
    jec_pars = {k: v[year] for k, v in jec_parameters.items()}

    weight_sets = jec_weight_sets(jec_pars, year)
    names = jec_names_and_sources(jec_pars, year)

    jec_factories = {}
    jec_factories_data = {}

    # Prepare evaluators for JEC, JER and their systematics
    jetext = extractor()
    jetext.add_weight_sets(weight_sets["jec_weight_sets"])
    jetext.add_weight_sets(weight_sets["jec_weight_sets_data"])
    jetext.finalize()
    jet_evaluator = jetext.make_evaluator()

    stacks_def = {
        "jec_stack": ["jec_names"],
        "jer_stack": ["jer_names", "jersf_names"],
        "junc_stack": ["junc_names"],
    }

    stacks = {}
    for key, vals in stacks_def.items():
        stacks[key] = []
        for v in vals:
            stacks[key].extend(names[v])

    jec_input_options = {}
    for opt in ["jec", "junc", "jer"]:
        jec_input_options[opt] = {
            name: jet_evaluator[name] for name in stacks[f"{opt}_stack"]
        }

    for src in names["junc_sources"]:
        for key in jet_evaluator.keys():
            if src in key:
                jec_input_options["junc"][key] = jet_evaluator[key]

    # Create separate factories for JEC, JER, JEC variations
    for opt in ["jec", "junc", "jer"]:
        stack = JECStack(jec_input_options[opt])
        jec_factories[opt] = CorrectedJetsFactory(get_name_map(stack), stack)

    # Create a separate factory for each data run
    for run in jec_pars["runs"]:
        jec_inputs_data = {}
        for opt in ["jec", "junc"]:
            jec_inputs_data.update(
                {name: jet_evaluator[name] for name in names[f"{opt}_names_data"][run]}
            )
        for src in names["junc_sources_data"][run]:
            for key in jet_evaluator.keys():
                if src in key:
                    jec_inputs_data[key] = jet_evaluator[key]

        jec_stack_data = JECStack(jec_inputs_data)
        jec_factories_data[run] = CorrectedJetsFactory(
            get_name_map(jec_stack_data), jec_stack_data
        )

    return jec_factories, jec_factories_data


#        if is_mc and self.do_jerunc:
#            jetarrays = {c: df.Jet[c].flatten() for c in
#                         df.Jet.columns if 'matched' not in c}
#            pt_gen_jet = df.Jet['matched_genjet'].pt.flatten(axis=0)
#            # pt_gen_jet = df.Jet.matched_genjet.pt.flatten(axis=0)
#            pt_gen_jet = np.zeros(len(df.Jet.flatten()))
#            pt_gen_jet[df.Jet.matched_genjet.pt.flatten(axis=0).counts >
#                       0] = df.Jet.matched_genjet.pt.flatten().flatten()
#            pt_gen_jet[df.Jet.matched_genjet.pt.flatten(
#                axis=0).counts <= 0] = 0
#            jetarrays['ptGenJet'] = pt_gen_jet
#            jets = JaggedCandidateArray.candidatesfromcounts(
#                df.Jet.counts, **jetarrays)
#            jet_pt_jec = df.Jet.pt
#            self.Jet_transformer_JER.transform(
#                jets, forceStochastic=False)
#            jet_pt_jec_jer = jets.pt
#            jet_pt_gen = jets.ptGenJet
#            jer_sf = ((jet_pt_jec_jer - jet_pt_gen) /
#                      (jet_pt_jec - jet_pt_gen +
#                       (jet_pt_jec == jet_pt_gen) *
#                       (jet_pt_jec_jer - jet_pt_jec)))
#            jer_down_sf = ((jets.pt_jer_down - jet_pt_gen) /
#                           (jet_pt_jec - jet_pt_gen +
#                           (jet_pt_jec == jet_pt_gen) * 10.))
#            jet_pt_jer_down = jet_pt_gen +\
#                (jet_pt_jec - jet_pt_gen) *\
#                (jer_down_sf / jer_sf)
#            jer_categories = {
#                'jer1': (abs(jets.eta) < 1.93),
#                'jer2': (abs(jets.eta) > 1.93) & (abs(jets.eta) < 2.5),
#                'jer3': ((abs(jets.eta) > 2.5) &
#                         (abs(jets.eta) < 3.139) &
#                         (jets.pt < 50)),
#                'jer4': ((abs(jets.eta) > 2.5) &
#                         (abs(jets.eta) < 3.139) &
#                         (jets.pt > 50)),
#                'jer5': (abs(jets.eta) > 3.139) & (jets.pt < 50),
#                'jer6': (abs(jets.eta) > 3.139) & (jets.pt > 50),
#            }
#            for jer_unc_name, jer_cut in jer_categories.items():
#                jer_cut = jer_cut & (jets.ptGenJet > 0)
#                up_ = (f"{jer_unc_name}_up" not in self.pt_variations)
#                dn_ = (f"{jer_unc_name}_down" not in
#                       self.pt_variations)
#                if up_ and dn_:
#                    continue
#                pt_name_up = f"pt_{jer_unc_name}_up"
#                pt_name_down = f"pt_{jer_unc_name}_down"
#                df.Jet[pt_name_up] = jet_pt_jec
#                df.Jet[pt_name_down] = jet_pt_jec
#                df.Jet[pt_name_up][jer_cut] = jet_pt_jec_jer[jer_cut]
#                df.Jet[pt_name_down][jer_cut] =\
#                    jet_pt_jer_down[jer_cut]
#
#                if (f"{jer_unc_name}_up" in self.pt_variations):
#                    jet_variation_names += [f"{jer_unc_name}_up"]
#                if (f"{jer_unc_name}_down" in self.pt_variations):
#                    jet_variation_names += [f"{jer_unc_name}_down"]
#            if self.timer:
#                self.timer.add_checkpoint("Computed JER nuisances")
