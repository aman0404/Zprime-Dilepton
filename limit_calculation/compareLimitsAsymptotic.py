#/usr/bin/env python
import os
import sys
sys.path.append('cfgs/')
from copy import deepcopy
import numpy
import math
import ROOT
from ROOT import TCanvas,TGraphAsymmErrors,TFile,TH1D,TH1F,TGraph,TGraphErrors,gStyle,TLegend,TLine,TGraphSmooth,TPaveText,TGraphAsymmErrors,TPaveLabel,gROOT, kRed, kBlue

ROOT.gROOT.SetBatch(True)

colors = {"ssm":ROOT.kGreen+3,"psi":ROOT.kBlue,"N":ROOT.kRed+2,"S":ROOT.kOrange,"I":ROOT.kMagenta+3,"kai":ROOT.kGreen+3,"eta":ROOT.kBlack,"RS_kMpl01":ROOT.kOrange+3,"RS_kMpl005":ROOT.kRed,"RS_kMpl001":ROOT.kViolet,"RS_kMpl0001":ROOT.kRed}
#labels = {"ssm":"Z'_{SSM}","psi":"Z'_{#psi}","S":"Z'_{S}","I":"Z'_{I}","N":"Z'_{N}","eta":"Z'_{#eta}","kai":"Z'_{#chi}","RS_kMpl01":"G_{KK} k/#bar{M}_{pl} = 0.1 (LO x 1.6)" ,"RS_kMpl005":"G_{KK} k/#bar{M}_{pl} = 0.05 (LO x 1.6)" ,"RS_kMpl001":"G_{KK} k/#bar{M}_{pl} = 0.01 (LO x 1.6)" ,"RS_kMpl0001":"G_{KK} k/#bar{M}_{pl} = 0.001 (LO x 1.6)" }
labels = {"ssm":"Z'_{SSM}","psi":"Z'_{#psi}","S":"Z'_{S}","I":"Z'_{I}","N":"Z'_{N}","eta":"Z'_{#eta}","kai":"Z'_{#chi}","RS_kMpl01":"k/#bar{M}_{pl} = 0.1" ,"RS_kMpl005":"k/#bar{M}_{pl} = 0.05" ,"RS_kMpl001":"k/#bar{M}_{pl} = 0.01" ,"RS_kMpl0001":"k/#bar{M}_{pl} = 0.001" }
kFacs  = {"ssm":1.0,"psi":1.0,"eta":1.0,"S":1.0,"N":1.0,"I":1.0,"kai":1.0,"RS_kMpl01":1.6,"RS_kMpl005":1.6,"RS_kMpl001":1.6,"RS_kMpl0001":1.6}

def getMassDependentKFactor(mass):
	if mass <= 1500:
		return 1.41
	else:
		return 1.35482 + 0.000121208*mass  - 6.25306e-08*mass*mass + 4.37854e-12*mass**3


def getAlphaSFactor(mass):
	#if mass <= 1500:
	#	return 1.41
	#else:
	#	return 1.35482 + 0.000121208*mass  - 6.25306e-08*mass*mass + 4.37854e-12*mass**3
	return 0.936557 + 4.45269e-05 * mass

def printPlots(canvas,name):
    	canvas.Print('plots/'+name+".png","png")
    	canvas.Print('plots/'+name+".pdf","pdf")
    	canvas.SaveSource('plots/'+name+".C","cxx")
    	canvas.Print('plots/'+name+".root","root")
    	canvas.Print('plots/'+name+".eps","eps")


def getXSecCurve(name,kFac,massDependent=False):
   	smoother=TGraphSmooth("normal")
    	X=[]
    	Y=[]
    	file=open('tools/xsec_%s.txt'%name,'r')
    	for entries in file:
        	entry=entries.split()
        	X.append(float(entry[0]))
		if not SPIN2:
			kFac = getAlphaSFactor(float(entry[0]))
			if massDependent:
				kFac = kFac*getMassDependentKFactor(float(entry[0]))
        	Y.append(float(entry[1])*kFac/1928)
   	aX=numpy.array(X)
	aY=numpy.array(Y)
    	Graph=TGraph(len(X),aX,aY)
    	GraphSmooth=smoother.SmoothSuper(Graph,"linear")
	if name == "ssm":
   		GraphSmooth.SetLineStyle(ROOT.kDashed)
   	GraphSmooth.SetLineWidth(3)
	if GUT:
		GraphSmooth.SetLineWidth(2)
    	GraphSmooth.SetLineColor(colors[name])
	
	if SPIN2:
    		Graph.SetLineColor(colors[name])
   		Graph.SetLineWidth(3)
		return deepcopy(Graph)
	else:
		if massDependent:
			GraphSmooth.SetLineStyle(ROOT.kDashed)	
		return deepcopy(GraphSmooth)



