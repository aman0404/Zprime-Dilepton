import argparse
import subprocess
import time
import os
import sys
sys.path.append('cfgs/')
sys.path.append('input/')

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
##Data card for Zprime -> ll analysis, created on %(date)s at %(time)s
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
'''


def getChannelBlock(nBkgs,bkgYields,signalScale,chan):

	result = "bin %s"%chan
	for i in range(0,nBkgs):
		result += " %s "%chan
	result+="\n"
	result += "process      sig"
	if nBkgs == 1:
		result+= "  bkg  "
	else:
		for i in range(0,nBkgs):
			result+= "  bkg_%d  "%i
	result +="\n"
	result +="process       0 "
	for i in range(0,nBkgs):
		result+=" %d"%(i+1)
	result +="\n"
	result += "rate         %.2f "%signalScale
	#result += "rate         1 "
	for i in range (0, nBkgs):
		result+= " %.2f"%bkgYields[i]
	return result
 


def getUncert(uncert, value, nBkgs, mass,channel,correlate,binned,bkgYields,signif):
	if uncert == "reco":
		if correlate:
			name = "reco_unc"
		else:
			name = "reco_unc_%s"%channel
		
	        if len(value) == 1:
	                result = "%s  lnN  %.4f"%(name,value[0])
	        else:
	                result = "%s  lnN  %.5f/%.4f"%(name, value[0], value[1] )

		for i in range(0,nBkgs):
	                result += "  -  "

	if uncert == "sigEff":
		if correlate:
			name = "sig_effUnc"
		else:
			name = "sig_effUnc_%s"%channel
	        if len(value) == 1:
	                result = "%s  lnN  %.4f"%(name,value[0])
	        else:
	                result = "%s  lnN  %.5f/%.4f"%(name, value[0], value[1] )

		for i in range(0,nBkgs):
	                result += "  -  "

	if uncert == "bkgUncert":
		#if value != 0:
		#	print "non-standard background uncertainties not supported yet"
		if correlate:
			name = "bkg_unc"
		else:
			name = "bkg_unc_%s"%channel
		result = "%s lnN   -  "%(name)  
		for i in range(0, nBkgs):
			#value = 0.8
			if not signif:

				result += " %.4f"%(1.+3*bkgYields[i]**0.5/bkgYields[i])
				#result += "  %.2f  "%(value)
			#result += "  %.2f  "%(1.4)
			else:
				result += " %.4f"%(1.+3*bkgYields[i]**0.5/bkgYields[i])
				#result += "  %.2f  "%(value)
	if uncert == "massScale":
		if binned:
			if correlate:
				name = "scale"
			else:
				name = "scale_%s"%channel
			result = "%s shape 1"%name
	                for i in range(0,nBkgs):
        	                result += "  -  "
			
	
		else:
			if correlate:
				name = "beta_peak"
			else:
				name = "beta_peak_%s"%channel
			if 'dimuon_2017' in channel or 'dimuon_2018' in channel or 'dimuon_Legacy2017' in channel or 'dimuon_Legacy2018' in channel:
				result = "%s param 0 -0.01/+1" %name
			else:
				result = "%s param 0 1" %name
	if uncert == "res":
		if binned:
			print 'you were to lazy to implment this uncertainty for binned yet. Do that and come back'
			sys.exit()	
	
		else:
			if correlate:
				name = "beta_res"
			else:
				name = "beta_res_%s"%channel
			result = "%s param 0 1" %name
	if uncert == "bkgParams":
		if binned:
			print 'you were to lazy to implment this uncertainty for binned yet. Do that and come back'
			sys.exit()	
	
		else:
			result = ""
			for label in value:

				name = "beta_%s_%s"%(label,channel)
				result += "%s param 0 1\n" %name
	
	result += "\n"		
        return result
		
	


def writeCard(card,fileName):

	text_file = open("%s.txt" % (fileName), "w")
	text_file.write(card)
	text_file.close()
	

def getDataset(binned,fileName, chan):

	if binned:
		return "shapes data_obs %s %s data_%s" % (chan, fileName, chan )
	else:
		return "shapes data_obs %s %s %s:data_%s" % (chan, fileName, chan, chan)	

def getSignalShape(binned,fileName,chan,scale):
	
	if binned:
		result =  "shapes sig %s %s sigHist_%s" % (chan, fileName, chan)
		if scale:
			#result += " sigHist_%s_scaleUp"%chan
			#result += " sigHist_%s_scaleDown"%chan
			result += " sigHist_%s_$SYSTEMATIC"%chan  
		return result
	else:
		return  "shapes sig %s %s %s:sig_pdf_%s" % (chan, fileName, chan, chan)

def getBackgroundShapes(binned,fileName,chan,nBkg=0):

	if binned:
		if nBkg == 0:
			return "shapes bkg %s %s bkgHist_%s" % (chan, fileName, chan)
		else:
			return "shapes bkg %s %s bkgHist_%s_%d" % (chan, fileName, chan, nBkg)
	else:
		if nBkg == 0:
			return "shapes bkg %s %s %s:bkgpdf_%s" % (chan, fileName, chan, chan)
		else:
			return "shapes bkg %s %s %s:bkgpdf_%s_%d" % (chan, fileName, chan, chan, nBkg)
def main():

	parser = argparse.ArgumentParser(description='Data writer for Zprime -> ll analysis interpretation in combine')
	parser.add_argument("-b", "--binned", action="store_true", default=False, help="use binned dataset")
	parser.add_argument("--expected", action="store_true", default=False, help="write datacards for expected limit mass binning")
	parser.add_argument("-i", "--inject", action="store_true", default=False, help="inject signal")
	parser.add_argument("--recreateToys", action="store_true", default=False, help="recreate toy dataset")
	parser.add_argument("-c", "--chan", dest = "chan", default="", help="name of the channel to use")
	parser.add_argument("-o", "--options", dest = "config", default="", help="name of config file")
	parser.add_argument("-m", "--mass", dest = "mass", default=-1,type=int, help="mass point")
	parser.add_argument("-t", "--tag", dest = "tag", default="", help="tag")
	parser.add_argument("-s", "--signif", action="store_true", default=False, help="write card for significances")
        parser.add_argument( "--workDir", dest = "workDir", default = "", help="tells batch jobs where to put the datacards. Not for human use!")
	parser.add_argument("--spin2", action="store_true", default=False, help="use spin2 efficiencies")
	parser.add_argument("--toysOnly", action="store_true", default=False, help="prepare LEE toys")
	#parser.add_argument("--prepare", action="store_true", default=False, help="prepare LEE toys")
				
	args = parser.parse_args()	
	tag = args.tag
	if not args.tag == "":
		tag = "_" + args.tag

        import glob
	from ROOT import gROOT
        for f in glob.glob("userfuncs/*.cxx"):
                gROOT.ProcessLine(".L "+f+"+")


	configName = "scanConfiguration_%s"%args.config
	config =  __import__(configName)

	moduleName = "channelConfig_%s"%args.chan
	module =  __import__(moduleName)

	from createInputs import createWS, createHistograms, createSignalDataset
	from tools import getCardDir
	cardDir = getCardDir(args,config)	
	if "toy" in tag:
		injectedFile = "input/%s%s.txt"%(args.chan,tag)
		if not os.path.isfile(injectedFile):
			print "dataset file %s does not yet exist. Will generate a dataset to use"%injectedFile
			name = "input/%s"%(args.chan)
			createSignalDataset(config.signalInjection["mass"],name,args.chan,config.signalInjection["width"],0,config.signalInjection["CB"],1,tag=tag)
	elif args.inject:
		if config.signalInjection["CB"]:
			injectedFile = "input/%s_%d_%.3f_%d_scale%d_CB.txt"%(args.chan,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"],config.signalInjection["scale"])
		else:	
			injectedFile = "input/%s_%d_%.3f_%d_scale%d.txt"%(args.chan,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"],config.signalInjection["scale"])
		if not os.path.isfile(injectedFile) or args.recreateToys:
			print "dataset file %s does not yet exist or you asked for it to be recreated. Will generate a dataset to use"%injectedFile
			name = "input/%s"%(args.chan)
			createSignalDataset(config.signalInjection["mass"],name,args.chan,config.signalInjection["width"],config.signalInjection["nEvents"],config.signalInjection["CB"],config.signalInjection["scale"])
	if args.toysOnly:
		exit()

	if not os.path.exists(cardDir):
    		os.makedirs(cardDir)
	if args.mass > 0:
		masses = [[5,args.mass,args.mass]]
	else:
		masses = config.masses
		if args.expected:
			masses = config.massesExp	
	nMasses = 0
	for massRange in masses:
		mass = massRange[1]
		while mass <= massRange[2]:
			nMasses +=1
			mass += massRange[0]
	i = 1
	useShapeUncert = False
	if "bkgParams" in config.systematics:
		useShapeUncert = True
	for massRange in masses:
		mass = massRange[1]
		while mass <= massRange[2]:
			if args.binned:
				name = "%s/%s_%d_binned" % (cardDir,args.chan, mass)
				if args.inject or "toy" in tag:
					bkgYields = [createHistograms(mass,100, name,args.chan,config.width,config.correlate,config.binWidth,dataFile=injectedFile,CB=config.CB)]
				else:	
					bkgYields = [createHistograms(mass,100, name,args.chan,config.width,config.correlate,config.binWidth,CB=config.CB)]
			else:
				name = "%s/%s_%d" % (cardDir,args.chan, mass)
				if args.inject or "toy" in tag:	
					bkgYields = [createWS(mass,100, name,args.chan,config.width,config.correlate,dataFile=injectedFile,CB=config.CB,useShapeUncert=useShapeUncert)]
				else:	
					bkgYields = [createWS(mass,100, name,args.chan,config.width,config.correlate,CB=config.CB,useShapeUncert=useShapeUncert)]
			scale=1
			if args.inject:
				scale = scale*config.signalInjection["scale"]	
			signalScale = module.provideSignalScaling(mass,spin2=args.spin2)*1e-7*scale
			nBkg = 1 # only one source of background supported at the moment

						

			channelDict = {}

			channelDict["date"] = time.strftime("%d/%m/%Y")
			channelDict["time"] = time.strftime("%H:%M:%S")
			#channelDict["hash"] = get_git_revision_hash()	
	
			channelDict["bin"] = args.chan

			channelDict["nBkgs"] = nBkg
			if nBkg == 1:
				channelDict["bkgShapes"] = getBackgroundShapes(args.binned,"%s.root"%name,args.chan,0)
			else:
				channelDict["bkgShapes"] = ""
				for i in range(1,nBkg+1):
                			channelDict["bkgShapes"] += getBackgroundShapes(args.binned,"%s.root"%nam,eargs.chan,i)
					if i < nBkg:
						channelDict["bkgShapes"] += "\n"
			scale = False
			if "massScale" in config.systematics:
				scale = True

	
			channelDict["sigShape"] = getSignalShape(args.binned,"%s.root"%name,args.chan,scale)
			channelDict["data"] = getDataset(args.binned,"%s.root"%name,args.chan)
			
			channelDict["channels"]	= getChannelBlock(nBkg,bkgYields,signalScale,args.chan)		

			uncertBlock = ""
			uncerts = module.provideUncertainties(mass)
			correlations = module.provideCorrelations()
			for uncert in config.systematics:
				uncertBlock += getUncert(uncert,uncerts[uncert],nBkg,mass,correlations[uncert],config.correlate,args.binned,bkgYields,args.signif)
			
			channelDict["systs"] = uncertBlock

			writeCard(cardTemplate % channelDict, name)
			printProgress(i, nMasses, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
			i += 1
			mass += massRange[0]
main()
