# import time
import subprocess
import glob
import tqdm

import uproot

uproot.open.defaults["xrootd_handler"] = uproot.MultithreadedXRootDSource

from config.parameters import parameters
from config.cross_sections import cross_sections
from config.parameters import lumis

def load_sample(dataset, parameters):
    xrootd = not (dataset == "test_file")
    args = {
        "year": parameters["year"],
        "out_path": parameters["out_path"],
        "server": parameters["server"],
        "datasets_from": parameters["channel"],
        "debug": False,
        "xrootd": xrootd,
        #"timeout": 1,
        "timeout": 1200,
    }
    samp_info = SamplesInfo(**args)
    samp_info.load(
        dataset,
        use_dask=True,
        from_das=parameters["from_das"],
        client=parameters["client"],
    )
    if samp_info.is_missing:
        return {dataset: "missing"}
    samp_info.finalize()
    return {dataset: samp_info}


def load_samples(datasets, parameters):
    print(parameters["year"])
    args = {
        "year": parameters["year"],
        "out_path": parameters["out_path"],
        "server": parameters["server"],
        "datasets_from": parameters["channel"],
        "debug": False,
    }
    samp_info_total = SamplesInfo(**args)
    print("Loading lists of paths to ROOT files for these datasets:", datasets)
    for d in tqdm.tqdm(datasets):
        if d in samp_info_total.samples:
            continue
        si = load_sample(d, parameters)[d]
        if si == "missing":
            continue
        if "files" not in si.fileset[d].keys():
            continue
        samp_info_total.data_entries += si.data_entries
        samp_info_total.fileset.update(si.fileset)
        samp_info_total.metadata.update(si.metadata)
        samp_info_total.lumi_weights.update(si.lumi_weights)
        samp_info_total.samples.append(si.sample)
    return samp_info_total


def read_via_xrootd(server, path, from_das=False):
    if from_das:
        print(path)
        if "USER" in path:
            command = f'dasgoclient --query=="file dataset={path} instance=prod/phys03"'
        else:
            command = f'dasgoclient --query=="file dataset={path}"'
    else:
        command = f"xrdfs {server} ls -R {path} | grep '.root'"
    print(command)
    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    result = proc.stdout.readlines()
    if proc.stderr.readlines():
        print("Loading error! This may help:")
        print("    voms-proxy-init --voms cms")
        print("    source /cvmfs/cms.cern.ch/cmsset_default.sh")
    result = [server + r.rstrip().decode("utf-8") for r in result]
    return result


