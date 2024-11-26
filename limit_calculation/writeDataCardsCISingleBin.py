import argparse
import subprocess
import time
import os
import sys
sys.path.append('cfgs/')
sys.path.append('input/')

from channelConfiguration import getChannelConfig #Aman

def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '%' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()


##Data card for Zprime -> ll analysis, created on %(date)s at %(time)s using revision %(hash)s of the package

cardTemplate='''
##Data card for CI interpretation of the Zprime -> ll analysis, created on %(date)s at %(time)s
imax 1  number of channels
jmax %(nBkgs)s  number of backgrounds
kmax *  number of nuisance parameters (sources of systematical uncertainties)
------------
# we have just one channel, in which we observe 0 events
bin %(bin)s
observation %(data)s
------------
# now we list the expected events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error)
# on each process and bin
%(channels)s  
------------
%(systs)s
'''


def getChannelBlock(backgrounds,inputs,signalScale,chan):
        nBkgs = len(backgrounds)
        result = "bin %s"%chan
        for i in range(0,nBkgs):
                result += " %s "%chan
        result+="\n"
        result += "process      sig"
        for background in backgrounds:
                result+= " %s  "%background
        result +="\n"
        result +="process       0 "
        for i in range(0,nBkgs):
                result+=" %d"%(i+1)
        result +="\n"
        if inputs["sig"] >= 0:
                result += "rate         %.4f "%inputs["sig"]
        else:   
                result += "rate         0.0 "
        #result += "rate         1 "
        for background in backgrounds:
                result+= " %.4f"%inputs["bkg%s"%background]
        return result
 
# correlations = {
# "xSecOther":2,
# "jets":2,
# "zPeak":1,
# "trig":1,
# "massScale":0,
# "stats":0,
# "res":0,
# "pdf":2,
# "ID":0,
# "lumi":2,
# "PU":2
# }
##AmanEdits##
# what uncertainties are correlated? 0 for none at all, 1 for correlation across years, 2 accross channels, 3 for both
correlations = {
    "trig":0,
    "zPeak":0,
    "ttbarSF":0,
    "ttbar_dnn":0,
    "xSecOther":3,
    "jets":2,
    "lumi":3,
    "l1prefiring":0,
    "stats":0,
    "massScale":0,
    "energyScale":0,
    "res":0,
    "pdf":3,
    "ttbarUncert" : 0,
    #"ID": 2, #for elec 
    #"ID": 0,#for mu
    "ISO":0,
    "HLT":0,
    "PU":2,
    "JEC": 2,
    "JER": 2,
    "reco" : 0,
    "btagSF_bc" : 2, #0,
    "btagSF_light" : 2, #0
    "btagSF_bc_corr" : 3, #0,
    "btagSF_light_corr" : 3, #0
}
##

