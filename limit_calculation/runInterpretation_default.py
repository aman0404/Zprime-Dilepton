import sys
import os
sys.path.append('cfgs/')
import argparse
import subprocess

supportedResources = ["Purdue","FNAL","SNU"]

def getRange(mass,CI=False,CILambda=False,BSLL=False):
    print("testing script aman ", mass )
    if CI and not CILambda and not BSLL:
        if mass == 6:
            return 10
        if mass == 10:
            return 50
        if mass == 14:
            return 200
        if mass == 18:
            return 500
        if mass == 100:
            return 100
        if mass == 22:
            return 1500
        if mass == 26:
            return 2000
        # return 3
    elif CI and CILambda:
        if mass == 6:
            return 10
        if mass == 10:
            return 50
        if mass == 14:
            return 200
        if mass == 18:
            return 500
        if mass == 100:
            return 100
        if mass == 22:
            return 1500
        if mass == 26:
            return 2000

    elif CI and BSLL:
         if mass == 1:
             return 10
         if mass == 2:
             return 50
         if mass == 3:
             return 100
         if mass == 4:
             return 100
         if mass == 5:
             return 200
         if mass == 6:
             return 500

        #if 400 <= mass <= 500:
        #    return 2000
        #elif 500 < mass <= 600:
        #    return 1800
        #elif 600 < mass <= 700:
        #    return 1500
        #elif 700 < mass <= 800:
        #    return 1300
        #elif 800 < mass <= 1000:
        #    return 1200
        #elif 1000 < mass <= 2000:
        #    return 1000



        # return 2
    else:
        if 120 <= mass <= 200:
            return 500
        elif 200 <= mass <= 300:
            return 200
        elif 300 <= mass <= 400:
            return 100
        elif 400 <= mass <= 500:
            return 100
        elif 500 < mass <= 600:
            return 100
        elif 600 < mass <= 700:
            return 20
        elif 700 < mass <= 800:
            return 20
        elif 800 < mass <= 1000:
            return 20
        elif 1000 < mass <= 2000:
            return 8
        elif 2000 < mass <= 3000:
            return 5
        elif 3000 < mass <= 4000:
            return 3
        else:
            return 5

def prepareToys(args,config,outDir):

    print("this is working 3.0")
    if args.BBLL or args.BSLL:
        if args.Lambda > 0:
            Lambdas = [args.Lambda]
        else:
            if args.BSLL:
                Lambdas = config.lambdasBSLL
                interferences = config.interferencesBSLL
            else:    
                Lambdas = config.lambdasBBLL
                interferences = config.interferencesBBLL
        for Lambda in Lambdas:
            for interference in interferences:
                print ("generate toys for Lambda %d and model %s"%(Lambda,interference))
                if len(config.channels) == 1:
                    cardName = outDir + "/" + config.channels[0] + "_%d_%s"%(Lambda,interference) + ".txt"
                else:
                    cardName = outDir + "/" + args.config + "_combined" + "_%d_%s"%(Lambda,interference) + ".txt"
                import random
                number = random.randint(0,100000)
                print("this is working 3.1")
                subCommand = ["combine","-M","GenerateOnly","--saveToys","%s"%cardName, "-n" "%s_%d"%(args.config,number) , "-m","%d"%Lambda,"-t","%d"%config.exptToys]
                subprocess.call(subCommand)
                print("this is working 3.2")
                #if args.workDir == "":
                subprocess.call(["mv","higgsCombine%s_%d.GenerateOnly.mH%d.123456.root"%(args.config,number,Lambda),outDir+"/higgsCombine%s%s_%s.GenerateOnly.mH%d.123456.root"%(args.config,args.tag,interference,Lambda)])
                #else:	
                #	subprocess.call(["mv",args.workDir+"/higgsCombine%s.GenerateOnly.mH%d.123456.root"%(args.config,Lambda),outDir+"/higgsCombine%s%s_%s.GenerateOnly.mH%d.123456.root"%(args.config,args.tag,interference,Lambda)])
                
                
    else:
        print ("not implemented for Z'")
        sys.exit()