def makeLimitPlot(output,exp,chan,printStats=False,obs2="",ratioLabel=""):
	#fileForHEPData = TFile("plots/"+output+"_forHEPData.root","RECREATE")
    	file1=open('cards/ZPrime_limitCard_DimuonRun2_Asymptotic_defaultFix.txt','r')
    	file2=open('cards/ZPrime_limitCard_DimuonRun2_Asymptotic_floatTest1Param2.txt','r')
    	file3=open('cards/ZPrime_limitCard_DimuonRun2_Asymptotic_floatTest1ParamE2.txt','r')

    	observedx=[]
    	observedy=[]

    	expectedy=[]
    	expected1SigLow=[]
   	expected1SigHigh=[]
    	expected2SigLow=[]
    	expected2SigHigh=[]


    	for entry in file1:
        	observedx.append(float(entry.split()[0]))
        	observedy.append(float(entry.split()[6]))
        	expectedy.append(float(entry.split()[3]))
        	expected2SigLow.append(float(entry.split()[1]))
        	expected1SigLow.append(float(entry.split()[2]))
         	expected2SigHigh.append(float(entry.split()[5]))
        	expected1SigHigh.append(float(entry.split()[4]))
       
    	expX=numpy.array(observedx)
    	expY=numpy.array(expectedy)

	values = []	
	values2 = []	

	print values
        xPointsForValues = []
	for i in range(0,len(observedx)):
		values.append(expected1SigLow[i])
		values2.append(expected2SigLow[i])
		
        	xPointsForValues.append(observedx[i])
	for i in range(0,len(observedx)):
		values.append(expected1SigHigh[len(observedx)-i-1])
		values2.append(expected2SigHigh[len(observedx)-i-1])

        	xPointsForValues.append(observedx[len(observedx)-i-1])
    	exp2Sig=numpy.array(values2)
    	exp1Sig=numpy.array(values)
	xPointsForValues = numpy.array(xPointsForValues)
    	
	GraphErr2Sig=TGraphAsymmErrors(len(xPointsForValues),xPointsForValues,exp2Sig)
    	GraphErr2Sig.SetFillColor(ROOT.kOrange)
    	GraphErr1Sig=TGraphAsymmErrors(len(xPointsForValues),xPointsForValues,exp1Sig)
    	GraphErr1Sig.SetFillColor(ROOT.kGreen+1)


    	observedx2=[]
    	observedy2=[]

    	expectedy2=[]
    	expected1SigLow2=[]
   	expected1SigHigh2=[]
    	expected2SigLow2=[]
    	expected2SigHigh2=[]


    	for entry in file2:
        	observedx2.append(float(entry.split()[0]))
        	observedy2.append(float(entry.split()[6]))
        	expectedy2.append(float(entry.split()[3]))
        	expected2SigLow2.append(float(entry.split()[1]))
        	expected1SigLow2.append(float(entry.split()[2]))
         	expected2SigHigh2.append(float(entry.split()[5]))
        	expected1SigHigh2.append(float(entry.split()[4]))
       
    	expX2=numpy.array(observedx2)
    	expY2=numpy.array(expectedy2)

	values2 = []	
	values22 = []	

	print values
        xPointsForValues2 = []
	for i in range(0,len(observedx2)):
		values2.append(expected1SigLow2[i])
		values22.append(expected2SigLow2[i])
		
        	xPointsForValues2.append(observedx2[i])
	for i in range(0,len(observedx2)):
		values2.append(expected1SigHigh2[len(observedx2)-i-1])
		values22.append(expected2SigHigh2[len(observedx2)-i-1])

        	xPointsForValues2.append(observedx2[len(observedx2)-i-1])
    	exp2Sig2=numpy.array(values22)
    	exp1Sig2=numpy.array(values2)
	xPointsForValues2 = numpy.array(xPointsForValues2)
    	
	GraphErr2Sig2=TGraphAsymmErrors(len(xPointsForValues2),xPointsForValues2,exp2Sig2)
    	GraphErr2Sig2.SetFillColor(ROOT.kOrange)
    	GraphErr1Sig2=TGraphAsymmErrors(len(xPointsForValues2),xPointsForValues2,exp1Sig2)
    	GraphErr1Sig2.SetFillColor(ROOT.kGreen+1)

    	observedx3=[]
    	observedy3=[]

    	expectedy3=[]
    	expected1SigLow3=[]
   	expected1SigHigh3=[]
    	expected2SigLow3=[]
    	expected2SigHigh3=[]


    	for entry in file3:
        	observedx3.append(float(entry.split()[0]))
        	observedy3.append(float(entry.split()[6]))
        	expectedy3.append(float(entry.split()[3]))
        	expected2SigLow3.append(float(entry.split()[1]))
        	expected1SigLow3.append(float(entry.split()[2]))
         	expected2SigHigh3.append(float(entry.split()[5]))
        	expected1SigHigh3.append(float(entry.split()[4]))
       
    	expX3=numpy.array(observedx3)
    	expY3=numpy.array(expectedy3)

	values3 = []	
	values23 = []	

	print values
        xPointsForValues3 = []
	for i in range(0,len(observedx3)):
		values3.append(expected1SigLow3[i])
		values23.append(expected2SigLow3[i])
		
        	xPointsForValues3.append(observedx3[i])
	for i in range(0,len(observedx3)):
		values3.append(expected1SigHigh3[len(observedx3)-i-1])
		values23.append(expected2SigHigh3[len(observedx3)-i-1])

        	xPointsForValues3.append(observedx[len(observedx3)-i-1])
    	exp2Sig3=numpy.array(values23)
    	exp1Sig3=numpy.array(values3)
	xPointsForValues3 = numpy.array(xPointsForValues3)
    	
	GraphErr2Sig3=TGraphAsymmErrors(len(xPointsForValues3),xPointsForValues3,exp2Sig3)
    	GraphErr2Sig3.SetFillColor(ROOT.kOrange)
    	GraphErr1Sig3=TGraphAsymmErrors(len(xPointsForValues3),xPointsForValues3,exp1Sig3)
    	GraphErr1Sig3.SetFillColor(ROOT.kGreen+1)
    	#cCL=TCanvas("cCL", "cCL",0,0,567,384)
    	cCL=TCanvas("cCL", "cCL",0,0,600,450)
    	gStyle.SetOptStat(0)
	gStyle.SetPadRightMargin(0.063)
	gStyle.SetPadLeftMargin(0.14)
	gStyle.SetPadBottomMargin(0.12)
	
	#if not obs2 == "":
    	plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
    	ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
    	plotPad.Draw()	
    	ratioPad.Draw()	
	plotPad.cd()
	#else:
    	#	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
    	#	plotPad.Draw()	
    	#	plotPad.cd()

    	expX=numpy.array(observedx)
    	expY=numpy.array(expectedy)
    	GraphExp=TGraph(len(expX),expX,expY)
    	GraphExp.SetLineWidth(3)
    	GraphExp.SetLineStyle(2)
    	#GraphExp.SetLineColor(ROOT.kBlue)

    	obsX=numpy.array(observedx)
    	obsY=numpy.array(observedy)
    	if printStats: print "obsX: ",obsX
    	if printStats: print "obsY: ",obsY

    	if SMOOTH:
        	smooth_obs=TGraphSmooth("normal")
        	GraphObs_nonSmooth=TGraph(len(obsX),obsX,obsY)
        	GraphObs=smooth_obs.SmoothSuper(GraphObs_nonSmooth,"linear",0,0.005)
    	else:
        	GraphObs=TGraph(len(obsX),obsX,obsY)
    
    	GraphObs.SetLineWidth(3)

     	expX2=numpy.array(observedx2)
    	expY2=numpy.array(expectedy2)
    	GraphExp2=TGraph(len(expX2),expX2,expY2)
    	GraphExp2.SetLineWidth(3)
    	GraphExp2.SetLineStyle(2)
    	GraphExp2.SetLineColor(ROOT.kBlue)

    	obsX2=numpy.array(observedx2)
    	obsY2=numpy.array(observedy2)

    	if SMOOTH:
        	smooth_obs2=TGraphSmooth("normal")
        	GraphObs_nonSmooth2=TGraph(len(obsX2),obsX2,obsY2)
        	GraphObs2=smooth_obs2.SmoothSuper(GraphObs_nonSmooth2,"linear",0,0.005)
    	else:
        	GraphObs2=TGraph(len(obsX2),obsX2,obsY2)
    
    	GraphObs2.SetLineWidth(3)
    	GraphObs2.SetLineColor(kRed)
   

    	expX3=numpy.array(observedx3)
    	expY3=numpy.array(expectedy3)
    	GraphExp3=TGraph(len(expX3),expX3,expY3)
    	GraphExp3.SetLineWidth(3)
    	GraphExp3.SetLineStyle(2)
    	GraphExp3.SetLineColor(ROOT.kBlue+3)

    	obsX3=numpy.array(observedx3)
    	obsY3=numpy.array(observedy3)

    	if SMOOTH:
        	smooth_obs3=TGraphSmooth("normal")
        	GraphObs_nonSmooth3=TGraph(len(obsX3),obsX3,obsY3)
        	GraphObs3=smooth_obs3.SmoothSuper(GraphObs_nonSmooth3,"linear",0,0.005)
    	else:
        	GraphObs3=TGraph(len(obsX3),obsX3,obsY3)
    
    	GraphObs3.SetLineWidth(3)
    	GraphObs3.SetLineColor(kRed+3)


	ratio = []
	ratiox = []
	for index,val in enumerate(observedy):
		mass = observedx[index]
		foundIndex = -1
		for index2, mass2 in enumerate(observedx2):
			if mass == mass2:
				foundIndex = index2

		if foundIndex > 0:
			ratio.append(observedy2[foundIndex]/val)
			ratiox.append(mass)
	ratioA = numpy.array(ratio)
	ratioX = numpy.array(ratiox)
	ratioGraph = TGraph(len(ratioX),ratioX,ratioA)

	ratio2 = []
	ratiox2 = []
	for index,val in enumerate(observedy):
		mass = observedx[index]
		foundIndex = -1
		for index2, mass2 in enumerate(observedx3):
			if mass == mass2:
				foundIndex = index2

		if foundIndex > 0:
			ratio2.append(observedy3[foundIndex]/val)
			ratiox2.append(mass)
	ratioA2 = numpy.array(ratio2)
	ratioX2 = numpy.array(ratiox2)
	ratioGraph2 = TGraph(len(ratioX2),ratioX2,ratioA2)

	ratioE = []
	ratioxE = []
	for index,val in enumerate(expectedy):
		mass = observedx[index]
		foundIndex = -1
		for index2, mass2 in enumerate(observedx2):
			if mass == mass2:
				foundIndex = index2

		if foundIndex > 0:
			ratioE.append(expectedy2[foundIndex]/val)
			ratioxE.append(mass)
	ratioAE = numpy.array(ratioE)
	ratioXE = numpy.array(ratioxE)
	ratioGraphE = TGraph(len(ratioXE),ratioXE,ratioAE)

	ratioE2 = []
	ratioxE2 = []
	for index,val in enumerate(expectedy):
		mass = observedx[index]
		foundIndex = -1
		for index2, mass2 in enumerate(observedx3):
			if mass == mass2:
				foundIndex = index2

		if foundIndex > 0:
			ratioE2.append(expectedy3[foundIndex]/val)
			ratioxE2.append(mass)
	ratioAE2 = numpy.array(ratioE2)
	ratioXE2 = numpy.array(ratioxE2)
	ratioGraphE2 = TGraph(len(ratioXE2),ratioXE2,ratioAE2)






	if SPIN2:
		signals = ["RS_kMpl01","RS_kMpl005","RS_kMpl001"]	
	elif GUT:
		signals = ["ssm","psi","kai","eta","I","S","N"]
	else:
		signals = ["ssm","psi"]

	xSecCurves = []
	for signal in signals:
		xSecCurves.append(getXSecCurve(signal,kFacs[signal])) 
		#xSecCurves.append(getXSecCurve(signal,kFacs[signal],massDependent=True)) 

	#Draw the graphs:
	plotPad.SetLogy()
    	DummyGraph=TH1F("DummyGraph","",100,200,5500)
    	DummyGraph.GetXaxis().SetTitle("M [GeV]")
	if SPIN2:
        		DummyGraph.GetYaxis().SetTitle("[#sigma#upoint#font[12]{B}] G_{KK} / [#sigma#upoint#font[12]{B}] Z")
	else:
        		DummyGraph.GetYaxis().SetTitle("[#sigma#upoint#font[12]{B}] Z' / [#sigma#upoint#font[12]{B}] Z")

