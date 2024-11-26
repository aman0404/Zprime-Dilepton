import ROOT

def main():

	import glob
	for f in glob.glob("userfuncs/*.so"):
		ROOT.gSystem.Load(f)
	

	#ROOT.gSystem.Load("shapes/ZPrimeMuonBkgPdf_cxx.so")
	f = ROOT.TFile("MoriondDielectron_width05.root")

	ws = f.Get("dielectron_Moriond2017_EBEE")
	ws.Print()
	frame = ws.var('mass_dielectron_Moriond2017_EBEE').frame(ROOT.RooFit.Title(''),ROOT.RooFit.Range(150,400))
	
	c1 = ROOT.TCanvas("c1","c1",800,600)
	#pad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	#pad.cd()
	#pad.Draw()
	ws.data("data_dielectron_Moriond2017_EBEE").plotOn(frame,ROOT.RooFit.Range(150,400))

	#frame.SetMaximum(20)
	ws.pdf('bkgpdf_dielectron_Moriond2017_EBEE').plotOn(frame,
								 ROOT.RooFit.Range(150,400),
								  #~ ROOT.RooFit.VisualizeError(fitOFOS, 1),
								  #~ ROOT.RooFit.FillColor(ROOT.kGreen + 2),
								  #~ ROOT.RooFit.FillStyle(3009),
								  ROOT.RooFit.LineWidth(2))	

	ws.pdf('sig_pdf_dielectron_Moriond2017_EBEE').plotOn(frame,
								  ROOT.RooFit.Range(150,400),
								  #~ ROOT.RooFit.VisualizeError(fitOFOS, 1),
								  ROOT.RooFit.LineColor(ROOT.kGreen + 2),
								  #~ ROOT.RooFit.FillStyle(3009),
								  ROOT.RooFit.LineWidth(2))	
	
	ws.Print()
	#pad.DrawFrame(800,0,3200,20,";M [GeV]; Events")
	frame.Draw()

	print ws.var('peak_dielectron_Moriond2017_EBEE').getVal()
	print ws.var('beta_peak_dielectron_Moriond2017_EBEE').getVal()
	c1.Print("eleCheck.pdf")
main()
