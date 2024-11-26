import sys
import os
sys.path.append('cfgs/')
sys.path.append('input/')
import ROOT
from ROOT import gROOT
from numpy import array

from createInputs import createWS

if __name__ == "__main__":
        import argparse
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument("-c","--config", dest="config",default="", required=True, help='configuration name')
        parser.add_argument( "--spin2", dest = "spin2",action="store_true", default = False, help="calculate limits for spin2 resonances")
        args = parser.parse_args()

        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)
	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		gROOT.ProcessLine(".L "+f+"+")

	if not os.path.exists("validation"):
		os.mkdir("validation")	

		
	for channel in config.channels:
		if True:
			c = ROOT.TCanvas('c1','c1',800,800)
    			plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
    			plotPad.Draw()	
    			plotPad.cd()


        		channelName ="channelConfig_%s"%channel
	        	channelConfig =  __import__(channelName)


			eff = []
			effSpin2 = []
			res = []
			alphaL = []
			alphaR = []
			nL = []
			nR = []
			scale = []
			masses = []
			massRanges = config.masses
	        	for massRange in massRanges:
        	        	mass = massRange[1]
                		while mass < massRange[2]:
					masses.append(mass)
					eff.append(channelConfig.signalEff(mass,spin2=args.spin2))	
					effSpin2.append(channelConfig.signalEff(mass,spin2=True))	
					resStuff = channelConfig.getResolution(mass)
					res.append(resStuff["res"])
					alphaL.append(resStuff["alphaL"])
					alphaR.append(resStuff["alphaR"])
					if 'nR' in resStuff:
						nL.append(resStuff["nL"])
						nR.append(resStuff["nR"])
					scale.append(resStuff["scale"])
                        		mass += massRange[0]


			effGraph = ROOT.TGraph()
			effGraphSpin2 = ROOT.TGraph()
			for i, mass in enumerate(masses):
				effGraph.SetPoint(i,mass,eff[i])
				effGraphSpin2.SetPoint(i,mass,effSpin2[i])
		
			maxVal = 1
			minVal = 0

			plotPad.DrawFrame(massRanges[0][1],minVal,massRanges[-1][2],maxVal,'%s ;m [GeV]; selection efficiency'%channel)

			effGraph.Draw('LPsame')
			effGraphSpin2.Draw('LPsame')
			effGraphSpin2.SetLineColor(ROOT.kRed)
			effGraphSpin2.SetMarkerColor(ROOT.kRed)
			c.Print('validation/%s_eff.pdf'%channel)
			
			resGraph = ROOT.TGraph()
			alphaLGraph = ROOT.TGraph()
			alphaRGraph = ROOT.TGraph()
			nLGraph = ROOT.TGraph()
			nRGraph = ROOT.TGraph()
			scaleGraph = ROOT.TGraph()
			for i, mass in enumerate(masses):
				resGraph.SetPoint(i,mass,res[i])
				if len(nL) > 0:
					nLGraph.SetPoint(i,mass,nL[i])
					nRGraph.SetPoint(i,mass,nR[i])
				alphaLGraph.SetPoint(i,mass,alphaL[i])
				alphaRGraph.SetPoint(i,mass,alphaR[i])
				scaleGraph.SetPoint(i,mass,scale[i])
		
			maxVal = max(res)*1.5
			minVal = 0
			plotPad.DrawFrame(massRanges[0][1],minVal,massRanges[-1][2],maxVal,'%s ;m [GeV]; mass resoltion'%channel)
			resGraph.Draw('LPsame')
			c.Print('validation/%s_res.pdf'%channel)

			maxVal = max(alphaL)*1.5
			minVal = 0
			plotPad.DrawFrame(massRanges[0][1],minVal,massRanges[-1][2],maxVal,'%s ;m [GeV]; alphaL'%channel)	
			alphaLGraph.Draw('LPsame')
			c.Print('validation/%s_alphaL.pdf'%channel)

			maxVal = max(alphaR)*1.5
			minVal = 0
			plotPad.DrawFrame(massRanges[0][1],minVal,massRanges[-1][2],maxVal,'%s ;m [GeV]; alphaR'%channel)
			alphaRGraph.Draw('LPsame')
			c.Print('validation/%s_alphaR.pdf'%channel)
			if len(nL) > 0:
				maxVal = max(nL)*1.5
				minVal = 0
				plotPad.DrawFrame(massRanges[0][1],minVal,massRanges[-1][2],maxVal,'%s ;m [GeV]; nL'%channel)
				nLGraph.Draw('LPsame')
				c.Print('validation/%s_nL.pdf'%channel)

				maxVal = max(nR)*1.5
				minVal = 0
				plotPad.DrawFrame(massRanges[0][1],minVal,massRanges[-1][2],maxVal,'%s ;m [GeV]; nR'%channel)
				nRGraph.Draw('LPsame')
				c.Print('validation/%s_nR.pdf'%channel)

			maxVal = max(scale)*1.5
			minVal = min(scale)*1.5
			plotPad.DrawFrame(massRanges[0][1],minVal,massRanges[-1][2],maxVal,'%s ;m [GeV]; scale'%channel)
			scaleGraph.Draw('LPsame')
			c.Print('validation/%s_scale.pdf'%channel)
			from tools import getMassRange

			mass = 4500

			massLow, massHigh = getMassRange(mass,100,0.006+channelConfig.getResolution(mass)['res'],channelConfig.dataFile,150)	

	
			ws = createWS(mass,100,args.config,channel,0.1,False,dataFile="",CB=True,write=False,useShapeUncert=True)	
			#massRanges[0][1] = 200
			#massRanges[-1][2] = 400
			frame = ws.var('mass_%s'%channel).frame(ROOT.RooFit.Title(''),ROOT.RooFit.Range(massLow,massHigh))
	
			ws.data("data_%s"%channel).plotOn(frame,ROOT.RooFit.Range(massLow,massHigh))

			ws.pdf('bkgpdf_%s'%channel).plotOn(frame,
								 ROOT.RooFit.Range(massLow,massHigh),
								  ROOT.RooFit.LineWidth(2))	

			ws.pdf('sig_pdf_%s'%channel).plotOn(frame,
								  ROOT.RooFit.Range(massLow,massHigh),
								  ROOT.RooFit.LineColor(ROOT.kGreen + 2),
								  ROOT.RooFit.LineWidth(2))	
			plotPad.DrawFrame(massLow,1e-3,massHigh,5e4,'%s;m [GeV]; Events'%channel)
			#plotPad.DrawFrame(massLow,1e-3,massHigh,10,'%s;m [GeV]; Events'%channel)
			#plotPad.DrawFrame(900,1e-3,6000,5e4,'%s;m [GeV]; Events'%channel)
			plotPad.SetLogy()
			frame.Draw('same')
			#ws.Print()
			c.Print("validation/%s_shapes.pdf"%channel)