def getUncert(uncert, value, backgrounds, mass,channel,correlate,yields,signif):
    # print("getUncert uncert : {0}".format(uncert))
    result = ""
    if len(value) == 1:
        value = value[0]

    if "ID" in uncert:
       if "dimuon" in channel:
           correlations[uncert] = 0
       else:
           correlations[uncert] = 2

    if correlate:
        if correlations[uncert] == 0: # specify both channel and year
            # remove BB or BE and add it as name
            if "BB" in channel:
                name = "%s_%s"%(uncert,channel.replace('BB_', ""))
            else:
                name = "%s_%s"%(uncert,channel.replace('BE_', ""))

        elif correlations[uncert] == 1:
            if "dimuon" in channel:
                name = "%s_dimuon"%uncert
            else:
                name = "%s_dielectron"%uncert
        elif correlations[uncert] == 2:
            if "dielectron" in channel:
                if "2018" in channel:
                    name = "%s_dielectron18"%(uncert)
                elif "2017" in channel:
                    name = "%s_dielectron17"%(uncert)
                elif "2016_post" in channel:
                    name = "%s_dielectron16_post"%(uncert)
                elif "2016_pre" in channel:
                    name = "%s_dielectron16_pre"%(uncert)
                else:
                    print("option not supported")
                    raise ValueError
            else:
                if "2018" in channel:
                    name = "%s_dilepton18"%(uncert)
                elif "2017" in channel:
                    name = "%s_dilepton17"%(uncert)
                elif "2016_post" in channel:
                    name = "%s_dilepton16_post"%(uncert)
                elif "2016_pre" in channel:
                    name = "%s_dilepton16_pre"%(uncert)
                else:
                    print("option not supported")
                    raise ValueError
        elif correlations[uncert] == 3:
            if "dielectron" in channel:
               name = "%s_dielectron"%(uncert)
            else:
               name = "%s_dilepton"%(uncert)
    else:
        name = "%s_%s"%(uncert,channel)
    # print("name: {0}".format(name))

    if "btagSF_bc" in uncert and not "btagSF_bc_corr" in uncert:
        print(name)
        result = "%s lnN  %.3f  "%(name, yields["sigbcUncorr"][0])
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  %.3f/%.3f  "%(yields["bkg%sbcUncorr"%background][0], yields["bkg%sbcUncorr"%background][1])
        result += "\n"

    if "btagSF_light" in uncert and not "btagSF_light_corr" in uncert:
        print(name)
        result = "%s lnN  %.3f  "%(name, yields["siglightUncorr"][0])
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  %.3f/%.3f  "%(yields["bkg%slightUncorr"%background][0], yields["bkg%slightUncorr"%background][1])
        result += "\n"


    if "btagSF_bc_corr" in uncert:
        print(name)
        result = "%s lnN  %.3f  "%(name, yields["sigbcCorr"][0])
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  %.3f/%.3f  "%(yields["bkg%sbcCorr"%background][0], yields["bkg%sbcCorr"%background][1])
        result += "\n"


    if "btagSF_light_corr" in uncert:
        print(name)
        result = "%s lnN  %.3f  "%(name, yields["siglightCorr"][0])
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  %.3f/%.3f  "%(yields["bkg%slightCorr"%background][0], yields["bkg%slightCorr"%background][1])
        result += "\n"


    if uncert == "jets":
        result = "%s lnN - "%name
        for background in backgrounds:
            if background == "Jets":
                    result += "  %.3f  "%value
            else:
                    result += " - "
        result += "\n"

    if uncert == "zPeak":
        if "ZeroB" in channel:
            result = "%s lnN  - "%name
            #result = "%s lnN %.3f"%(name,value)
            for background in backgrounds:
                if background == "Jets":
                       result += "  -  "
                else:
                       result += "  %.3f"%value
            result += "\n"
        else:
            result = "%s lnN  -  "%name
            for background in backgrounds:
                if background == "Jets":
                       result += "  -  "
                elif background == "DY":
                       result += "  1.10  "
                else:
                       result += "  %.3f"%value
            result += "\n"

    if uncert == "ttbarSF":
        result = "%s lnN   -  "%name
        #result = "%s lnN %.3f"%(name,value)
        for background in backgrounds:
            if background == "Top":
                    result += "  %.3f"%value
            else:
                    result += "  - "
        result += "\n"

    if uncert == "ttbar_dnn":
        result = "%s lnN   -  "%name
        if "ZeroB" in channel:
            for background in backgrounds:
                result += "  - "
        else:
            for background in backgrounds:
                if background == "Top":
                        if "2018" in channel:
                            if "BB" in channel:
                                result += " 1.50 "
                            if "BE" in channel:
                                result += " 1.14 "
                        elif "2017" in channel:
                            if "BB" in channel:
                                result += " 1.13 "
                            if "BE" in channel:
                                result += " 1.33 "
                        else:
                            if "BB" in channel:
                                result += " 1.05 "
                            if "BE" in channel:
                                result += " 1.08 "
                else:
                        result += "  - "
        result += "\n"

    if uncert == "trig" and not "muon" in channel:
        result = "%s lnN %.3f"%(name,value)
        for background in backgrounds:
            if background == "Jets":
                    result += "  -  "
            else:
                    result += "  %.3f"%value
        result += "\n"


    if uncert == "massScale" and not "electron" in channel:
        result = "%s lnN   %.3f/%.3f  "%(name, yields["sigScale"][0], yields["sigScale"][1])
        for background in backgrounds:
            if background == "Jets":
                    result += "  -  "
            else:
                    #result += "  %.3f"%value
                    result += "  %.3f/%.3f  "%(yields["bkg%sScale"%background][0], yields["bkg%sScale"%background][1])
        result += "\n"

    if uncert == "energyScale" and not "muon" in channel:
        result = "%s lnN   %.3f/%.3f  "%(name, yields["sigScale"][0], yields["sigScale"][1])
        for background in backgrounds:
            if background == "Jets":
                    result += "  -  "
            else:
                    #result += "  %.3f"%value
                    result += "  %.3f/%.3f  "%(yields["bkg%sScale"%background][0], yields["bkg%sScale"%background][1])

        result += "\n"

    # if uncert == "scaleUnc" and not "muon" in channel: # energyScale replaces this
    #     result = "%s shape 1"%name
    #     for background in backgrounds:
    #         if background == "Jets":
    #                 result += "  -  "
    #         else:
    #                 result += "  1  "

    #     result += "\n"                

    if uncert == "stats":
        result = "%s lnN   %.3f  "%(name, yields["sigStats"])
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "
            else:
                result += "  %.3f"%yields["bkg%sStats"%background]

        result += "\n"


    if uncert == "res" : #and not "electron" in channel
        result = "%s lnN   %.3f/%.3f  "%(name, yields["sigRes"][0], yields["sigRes"][1])
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "
            else:
                result += "  1.02"
                #result += "  %.3f"%value
        result += "\n"
    # if uncert == "PU" and not "muon" in channel:
    if uncert == "PU":
        result = "%s lnN  %.3f/%.3f  "%(name, yields["sigPU"][0], yields["sigPU"][1])
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "
            else:
                #result += "  %.3f"%value
                result += "  %.3f/%.3f  "%(yields["bkg%sPU"%background][0],yields["bkg%sPU"%background][1])
        result += "\n"

    if uncert == "pdf":
        result = "%s lnN %.3f  "%(name, yields["sigPDF"][0])
        #result = "%s lnN %.3f/%.3f  "%(name, yields["sigPDF"][0], yields["sigPDF"][1])
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  %.3f "%yields["bkg%sPDF"%background][0]
        result += "\n"

    if uncert == "ttbarUncert":
        result = "%s lnN - "%name
        if "ZeroB" in channel:
            for background in backgrounds:
                result += "  - "
        else:
            for background in backgrounds:
                if background == "Top":
                   result += "  %.3f/%.3f  "%(yields["bkg%sttbarUncert"%background][0],yields["bkg%sttbarUncert"%background][1])
                else:
                   result += "  -  "
        result += "\n"




    if uncert == "ID": # and not "electron" in channel
        result = "%s lnN   %.3f/%.3f  "%(name, yields["sigID"][0], yields["sigID"][1]) 
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "
            else:
                result += "   %.3f/%.3f  "%(yields["bkg%sID"%background][0], yields["bkg%sID"%background][1])
        result += "\n"

    if uncert == "ISO" and not "electron" in channel:
        result = "%s lnN   %.3f/%.3f  "%(name, yields["sigIso"][0], yields["sigIso"][1])
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "
            else:
                result += "   %.3f/%.3f "%(yields["bkg%sIso"%background][0], yields["bkg%sIso"%background][1])
        result += "\n"

    if uncert == "HLT" and not "electron" in channel:
        result = "%s lnN   %.3f/%.3f  "%(name, yields["sigHLT"][0], yields["sigHLT"][1])
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "
            else:
                result += "   %.3f/%.3f  "%(yields["bkg%sHLT"%background][0], yields["bkg%sHLT"%background][1])
        result += "\n"

    if uncert == "lumi":
        result = "%s lnN %.3f"%(name,value)
        for background in backgrounds:
            result += "  -  "
        result += "\n"


    if uncert == "l1prefiring":
        result = "%s lnN  %.3f/%.3f  "%(name, yields["sigL1Prefiring"][0], yields["sigL1Prefiring"][1])
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "   %.3f/%.3f "%(yields["bkg%sl1prefiring"%background][0],yields["bkg%sl1prefiring"%background][1])
        result += "\n"


    if uncert == "JEC":
        result = "%s lnN %.3f "%(name, value)
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  %.3f  "%(value)
        result += "\n"

    if uncert == "JER":
        result = "%s lnN %.3f "%(name, value)
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  %.3f  "%(value)
        result += "\n"

    if uncert == "reco" and not "electron" in channel:
        result = "%s lnN   %.3f/%.3f  "%(name, yields["sigReco"][0], yields["sigReco"][1])
        for background in backgrounds:
            if background == "Jets":
                    result += "  -  "
            else:
                    result += "   %.3f/%.3f"%(yields["bkg%sReco"%background][0], yields["bkg%sReco"%background][1])
        result += "\n"

    return result

                
        


