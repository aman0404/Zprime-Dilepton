import sys
import os
sys.path.append('cfgs/')
import ROOT
import re
if __name__ == "__main__":
        import argparse
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument("-c","--config", dest="config",default="", required=True, help='configuration name')
        parser.add_argument("-t","--tag",dest="tag", default='', help='tag')
    	parser.add_argument("--binned",dest="binned", action="store_true", default=False, help='binned')
        args = parser.parse_args()

	tag = ""
	if not args.tag == "":
		tag = "_"  + args.tag

        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)

	
	outDir = "pValueScans_" +args.config + tag
        if not os.path.exists(outDir):
                os.makedirs(outDir)	
	#nameStub = "results_"+args.config+tag+"_toy\d*"
	nameStub = "results_"+args.config + "_%d_%.4f_%d_"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + args.tag

	nameStub = re.compile(nameStub)
	for name in os.listdir("."):
		if nameStub.match(name):
			outFileName = outDir+"/limitCard_%s%s"%(args.config+tag,name.split("_")[-1])
			outFile = open("%s.txt"%outFileName, "w")
			dirs= os.listdir(name)
			if len(dirs) > 0:
				lastDir = sorted(dirs)[-1]
				for massRange in config.masses:
					mass = massRange[1]
					while mass < massRange[2]:
						fileName = name + "/" + lastDir + "/higgsCombine%s_%d_%.4f_%d%s.Significance.mH%d.root"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"],tag+"_"+name.split("_")[-1],mass)
						if os.path.isfile(fileName):
							limitTree = ROOT.TChain()
							limitTree.Add(fileName+"/limit")
							for entry in limitTree:
								outFile.write("%d %.10f\n"%(mass,entry.limit))        
						mass += massRange[0]
			outFile.close()
