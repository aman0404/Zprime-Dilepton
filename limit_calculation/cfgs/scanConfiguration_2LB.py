leptons = "mumu"
#systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU"]
systematics = ["lumi",'res','massScale',"zPeak","trig","pdf","ID","PU"]

backgrounds = ['DY','Top','Diboson']

correlate = True

lambdasBBLL = [6,10,14,18,22,26]
lambdasBSLL = [1,2,3,4,5,6]

#interferencesBBLL = ["posLL","posLR","posRL","posRR","negLL","negRL","negLR","negRR"]
interferencesBBLL = ["posLL"]
interferencesBSLL = ["default"]

binning = [400,500,700,1100,1900,3500,10000]

libraries = []

channels = ["dimuon_2018_BB_ZeroB"]
#channels = ["dimuon_2018_BB_ZeroB","dimuon_2018_BE_ZeroB","dimuon_2018_BB_OneB","dimuon_2018_BE_OneB","dimuon_2018_BB_TwoB","dimuon_2018_BE_TwoB"]
numInt = 100000
numToys = 6
exptToys = 500
submitTo = "Purdue"
LPCUsername = "jschulte"