#	if SPIN2:
#	    	if chan=="mumu":
#       	 		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowG_{KK}+X#rightarrow#mu^{+}#mu^{-}+X) / #sigma(pp#rightarrowZ+X#rightarrow#mu^{+}#mu^{-}+X)")
#    		elif chan=="elel":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowG_{KK}+X#rightarrowee+X) / #sigma(pp#rightarrowZ+X#rightarrowee+X)")
#    		elif chan=="elmu":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowG_{KK}+X#rightarrow#font[12]{ll}+X) / #sigma(pp#rightarrowZ+X#rightarrow#font[12]{ll}+X)")
#	else:
#    		if chan=="mumu":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrow#mu^{+}#mu^{-}+X) / #sigma(pp#rightarrowZ+X#rightarrow#mu^{+}#mu^{-}+X)")
#    		elif chan=="elel":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrowee+X) / #sigma(pp#rightarrowZ+X#rightarrowee+X)")
#    		elif chan=="elmu":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrow#font[12]{ll}+X) / #sigma(pp#rightarrowZ+X#rightarrow#font[12]{ll}+X)")



    	gStyle.SetOptStat(0)
	DummyGraph.GetXaxis().SetRangeUser(200,5500)

    	DummyGraph.SetMinimum(5e-9)
    	DummyGraph.SetMaximum(1e-4)
    	DummyGraph.GetXaxis().SetLabelSize(0.055)
    	DummyGraph.GetXaxis().SetTitleSize(0.055)
   	DummyGraph.GetXaxis().SetTitleOffset(1.05)
    	DummyGraph.GetYaxis().SetLabelSize(0.055)
    	DummyGraph.GetYaxis().SetTitleSize(0.055)
    	DummyGraph.GetYaxis().SetTitleOffset(1.3)
    	DummyGraph.Draw()
    	if (FULL):
        	GraphErr2Sig.Draw("F")
        	GraphErr1Sig.Draw("F")
        	GraphExp.Draw("lsame")
    	else:
        	GraphExp.Draw("l")
        	GraphExp2.Draw("l")
        	#GraphExp3.Draw("l")
	if not EXPONLY:
    		GraphObs.Draw("lsame")
    		GraphObs2.Draw("lsame")
    		#GraphObs3.Draw("lsame")

    	for curve in xSecCurves:
        	curve.Draw("lsame")


    	plCMS=TPaveLabel(.16,.81,.27,.88,"CMS","NBNDC")
