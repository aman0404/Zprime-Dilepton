python makeLimitPlot.py -c DimuonRun2 -t legcay --full --smooth
python makeLimitPlot.py -c DimuonRun2 -t legcayRS --full --smooth --spin2
python makeLimitPlot.py -c DielectronRun2 -t legcay --full --smooth
python makeLimitPlot.py -c DielectronRun2 -t finalRS --full --smooth --spin2
python makeLimitPlot.py -c Run2 -t legcay --full --smooth
python makeLimitPlot.py -c Run2 -t finalRS --full --smooth --spin2
python makeLimitPlotWidths.py -c DimuonRun2 -t legcay --obs cards/ZPrime_limitCard_DimuonRun2_Obs_legcay.txt --obs cards/ZPrime_limitCard_DimuonRun2_width03_Obs_legcay.txt --obs cards/ZPrime_limitCard_DimuonRun2_width05_Obs_legcay.txt --obs cards/ZPrime_limitCard_DimuonRun2_width10_Obs_legcay.txt --exp cards/ZPrime_limitCard_DimuonRun2_Exp_legcay.txt --exp cards/ZPrime_limitCard_DimuonRun2_width03_Exp_legcay.txt --exp cards/ZPrime_limitCard_DimuonRun2_width05_Exp_legcay.txt --exp cards/ZPrime_limitCard_DimuonRun2_width10_Exp_legcay.txt --smooth
python makeLimitPlotWidths.py -c DielectronRun2 -t legcay --obs cards/ZPrime_limitCard_DielectronRun2_Obs_legcay.txt --obs cards/ZPrime_limitCard_DielectronRun2_width03_Obs_legcay.txt --obs cards/ZPrime_limitCard_DielectronRun2_width05_Obs_legcay.txt --obs cards/ZPrime_limitCard_DielectronRun2_width10_Obs_legcay.txt --exp cards/ZPrime_limitCard_DielectronRun2_Exp_legcay.txt --exp cards/ZPrime_limitCard_DielectronRun2_width03_Exp_legcay.txt --exp cards/ZPrime_limitCard_DielectronRun2_width05_Exp_legcay.txt --exp cards/ZPrime_limitCard_DielectronRun2_width10_Exp_legcay.txt --smooth
python makeLimitPlotWidths.py -c Run2 -t legcay --obs cards/ZPrime_limitCard_Run2_Obs_legcay.txt --obs cards/ZPrime_limitCard_Run2_width03_Obs_legcay.txt --obs cards/ZPrime_limitCard_Run2_width05_Obs_legcay.txt --obs cards/ZPrime_limitCard_Run2_width10_Obs_legcay.txt --exp cards/ZPrime_limitCard_Run2_Exp_legcay.txt --exp cards/ZPrime_limitCard_Run2_width03_Exp_legcay.txt --exp cards/ZPrime_limitCard_Run2_width05_Exp_legcay.txt --exp cards/ZPrime_limitCard_Run2_width10_Exp_legcay.txt --smooth
python makePValuePlot.py -c DimuonRun2 -t legcay --card cards/ZPrime_limitCard_DimuonRun2_Signif_legcay.txt --card cards/ZPrime_limitCard_DimuonRun2_width03_Signif_legcay.txt --card cards/ZPrime_limitCard_DimuonRun2_width05_Signif_legcay.txt --card cards/ZPrime_limitCard_DimuonRun2_width10_Signif_legcay.txt
python makePValuePlot.py -c DielectronRun2 -t legcay --card cards/ZPrime_limitCard_DielectronRun2_Signif_legcay.txt --card cards/ZPrime_limitCard_DielectronRun2_width03_Signif_legcay.txt --card cards/ZPrime_limitCard_DielectronRun2_width05_Signif_legcay.txt --card cards/ZPrime_limitCard_DielectronRun2_width10_Signif_legcay.txt
python makePValuePlot.py -c Run2 -t legcay --card cards/ZPrime_limitCard_Run2_Signif_legcay.txt --card cards/ZPrime_limitCard_Run2_width03_Signif_legcay.txt --card cards/ZPrime_limitCard_Run2_width05_Signif_legcay.txt --card cards/ZPrime_limitCard_Run2_width10_Signif_Signif.txt
python makePValuePlotChannels.py -c Run2 -t legcay --card cards/ZPrime_limitCard_Run2_Signif_legcay.txt --card cards/ZPrime_limitCard_DielectronRun2_Signif_legcay.txt --card cards/ZPrime_limitCard_DimuonRun2_Signif_legcay.txt