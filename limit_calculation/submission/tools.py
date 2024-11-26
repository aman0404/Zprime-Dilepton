def getCardDir(args,config):

	if args.inject:
		if "." in args.tag:
			cardDir = "dataCards_" + args.config + args.tag
		else:	
			cardDir = "dataCards_" + args.config + "_%d_%.4f_%d"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + args.tag
	else:
		cardDir = "dataCards_" + args.config +  args.tag
	if hasattr(args,'binned'):	
		if args.binned:
			cardDir = cardDir + "_binned"

	if not args.workDir == "":
		cardDir = args.workDir + "/" + cardDir
	return cardDir
def getOutDir(args,config):

	if args.inject:
		outDir = "results_" + args.config + "_%d_%.4f_%d"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + args.tag
	else:
		outDir = "results_" + args.config +  args.tag
	if args.binned:
		outDir = outDir + "_binned"

	return outDir

def getMassRange(massVal,minNrEv,effWidth,dataFile,lowestMass):
	with open(dataFile) as f:
		masses = f.readlines()
	massDiffs = []
	for evMass in masses:
		massDiffs.append(abs(float(evMass)-massVal)) 
	massDiffs = sorted(massDiffs)
	
	if minNrEv <= len(massDiffs):
		massDiff = massDiffs[minNrEv]
		massLow = massVal - massDiff
		massHigh = massVal + massDiff
	else:
		massLow = lowestMass
		massHigh = 6000
	nSigma = 4  # 6
	if (massVal-nSigma*effWidth*massVal) < massLow:
		massLow = massVal - nSigma*effWidth*massVal
	if (massVal+nSigma*effWidth*massVal) > massHigh:
		massHigh = massVal + nSigma*effWidth*massVal
	massLow= max(massLow,lowestMass)
	return massLow, massHigh


def getBkgEstInWindow(ws,massLow,massHigh,nBkgTotal):
	import ROOT
	ws.var("massFullRange").setRange("window",massLow,massHigh)
	#ws.var("massFullRange").setRange("window",120,400)
	argSet = ROOT.RooArgSet(ws.var("massFullRange"))
	integral = ws.pdf("bkgpdf_fullRange").createIntegral(argSet,ROOT.RooFit.NormSet(argSet), ROOT.RooFit.Range("window"))
	return nBkgTotal*integral.getVal()



def createGridPack():

	import subprocess
	args = ['tar', '-cvf', 'gridPack.tar','cfgs/',"input/",'writeDataCards.py','runInterpretation.py','createInputs.py']
	subprocess.call(args)

def findLowerLimit(hist,CL): 

	bins = hist.GetNbinsX()

	best_i = 1
	best_j = 1
	bd = bins+1
	val = 0;

	integral = 0 
	for i in range(1,bins+1): 
		integral += hist.GetBinContent(bins+2-i)
		if integral > CL :
      			val = integral
 
      			if integral > CL and  i  < bd : 
          			bd = i 
          			best_i = bins+2-i
          			val = integral
      			break

	return hist.GetBinLowEdge(best_i)

def convertToLowerLimit(fileName,upper,rName,average=True):
	from ROOT import TFile, TH1F	
	fi_MCMC = TFile.Open(fileName)
	CL = 0.95
	rmin = 0 
	rmax = upper 
	nbins = 500

	# Sum up all of the chains / or could take the average limit
	mychain= []
	for k in fi_MCMC.Get("toys").GetListOfKeys():
        	mychain.append(k.ReadObj().GetAsDataSet())

	# Easier to fill a histogram why not ?

	limits = []
	for j in range(0,len(mychain)):
		hist = TH1F("h_post",";r;posterior probability",nbins,rmin,rmax)
		for i in range(mychain[j].numEntries()): 
  			mychain[j].get(i)
  			hist.Fill(mychain[j].get(i).getRealValue(rName), mychain[j].weight())

		hist.Scale(1./hist.Integral())

		limits.append(findLowerLimit(hist,CL))

	if average:
		return [sum(limits)/float(len(limits))]

	else:
		return limits