#plCMS.SetTextSize(0.8)
    	plCMS.SetTextAlign(12)
    	plCMS.SetTextFont(62)
    	plCMS.SetFillColor(0)
    	plCMS.SetFillStyle(0)
    	plCMS.SetBorderSize(0)
    
    	plCMS.Draw()

    	plPrelim=TPaveLabel(.16,.76,.27,.82,"Preliminary","NBNDC")
    	plPrelim.SetTextSize(0.6)
    	plPrelim.SetTextAlign(12)
    	plPrelim.SetTextFont(52)
    	plPrelim.SetFillColor(0)
    	plPrelim.SetFillStyle(0)
    	plPrelim.SetBorderSize(0)
	if "2017" in output or "Combination" in output or 'Run2' in output:
	    	plPrelim.Draw()


    	cCL.SetTickx(1)
    	cCL.SetTicky(1)
    	cCL.RedrawAxis()
    	cCL.Update()
    
    	#leg=TLegend(0.65,0.65,0.87,0.87,"","brNDC")   
    	#leg=TLegend(0.540517,0.623051,0.834885,0.878644,"","brNDC")   Default
    	leg=TLegend(0.5,0.58,0.834885,0.878644,"","brNDC")   
    	if SPIN2:
		leg=TLegend(0.5,0.58,0.834885,0.878644,"","brNDC")   