#		else:	
#			c = ROOT.TCanvas('c1','c1',800,800)
#    			plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
#    			plotPad.Draw()	
#    			plotPad.cd()
#
#
#        		channelName ="channelConfig_%s"%channel
#	        	channelConfig =  __import__(channelName)
#
#
#			eff = []
#			resolution = []
#			masses = []
#			massRanges = config.masses
#	        	for massRange in massRanges:
#        	        	mass = massRange[1]
#                		while mass < massRange[2]:
#					masses.append(mass)
#					eff.append(channelConfig.signalEff(mass))	
#					resolution.append(channelConfig.getResolution(mass))
#                       		mass += massRange[0]
#
#
#			effGraph = ROOT.TGraph()
#			for i, mass in enumerate(masses):
#				effGraph.SetPoint(i,mass,eff[i])
#		
#			maxVal = 1
#			minVal = 0
#
#			plotPad.DrawFrame(massRanges[0][1],minVal,massRanges[-1][2],maxVal,'%s ;m [GeV]; selection efficiency'%channel)
#
#			effGraph.Draw('LPsame')
#		
#			c.Print('validation/%s_eff.pdf'%channel)
#			
#			resGraph = ROOT.TGraph()
#			for i, mass in enumerate(masses):
#				resGraph.SetPoint(i,mass,resolution[i])
#		
#			maxVal = max(resolution)*1.5
#			minVal = 0
#
#			plotPad.DrawFrame(massRanges[0][1],minVal,massRanges[-1][2],maxVal,'%s ;m [GeV]; mass resoltion'%channel)
#
#			resGraph.Draw('LPsame')
#		
#			c.Print('validation/%s_res.pdf'%channel)
#	
#			ws = createWS(2000,1e06,args.config,channel,0.006,False,dataFile="",CB=True,write=False)	
#
#			frame = ws.var('mass_%s'%channel).frame(ROOT.RooFit.Title(''),ROOT.RooFit.Range(massRanges[0][1],massRanges[-1][2]))
#	
##			ws.data("data_%s"%channel).plotOn(frame,ROOT.RooFit.Range(massRanges[0][1],massRanges[-1][2]))
#
#			ws.pdf('bkgpdf_%s'%channel).plotOn(frame,
#								 ROOT.RooFit.Range(massRanges[0][1],massRanges[-1][2]),
#								  ROOT.RooFit.LineWidth(2))	
#
#			ws.pdf('sig_pdf_%s'%channel).plotOn(frame,
#								  ROOT.RooFit.Range(massRanges[0][1],massRanges[-1][2]),
#								  ROOT.RooFit.LineColor(ROOT.kGreen + 2),
#								  ROOT.RooFit.LineWidth(2))	
#			plotPad.DrawFrame(massRanges[0][1],0.5,massRanges[-1][2],5e4,'%s;m [GeV]; Events'%channel)
#			plotPad.SetLogy()
#			frame.Draw('same')
#			c.Print("validation/%s_shapes.pdf"%channel)
#