def runLocalLimits(args,config,outDir,cardDir,binned):

    if args.frequentist:
        algo = "HybridNew"
    elif args.asymptotic:
        algo = "AsymptoticLimits"
    else:
        algo = "MarkovChainMC"	

    if args.BBLL or args.BSLL:
        if args.Lambda > 0:
            Lambdas = [args.Lambda]
        else:
            if args.BSLL:
                Lambdas = config.lambdasBSLL
                interferences = config.interferencesBSLL
            else:    
                Lambdas = config.lambdasBBLL
                interferences = config.interferencesBBLL
        for Lambda in Lambdas:
            for interference in interferences:
                print ("calculate limit for Lambda %d and model %s"%(Lambda,interference))
                if len(config.channels) == 1:
                    cardName = cardDir + "/" + config.channels[0] + "_%d_%s"%(Lambda,interference) + ".txt"
                else:
                    cardName = cardDir + "/" + args.config + "_combined" + "_%d_%s"%(Lambda,interference) + ".txt"
        
                if args.usePhysicsModel or args.is_int:
                    cardName = cardName.split(".")[0]+".root"

                numToys = config.numToys
                if args.expected:
                    numToys = 1
                if args.frequentist:
                    subCommand = ["combine","-M","HybridNew","--frequentist","--testStat","LHC","%s"%cardName, "-n", "%s"%args.config , "-m","%d"%Lambda,"--rMax","%d"%getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL), "--rMin", "0"]
                elif args.asymptotic:
                    subCommand = ["combine","-M","AsymptoticLimits","%s"%cardName, "-n", "%s"%args.config , "-m","%d"%Lambda,"--rMax","%d"%getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL), "--rMin", "0"]
                else:
                    print('getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL): {0}'.format(getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL)))
                    subCommand = ["combine","-M","MarkovChainMC","%s"%cardName, "-n", "%s"%args.config , "-m","%d"%Lambda, "-i", "%d"%config.numInt, "--tries", "%d"%numToys ,  "--prior","flat","--rMax","%d"%getRange(Lambda,True,args.usePhysicsModel,BSLL=args.BSLL)]
                if args.expected and not args.asymptotic: 
                    subCommand.append("-t")
                    # subCommand.append("-1")
                    subCommand.append("%d"%config.exptToys)
                    subCommand.append("-s")
                    subCommand.append("0")
                    if args.is_int or args.usePhysicsModel: ##Aman edits here 
                        subCommand.append("--toysFile="+cardDir+"_expGen"+"/higgsCombine%s%s_%s.GenerateOnly.mH%d.123456.root"%(args.config,args.tag,interference,Lambda))
                            
                if args.lower:
                    subCommand.append("--saveChain")
                
                print("subCommand: {0}".format(subCommand))
                subprocess.call(subCommand)

                if args.expected:	
                    resultFile = "higgsCombine%s.%s.mH%d.0.root"%(args.config,algo,Lambda)
                else:
                    resultFile = "higgsCombine%s.%s.mH%d.root"%(args.config,algo,Lambda)
                
                subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s%s_%s.%s.mH%d.root"%(outDir,args.config,args.tag,interference,algo,Lambda)])
    
                if args.lower:
                    resultFile = "higgsCombine%s%s_%s.%s.mH%d.root"%(args.config,args.tag,interference,algo,Lambda)
                    from tools import convertToLowerLimit
                    rName = "r"
                    average = True
                    if args.usePhysicsModel:
                        rName = "Lambda"
                    if args.expected:
                        average = False
                    limits = convertToLowerLimit(outDir+"/"+resultFile,getRange(Lambda,args.BBLL,args.usePhysicsModel, BSLL=args.BSLL),rName,average)
                    
                    outFile = resultFile.split(".root")[0]+".txt"
                    thefile = open(outDir+"/"+outFile, 'w')
                    for limit in limits:
                          thefile.write("%.2f %.8f\n" % (Lambda,limit))	
    else:
        if args.mass > 0:
            masses = [[5,args.mass,args.mass]]
        else:
            masses = config.masses

        for massRange in masses:
            mass = massRange[1]
            while mass <= massRange[2]:
                print ("calculate limit for mass %d"%mass)
                if len(config.channels) == 1:
                    cardName = cardDir + "/" + config.channels[0] + "_%d"%(mass) + ".txt"
                else:
                    cardName = cardDir + "/" + args.config + "_combined" + "_%d"%(mass) + ".txt"
        
                if binned:
                    cardName = cardName.split(".")[0] + "_binned.txt"
                numToys = config.numToys
                if args.expected:
                    numToys = 1
                    if config.exptToys > -1:
                        numToys = config.exptToys
                if args.frequentist:
                    subCommand = ["combine","-M","HybridNew","--frequentist","--testStat","LHC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass,"--rMax","%d"%getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL), "--rMin", "-10"]	
                elif args.asymptotic:
                    #subCommand = ["combine","-M","AsymptoticLimits","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass,"--rMax","%d"%getRange(mass,args.CI,args.usePhysicsModel, BSLL=args.BSLL), "--rMin", "-10",'-v5']
                    subCommand = ["combine","-M","AsymptoticLimits","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass,"--rMax","%d"%getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL)]
                else:
                    print("using this combine command")
                    subCommand = ["combine","-M","MarkovChainMC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "-i", "%d"%config.numInt, "--tries", "%d"%numToys ,  "--prior","flat","--rMax","%d"%getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL)]
                if args.expected and not args.asymptotic: 
                    subCommand.append("-t")
                    subCommand.append("%d"%config.exptToys)
                    subCommand.append("-s")
                    subCommand.append("0")
        
                if args.lower:
                    subCommand.append("--saveChain")
        
                for library in config.libraries:		
                    subCommand.append("--LoadLibrary")
                    subCommand.append("userfuncs/%s"%library)
                subprocess.call(subCommand)

                if args.expected:	
                    resultFile = "higgsCombine%s.%s.mH%d.0.root"%(args.config,algo,mass)
                else:
                    resultFile = "higgsCombine%s.%s.mH%d.root"%(args.config,algo,mass)
                
                subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s.%s.mH%d.root"%(outDir,args.config,algo,mass)])

                mass += massRange[0]

def runLocalSignificance(args,config,outDir,cardDir,binned,tag):

    if args.hybrid or args.frequentist:
        algo = "HybridNew"
    else:
        algo = "Significance"	

    if args.mass > 0:
        masses = [[5,args.mass,args.mass]]
    else:
        masses = config.masses
    for massRange in masses:
        mass = massRange[1]
        while mass <= massRange[2]:
            print ("calculate significance for mass %d"%mass)
            if len(config.channels) == 1:
                cardName = cardDir + "/" + config.channels[0] + "_%d"%mass + ".txt"
            else:
                cardName = cardDir + "/" + args.config + "_combined" + "_%d"%mass + ".txt"
            if binned:
                cardName = cardName.split(".")[0]+"_binned.txt"
            if args.frequentist:	
                subCommand = ["combine","-M","HybridNew","%s"%cardName, "-n" "%s"%(args.config) , "-m","%d"%mass, "--signif" , "--pvalue", "--frequentist", "--testStat","LHC","-T","10000"]
            elif args.hybrid:
                subCommand = ["combine","-M","HybridNew","%s"%cardName, "-n" "%s"%(args.config) , "-m","%d"%mass, "--signif" , "--pvalue","--testStat","LHC","-T","10000"]
            elif args.plc:	
                subCommand = ["combine","-M","Significance","%s"%cardName, "-n" "%s"%(args.config) , "-m","%d"%mass, "--signif" , "--pvalue", "--usePLC","--rMax","%d"%getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL)]
            else:
                subCommand = ["combine","-M","Significance","%s"%cardName, "-n" "%s"%(args.config) , "-m","%d"%mass, "--signif" , "--pvalue","--uncapped","1","--rMax","%d"%getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL)]
            for library in config.libraries:
                                subCommand.append("--LoadLibrary")
                                subCommand.append("userfuncs/%s"%library)


            subprocess.call(subCommand)
            if args.expected:
                resultFile = "higgsCombine%s.%s.mH%d.123456.root"%(args.config,algo,mass)
            else:
                resultFile = "higgsCombine%s.%s.mH%d.root"%(args.config,algo,mass)
                subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s%s.%s.mH%d.root"%(outDir,args.config,tag,algo,mass)])
                mass += massRange[0]

def runBiasStudy(args,config,outDir,cardDir,binned):

    algo = "FitDiagnostics"

    if args.BBLL or args.BSLL:
        if args.Lambda > 0:
            Lambdas = [args.Lambda]
        else:
            if config.BSLL:
                Lambdas = config.lambdasBSLL
                interferences = config.interferencesBSLL
            else:
                Lambdas = config.lambdasBBLL
                interferences = config.interferencesBBLL
        for Lambda in Lambdas:
            for interference in interferences:
                print ("perform bias study for Lambda %d and model %s"%(Lambda,interference))
                if len(config.channels) == 1:
                    cardName = cardDir + "/" + config.channels[0] + "_%d_%s"%(Lambda,interference) + ".txt"
                else:
                    cardName = cardDir + "/" + args.config + "_combined" + "_%d_%s"%(Lambda,interference) + ".txt"
        
                if args.usePhysicsModel or args.is_int:
                    cardName = cardName.split(".")[0]+".root"

                numToys = config.numToys
                subCommand = ["combine","-M",algo,"%s"%cardName, "-n" "%s"%args.config , "-m","%d"%Lambda, "-t", "1000", "--expectSignal","0","--rMax","100","--rMin","-100","--forceRecreateNLL"]
        
                subprocess.call(subCommand)

                resultFile = "higgsCombine%s.%s.mH%d.123456.root"%(args.config,algo,Lambda)
                
                subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s%s_%s.%s.mH%d_mu0.root"%(outDir,args.config,args.tag,interference,algo,Lambda)])

                subCommand = ["combine","-M",algo,"%s"%cardName, "-n" "%s"%args.config , "-m","%d"%Lambda, "-t", "1000", "--expectSignal","1","--rMax","100","--rMin","-100","--forceRecreateNLL"]
        
                subprocess.call(subCommand)

                resultFile = "higgsCombine%s.%s.mH%d.123456.root"%(args.config,algo,Lambda)
                
                subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s%s_%s.%s.mH%d_mu1.root"%(outDir,args.config,args.tag,interference,algo,Lambda)])
    else:
        if args.mass > 0:
            masses = [[5,args.mass,args.mass]]
        else:
            masses = config.masses

        for mass in masses:
            for interference in config.interferences:
                print ("calculate bias study for mass %d"%mass)
                if len(config.channels) == 1:
                    cardName = cardDir + "/" + config.channels[0] + "_%d_%s"%(mass,interference) + ".txt"
                else:
                    cardName = cardDir + "/" + args.config + "_combined" + "_%d_%s"%(mass,interference) + ".txt"
        
                if binned:
                    cardName = cardName.split(".")[0] + "_binned.txt"
                    numToys = config.numToys
                if args.expected:
                    numToys = 1
    
                if not args.frequentist:
                    subCommand = ["combine","-M","MarkovChainMC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "-i", "%d"%config.numInt, "--tries", "%d"%numToys ,  "--prior","flat","--rMax","%d"%getRange(mass,args.DM,False,args.usePhysicsModel, BSLL=args.BSLL)]
                else:
                    subCommand = ["combine","-M","HybridNew","--frequentist","--testStat","LHC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass,"--rMax","%d"%getRange(mass,args.DM,False,args.usePhysicsModel, BSLL=args.BSLL), "--rMin", "-10"]
                if args.expected: 
                    subCommand.append("-t")
                    subCommand.append("%d"%config.exptToys)
        
                if args.lower:
                    subCommand.append("--saveChain")
        
                for library in config.libraries:		
                    subCommand.append("--LoadLibrary")
                    subCommand.append("userfuncs/%s"%library)
                subprocess.call(subCommand)

                if args.expected:	
                    resultFile = "higgsCombine%s.%s.mH%d.123456.root"%(args.config,algo,mass)
                else:
                    resultFile = "higgsCombine%s.%s.mH%d.root"%(args.config,algo,mass)
                
                subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s.%s.mH%d_%s.root"%(outDir,args.config,algo,mass,interference)])
def runFitDiagnostics(args,config,outDir,cardDir,binned):

    # algo = "FitDiagnostics"
    algo = "Impacts"

   
    if args.BBLL or args.BSLL:
        
        if args.Lambda > 0:
            Lambdas = [args.Lambda]
        else:
            if args.BSLL:
                Lambdas = config.lambdasBSLL
                interferences = config.interferencesBSLL
            else:    
                Lambdas = config.lambdasBBLL
                interferences = config.interferencesBBLL
        for Lambda in Lambdas:
            for interference in interferences:
                print ("calculate limit for Lambda %d and model %s"%(Lambda,interference))
                if len(config.channels) == 1:
                    cardName = cardDir + "/" + config.channels[0] + "_%d_%s"%(Lambda,interference) 
                else:
                    cardName = cardDir + "/" + args.config + "_combined" + "_%d_%s"%(Lambda,interference) 
        
                if binned:
                    cardName = cardName.split(".")[0] + "_binned"
                    numToys = config.numToys
                if args.expected:
                    numToys = 1

                #print "getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL): {0}".format(getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL))
                
                # for library in config.libraries:		
                #     subCommand.append("--LoadLibrary")
                #     subCommand.append("userfuncs/%s"%library)

                # get root files for combineTool
                subCommand = ["text2workspace.py", "%s.txt"%cardName,"-m","%d"%Lambda, "--out", "%s_workspace.root"%cardName] 
                # subCommand = ["text2workspace.py", "%s.txt"%cardName,"-m","%d"%Lambda] 
                subprocess.call(subCommand)
                print ("text2workspace")
                print (subCommand)

                for expectSignal_val in ['0','1']: 
                    # doInitialFit
                    subCommand = ["combineTool.py","-M",algo, "-d", "%s_workspace.root"%cardName, "--expectSignal", expectSignal_val, "-t", "-1","--rMin", "-10", "--rMax", "%d"%getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL), "--doInitialFit", "--allPars", "-m","%d"%Lambda, "-n", "%s"%args.config] 
                    print (subCommand)
                    subprocess.call(subCommand)
                    print ("after call")
                    # doFits 
                    subCommand = ["combineTool.py","-M",algo, "-d", "%s_workspace.root"%cardName, "--expectSignal", expectSignal_val, "-t", "-1","--rMin", "-10", "--rMax", "%d"%getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL), "-m","%d"%Lambda, "-n", "%s"%args.config, "--doFits"]  
                    subprocess.call(subCommand)

                    # collect to json file
                    out_json_name = "%s_impacts_expSig"%cardName + expectSignal_val + ".json"
                    subCommand = ["combineTool.py","-M",algo, "-d", "%s_workspace.root"%cardName, "--expectSignal", expectSignal_val, "-t", "-1","--rMin", "-10", "--rMax", "%d"%getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL), "-m","%d"%Lambda, "-n", "%s"%args.config, "-o", out_json_name]  
                    subprocess.call(subCommand)

                    # plot
                    subCommand = ["plotImpacts.py","-i", out_json_name, "-o", "%s_impacts_expSig"%cardName + expectSignal_val]
                    subprocess.call(subCommand)

                # resultFile = "fitDiagnostics%s.root"%(args.config)
                
                # subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s.%s.mH%d_%s.root"%(outDir,args.config,algo,Lambda,interference)])


    else:
        #print "ERROR: we don't uses masses, so this option is defunct"
        raise ValueError
        if args.mass > 0:
            masses = [[5,args.mass,args.mass]]
        else:
            masses = config.masses

        for massRange in masses:
            mass = massRange[1]
            while mass <= massRange[2]:

                print ("perform fit diagnostics for mass %d"%mass)
                if len(config.channels) == 1:
                    cardName = cardDir + "/" + config.channels[0] + "_%d"%(mass) + ".txt"
                else:
                    cardName = cardDir + "/" + args.config + "_combined" + "_%d"%(mass) + ".txt"
        
                if binned:
                    cardName = cardName.split(".")[0] + "_binned.txt"
                    numToys = config.numToys
                if args.expected:
                    numToys = 1
    
                #subCommand = ["combine","-M",algo,"%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass,"--rMax","%d"%getRange(mass,args.CI,args.usePhysicsModel, BSLL=args.BSLL), "--rMin", "-10", "-t", "-1", "--expectSignal","1","--forceRecreateNLL","--plots"]
                #subCommand = ["combine","-M",algo,"%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass,"--rMax","%d"%getRange(mass,args.CI,args.usePhysicsModel, BSLL=args.BSLL),"--robustFit","1","--plots","--setRobustFitAlgo","migrad","--setRobustFitStrategy","2","--stepSize","0.001","--setRobustFitTolerance","0.5"]
                subCommand = ["combine","-M",algo,"%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass,"--rMax","%d"%getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),"--robustFit","1","--plots"]
        
                for library in config.libraries:		
                    subCommand.append("--LoadLibrary")
                    subCommand.append("userfuncs/%s"%library)
                subprocess.call(subCommand)

                resultFile = "fitDiagnostics%s.root"%(args.config)
                
                subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s.%s.mH%d.root"%(outDir,args.config,algo,mass)])


                mass += massRange[0]



def submitLimits(args,config,outDir,binned,tag):
    #Aman
    mass = args.mass
    print ("Job submission requested")
    if config.submitTo in supportedResources:
        print ("%s resources will be used"%config.submitTo)
    else:
        print ("Computing resource not supported at the moment. Supported resources are:")
        for resource in supportedResources:
            print (resource)
        sys.exit()	
    if not os.path.exists("logFiles_%s%s"%(args.config,args.tag)):
            os.makedirs("logFiles_%s%s"%(args.config,args.tag))

    if not args.inject:
        srcDir = os.getcwd()
        os.chdir(srcDir+"/logFiles_%s%s"%(args.config,args.tag))
    else:
        srcDir = os.getcwd()
        if not os.path.exists("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"])):
                os.makedirs("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
        os.chdir(srcDir+"/logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
    
    Libs = ""
    #for library in config.libraries:
    #        Libs += "%s/userfuncs/%s "%(srcDir,library)

    name = "_"
    if args.inject:
        name += "_%d_%.4f_%d"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
    else:
        name += tag
    import time
    timestamp = time.strftime("%Y%m%d") + "_" + time.strftime("%H%M")
    if args.BBLL or args.BSLL:

        if args.Lambda > 0:
            Lambdas = [args.Lambda]
        else:
            if args.BSLL:
                Lambdas = config.lambdasBSLL
                interferences = config.interferencesBSLL
            else:    
                Lambdas = config.lambdasBBLL
                interferences = config.interferencesBBLL
               
        for Lambda in Lambdas:

            print ("submit limit for Lambda %d"%Lambda)
            for interference in interferences:
                if len(config.channels) == 1:
                    cardName = config.channels[0] + "_%d_%s"%(Lambda,interference) + ".txt"
                else:
                    cardName = args.config + "_combined" + "_%d_%s"%(Lambda,interference) + ".txt"
                if binned:
                    cardName = cardName.split(".")[0] + "_binned.txt"

                if config.submitTo == "FNAL":
                    if args.expected:
                        numJobs = int(config.exptToys/10)
                        for i in range(0,numJobs):
                            arguments='%s %s %s %s %d %d %d %d %d %s %d %d %s'%(args.config,name+"_"+interference,srcDir,cardName,config.numInt,i,10,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)
                            condorFile = open("condor_FNAL.cfg", "w")
                            condorFile.write(condorTemplateFNAL%arguments)
                            condorFile.close()
                            subCommand = "condor_submit condor_FNAL.cfg"
                            subprocess.call(subCommand,shell=True)			
                    else:
                        #for i in range(0,config.numToys):
                        arguments='%s %s %s %s %d %d %d %d %d %s %d %d %s'%(args.config,name+"_"+interference,srcDir,cardName,config.numInt,config.numToys,0,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)
                        condorFile = open("condor_FNAL.cfg", "w")
                        condorFile.write(condorTemplateFNAL%arguments)
                        condorFile.close()
                        subCommand = "condor_submit condor_FNAL.cfg"
                        subprocess.call(subCommand,shell=True)	
                        import time
                        time.sleep(0.1)		

                if config.submitTo == "Purdue":
                    if args.is_int or args.usePhysicsModel:  ##Aman edits here
                        cardName = cardName.replace(".txt",".root")
                        if args.expected:
                            numJobs = int(config.exptToys/50)
                            for i in range(0,numJobs):
                                subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00 -A cms  %s/submission/CILimitsInt_PURDUE.job %s %s %s %s %d %d %d %d %d %s %s"%(srcDir,args.config,name,srcDir,cardName,config.numInt,i,50,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,interference)
                                print (subCommand)
                                subprocess.call(subCommand,shell=True)			
                        else:
                            #for i in range(0,config.numToys):
                            subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  -A cms %s/submission/CILimitsInt_PURDUE.job %s %s %s %s %d %d %d %d %d %s %s"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,0,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,interference)
                            subprocess.call(subCommand,shell=True)	
                            import time
                            time.sleep(0.1)	
                    else:	
                        print("fails subcommand with expected")

                        if args.expected:
                            numJobs = int(config.exptToys/50)
                            print("numJobs: {0}".format(numJobs))
                            for i in range(0,numJobs):
                                print ("here")
                                # print(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,i,50,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)
                                if args.BSLL:
                                    #subCommand = "sbatch --mem=4G -N1 -n1 -A cms --time=48:00:00  %s/submission/CILimits_PURDUE_BSLL.job %s %s %s %s %d %d %d %d %d %s %d %d %s"%(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,i,50,Lambda,getRange(mass,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)
                                    #Aman edits ; the below one is default
                                    subCommand = "sbatch --mem=4G -N1 -n1 -A cms --time=48:00:00  %s/submission/CILimits_PURDUE_BSLL.job %s %s %s %s %d %d %d %d %d %s %d %d %s"%(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,i,50,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)
                                else: # bbll
                                    subCommand = "sbatch --mem=4G -N1 -n1 -A cms --time=48:00:00  %s/submission/CILimits_PURDUE.job %s %s %s %s %d %d %d %d %d %s %d %d %s"%(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,i,50,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)
                                print ("subCommand: {0}".format(subCommand))
                                subprocess.call(subCommand,shell=True)			
                        else:
                           if args.BSLL:
                                subCommand = "sbatch -N1 -n1 --time=48:00:00 -A cms %s/submission/CILimits_PURDUE_BSLL.job %s %s %s %s %d %d %d %d %d %s %d %d %s"%(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,config.numToys,0,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)
                           else:
                                subCommand = "sbatch -N1 -n1 --time=48:00:00 -A cms %s/submission/CILimits_PURDUE.job %s %s %s %s %d %d %d %d %d %s %d %d %s"%(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,config.numToys,0,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)
 
                           print ("subCommand: {0}".format(subCommand))
                           subprocess.call(subCommand,shell=True) 
                           import time
                           time.sleep(0.1)
##Aman edits
#                            numJobs = int(config.exptToys/50)
#                            print("numJobs: {0}".format(numJobs))
#                            for i in range(0,numJobs):
#                            #for i in range(0,config.numToys/50):
#                                print ("here")
#                                if args.BSLL:
#                                    subCommand = "sbatch -N1 -n1 --time=48:00:00 -A cms %s/submission/CILimits_PURDUE_BSLL.job %s %s %s %s %d %d %d %d %d %s %d %d %s"%(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,config.numToys,0,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)
#                                else: # bbll
#                                    subCommand = "sbatch -N1 -n1 --time=48:00:00 -A cms %s/submission/CILimits_PURDUE.job %s %s %s %s %d %d %d %d %d %s %d %d %s"%(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,config.numToys,0,Lambda,getRange(Lambda,True,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.singlebin,args.mass,Libs)

#                                print ("subCommand: {0}".format(subCommand))
#                                subprocess.call(subCommand,shell=True)	
#                                import time
#                                time.sleep(0.1)		


    else:

        if args.mass > 0:
                  masses = [[5,args.mass,args.mass]]
        else:        
            masses = config.masses

        for massRange in masses:
            mass = massRange[1]
            while mass <= massRange[2]:

                print ("submit limit for mass %d"%mass)
                if len(config.channels) == 1:
                    cardName = config.channels[0] + "_%d"%mass + ".txt"
                else:
                    cardName = args.config + "_combined" + "_%d"%mass + ".txt"
                if binned:
                    cardName = cardName.split(".")[0] + "_binned.txt"
                if config.submitTo == "Purdue":
                    if args.frequentist:
                        if args.expected:
                            subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimeLimitsFreq_PURDUE.job %s %s %s %s %d %d %d %d %d %s %d %s"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,config.exptToys,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,Libs)
                            subprocess.call(subCommand,shell=True)			
                        else:
                            for i in range(0,config.numToys):
                                subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimeLimitsFreq_PURDUE.job %s %s %s %s %d %d %d %d %d %s %d %s"%(srcDir,args.config,name,srcDir,cardName,config.numInt,i,0,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,Libs)
                                subprocess.call(subCommand,shell=True)			
                    elif args.asymptotic:
                        
                        subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimeLimitsAsymp_PURDUE.job %s %s %s %s %d %d %d %d %d %s %d %s"%(srcDir,args.config,name,srcDir,cardName,config.numInt,0,0,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,Libs)
                        subprocess.call(subCommand,shell=True)			


                    else:
                        if args.expected:
                            numJobs = int(config.exptToys/10)
                            for i in range(1,numJobs+1):
                                if args.BSLL:
                                    subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimeLimits_PURDUE_BSLL.job %s %s %s %s %d %d %d %d %d %s %d %d %d %s"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,config.exptToys/500,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,args.inject,i,Libs)
                                else: #bbll
                                    subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimeLimits_PURDUE.job %s %s %s %s %d %d %d %d %d %s %d %d %d %s"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,config.exptToys/500,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,args.inject,i,Libs)
                                subprocess.call(subCommand,shell=True)			
                        else:
                            #for i in range(0,config.numToys):
                            if args.BSLL:
                                subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimeLimits_PURDUE_BSLL.job %s %s %s %s %d %d %d %d %d %s %d %d %d %s"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,0,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,args.inject,0,Libs)
                            else:
                                subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimeLimits_PURDUE.job %s %s %s %s %d %d %d %d %d %s %d %d %d %s"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,0,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,args.inject,0,Libs)
                            subprocess.call(subCommand,shell=True)	
                            import time
                            time.sleep(0.1)		

                if config.submitTo == "SNU":
                    if args.frequentist:
                        print ('frequentist option is not yet suppored in SNU cluster')
                        # if args.expected:
                        #         subCommand = "sbatch --time=48:00:00 -q cms-express %s/submission/zPrimeLimitsFreq_PURDUE.job -F '%s %s %s %s %d %d %d %d %d %s %d %s '"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,config.exptToys,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,Libs)
                        #         subprocess.call(subCommand,shell=True)                  
                        # else:
                        #         for i in range(0,config.numToys):
                        #                 subCommand = "sbatch --time=48:00:00 -q cms-express %s/submission/zPrimeLimitsFreq_PURDUE.job -F '%s %s %s %s %d %d %d %d %d %s %d %s '"%(srcDir,args.config,name,srcDir,cardName,config.numInt,i,0,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,Libs)
                        #                 subprocess.call(subCommand,shell=True)                  

                    else:
                        if args.expected:
                            subCommand = "source %s/submission/zPrimeLimits_SNU.sh %s %s %s %s %d %d %d %d %d %s %d %s" % (srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,config.exptToys,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,Libs)
                            subprocess.call(subCommand,shell=True)
                        else:
                            subCommand = "source %s/submission/zPrimeLimits_SNU.sh %s %s %s %s %d %d %d %d %d %s %d %s" % (srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,0,mass,getRange(mass,False,args.usePhysicsModel, BSLL=args.BSLL),timestamp,args.spin2,Libs)
                            subprocess.call(subCommand,shell=True)
                            import time
                            time.sleep(0.1)

                mass += massRange[0]

def submitPValues(args,config,outDir,binned,tag):

    print ("Job submission requested")
    if config.submitTo in supportedResources:
        print ("%s resources will be used"%config.submitTo)
    else:
        print ("Computing resource not supported at the moment. Supported resources are:")
        for resource in supportedResources:
            print (resource)
        sys.exit()	
        if args.mass > 0:
                masses = [[5,args.mass,args.mass]]
        else:
                masses = config.masses
    if args.LEE:
        masses = [[5,200,5000]]
    if not args.inject:
        if not os.path.exists("logFiles_%s"%args.config):
                os.makedirs("logFiles_%s"%args.config)
        srcDir = os.getcwd()
        os.chdir(srcDir+"/logFiles_%s"%args.config)
    else:
        srcDir = os.getcwd()
        if not os.path.exists("logFiles_%s%s_%d_%.4f_%d"%(args.config,args.tag,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"])):
                os.makedirs("logFiles_%s%s_%d_%.4f_%d"%(args.config,args.tag,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
        os.chdir(srcDir+"/logFiles_%s%s_%d_%.4f_%d"%(args.config,args.tag,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
    
    Libs = ""
    #for library in config.libraries:
    #        Libs += "%s/userfuncs/%s "%(srcDir,library)

    name = "_"
    if args.inject:
        name += "_%d_%.4f_%d"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
    else:
        name += tag
    import time
    timestamp = time.strftime("%Y%m%d") + "_" + time.strftime("%H%M")
    for massRange in masses:
        print ("submit p-value for mass range %d - %d GeV in %d GeV steps"%(massRange[1],massRange[2],massRange[0]))
        if len(config.channels) == 1:
            cardName = config.channels[0] + "_"
        else:
            cardName = args.config + "_combined" + "_"
        if binned:
            cardName = cardName + "binned.txt"
        if config.submitTo == "Purdue":
            if args.hybrid:
                mass = massRange[1]
                while mass <= massRange[2]:
                    subCommand = "sbatch  --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimePValuesHybrid_PURDUE.job %s %s %s %s %d %s %s"%(srcDir,args.config,name,srcDir,cardName,mass,timestamp,Libs)
                    mass += massRange[0]
                    subprocess.call(subCommand,shell=True)			
            elif args.frequentist:	
                mass = massRange[1]
                while mass <= massRange[2]:
                    subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimePValuesFreq_PURDUE.job %s %s %s %s %d %s %s"%(srcDir,args.config,name,srcDir,cardName,mass,timestamp,Libs)
                    mass += massRange[0]
                    subprocess.call(subCommand,shell=True)			
            elif args.plc:	
                subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimePValuesPLC_PURDUE.job %s %s %s %s %d %d %d %s %s"%(srcDir,args.config,name,srcDir,cardName,massRange[1],massRange[2],massRange[0],timestamp,Libs)
                subprocess.call(subCommand,shell=True)			
            else:
                if args.LEE:
                    subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimePValuesLEE_PURDUE.job %s %s %s %s %d %d %d %s %s"%(srcDir,args.config,name,srcDir,cardName,massRange[1],massRange[2],massRange[0],timestamp,Libs)
                else:	
                    subCommand = "sbatch --mem=4G -N1 -n1 --time=48:00:00  %s/submission/zPrimePValues_PURDUE.job %s %s %s %s %d %d %d %s %s"%(srcDir,args.config,name,srcDir,cardName,massRange[1],massRange[2],massRange[0],timestamp,Libs)
                subprocess.call(subCommand,shell=True)			
    os.chdir(srcDir)	


def submitLimitsToCrab(args,config,cardDir):

    if args.redo:
        createInputs(args,config,cardDir,CRAB=False)
    masses = config.masses
    if args.expected:
        masses = config.massesExp
    if args.mass > 0:
        if args.expected:
            for massRange in masses:
                if args.mass >= massRange[1] and args.mass < massRange[2]:
                    masses = [massRange]
                    masses[0][1] = args.mass
                    masses[0][2] = args.mass+1
        else:
            masses = [[5,args.mass,args.mass+1]]
    workspaces = []
    i = 0
    for massRange in masses:
        mass = massRange[1]
        while mass < massRange[2]:
            if len(config.channels) ==1:
                command = ["text2workspace.py","%s/%s_%d.txt"%(cardDir,config.channels[0],mass)]
                workspaces.append("%s/%s_%d.root"%(cardDir,config.channels[0],mass))
                
                for library in config.libraries:		
                    command.append("--LoadLibrary")
                    command.append("userfuncs/%s"%library)
                if args.redo:
                    subprocess.call(command)	
                i += 1
                mass += massRange[0]			
            else:
                command = ["text2workspace.py","%s/%s_combined_%d.txt"%(cardDir,args.config,mass)]
                workspaces.append("%s/%s_combined_%d.root"%(cardDir,args.config,mass))
                for library in config.libraries:		
                    command.append("--LoadLibrary")
                    command.append("userfuncs/%s"%library)
    
                if args.redo:
                    subprocess.call(command)	
                i += 1
                mass += massRange[0]			
    libPart = []
    for lib in config.libraries:
        libPart.append("userfuncs/"+lib)
        libPart.append("userfuncs/"+lib.split("_")[0]+".cxx")
        libPart.append("userfuncs/"+lib.split("_")[0]+".h")
        libPart.append("userfuncs/"+lib.split(".")[0]+".d")

    nrJobs = 1

    script="submitLimitCrabJob.py"
    injectArgument = "0"
    if args.inject:
        injectArgument = "1"
    if args.expected:
         for massRange in masses:
            mass = massRange[1]
            while mass < massRange[2]:
            
                nJobs = str(massRange[3])
                nToys = str(massRange[4])
                nIter = str(massRange[5])
                if len(config.channels) > 1:	
                    workspace = "%s/%s_combined_%d.root"%(cardDir,args.config,mass)
                else:	
                    workspace = "%s/%s_%d.root"%(cardDir,config.channels[0],mass)
                
                print("runInterpretation script flag 2")
                tarCommand = ['tar', '-cvf', 'gridPack.tar',"cfgs/","runInterpretation.py","userfuncs/"] + [workspace]
                #tarCommand = ['tar', '-cvf', 'gridPack.tar',"cfgs/","runInterpretation.py"] + [workspace] + libPart
                subprocess.call(tarCommand)

                mvCmd = ["mv gridPack.tar submission/"]
                subprocess.call(mvCmd,shell=True)

                os.chdir("submission/")

                scriptArgs=["python",script,"--mass",str(mass),"--nIter",nIter,"--nrJobs",nJobs,"--nToys",nToys,"--gridPack","gridPack.tar","--outputTag",args.tag.split("_")[-1],"--crabConfig","crab_base.py","--config",args.config,"--expected","1","--inject",injectArgument]
                result = subprocess.Popen(scriptArgs,stdout=subprocess.PIPE).communicate()[0].splitlines()
                for line in result:
                        print (line)

                mass += massRange[0]			
                os.chdir('../')
    else:
        nJobs = str(i)
        nToys = str(config.numToys)
        nIter = str(config.numInt)

        print("runInterpretation script flag 3")
        tarCommand = ['tar', '-cvf', 'gridPack.tar',"cfgs/","runInterpretation.py","userfuncs/"] + workspaces
        subprocess.call(tarCommand)

        mvCmd = ["mv gridPack.tar submission/"]
        subprocess.call(mvCmd,shell=True)

        os.chdir("submission/")

        scriptArgs=["python",script,"--mass",str(mass),"--nIter",nIter,"--nrJobs",nJobs,"--nToys",nToys,"--gridPack","gridPack.tar","--outputTag",args.tag.split("_")[-1],"--crabConfig","crab_base.py","--config",args.config,"--expected","0","--inject",injectArgument]
        result = subprocess.Popen(scriptArgs,stdout=subprocess.PIPE).communicate()[0].splitlines()
        for line in result:
            print (line)




        

    sys.exit(0)

#def submitToFNALCondor(args,config):
#
#    from prepareLPCSubmission import createRunSH, createJDL
#    if not os.path.exists("../../../submission"):
#        os.mkdir("../../../submission")
#    os.chdir("../../../")
#    print ("tar-ing the CMSSW installation")
#    subprocess.call(['tar', '-zcf', 'CMSSW10213.tgz', 'CMSSW_10_2_13'])
#    print ("copying tar file to eos")
#    subprocess.call(['xrdcp', "-f", 'CMSSW10213.tgz', 'root://cmseos.fnal.gov//store/user/%s/CMSSW10213.tgz'%config.LPCUsername])
#    os.chdir("submission/")
#    print ("creating executable for condor jobs")
#    createRunSH(args,config)
#    print (os.getcwd())
#    if args.expected:
#        #os.chmod("runInterpretationExp.sh",0755)
#    else:
#        #os.chmod("runInterpretation.sh",0755)
#    if args.expected:
#        if args.BBLL or args.BSLL:
#            if args.BSLL:
#                Lambdas = config.lambdasBSLL
#            else:
#                Lambdas = config.lambdasBBLL
#            for L in Lambdas:
#                print ("creating JDL file for Lambda %d"%L)
#                createJDL(args,config,L)
#                print ("submitting jobs for Lambda %d"%L)
#                os.system("condor_submit condor.jdl")
#
#        else:
#            for massBlock in config.massesExp:
#                mass = massBlock[1]
#                while mass <= massBlock[2]:
#                    print ("creating JDL file for mass %d"%mass)
#                    createJDL(args,config,mass)
#                    print ("submitting jobs for mass %d"%mass)
#                    os.system("condor_submit condor.jdl")
#                    mass += massBlock[0]
#    else:
#        print ("creating JDL file")
#        createJDL(args,config)
#        print ("submitting jobs")
#        os.system("condor_submit condor.jdl")



def createInputs(args,config,cardDir,CRAB=False,LEE=True):
    for channel in config.channels:
        print ("writing datacards and workspaces for channel %s ...."%channel)
        call = ["python","writeDataCards.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s"%args.tag]
        if args.mass > 0:
            call.append("-m")
            call.append("%d"%args.mass)
        if args.inject:
            call.append("-i")
        if args.recreateToys:
            call.append("--recreateToys")
        if args.binned:
            call.append("-b")
        if args.expected:
            call.append("--expected")
        if args.signif:
            call.append("-s")
        if args.spin2:
            call.append("--spin2")
        #if LEE:
        #	call.append("--prepare")
        if args.frequentist:
            if not "-s" in call:
                call.append("-s")
        if not args.workDir == '':
            call.append("--workDir")
            call.append(args.workDir)
        subprocess.call(call)

    print ("createInputs done!")
    tag = args.tag
    if not args.tag == "":
        tag = "_" + args.tag
    #if not LEE:
    if len(config.channels) > 1 or CRAB:
        print ("writing combined channel datacards ....")
        if args.mass > 0:
            masses = [[5,args.mass,args.mass]]
        else:
            masses = config.masses
            if args.expected:
                masses = config.massesExp
        for massRange in masses:
            mass = massRange[1]
            while mass <= massRange[2]:
                command = ["combineCards.py"]	
                for channel in config.channels:
                    if args.binned:
                        command.append( "%s=%s_%d_binned.txt"%(channel,channel,mass))			
                    else:	
                        command.append( "%s=%s_%d.txt"%(channel,channel,mass))			
                outName = "%s/%s_combined_%d.txt"%(cardDir,args.config,mass)
                if args.binned:
                    outName = outName.split(".")[0]+"_binned.txt"
                with open('%s'%outName, "w") as outfile:
                    subprocess.call(command, stdout=outfile,cwd=cardDir)

                mass += massRange[0]			
        print ("done!")

def createInputsGen(args,config,cardDir):
    for channel in config.channels:
        print ("writing datacards and workspaces for channel %s ...."%channel)
        if args.singlebin:
            mass = args.mass
            if args.mass == -1:
                mass = 2000
            call = ["python3","writeDataCardsCISingleBin.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s"%args.tag, "-m","%d"%mass]
        else:	
            print("BBLL contact interaction")
            call = ["python3","writeDataCardsCI.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s_expGen"%args.tag]
        if args.expected:
            call.append("--expected")
        if args.signif:
            call.append("-s")
        if args.frequentist:
            if not "-s" in call:
                call.append("-s")
        if not args.workDir == '':
            call.append("--workDir")
            call.append(args.workDir)
        subprocess.call(call)

    print ("done!")
    tag = args.tag
    if not args.tag == "":
        tag = "_" + args.tag

    if len(config.channels) > 1:
        print ("writing combined channel datacards ....")
        if int(args.Lambda) > 0:
            lambdas = [args.Lambda]
        else:
            lambdas = config.lambdasBBLL
        for Lambda in lambdas:
            for interference in config.interferencesBBLL:
                command = ["combineCards.py"]	
                for channel in config.channels:
                    command.append( "%s=%s_%d_%s.txt"%(channel,channel,Lambda,interference))			
                outName = "%s/%s_combined_%d_%s.txt"%(cardDir,args.config,Lambda,interference)
                with open('%s'%outName, "w") as outfile:
                    subprocess.call(command, stdout=outfile,cwd=cardDir)
                   # if args.usePhysicsModel or args.is_int:
                   #      subprocess.call(command, stdout=outfile,cwd=cardDir)
                   #      outFile = outName.split(".")[0]+".root"

                   #      print("here is aman ", outName)
                   #      print("here is aman ", outFile, cardDir)
                   #      command = ["text2workspace.py", outName, "-o", outFile, "-P", "HiggsAnalysis.CombinedLimit.CIInterference:CIInterference"]
                   #      subprocess.call(command)
                   # else:
                   #      subprocess.call(command, stdout=outfile,cwd=cardDir)
                   # # subprocess.call(command)
        print ("createInputsBBLL done!")


def createInputsBSLL(args,config,cardDir):
    for channel in config.channels:
        print ("writing datacards and workspaces for channel %s ...."%channel)
        if args.singlebin:
            mass = args.mass
            if args.mass == -1:
                mass = 2000
            call = ["python","writeDataCardsCISingleBin.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s"%args.tag, "-m","%d"%mass, "--BSLL"]
        else:	
            if args.is_int:
                call = ["python","writeDataCardsCIInt.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s"%args.tag, "--BSLL"]
            else:
                print("BSLL contact interaction")
                call = ["python","writeDataCardsCI.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s"%args.tag, "--BSLL"]
        if args.expected:
            call.append("--expected")
        if args.signif:
            call.append("-s")
        if args.frequentist:
            if not "-s" in call:
                call.append("-s")
        if not args.workDir == '':
            call.append("--workDir")
            call.append(args.workDir)
        subprocess.call(call)

    print ("done!")
    tag = args.tag
    if not args.tag == "":
        tag = "_" + args.tag

    if len(config.channels) > 1:
        print ("writing combined channel datacards ....")
        if int(args.Lambda) > 0:
            lambdas = [args.Lambda]
        else:
            lambdas = config.lambdasBSLL
        for Lambda in lambdas:
            for interference in config.interferencesBSLL:
                command = ["combineCards.py"]	
                for channel in config.channels:
                    command.append( "%s=%s_%d_%s.txt"%(channel,channel,Lambda,interference))			
                outName = "%s/%s_combined_%d_%s.txt"%(cardDir,args.config,Lambda,interference)
                with open('%s'%outName, "w") as outfile:
                    subprocess.call(command, stdout=outfile,cwd=cardDir)

                    # if args.usePhysicsModel or args.int:
                    #     outFile = outName.split(".")[0]+".root"
                    # outFile = outName.split(".")[0]+".root"
                    # if args.int:
                    #     command = ["text2workspace.py", outName, "-o", outFile, "-P", "HiggsAnalysis.CombinedLimit.CIInterference:CIInterference"]
                    # else:	
                    #     command = ["text2workspace.py", outName, "-o", outFile, "-P", "HiggsAnalysis.CombinedLimit.LambdaCI:CIlambda"]
                    # subprocess.call(command)
        print ("createInputsBSLL done!")



def summarizeConfig(config,args,cardDir):
    print ("      ")
    print ("Z' -> ll statistics tool based on Higgs Combine")
    print ("               ")
    print ("------- Configuration Summary --------")
    if args.signif:
        print ("Calculation of significances requested")
    else:
        print ("Limit calculation requested")
        if args.expected:
            print ("Calculating expected limits with %d toy datasets"%config.exptToys)
        else:
            print ("Calculating observed limits")
        print ("MCMC configuration: iterations %d toys: %d"%(config.numInt,config.numToys))
    channelList = ""
    for channel in config.channels:
        channelList += " %s "%(channel)
    print ("Consider channels: %s"%channelList)
    systList = "" 
    for syst in config.systematics:
        systList += " %s "%(syst)
    print ("Systematic uncertainties: %s"%systList)
    if args.mass > 0:
        print ("run for single mass point at %d GeV"%args.mass)
    
    else:
        print ("Mass scan configuration: ")
        for massRange in config.masses:
            print ("from %d to %d in %d GeV steps"%(massRange[1],massRange[2],massRange[0]))
    print ("data cards and workspaces are saved in %s"%cardDir)	
    print ("--------------------------------------")
    print ("                                      ")

def summarizeConfigCI(config,args,cardDir):
    print ("      ")
    print ("Z' -> ll statistics tool based on Higgs Combine")
    print ("               ")
    print ("------- Configuration Summary --------")
    if args.signif:
        print ("Calculation of significances requested")
    else:
        print ("Limit calculation requested")
        #if args.expected:
        #    print ("Calculating expected limits with %d toy datasets"%config.exptToys)
        #else:
        #    print ("Calculating observed limits")
        print ("MCMC configuration: iterations %d toys: %d"%(config.numInt,config.numToys))
    channelList = ""
    for channel in config.channels:
        channelList += " %s "%(channel)
    print ("Consider channels: %s"%channelList)
    systList = "" 
    for syst in config.systematics:
        systList += " %s "%(syst)
    print ("Systematic uncertainties: %s"%systList)
    
    print ("Lambda scan configuration: ")
    if args.BSLL:
        print ("from %d to %d"%(config.lambdasBSLL[0],config.lambdasBSLL[-1]))
    else:    
        print ("from %d to %d"%(config.lambdasBBLL[0],config.lambdasBBLL[-1]))
    print ("data cards and workspaces are saved in %s"%cardDir)
    #if args.singlebin:
    #    if args.mass == -1:
    #        print ("Use single bin counting with threshold 2000 GeV")
    #    else:	
    #        print ("Use single bin counting with threshold %d GeV"%args.mass)
    print ("--------------------------------------")
    print ("                                      ")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Steering tool for Zprime -> ll analysis interpretation in combine')
    parser.add_argument("-w", "--write", action="store_true", default=False, help="create datacards and workspaces for this configuration")
    parser.add_argument("-c", "--config", dest = "config", required=True, help="name of the congiguration to use")
    parser.add_argument("-t", "--tag", dest = "tag", default = "", help="tag to label output")
    parser.add_argument( "--workDir", dest = "workDir", default = "", help="tells batch jobs where to put the datacards. Not for human use!")
    parser.add_argument("--BBLL", dest = "BBLL",action="store_true", default = False, help="calculate limits for bbll model")
    parser.add_argument("--BSLL", dest = "BSLL",action="store_true",default = False, help="calculate limits for bsll model")
    parser.add_argument("-i", "--inject", action="store_true", default=False, help="inject signal")
    parser.add_argument("--signif", action="store_true", default=False, help="run significance instead of limits")
    parser.add_argument("-b", "--binned", action="store_true", default=False, help="use binned dataset")
    args = parser.parse_args()

    print(f"args.BBLL: {args.BBLL}")
    print(f"args.write: {args.write}")


    configName = "scanConfiguration_%s"%args.config

    config =  __import__(configName)

    tag = args.tag
    if not args.tag == "":
        args.tag = "_" + args.tag

    from tools import getCardDir, getOutDir
    cardDir = getCardDir(args,config)
        
    print("args.BBLL: {0}".format(args.BBLL))
    if args.BBLL or args.BSLL:	
        summarizeConfigCI(config,args,cardDir)
    else:	
        summarizeConfig(config,args,cardDir)



    outDir = getOutDir(args,config)
        
    if not os.path.exists(outDir):
        os.makedirs(outDir)
