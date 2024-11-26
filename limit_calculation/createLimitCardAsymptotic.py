import sys
import os
sys.path.append('cfgs/')
import ROOT
import subprocess

if __name__ == "__main__":
        import argparse
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument("-c","--config", dest="config",default="", required=True, help='configuration name')
        parser.add_argument("--input",dest="input", default='', help='folder with input root files')
        parser.add_argument("-t","--tag",dest="tag", default='', help='tag')
        parser.add_argument("--injected",dest="injected", action="store_true", default=False, help='injected')

        args = parser.parse_args()

        tag = ""
        if not args.tag == "":
                tag = "_"  + args.tag

        

        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)


        if args.input == "":
                dirs=sorted([d for d in os.listdir(os.getcwd()+"/results_%s"%args.config + tag) if os.path.isdir(os.getcwd()+"/results_%s"%args.config+tag+"/"+d)])
                inputDir = "results_%s/"%(args.config+tag)
                #inputDir = "results_%s/"%(args.config+tag)+dirs[-1]

        else:
                inputDir = args.input

        print("Taking inputs from %s"%inputDir)

        algo = "AsymptoticLimits"
        outFileName = "limitCard_%s_Asymptotic"%(args.config)
        if not args.tag =='':
                outFileName = outFileName + "_" + args.tag      
        
        interferences = config.interferencesBBLL
        interference = interferences[0]
        # add model indentifier
        modelID = "ZPrime_"
        outFileName = modelID + outFileName

        if not os.path.exists("cards"):
                os.mkdir("cards")       



        outFile = open("cards/%s.txt"%outFileName, "w")
        if args.injected:
                name = "%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
        else:
                name=args.config + "_" + args.tag
                #name=args.config

        cross_section = {6: 1.2905616, 10: 1.2915521, 14: 1.2903995, 18: 1.3033036}
        masses = config.masses
        missingFiles = []
        for massRange in masses:
                mass = massRange[1]
                while mass <= massRange[2]:
                        fileName = inputDir + "/higgsCombine%s_%s.%s.mH%d.root"%(name,interference, algo,mass)
                        if os.path.isfile(fileName):
                                limitTree = ROOT.TChain()
                                limitTree.Add(fileName+"/limit")
                                for i, entry in enumerate(limitTree):
                                        if i == 0:
                                                outFile.write("%d %.15f "%(mass,entry.limit*cross_section[mass]))        
                                        else:
                                                outFile.write("%.15f "%(entry.limit*cross_section[mass]))        
                                outFile.write("\n")        
                        else:
                                missingFiles.append(fileName)   
                        mass += massRange[0]
        if len(missingFiles) == 0:
                print("all files present")
        else:
                print("missing files:")
                for fileN in missingFiles:
                        print(fileN)
        outFile.close()
