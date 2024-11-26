import argparse
import subprocess
import time
import os
import sys

sys.path.append('cfgs/')
sys.path.append('input/')



from channelConfiguration import getChannelConfig

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
jmax %(nBkgs)d  number of backgrounds
kmax *  number of nuisance parameters (sources of systematical uncertainties)
------------
#for background shapes
%(bkgShapes)s
#for signal shape
%(sigShape)s
#for data
%(data)s
------------
# we have just one channel, in which we observe 0 events
bin %(bin)s
observation -1.
------------
# now we list the expected events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error)
# on each process and bin
%(channels)s  
------------
%(systs)s

* autoMCStats 0  0  1
'''

#* autoMCStats 0  0  1


def getChannelBlock(backgrounds,yields,signalScale,chan):

    result = "bin %s"%chan
    for i in range(0,len(backgrounds)):
        result += " %s "%chan
    result+="\n"
    result += "process      sig"
    for background in backgrounds:
        result+= "  %s  "%background
    result +="\n"
    result +="process       0 "
    for i in range(0,len(backgrounds)):
        result+=" %d"%(i+1)
    result +="\n"
    result += "rate         %.4f "%yields[-1]
    #result += "rate         1 "
    for i in range (0, len(backgrounds)):
        result+= " %.4f"%yields[i]
        #result+= " %.2f"%yields[i]
    return result
 

# # what uncertainties are correlated? 0 for none at all, 1 for within channels, 2 accross channels
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
# "PU":2,
# "JEC": 2,
# "JER": 2
# }

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

    if "btagSF" in uncert:
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  1  "
        result += "\n"


#    if "btagSF" in uncert:
#        print("name,value: {0}".format((name,value)))
#        result = "%s lnN %.3f"%(name,value)
#        for background in backgrounds:
#            result += "  %.3f  "%(value)
#        result += "\n"	


    # if uncert == "xSecOther":
    #     result = "%s lnN - "%name
    #     for background in backgrounds:
    #         if background == "Other":
    #             result += "  %.3f  "%value
    #         else:
    #             result += " - "
    #     result += "\n"		

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
            result = "%s lnN %.3f"%(name,value)
            for background in backgrounds:
                if background == "Jets":
                       result += "  -  "
                elif background == "DY":
                       result += "  1.10  "
                else:
                       result += "  %.3f"%value
            result += "\n"
               		


#    if uncert == "zPeak":
#        result = "%s lnN %.3f"%(name,value)
#        for background in backgrounds:
#            if background == "Jets":
#                    result += "  -  "
#            else:
#                    result += "  %.3f"%value
#        result += "\n"		

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
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                    result += "  -  "
            else:
                    result += "  1  "
    
        result += "\n"		

    if uncert == "energyScale" and not "muon" in channel: 
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                    result += "  -  "
            else:
                    result += "  1  "
    
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
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "
            else:
                result += "  1  "
    
        result += "\n"		


    #if uncert == "res" : #and not "electron" in channel
    if uncert == "res" and not "electron" in channel:
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "
            else:
                result += "  1  "
    
        result += "\n"		
    # if uncert == "PU" and not "muon" in channel:
    if uncert == "PU":
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "	
            else:
                result += "  1  "	
        result += "\n"		

    if uncert == "pdf":
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  1  "
        result += "\n"		

    if uncert == "ttbarUncert":
        result = "%s shape - "%name
        if "ZeroB" in channel:
            for background in backgrounds:
                result += "  - "
        else:
            for background in backgrounds:
                if background == "Top":
                   result += "  1  "
                else:
                   result += "  -  "
        result += "\n"




    if uncert == "ID": # and not "electron" in channel
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "	
            else:
                result += "  1  "	
        result += "\n"		

    #if uncert == "ISO": # and not "electron" in channel
    if uncert == "ISO" and not "electron" in channel:
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "	
            else:
                result += "  1  "	
        result += "\n"		

    #if uncert == "HLT": # and not "electron" in channel
    if uncert == "HLT" and not "electron" in channel:
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                result += "  -  "	
            else:
                result += "  1  "	
        result += "\n"		


    if uncert == "lumi":
        result = "%s lnN %.3f"%(name,value)
        for background in backgrounds:
            result += "  -  "
        result += "\n"		

    if uncert == "l1prefiring":
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  1  " 
        result += "\n"


    if uncert == "JEC":
        result = "%s lnN %.3f"%(name,value)
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  %.3f  "%(value)
        result += "\n"	

    if uncert == "JER":
        result = "%s lnN %.3f"%(name,value)
        for background in backgrounds:
            if background == "Jets":
                 result += "  -  "
            else:
                 result += "  %.3f  "%(value)
        result += "\n"	

    if uncert == "reco" and not "electron" in channel:
        result = "%s shape 1"%name
        for background in backgrounds:
            if background == "Jets":
                    result += "  -  "
            else:
                    result += "  1  "
        result += "\n"
    
    # if uncert == "btag":
    #     result = "%s shape 1"%name
    #     for background in backgrounds:
    #         if background == "Jets":
    #                 result += "  -  "
    #         else:
    #                 result += "  1  "
    #     result += "\n"


    # print "getUncert uncert: {0}".format(uncert)
    # print "getUncert value: {0}".format(value)
    # print "getUncert backgrounds: {0}".format(backgrounds)
    # print "getUncert mass: {0}".format(mass)
    # print "getUncert channel: {0}".format(channel)
    # print "getUncert correlate: {0}".format(correlate)
    # print "getUncert yields: {0}".format(yields)
    # print "getUncert signif: {0}".format(signif)
    # print "getUncert result: {0}".format(result)
    return result
        
    


def writeCard(card,fileName):

    text_file = open("%s.txt" % (fileName), "w")
    text_file.write(card)
    text_file.close()
    

def getDataset(fileName, chan):
    print("getDataset test")
    return "shapes data_obs %s %s dataHist_%s" % (chan, fileName, chan )

def getSignalShape(fileName,chan,shape):
    
    result =  "shapes sig %s %s sigHist_%s" % (chan, fileName, chan)
    if shape:
        result += " sigHist_$SYSTEMATIC"  
    return result

def getBackgroundShapes(fileName,chan,name, shape):
    result =  "shapes %s %s %s bkgHist%s_%s" % (name, chan, fileName, name, chan)
    if shape:
        result += " bkgHist%s_$SYSTEMATIC"%name

    result += "\n"
    return result

def main():

    parser = argparse.ArgumentParser(description='Data writer for Zprime -> ll analysis interpretation in combine')
    parser.add_argument("--expected", action="store_true", default=False, help="write datacards for expected limit mass binning")
    parser.add_argument("-i", "--inject", action="store_true", default=False, help="inject signal")
    parser.add_argument("-c", "--chan", dest = "chan", default="", help="name of the channel to use")
    parser.add_argument("-o", "--options", dest = "config", default="", help="name of config file")
    parser.add_argument("-t", "--tag", dest = "tag", default="", help="tag")
    parser.add_argument("-s", "--signif", action="store_true", default=False, help="write card for significances")
    parser.add_argument( "--workDir", dest = "workDir", default = "", help="tells batch jobs where to put the datacards. Not for human use!")
    parser.add_argument("--BSLL", dest="BSLL",default=False,action="store_true",help="use BSLL signal (default is BBLL)")
            
    args = parser.parse_args()	
    tag = args.tag
    if not args.tag == "":
        tag = "_" + args.tag

    configName = "scanConfiguration_%s"%args.config
    config =  __import__(configName)

    # print("module args.chan: {0}".format(args.chan))
    module = getChannelConfig(args.chan)

    from createInputs import createHistogramsCI
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



    nPoints = len(lambdas)*len(interferences)
    

    index = 0
    print("lambdas: {0}".format(lambdas))
    for Lambda in lambdas:
        for interference in interferences:

            name = "%s/%s_%d_%s" % (cardDir,args.chan, Lambda, interference)

            yields = createHistogramsCI(Lambda,interference, name,args.chan,args.config, bbll=(not args.BSLL))
            
            backgrounds = config.backgrounds

            nBkg = len(backgrounds) 
                                    
            shape = False
            if "massScale" in config.systematics:
                shape = True
            if "res" in config.systematics:
                shape = True
            if "pdf" in config.systematics:
                shape = True

            channelDict = {}

            channelDict["date"] = time.strftime("%d/%m/%Y")
            channelDict["time"] = time.strftime("%H:%M:%S")
            #channelDict["hash"] = get_git_revision_hash()	

            channelDict["bin"] = args.chan

            channelDict["nBkgs"] = nBkg
            channelDict["bkgShapes"] = ''
            for background in backgrounds:
                channelDict["bkgShapes"] += getBackgroundShapes("%s.root"%name,args.chan,background,shape)
            
        
    
            channelDict["sigShape"] = getSignalShape("%s.root"%name,args.chan,shape)
            channelDict["data"] = getDataset("%s.root"%name,args.chan)
        
            channelDict["channels"]	= getChannelBlock(backgrounds,yields,1,args.chan)		

            uncertBlock = ""
            #uncerts = module.provideUncertaintiesCI(Lambda)
            for uncert in config.systematics:
                # print("module.uncertainties: {0}".format(module.uncertainties))
                # print("args.chan: {0}".format(args.chan))
                uncertBlock += getUncert(uncert,module.uncertainties[uncert]["values"],backgrounds,Lambda,args.chan,config.correlate,yields,args.signif)
        
            channelDict["systs"] = uncertBlock
            print("channelDict: {0}".format(channelDict))

            writeCard(cardTemplate % channelDict, name)
            printProgress(index+1, nPoints, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
            index += 1	
main()