#    	leg=TLegend(0.55,0.55,0.87,0.87,"","brNDC")   
    	leg.SetTextSize(0.0425)
	if not obs2 == "":
		if ratioLabel == "":
			ratioLabel = "Variant/Default"
		ratioLabels = ratioLabel.split("/")
		print ratioLabels	
		leg.AddEntry(GraphObs, "%s Obs. 95%% CL limit"%ratioLabels[1],"l")
    		leg.AddEntry(GraphObs2,"%s Obs. 95%% CL limit"%ratioLabels[0],"l")
    	
	else:
		if not EXPONLY:
			leg.AddEntry(GraphObs,"Default Obs. 95% CL limit","l")
			leg.AddEntry(GraphObs2,"1 params floating uncert. Obs. 95% CL limit","l")
			leg.AddEntry(GraphObs3,"exp param floating Obs. 95% CL limit","l")
    		leg.AddEntry(GraphExp,"Default Exp. 95% CL limit, median","l")
    		leg.AddEntry(GraphExp2,"1 params floating Exp. 95% CL limit, median","l")
    		leg.AddEntry(GraphExp3,"exp param floating Exp. 95% CL limit, median","l")
        	if (FULL):
   		     	leg.AddEntry(GraphErr1Sig,"Exp. (68%)","f")
        		leg.AddEntry(GraphErr2Sig,"Exp. (95%)","f")


    	leg1=TLegend(0.7,0.4,0.9,0.55,"","brNDC")
	leg1.SetTextSize(0.05)
	if GUT: 
    		leg1=TLegend(0.6,0.35,0.75,0.623051,"","brNDC")
	if SPIN2:
    		leg1=TLegend(0.7,0.35,0.9,0.58,"G_{KK} (LO x 1.6)","brNDC")
		leg1.SetTextSize(0.045)
      	for index, signal in enumerate(signals):
		xSecCurves[index].SetName(labels[signal])
		xSecCurves[index].Write(labels[signal])	
        	leg1.AddEntry(xSecCurves[index],labels[signal],"l")
	leg1.SetBorderSize(0)

    	leg.SetLineWidth(0)
    	leg.SetLineStyle(0)
    	leg.SetFillStyle(0)
    	leg.SetLineColor(0)
    	leg.Draw("hist")

    	leg1.SetLineWidth(0)
    	leg1.SetLineStyle(0)
    	leg1.SetFillStyle(0)
    	leg1.SetLineColor(0)
    	leg1.Draw("hist")
	if "Moriond" in output:
         	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.885,.9,.99,"36.3 fb^{-1} (13 TeV, #mu^{+}#mu^{-})","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.885,.9,.99,"35.9 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.27,.885,.9,.99,"35.9 fb^{-1} (13 TeV, ee) + 36.3 fb^{-1} (13 TeV, #mu^{+}#mu^{-})","NBNDC")

	elif "2017" in output or "Combination" in output:
         	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.885,.9,.99,"42.4 fb^{-1} (13 TeV, #mu^{+}#mu^{-})","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.885,.9,.99,"41.4 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.27,.885,.9,.99,"77.3 fb^{-1} (13 TeV, ee) + 78.7 fb^{-1} (13 TeV, #mu^{+}#mu^{-})","NBNDC")
	else:
 	      	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.905,.9,.99," 139.7 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.905,.9,.99,"136.8 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.4,.905,.9,.99,"136.8 fb^{-1} (13 TeV, ee) + 139.7 fb^{-1} (13 TeV, #mu#mu)","NBNDC")

    	
	plLumi.SetTextSize(0.5)
    	plLumi.SetTextFont(42)
    	plLumi.SetFillColor(0)
    	plLumi.SetBorderSize(0)
    	plLumi.Draw()
    
	plotPad.SetTicks(1,1)
	plotPad.RedrawAxis()
		
	if obs2 == "":

    		ratioPad.cd()

    		line = ROOT.TLine(200,1,5500,1)
    		line.SetLineStyle(ROOT.kDashed)

    		ROOT.gStyle.SetTitleSize(0.12, "Y")
    		ROOT.gStyle.SetTitleYOffset(0.35) 
    		ROOT.gStyle.SetNdivisions(000, "Y")
    		ROOT.gStyle.SetNdivisions(408, "Y")
    		ratioPad.DrawFrame(200,0.8,5500,1.2, "; ; variation/default")

    		line.Draw("same")

    		ratioGraph.SetMarkerStyle(20)
    		ratioGraph2.SetMarkerStyle(20)
    		ratioGraphE.SetMarkerStyle(20)
    		ratioGraphE2.SetMarkerStyle(20)

		ratioGraph.SetMarkerSize(0.5)
    		ratioGraph2.SetMarkerSize(0.5)
    		ratioGraphE.SetMarkerSize(0.5)
    		ratioGraphE2.SetMarkerSize(0.5)


    		ratioGraph.SetMarkerColor(kRed)
    		ratioGraph2.SetMarkerColor(kRed+3)
    		ratioGraphE.SetMarkerColor(kBlue)
    		ratioGraphE2.SetMarkerColor(kBlue+3)



    		#ratioGraph.Draw("sameP")
    		#ratioGraph2.Draw("sameP")
    		ratioGraphE.Draw("sameP")
    		ratioGraphE2.Draw("sameP")


	#GraphErr2SigForHEPData.SetName("graph2Sig")
	#GraphErr2SigForHEPData.Write("graph2Sig")

	#GraphErr1SigForHEPData.SetName("graph1Sig")
	#GraphErr1SigForHEPData.Write("graph1Sig")

	#GraphExp.SetName("graphExp")
	#GraphExp.Write("graphExp")

	#GraphObs.SetName("graphObs")
	#GraphObs.Write("graphObs")

   	#fileForHEPData.Write()
	#fileForHEPData.Close() 
    	cCL.Update()
    	printPlots(cCL,output)
    