class SamplesInfo(object):
    def __init__(self, **kwargs):
        self.years = kwargs.pop("year", "2017")
        self.out_path = kwargs.pop("out_path", "/output/")
        self.xrootd = kwargs.pop("xrootd", True)
        self.server = kwargs.pop("server", "root://xrootd.rcac.purdue.edu/")
        self.timeout = kwargs.pop("timeout", 1200)
        self.debug = kwargs.pop("debug", False)
        datasets_from = kwargs.pop("datasets_from", "Zprime")
        self.parameters = {}
        for k, v in parameters.items():
            try:
                if "2018" in self.years:
                    self.parameters.update({k: v["2018"]})
                else:
                    self.parameters.update({k: v.get(self.years, None)})
            except Exception:
                print(k, v)
        self.is_mc = True
        print(datasets_from)
        if "mu" in datasets_from:
            from config.datasets_muon import datasets
            #from config.datasets_muon import datasets
        elif "el" in datasets_from:
            from config.datasets_electron import datasets
        self.paths = datasets[self.years]

        if "2016pre" in self.years:
            self.lumi = 19120.0
            #self.lumi = 19290.0
        elif "2016post" in self.years:
            self.lumi = 16810.0
            #self.lumi = 17010.0

        elif "2017" in self.years:
            self.lumi = 41480.0
        elif "2018" in self.years:
            #self.lumi = 61310.0
            self.lumi = 59830.0

        self.data_entries = 0
        self.sample = ""
        self.samples = []

        self.fileset = {}
        self.metadata = {}

        self.lumi_weights = {}

    def load(self, sample, use_dask, from_das=False, client=None):
        if "data" in sample:
            self.is_mc = False

        res = self.load_sample(sample, from_das, use_dask, client)
        self.sample = sample
        self.samples = [sample]
        self.fileset = {sample: res["files"]}

        self.metadata = res["metadata"]
        self.data_entries = res["data_entries"]
        self.is_missing = res["is_missing"]

    def load_sample(self, sample, from_das=False, use_dask=False, client=None):
        if sample not in self.paths:
            print(f"Couldn't load {sample}! Skipping.")
            return {
                "sample": sample,
                "metadata": {},
                "files": {},
                "data_entries": 0,
                "is_missing": True,
            }

        all_files = []
        metadata = {}
        data_entries = 0

        if self.xrootd:
            all_files = read_via_xrootd(self.server, self.paths[sample], from_das)
            # all_files = [self.server + _file for _file in self.paths[sample]]
        elif self.paths[sample].endswith(".root"):
            all_files = [self.paths[sample]]
        else:
            print("check")
            print(self.paths[sample])
            all_files = [
                self.server + f for f in glob.glob(self.paths[sample] + "/**/**/*.root")
            ]

        if self.debug:
            all_files = [all_files[0]]

        sumGenWgts = 0
        nGenEvts = 0
        if use_dask:
            from dask.distributed import get_client

            if not client:
                client = get_client()
            if "data" in sample:
                work = client.map(self.get_data, all_files, priority=100)
            else:
                work = client.map(self.get_mc, all_files, priority=100)
            for w in work:
                ret = w.result()
                if "data" in sample:
                    data_entries += ret["data_entries"]
                else:
                    sumGenWgts += ret["sumGenWgts"]
                    nGenEvts += ret["nGenEvts"]
        else:
            for f in all_files:
                if "data" in sample:
                    tree = uproot.open(f, timeout=self.timeout)["Events"]
                    data_entries += tree.num_entries
                else:
                    tree = uproot.open(f, timeout=self.timeout)["Runs"]
                    if ("NanoAODv6" in self.paths[sample]) or (
                        "NANOV10" in self.paths[sample]
                    ):
                        sumGenWgts += tree["genEventSumw_"].array()[0]
                        nGenEvts += tree["genEventCount_"].array()[0]
                    else:
                        sumGenWgts += tree["genEventSumw"].array()[0]
                        nGenEvts += tree["genEventCount"].array()[0]
        metadata["sumGenWgts"] = sumGenWgts
        metadata["nGenEvts"] = nGenEvts

        files = {"files": all_files, "treename": "Events"}
        return {
            "sample": sample,
            "metadata": metadata,
            "files": files,
            "data_entries": data_entries,
            "is_missing": False,
        }

    def get_data(self, f):
        ret = {}
        tree = uproot.open(f, timeout=self.timeout)["Events"]
        ret["data_entries"] = tree.num_entries
        return ret

    def get_mc(self, f):
        ret = {}
        tree = uproot.open(f, timeout=self.timeout)["Runs"]
        if ("NanoAODv6" in f) or ("NANOV10" in f):
            ret["sumGenWgts"] = tree["genEventSumw_"].array()[0]
            ret["nGenEvts"] = tree["genEventCount_"].array()[0]
        else:
            ret["sumGenWgts"] = tree["genEventSumw"].array()[0]
            ret["nGenEvts"] = tree["genEventCount"].array()[0]
        return ret

    def finalize(self):
        if self.is_mc:
            N = self.metadata["sumGenWgts"]
            numevents = self.metadata["nGenEvts"]
            if isinstance(cross_sections[self.sample], dict):
                xsec = cross_sections[self.sample][self.years]
            else:
                xsec = cross_sections[self.sample]
            if N > 0:
                self.lumi_weights[self.sample] = xsec * self.lumi / N
            else:
                self.lumi_weights[self.sample] = 0
            # print(f"{self.sample}: events={numevents}")
            return numevents
        else:
            return self.data_entries