def writeCard(card,fileName):

        text_file = open("%s.txt" % (fileName), "w")
        text_file.write(card)
        text_file.close()
        

def main():

        parser = argparse.ArgumentParser(description='Data writer for Zprime -> ll analysis interpretation in combine')
        parser.add_argument("--expected", action="store_true", default=False, help="write datacards for expected limit mass binning")
        parser.add_argument("-i", "--inject", action="store_true", default=False, help="inject signal")
        parser.add_argument("-c", "--chan", dest = "chan", default="", help="name of the channel to use")
        parser.add_argument("-o", "--options", dest = "config", default="", help="name of config file")
        parser.add_argument("-t", "--tag", dest = "tag", default="", help="tag")
        parser.add_argument("-m", "--mass", dest = "mass", default=2000, help="tag")
        parser.add_argument("-s", "--signif", action="store_true", default=False, help="write card for significances")
        parser.add_argument( "--workDir", dest = "workDir", default = "", help="tells batch jobs where to put the datacards. Not for human use!")
        parser.add_argument("--BSLL", dest="BSLL",default=False,action="store_true",help="use BSLL signal (default is BBLL)")
                                
        args = parser.parse_args()      
        tag = args.tag
        if not args.tag == "":
                tag = "_" + args.tag

        import glob
        from ROOT import gROOT
        #for f in glob.glob("userfuncs/*.cxx"):
        #        gROOT.ProcessLine(".L "+f+"+")


        configName = "scanConfiguration_%s"%args.config
        config =  __import__(configName)

        #moduleName = "channelConfig_%s"%args.chan
        #module =  __import__(moduleName)
        module = getChannelConfig(args.chan)

        from createInputs import createSingleBinCI
        from tools import getCardDir
        cardDir = getCardDir(args,config)       
        if not os.path.exists(cardDir):
                os.makedirs(cardDir)

        if args.BSLL:
                lambdas = config.lambdasBSLL
                interferences = config.interferencesBSLL
        else:
                lambdas = config.lambdasBBLL
                interferences = config.interferencesBBLL
        #lambdas = config.lambdas

        nPoints = len(lambdas)*len(interferences)


        index = 0
        print("lambdas: {0}".format(lambdas))

        for Lambda in lambdas:
                for interference in interferences:
                        name = "%s/%s_%d_%s" % (cardDir,args.chan, Lambda, interference)
                        if args.inject or "toy" in tag: 
                                yields = createSingleBinCI(Lambda,interference, name,args.chan,args.config, args.mass ,dataFile=injectedFile)
                        else:   
                                yields = createSingleBinCI(Lambda,interference, name,args.chan,args.config, args.mass)
                        backgrounds = config.backgrounds

                        nBkg = len(backgrounds) 
        
                                                

                        channelDict = {}

                        channelDict["date"] = time.strftime("%d/%m/%Y")
                        channelDict["time"] = time.strftime("%H:%M:%S")
                        #channelDict["hash"] = get_git_revision_hash()  

                        channelDict["bin"] = args.chan

                        channelDict["nBkgs"] = nBkg
                        scale = False
                        res = False
                        ID = False
                        PDF = False

        
                        channelDict["data"] = yields["data"]
                
                        channelDict["channels"] = getChannelBlock(backgrounds,yields,1,args.chan)               
                        #print(channelDict["channels"]) 
                        uncertBlock = ""
                        #uncerts = module.provideUncertaintiesCI(Lambda)
                        for uncert in config.systematics:
                                #uncertBlock += getUncert(uncert,uncerts[uncert],backgrounds,Lambda,args.chan,config.correlate,yields,args.signif)
                                uncertBlock += getUncert(uncert,module.uncertainties[uncert]["values"],backgrounds,Lambda,args.chan,config.correlate,yields,args.signif)
                        channelDict["systs"] = uncertBlock

                        writeCard(cardTemplate % channelDict, name)
                        printProgress(index+1, nPoints, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
                        index += 1      
main()