#### ========= MAIN =======================
SMOOTH=False
FULL=False
SPIN2=False
KFAC=False
GUT=False
EXPONLY = False
TWOENERGY=False
if __name__ == "__main__":
    	import argparse
    	parser = argparse.ArgumentParser(usage="makeLimitPlot.py [options] -o OUTPUTFILE --obs CARD1 --exp CARD2",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    	parser.add_argument("--obs",dest="obs", default='', help='Observed datacard')
    	parser.add_argument("--obs2",dest="obs2", default='', help='2nd Observed datacard')
    	parser.add_argument("--exp",dest="exp", default='', help='Expected datacard')
    	parser.add_argument("--stats",dest="stats", action="store_true", default=False, help='Print stats')
    	parser.add_argument("--smooth",dest="smooth",action="store_true",default=False, help="Smooth observed values")
    	parser.add_argument("--full",dest="full",action="store_true",default=False, help="Draw 2sigma bands")
    	parser.add_argument("--spin2",dest="spin2",action="store_true",default=False, help="Make Spin2 limits")
    	parser.add_argument("--kFac",dest="kFac",action="store_true",default=False, help="use mass dependent k factor")
    	parser.add_argument("--expOnly",dest="expOnly",action="store_true",default=False, help="plot only expected")
    	parser.add_argument("--gut",dest="gut",action="store_true",default=False, help="Make GUT limits")
    	parser.add_argument("-c","--config",dest="config",default='', help="config name")
    	parser.add_argument("-t","--tag",dest="tag",default='', help="limit tag")
    	parser.add_argument("--ratioLabel",dest="ratioLabel",default='', help="label for ratio")
    	args = parser.parse_args()
    	SMOOTH=args.smooth
    	FULL=args.full
    	SPIN2=args.spin2
    	KFAC=args.kFac
	GUT = args.gut
        EXPONLY = args.expOnly
	configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)

    	if ("mumu" in config.leptons):  
        	print "Running Limts for dimuon channel"
    	elif ("elel" in config.leptons):
        	print "Running Limts for dielectron channel"
    	elif ("elmu" in config.leptons):
        	print "Running Limts for Combination of dielectron and dimuon channel"
    	else: 
        	print "ERROR, --chan must be mumu, elel or elmu"
        	exit
	
	outputfile = "limitPlotCompare_%s"%args.config
	if not args.tag == "":
		outputfile += "_"+args.tag        
	if GUT:
		outputfile += "_GUT"
	if SPIN2:
		outputfile += "_RS"
	if KFAC:
		outputfile += "_KFAC"
	obs = "cards/ZPrime_limitCard_%s_Asymptotic"%args.config 
	if not args.tag == "":
		obs += "_" + args.tag
	obs += ".txt"
	if not args.obs == "":
		obs = args.obs
    	print "Saving histograms in %s" %(outputfile)
    	print " - Obs file: %s" %(obs)
    	if (SMOOTH):
        	print "                  "
        	print "Smoothing observed lines..." 
    	print "\n"


	
    	makeLimitPlot(outputfile,obs,config.leptons,args.stats,args.obs2,args.ratioLabel)
    
