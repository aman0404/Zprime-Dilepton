import os
import numpy as np
from hepdata_lib import *

def make_table_10():
	# This is the raw data from EXO-23-010 in the electron (0b) channel 
	# It has seven columns
	data = [
		[(200, 300),   108042, (107890, 940), (87200, 620),  (12460, 110), (4122,  35),   (4100, 2100)],	
		[(300, 400),   26639,  (26640, 240),  (20950, 160),  (3498,  35),  (1188,  11),   (1000, 500)],
		[(400, 500),   9004,   (9093, 84),    (7250,  61),   (1128,  13),  (417.1, 4.3),  (300,  150)],
		[(500, 700),   5482,   (5536, 53),    (4542,  42),   (583.7, 8.2), (255.6, 2.8),  (155,  27)],
		[(700, 1100),  1885,   (1910, 21),    (1641,  19),   (139.5, 3.4), (86.6,  1.2),  (42,   21)],
		[(1100, 1900), 323,    (325.6, 4.4),  (288.8, 4.0),  (18.7,  1.4), (13.27, 0.68), (4.8,   2.4)],
		[(1900,10000), 	29,    (21.01, 0.55), (18.96, 0.36), (0.86,  0.40),(0.94 , 0.07), (0.24, 0.12)],
	]
	table = Table("Data and background yields in the dielectron 0b channel")
	table.location = "Data from Table 10."
	table.description = """Observed and expected background yields for different mass ranges in the dielectron channel in 0 b jet final state. The sum of all background contributions is shown as well as a breakdown into the three main categories. The quoted uncertainty includes both the statistical and the systematic components."""
	# First variable/column ---> Mass
	mass = Variable("MASS", is_independent=True, is_binned=True, units="GeV")
	mass.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	obs = Variable("Data", is_independent=False,
				   is_binned=False, units="Events")
	obs.values = [item[1] for item in data]
	obs.digits = 999
    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	exp_full = Variable("Total background estimate",
						is_independent=False, is_binned=False, units="Events")
	exp_full.values = [item[2][0] for item in data]
	exp_full.digits = 999

	unc_full = Uncertainty("total")
	unc_full.values = [item[2][1] for item in data]
	exp_full.uncertainties.append(unc_full)

	# Fourth variable/column ---> Number of predicted DY events from MC
	exp_dy = Variable("DY background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_dy.values = [item[3][0] for item in data]
	exp_dy.digits = 999

	unc_dy = Uncertainty("total")
	unc_dy.values = [item[3][1] for item in data]
	exp_dy.uncertainties.append(unc_dy)

	# Fifth variable/column ---> Number of predicted tt events from MC
	exp_tt = Variable("ttbar + Other background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_tt.values = [item[4][0] for item in data]
	exp_tt.digits = 999
	
	unc_tt = Uncertainty("total")
	unc_tt.values = [item[4][1] for item in data]
	exp_tt.uncertainties.append(unc_tt)

	# Sixth variable/column ---> Number of predicted VV+VVV+Higgs events from MC
	exp_vv = Variable("VV+VVV+Higgs background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_vv.values = [item[5][0] for item in data]
	exp_vv.digits = 999
	unc_vv = Uncertainty("total")
	unc_vv.values = [item[5][1] for item in data]
	exp_vv.uncertainties.append(unc_vv)

	# Seventh variable/column ---> Number of predicted Jets events from data driven method
	exp_jet = Variable("jet background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_jet.values = [item[6][0] for item in data]
	exp_jet.digits = 999
	unc_jet = Uncertainty("total")
	unc_jet.values = [item[6][1] for item in data]
	exp_jet.uncertainties.append(unc_jet)


	table.add_variable(mass)
	table.add_variable(obs)
	table.add_variable(exp_full)
	table.add_variable(exp_dy)
	table.add_variable(exp_tt)
	table.add_variable(exp_vv)
	table.add_variable(exp_jet)

	return table


def make_table_11():
	# This is the raw data from EXO-23-010 in the electron (1b) channel 
	# It has seven columns
	data = [
		[(200, 300),   44,   (52.8, 4.3),  (44.4, 4.0),  (5.9,  1.4),  (0.83, 0.07),  (1.64, 0.82)],	
		[(300, 400),   35,   (31.4, 2.9),  (25.8, 2.8),  (4.34, 0.86), (0.42, 0.08),  (0.83, 0.42)],
		[(400, 500),   11,   (16.0, 1.7),   (12.1, 1.5),  (3.09, 0.93), (0.36, 0.05),  (0.45, 0.23)],
		[(500, 700),   28,   (20.2, 2.5),  (14.8, 1.5),  (4.0,  2.0),  (0.58, 0.04),  (0.68, 0.34)],
		[(700, 1100),  17,   (11.4, 1.2),  (9.05, 0.91), (1.67, 0.84), (0.36, 0.08),  (0.31, 0.16)],
		[(1100, 1900), 4,    (2.76, 0.41), (2.26, 0.20), (0.35, 0.35), (0.09, 0.02),   (0.07, 0.03)],
		[(1900,10000), 0,    (0.28, 0.11), (0.18, 0.02), (0.00, 0.09), (0.03, 0.03),  (0.06, 0.03)],
	]
	table = Table("Data and  background yields in the dielectron 1b channel")
	table.location = "Data from Table 11."
	table.description = """Observed and expected background yields for different mass ranges in the dielectron channel in 1 b jet final state. The sum of all background contributions is shown as well as a breakdown into the three main categories. The quoted uncertainty includes both the statistical and the systematic components."""
	# First variable/column ---> Mass
	mass = Variable("MASS", is_independent=True, is_binned=True, units="GeV")
	mass.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	obs = Variable("Data", is_independent=False,
				   is_binned=False, units="Events")
	obs.values = [item[1] for item in data]
	obs.digits = 999
    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	exp_full = Variable("Total background estimate",
						is_independent=False, is_binned=False, units="Events")
	exp_full.values = [item[2][0] for item in data]
	exp_full.digits = 999

	unc_full = Uncertainty("total")
	unc_full.values = [item[2][1] for item in data]
	exp_full.uncertainties.append(unc_full)

	# Fourth variable/column ---> Number of predicted DY events from MC
	exp_dy = Variable("DY background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_dy.values = [item[3][0] for item in data]
	exp_dy.digits = 999

	unc_dy = Uncertainty("total")
	unc_dy.values = [item[3][1] for item in data]
	exp_dy.uncertainties.append(unc_dy)

	# Fifth variable/column ---> Number of predicted tt events from MC
	exp_tt = Variable("ttbar + Other background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_tt.values = [item[4][0] for item in data]
	exp_tt.digits = 999
	
	unc_tt = Uncertainty("total")
	unc_tt.values = [item[4][1] for item in data]
	exp_tt.uncertainties.append(unc_tt)

	# Sixth variable/column ---> Number of predicted VV+VVV+Higgs events from MC
	exp_vv = Variable("VV+VVV+Higgs background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_vv.values = [item[5][0] for item in data]
	exp_vv.digits = 999
	unc_vv = Uncertainty("total")
	unc_vv.values = [item[5][1] for item in data]
	exp_vv.uncertainties.append(unc_vv)

	# Seventh variable/column ---> Number of predicted Jets events from data driven method
	exp_jet = Variable("jet background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_jet.values = [item[6][0] for item in data]
	exp_jet.digits = 999
	unc_jet = Uncertainty("total")
	unc_jet.values = [item[6][1] for item in data]
	exp_jet.uncertainties.append(unc_jet)


	table.add_variable(mass)
	table.add_variable(obs)
	table.add_variable(exp_full)
	table.add_variable(exp_dy)
	table.add_variable(exp_tt)
	table.add_variable(exp_vv)
	table.add_variable(exp_jet)

	return table

def make_table_12():
	# This is the raw data from EXO-23-010 in the electron (2b) channel 
	# It has seven columns
	data = [
		[(200, 400),   2,   (2.03, 0.95),  (1.52, 0.93),  (0.43, 0.19),  (0.01, 0.01),  (0.07, 0.04)],	
		[(400, 600),   2,   (1.30, 1.2 ),  (0.78, 0.50),  (0.40, 1.10),  (0.06, 0.04),  (0.01, 0.00)],
		[(600, 900),   2,   (2.20, 0.95),  (1.48, 0.75),  (0.70, 0.58),  (0.02, 0.01),  (0.00, 0.00)],
		[(900, 10000), 1,   (0.81, 0.35),  (0.56, 0.24),  (0.22, 0.24),  (0.01, 0.05),  (0.01, 0.01)],
	]
	table = Table("Data and  background yields in the dielectron 2b channel")
	table.location = "Data from Table 12."
	table.description = """Observed and expected background yields for different mass ranges in the dielectron channel in 2 b jet final state. The sum of all background contributions is shown as well as a breakdown into the three main categories. The quoted uncertainty includes both the statistical and the systematic components."""
	# First variable/column ---> Mass
	mass = Variable("MASS", is_independent=True, is_binned=True, units="GeV")
	mass.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	obs = Variable("Data", is_independent=False,
				   is_binned=False, units="Events")
	obs.values = [item[1] for item in data]
	obs.digits = 999
    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	exp_full = Variable("Total background estimate",
						is_independent=False, is_binned=False, units="Events")
	exp_full.values = [item[2][0] for item in data]
	exp_full.digits = 999

	unc_full = Uncertainty("total")
	unc_full.values = [item[2][1] for item in data]
	exp_full.uncertainties.append(unc_full)

	# Fourth variable/column ---> Number of predicted DY events from MC
	exp_dy = Variable("DY background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_dy.values = [item[3][0] for item in data]
	exp_dy.digits = 999

	unc_dy = Uncertainty("total")
	unc_dy.values = [item[3][1] for item in data]
	exp_dy.uncertainties.append(unc_dy)

	# Fifth variable/column ---> Number of predicted tt events from MC
	exp_tt = Variable("ttbar + Other background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_tt.values = [item[4][0] for item in data]
	exp_tt.digits = 999
	
	unc_tt = Uncertainty("total")
	unc_tt.values = [item[4][1] for item in data]
	exp_tt.uncertainties.append(unc_tt)

	# Sixth variable/column ---> Number of predicted VV+VVV+Higgs events from MC
	exp_vv = Variable("VV+VVV+Higgs background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_vv.values = [item[5][0] for item in data]
	exp_vv.digits = 999
	unc_vv = Uncertainty("total")
	unc_vv.values = [item[5][1] for item in data]
	exp_vv.uncertainties.append(unc_vv)

	# Seventh variable/column ---> Number of predicted Jets events from data driven method
	exp_jet = Variable("jet background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_jet.values = [item[6][0] for item in data]
	exp_jet.digits = 999
	unc_jet = Uncertainty("total")
	unc_jet.values = [item[6][1] for item in data]
	exp_jet.uncertainties.append(unc_jet)


	table.add_variable(mass)
	table.add_variable(obs)
	table.add_variable(exp_full)
	table.add_variable(exp_dy)
	table.add_variable(exp_tt)
	table.add_variable(exp_vv)
	table.add_variable(exp_jet)

	return table

def make_table_13():
	# This is the raw data from EXO-23-010 in the muon (0b) channel 
	# It has seven columns
	data = [
		[(200, 300),   161236, (161000, 440), (137700,400),  (17466, 85),  (5039,   17),   (800, 400)],	
		[(300, 400),   40982,  (41700,  120), (34200, 100),  (5505,  30),  (1693.2, 4.8),  (300, 150)],
		[(400, 500),   14135,  (14370,  53),  (11688, 45),   (1926,  13),  (651.4,  2.3),  (107, 54)],
		[(500, 700),   8530,   (8738,   39),  (7170,  35),   (1070.9,9.7), (420.3,  1.8),  (78,  39)],
		[(700, 1100),  2762,   (2852,   16),  (2397,  14),   (280.1, 4.3), (144,    1.0),  (31,  16)],
		[(1100, 1900), 429,    (457.6,  4.7), (397.7, 3.6),  (36.1,  1.4), (19.8,   1.1),  (4.0, 2.0)],
		[(1900,10000), 	30,    (33.0,   1.4), (25.23, 0.35), (1.00,  0.36),(1.23 ,  0.07), (5.5, 2.7)],
	]
	table = Table("Data and  background yields in the dimuon 0b channel")
	table.location = "Data from Table 10."
	table.description = """Observed and expected background yields for different mass ranges in the dimuon channel in 0 b jet final state. The sum of all background contributions is shown as well as a breakdown into the three main categories. The quoted uncertainty includes both the statistical and the systematic components."""
	# First variable/column ---> Mass
	mass = Variable("MASS", is_independent=True, is_binned=True, units="GeV")
	mass.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	obs = Variable("Data", is_independent=False,
				   is_binned=False, units="Events")
	obs.values = [item[1] for item in data]
	obs.digits = 999
    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	exp_full = Variable("Total background estimate",
						is_independent=False, is_binned=False, units="Events")
	exp_full.values = [item[2][0] for item in data]
	exp_full.digits = 999

	unc_full = Uncertainty("total")
	unc_full.values = [item[2][1] for item in data]
	exp_full.uncertainties.append(unc_full)

	# Fourth variable/column ---> Number of predicted DY events from MC
	exp_dy = Variable("DY background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_dy.values = [item[3][0] for item in data]
	exp_dy.digits = 999

	unc_dy = Uncertainty("total")
	unc_dy.values = [item[3][1] for item in data]
	exp_dy.uncertainties.append(unc_dy)

	# Fifth variable/column ---> Number of predicted tt events from MC
	exp_tt = Variable("ttbar + Other background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_tt.values = [item[4][0] for item in data]
	exp_tt.digits = 999
	
	unc_tt = Uncertainty("total")
	unc_tt.values = [item[4][1] for item in data]
	exp_tt.uncertainties.append(unc_tt)

	# Sixth variable/column ---> Number of predicted VV+VVV+Higgs events from MC
	exp_vv = Variable("VV+VVV+Higgs background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_vv.values = [item[5][0] for item in data]
	exp_vv.digits = 999
	unc_vv = Uncertainty("total")
	unc_vv.values = [item[5][1] for item in data]
	exp_vv.uncertainties.append(unc_vv)

	# Seventh variable/column ---> Number of predicted Jets events from data driven method
	exp_jet = Variable("jet background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_jet.values = [item[6][0] for item in data]
	exp_jet.digits = 999
	unc_jet = Uncertainty("total")
	unc_jet.values = [item[6][1] for item in data]
	exp_jet.uncertainties.append(unc_jet)


	table.add_variable(mass)
	table.add_variable(obs)
	table.add_variable(exp_full)
	table.add_variable(exp_dy)
	table.add_variable(exp_tt)
	table.add_variable(exp_vv)
	table.add_variable(exp_jet)

	return table

def make_table_14():
	# This is the raw data from EXO-23-010 in the muon (1b) channel 
	# It has seven columns
	data = [
		[(200, 300),   127,  (116, 6.3),  (99,   6.0),  (15,  2.0),  (1.53, 0.09),  (0.88, 0.44)],	
		[(300, 400),   49,   (47,  4.2),  (38.3, 4.1),  (7.3, 1.1),  (1.04, 0.11),  (0.23, 0.11)],
		[(400, 500),   26,   (28,  2.7),  (23.6, 2.5),  (3.8, 0.9),  (0.38, 0.22),  (0.23, 0.11)],
		[(500, 700),   39,   (30,  2.9),  (22.5, 2.5),  (6.8, 1.4),  (0.56, 0.09),  (0.00, 0.00)],
		[(700, 1100),  27,   (22,  2.0),  (15.0, 1.3),  (5.8, 1.5),  (0.58, 0.17),  (0.62, 0.32)],
		[(1100, 1900), 6,    (4.65,0.51), (3.45, 0.23), (1.08,0.45), (0.11, 0.03),  (0.01, 0.00)],
		[(1900,10000), 1,    (0.58,0.40), (0.30, 0.02), (0.23,0.40), (0.04 ,0.02),  (0.00, 0.00)],
	]
	table = Table("Data and  background yields in the dimuon 1b channel")
	table.location = "Data from Table 10."
	table.description = """Observed and expected background yields for different mass ranges in the dimuon channel in 1 b jet final state. The sum of all background contributions is shown as well as a breakdown into the three main categories. The quoted uncertainty includes both the statistical and the systematic components."""
	# First variable/column ---> Mass
	mass = Variable("MASS", is_independent=True, is_binned=True, units="GeV")
	mass.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	obs = Variable("Data", is_independent=False,
				   is_binned=False, units="Events")
	obs.values = [item[1] for item in data]
	obs.digits = 999
    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	exp_full = Variable("Total background estimate",
						is_independent=False, is_binned=False, units="Events")
	exp_full.values = [item[2][0] for item in data]
	exp_full.digits = 999

	unc_full = Uncertainty("total")
	unc_full.values = [item[2][1] for item in data]
	exp_full.uncertainties.append(unc_full)

	# Fourth variable/column ---> Number of predicted DY events from MC
	exp_dy = Variable("DY background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_dy.values = [item[3][0] for item in data]
	exp_dy.digits = 999

	unc_dy = Uncertainty("total")
	unc_dy.values = [item[3][1] for item in data]
	exp_dy.uncertainties.append(unc_dy)

	# Fifth variable/column ---> Number of predicted tt events from MC
	exp_tt = Variable("ttbar + Other background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_tt.values = [item[4][0] for item in data]
	exp_tt.digits = 999
	
	unc_tt = Uncertainty("total")
	unc_tt.values = [item[4][1] for item in data]
	exp_tt.uncertainties.append(unc_tt)

	# Sixth variable/column ---> Number of predicted VV+VVV+Higgs events from MC
	exp_vv = Variable("VV+VVV+Higgs background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_vv.values = [item[5][0] for item in data]
	exp_vv.digits = 999
	unc_vv = Uncertainty("total")
	unc_vv.values = [item[5][1] for item in data]
	exp_vv.uncertainties.append(unc_vv)

	# Seventh variable/column ---> Number of predicted Jets events from data driven method
	exp_jet = Variable("jet background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_jet.values = [item[6][0] for item in data]
	exp_jet.digits = 999
	unc_jet = Uncertainty("total")
	unc_jet.values = [item[6][1] for item in data]
	exp_jet.uncertainties.append(unc_jet)


	table.add_variable(mass)
	table.add_variable(obs)
	table.add_variable(exp_full)
	table.add_variable(exp_dy)
	table.add_variable(exp_tt)
	table.add_variable(exp_vv)
	table.add_variable(exp_jet)

	return table

def make_table_15():
	# This is the raw data from EXO-23-010 in the muon (2b) channel 
	# It has seven columns
	data = [
		[(200, 400),   4,   (2.76, 0.68),  (2.32, 0.86),  (0.38, 0.15),  (0.07, 0.03),  (0.00, 0.00)],	
		[(400, 600),   0,   (0.95, 0.33 ), (0.49, 0.30),  (0.40, 0.15),  (0.06, 0.02),  (0.00, 0.00)],
		[(600, 900),   1,   (1.98, 0.35),  (1.17, 0.22),  (0.77, 0.28),  (0.04, 0.01),  (0.00, 0.00)],
		[(900, 10000), 2,   (1.47, 0.29),  (1.07, 0.06),  (0.38, 0.29),  (0.03, 0.01),  (0.00, 0.00)],
	]
	table = Table("Data and  background yields in the dimuon 2b channel")
	table.location = "Data from Table 12."
	table.description = """Observed and expected background yields for different mass ranges in the dimuon channel in 2 b jet final state. The sum of all background contributions is shown as well as a breakdown into the three main categories. The quoted uncertainty includes both the statistical and the systematic components."""
	# First variable/column ---> Mass
	mass = Variable("MASS", is_independent=True, is_binned=True, units="GeV")
	mass.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	obs = Variable("Data", is_independent=False,
				   is_binned=False, units="Events")
	obs.values = [item[1] for item in data]
	obs.digits = 999
    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	exp_full = Variable("Total background estimate",
						is_independent=False, is_binned=False, units="Events")
	exp_full.values = [item[2][0] for item in data]
	exp_full.digits = 999

	unc_full = Uncertainty("total")
	unc_full.values = [item[2][1] for item in data]
	exp_full.uncertainties.append(unc_full)

	# Fourth variable/column ---> Number of predicted DY events from MC
	exp_dy = Variable("DY background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_dy.values = [item[3][0] for item in data]
	exp_dy.digits = 999

	unc_dy = Uncertainty("total")
	unc_dy.values = [item[3][1] for item in data]
	exp_dy.uncertainties.append(unc_dy)

	# Fifth variable/column ---> Number of predicted tt events from MC
	exp_tt = Variable("ttbar + Other background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_tt.values = [item[4][0] for item in data]
	exp_tt.digits = 999
	
	unc_tt = Uncertainty("total")
	unc_tt.values = [item[4][1] for item in data]
	exp_tt.uncertainties.append(unc_tt)

	# Sixth variable/column ---> Number of predicted VV+VVV+Higgs events from MC
	exp_vv = Variable("VV+VVV+Higgs background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_vv.values = [item[5][0] for item in data]
	exp_vv.digits = 999
	unc_vv = Uncertainty("total")
	unc_vv.values = [item[5][1] for item in data]
	exp_vv.uncertainties.append(unc_vv)

	# Seventh variable/column ---> Number of predicted Jets events from data driven method
	exp_jet = Variable("jet background estimate",
					  is_independent=False, is_binned=False, units="Events")
	exp_jet.values = [item[6][0] for item in data]
	exp_jet.digits = 999
	unc_jet = Uncertainty("total")
	unc_jet.values = [item[6][1] for item in data]
	exp_jet.uncertainties.append(unc_jet)


	table.add_variable(mass)
	table.add_variable(obs)
	table.add_variable(exp_full)
	table.add_variable(exp_dy)
	table.add_variable(exp_tt)
	table.add_variable(exp_vv)
	table.add_variable(exp_jet)

	return table

def make_figure_12a():
	# This is the raw data from EXO-23-010 for flavor ratio for 0b channel 
	# It has three columns with ratio from DY+jets MC and observed data
	data = [
		[(200,  300),   (0.977, 0.037),  (0.983, 0.042)],	
		[(300,  400),   (1.088, 0.061),  (1.039, 0.064)],
		[(400,  500),   (1.107, 0.060),  (1.066, 0.066)],
		[(500,  700),   (1.117, 0.064),  (1.046, 0.069)],
        [(700,  1100),  (1.101, 0.071),  (0.984, 0.077)],
        [(1100, 1900),  (1.086, 0.089),  (0.906, 0.116)],
        [(1900, 10000), (1.117, 0.118),  (0.624, 0.228)],
	]
	table = Table("Flavor ratio from DY+jets and data in 0b channel")
	table.location = "Data from Figure 12a"
	table.description = """OFlavor ratio from DY+jets and data in 0b channel. The quoted uncertainty includes both the statistical and the systematic components."""
	# First variable/column ---> Mass
	mass = Variable("MASS", is_independent=True, is_binned=True, units="GeV")
	mass.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	exp_dy = Variable("Flavor ratio from DY+jets MC",
					  is_independent=False, is_binned=False, units="ratio")
	exp_dy.values = [item[1][0] for item in data]
	exp_dy.digits = 999

	unc_dy = Uncertainty("total")
	unc_dy.values = [item[1][1] for item in data]
	exp_dy.uncertainties.append(unc_dy)
    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	obs_ratio = Variable("Flavor ratio from data",
						is_independent=False, is_binned=False, units="ratio")
	obs_ratio.values = [item[2][0] for item in data]
	obs_ratio.digits = 999

	unc_data = Uncertainty("total")
	unc_data.values = [item[2][1] for item in data]
	obs_ratio.uncertainties.append(unc_data)

	
	table.add_variable(mass)
	table.add_variable(exp_dy)
	table.add_variable(obs_ratio)
	

	return table

def make_figure_12b():
	# This is the raw data from EXO-23-010 for flavor ratio for 1b+2b channel 
	# It has three columns with ratio from DY+jets MC and observed data
	data = [
		[(200,  400),   (1.000 , 0.088),  (1.000 , 0.239)],	
		[(400,  700),   (0.930 , 0.093),  (0.738 , 0.239)],
		[(700,  1100),  (0.978 , 0.110),  (0.682 , 0.310)],
		[(1100, 10000), (0.942 , 0.110),  (0.789 , 0.547)],

	]
	table = Table("Flavor ratio from DY+jets and data in 1b+2b channel")
	table.location = "Data from Figure 12b."
	table.description = """OFlavor ratio from DY+jets and data in 1b+2b channel. The quoted uncertainty includes both the statistical and the systematic components."""
	# First variable/column ---> Mass
	mass = Variable("MASS", is_independent=True, is_binned=True, units="GeV")
	mass.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	exp_dy = Variable("Flavor ratio from DY+jets MC",
					  is_independent=False, is_binned=False, units="ratio")
	exp_dy.values = [item[1][0] for item in data]
	exp_dy.digits = 999

	unc_dy = Uncertainty("total")
	unc_dy.values = [item[1][1] for item in data]
	exp_dy.uncertainties.append(unc_dy)
    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	obs_ratio = Variable("Flavor ratio from data",
						is_independent=False, is_binned=False, units="ratio")
	obs_ratio.values = [item[2][0] for item in data]
	obs_ratio.digits = 999

	unc_data = Uncertainty("total")
	unc_data.values = [item[2][1] for item in data]
	obs_ratio.uncertainties.append(unc_data)

	
	table.add_variable(mass)
	table.add_variable(exp_dy)
	table.add_variable(obs_ratio)
	

	return table

def make_figure_13a():
	bins = Variable("BBLL Model dielectron channel", is_independent=True, is_binned=False, units="")
	bins.values = ["LL Const","LR Const", "RL Const", "RR Const", "LL Dest", "LR Dest", "RL Dest","RR Dest"]

	
	exp = Variable("Median expected limit", is_independent=False, is_binned=False, units="TeV")
	exp.values = [9.8, 8.4, 8.9, 9.2, 7.4, 8.1, 7.7, 7.9]

	obs = Variable("Observed limit", is_independent=False, is_binned=False, units="TeV")
	obs.values = [9.1, 7.9, 8.3, 8.6, 6.9, 7.5, 7.2, 7.4]


	exp1SUp = [11.0, 9.0, 9.7, 10.0, 7.9, 9.0, 8.5, 8.5]
	exp1SDown = [8.9, 7.7, 8.1, 8.4, 6.8, 7.4, 7.1, 7.2]
	exp2SUp = [12.0, 9.6, 11.0, 11.0, 8.5, 9.7, 9.3, 9.0]
	exp2SDown = [8.2, 7.2, 7.5, 7.7, 6.4, 6.9, 6.7, 6.8]
		
	exp_1sigma = Variable("Expected limit $\pm$ 1 s.d.", is_independent=False, is_binned=False, units="TeV")
	exp_1sigma.values = [9.8, 8.4, 8.9, 9.2, 7.4, 8.1, 7.7, 7.9]

	

	unc1 = Uncertainty("1 s.d.", is_symmetric=False)
	band_1sigma = []
	for i in range(0,8):
		band_1sigma.append(( -1*(exp_1sigma.values[i] - exp1SDown[i]), exp1SUp[i] - exp_1sigma.values[i]) )
	
	unc1.values = band_1sigma

	exp_1sigma.uncertainties.append(unc1)

	exp_2sigma = Variable("Expected limit $\pm$ 2 s.d.", is_independent=False, is_binned=False, units="TeV")
	exp_2sigma.values = [9.8, 8.4, 8.9, 9.2, 7.4, 8.1, 7.7, 7.9]

	unc2 = Uncertainty("2 s.d.", is_symmetric=False)
	band_2sigma = []
	for i in range(0,8):
		band_2sigma.append(( -1*(exp_2sigma.values[i] - exp2SDown[i]), exp2SUp[i] - exp_2sigma.values[i]) )

	unc2.values = band_2sigma

	exp_2sigma.uncertainties.append(unc2)


	table = Table("Limits on the energy scale Lambda for the dielectron channel")
	table.location = "Data from Figure 13."
	#table.add_image("./input/figures/Figure_013-a.pdf")
	table.description = "Lower limits on the energy scale ($\Lambda$) at 95% CL for bbll signal with different chirality and interference assumptions in the dielectron channel combining all b jet final states. The limits are obtained for $m_{ee}>300$ GeV."
	table.add_variable(bins)
	table.add_variable(obs)
	table.add_variable(exp_1sigma)
	table.add_variable(exp_2sigma)
	table.keywords["reactions"] = ["P P --> CI --> LEPTON+ LEPTON-"]
	
	return table	

def make_figure_13b():
	bins = Variable("BBLL Model dimuon channel", is_independent=True, is_binned=False, units="")
	bins.values = ["LL Const","LR Const", "RL Const", "RR Const", "LL Dest", "LR Dest", "RL Dest","RR Dest"]

	
	exp = Variable("Median expected limit", is_independent=False, is_binned=False, units="TeV")
	exp.values = [10.0, 8.7, 9.3, 9.6, 7.8, 8.7, 8.5, 8.3]

	obs = Variable("Observed limit", is_independent=False, is_binned=False, units="TeV")
	obs.values = [8.2, 7.6, 7.8, 7.9, 7.4, 8.4, 8.0, 8.0]


	exp1SUp = [11.8, 9.4, 10.2, 10.6, 8.4, 9.5, 9.3, 9.0]
	exp1SDown = [9.4, 8.0, 8.5, 8.8, 7.3, 8.0, 7.8, 7.7]
	exp2SUp = [13.2, 10.0, 11.0, 11.7, 8.9, 10.0, 10.0, 9.5]
	exp2SDown = [8.5, 7.4, 7.8, 8.0, 6.8, 7.4, 7.2, 7.2]
		
	exp_1sigma = Variable("Expected limit $\pm$ 1 s.d.", is_independent=False, is_binned=False, units="TeV")
	exp_1sigma.values = [10.0, 8.7, 9.3, 9.6, 7.8, 8.7, 8.5, 8.3]

	

	unc1 = Uncertainty("1 s.d.", is_symmetric=False)
	band_1sigma = []
	for i in range(0,8):
		band_1sigma.append(( -1*(exp_1sigma.values[i] - exp1SDown[i]), exp1SUp[i] - exp_1sigma.values[i]) )
	
	unc1.values = band_1sigma

	exp_1sigma.uncertainties.append(unc1)

	exp_2sigma = Variable("Expected limit $\pm$ 2 s.d.", is_independent=False, is_binned=False, units="TeV")
	exp_2sigma.values = [10.0, 8.7, 9.3, 9.6, 7.8, 8.7, 8.5, 8.3]

	unc2 = Uncertainty("2 s.d.", is_symmetric=False)
	band_2sigma = []
	for i in range(0,8):
		band_2sigma.append(( -1*(exp_2sigma.values[i] - exp2SDown[i]), exp2SUp[i] - exp_2sigma.values[i]) )

	unc2.values = band_2sigma

	exp_2sigma.uncertainties.append(unc2)


	table = Table("Limits on the energy scale Lambda for the dimuon channel")
	table.location = "Data from Figure 13."
	#table.add_image("./input/figures/Figure_013-b.pdf")
	table.description = "Lower limits on the energy scale ($\Lambda$) at 95% CL for bbll signal with different chirality and interference assumptions in the dimuon channel combining all b jet final states. The limits are obtained for $m_{\mu\mu}>300$ GeV."
	table.add_variable(bins)
	table.add_variable(obs)
	table.add_variable(exp_1sigma)
	table.add_variable(exp_2sigma)
	table.keywords["reactions"] = ["P P --> CI --> LEPTON+ LEPTON-"]
	
	return table	

def make_figure_13c():
	bins = Variable("BBLL Model combined channel", is_independent=True, is_binned=False, units="")
	bins.values = ["LL Const","LR Const", "RL Const", "RR Const", "LL Dest", "LR Dest", "RL Dest","RR Dest"]

	
	exp = Variable("Median expected limit", is_independent=False, is_binned=False, units="TeV")
	exp.values = [11.0, 9.3, 10.0, 10.4, 8.3, 9.4, 9.2, 8.7]

	obs = Variable("Observed limit", is_independent=False, is_binned=False, units="TeV")
	obs.values = [9.0, 8.3, 8.5, 8.6, 7.7, 8.6, 8.2, 8.2]


	exp1SUp = [12.7, 10.0, 11.0, 11.5, 9.1, 10.0, 10.0, 9.5]
	exp1SDown = [10.2, 8.7, 9.2, 9.5, 7.7, 8.6, 8.3, 8.3]
	exp2SUp = [14.2, 10.7, 12.0, 12.6, 9.6, 12.0, 11.0, 10.0]
	exp2SDown = [9.2, 8.1, 8.5, 8.7, 7.4, 7.9, 7.7, 7.8]
		
	exp_1sigma = Variable("Expected limit $\pm$ 1 s.d.", is_independent=False, is_binned=False, units="TeV")
	exp_1sigma.values = [11.0, 9.3, 10.0, 10.4, 8.3, 9.4, 9.2, 8.7]

	

	unc1 = Uncertainty("1 s.d.", is_symmetric=False)
	band_1sigma = []
	for i in range(0,8):
		band_1sigma.append(( -1*(exp_1sigma.values[i] - exp1SDown[i]), exp1SUp[i] - exp_1sigma.values[i]) )
	
	unc1.values = band_1sigma

	exp_1sigma.uncertainties.append(unc1)

	exp_2sigma = Variable("Expected limit $\pm$ 2 s.d.", is_independent=False, is_binned=False, units="TeV")
	exp_2sigma.values = [11.0, 9.3, 10.0, 10.4, 8.3, 9.4, 9.2, 8.7]

	unc2 = Uncertainty("2 s.d.", is_symmetric=False)
	band_2sigma = []
	for i in range(0,8):
		band_2sigma.append(( -1*(exp_2sigma.values[i] - exp2SDown[i]), exp2SUp[i] - exp_2sigma.values[i]) )

	unc2.values = band_2sigma

	exp_2sigma.uncertainties.append(unc2)


	table = Table("Limits on the energy scale Lambda for the combined channel")
	table.location = "Data from Figure 13."
	#table.add_image("./input/figures/Figure_013-c.pdf")
	table.description = "Lower limits on the energy scale ($\Lambda$) at 95% CL for bbll signal with different chirality and interference assumptions in the combined (dimuon+dielectron) channel combining all b jet final states. The limits are obtained for $m_{\ell\ell}>300$ GeV."
	table.add_variable(bins)
	table.add_variable(obs)
	table.add_variable(exp_1sigma)
	table.add_variable(exp_2sigma)
	table.keywords["reactions"] = ["P P --> CI --> LEPTON+ LEPTON-"]
	
	return table	

def make_figure_14_obs():
	# Observed Limits for BSLL model in 0b channel  
	# It has three columns with dielectron channel and dimuon channel
	data = [
		[1,   0.01021072,  0.009508905],	
		[2,   0.01094965,  0.008546409],
		[3,   0.0109817,   0.009046931],
		[4,   0.01079408,  0.009232464],
        [5,   0.01060404,  0.009235527],
        [6,   0.01056393,  0.009167818],
	]
	table = Table("Observed upper limits for BSLL model in 0b channel")
	table.location = "Data from Figure 14 obs"
	table.description = """Observed upper limits on the product of the production cross section and the branching fraction for the bsll signal in the dielectron and dimuon channels for 0 b-tagged jets."""
	# First variable/column ---> Mass
	bins = Variable("\Lambda/g_{*}", is_independent=True, is_binned=False, units="TeV")
	bins.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	obs_ee = Variable("Observed limit dielectron 0 b-tagged jets",
					  is_independent=False, is_binned=False, units="pb")
	obs_ee.values = [item[1] for item in data]
	obs_ee.digits = 999

    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	obs_mumu = Variable("Observed limit dimuon 0 b-tagged jets",
						is_independent=False, is_binned=False, units="pb")
	obs_mumu.values = [item[2] for item in data]
	obs_mumu.digits = 999

	
	table.add_variable(bins)
	table.add_variable(obs_ee)
	table.add_variable(obs_mumu)
	

	return table


def make_figure_15_obs():
	# Observed Limits for BSLL model in 1b channel  
	# It has three columns with dielectron channel and dimuon channel
	data = [
		[1,   0.01331075,   0.01584829],	
		[2,   0.01409038,   0.01581532],
		[3,   0.01348617,   0.01625835],
		[4,   0.01306535,   0.01552263],
        [5,   0.0135571,    0.01540512],
        [6,   0.01408687,   0.01533086],
	]
	table = Table("Observed upper limits for BSLL model in 1b channel")
	table.location = "Data from Figure 15 obs"
	table.description = """Observed upper limits on the product of the production cross section and the branching fraction for the bsll signal in the dielectron and dimuon channels for 1 b-tagged jets."""
	# First variable/column ---> Mass
	bins = Variable("\Lambda/g_{*}", is_independent=True, is_binned=False, units="TeV")
	bins.values = [item[0] for item in data]

	# Second variable/column ---> Number of observed events
	obs_ee = Variable("Observed limit dielectron 1 b-tagged jets",
					  is_independent=False, is_binned=False, units="pb")
	obs_ee.values = [item[1] for item in data]
	obs_ee.digits = 999

    
	# Third variable/column ---> Total Number of predicted events from MC + data driven QCD
	obs_mumu = Variable("Observed limit dimuon 1 b-tagged jets",
						is_independent=False, is_binned=False, units="pb")
	obs_mumu.values = [item[2] for item in data]
	obs_mumu.digits = 999

	
	table.add_variable(bins)
	table.add_variable(obs_ee)
	table.add_variable(obs_mumu)
	

	return table

def make_figure_14_exp():
	# Expected Limits for BSLL model in 0b channel  
	# It has three columns with dielectron channel and dimuon channel

	points_exp_ele = [0.01330477, 0.01277316, 0.01242044, 0.01218401, 0.01222481, 0.01207134]
	points_2s_ele =  [(0.03052934, -0.005748546), (0.026047, -0.006116763), (0.02376186, -0.006404438), (0.02302891, -0.006559447), (0.02298133, -0.006651113), (0.022972, -0.006471413) ] 
	points_1s_ele =  [(0.02106373, -0.008462603), (0.01841087, -0.008640938), (0.01775884, -0.008807367), (0.01691305, -0.008788887), (0.01705346, -0.00875852), (0.01729973, -0.008724453) ]

	points_exp_mu = [0.01199218, 0.0114619, 0.01149917, 0.01130076, 0.01133589, 0.01136481]  
	points_2s_mu = [ (0.02524509, -0.004899899), (0.02191297, -0.005524587), (0.02156768, -0.00601598), (0.02129686, -0.005965296), (0.02185303, -0.006098288), (0.02190805, -0.006106613) ]
	points_1s_mu = [ (0.01809581, -0.007485923), (0.01688877, -0.007783844), (0.01612449, -0.008115954), (0.01567705, -0.008013734), (0.01600634, -0.008176043), (0.01595336, -0.008082578) ]


	table = Table("Expected upper limits for BSLL model in 0b channel")
	table.location = "Data from Figure 14 exp"
	table.description = """Expected upper limits on the product of the production cross section and the branching fraction for the bsll signal in the dielectron and dimuon channels for 0 b-tagged jets."""
	# First variable/column ---> Mass
	bins = Variable("\Lambda/g_{*}", is_independent=True, is_binned=False, units="TeV")
	bins.values = [1, 2, 3, 4, 5, 6]

	# 1 Sigmaa
	exp_1s_ele = Variable("Expected limit dielectron $\pm$ 1 s.d.", is_independent=False, is_binned=False, units="pb")
	exp_1s_ele.values = points_exp_ele

	unc1_ele = Uncertainty("1 s.d.", is_symmetric=False)
	unc1_ele.values = points_1s_ele

	exp_1s_ele.uncertainties.append(unc1_ele)

	# 2 Sigma
	exp_2s_ele = Variable("Expected limit dielectron $\pm$ 2 s.d.", is_independent=False, is_binned=False, units="pb")
	exp_2s_ele.values = points_exp_ele

	unc2_ele = Uncertainty("2 s.d.", is_symmetric=False)
	unc2_ele.values = points_2s_ele

	exp_2s_ele.uncertainties.append(unc2_ele)


	# 1 Sigmaa
	exp_1s_mu = Variable("Expected limit dimuon $\pm$ 1 s.d.", is_independent=False, is_binned=False, units="pb")
	exp_1s_mu.values = points_exp_mu

	unc1_mu = Uncertainty("1 s.d.", is_symmetric=False)
	unc1_mu.values = points_1s_mu

	exp_1s_mu.uncertainties.append(unc1_mu)

	# 2 Sigma
	exp_2s_mu = Variable("Expected limit dimuon $\pm$ 2 s.d.", is_independent=False, is_binned=False, units="pb")
	exp_2s_mu.values = points_exp_mu

	unc2_mu = Uncertainty("2 s.d.", is_symmetric=False)
	unc2_mu.values = points_2s_mu

	exp_2s_mu.uncertainties.append(unc2_mu)

	table.add_variable(bins)
	table.add_variable(exp_1s_ele)
	table.add_variable(exp_2s_ele)
	table.add_variable(exp_1s_mu)
	table.add_variable(exp_2s_mu)

	

	return table


def make_figure_15_exp():
	# Expected Limits for BSLL model in 1b channel  
	# It has three columns with dielectron channel and dimuon channel

	points_exp_ele = [0.00920813, 0.009517323, 0.009126625, 0.009016467, 0.009335338, 0.009155997]
	points_2s_ele =  [(0.01803157, -0.00503828), (0.0185714, -0.005149029), (0.01822164, -0.004879901), (0.01774499, -0.005003189), (0.01818455, -0.005138607), (0.01794392, -0.005011969) ] 
	points_1s_ele =  [(0.01303578, -0.006564217), (0.01367559, -0.006743422), (0.01313155, -0.006463733), (0.01294186, -0.006483535), (0.01312229, -0.006685442), (0.0131514, -0.006578676) ]

	points_exp_mu = [0.00770541, 0.007425584, 0.007579199, 0.007524161, 0.00743325, 0.007508719]  
	points_2s_mu =  [(0.01510267, -0.004046263), (0.01436232, -0.003968979), (0.0150655, -0.004120201), (0.01480178, -0.003964796), (0.01495488, -0.003898099), (0.01516958, -0.003992393) ] 
	points_1s_mu =  [(0.01094257, -0.005434429), (0.0105785, -0.00524278), (0.01090025, -0.005349777), (0.01075752, -0.005317272), (0.01073665, -0.005251718), (0.01098412, -0.005294441) ] 


	table = Table("Expected upper limits for BSLL model in 1b channel")
	table.location = "Data from Figure 15 exp"
	table.description = """Expected upper limits on the product of the production cross section and the branching fraction for the bsll signal in the dielectron and dimuon channels for 1 b-tagged jets."""
	# First variable/column ---> Mass
	bins = Variable("\Lambda/g_{*}", is_independent=True, is_binned=False, units="TeV")
	bins.values = [1, 2, 3, 4, 5, 6]

	# 1 Sigmaa
	exp_1s_ele = Variable("Expected limit dielectron $\pm$ 1 s.d.", is_independent=False, is_binned=False, units="pb")
	exp_1s_ele.values = points_exp_ele

	unc1_ele = Uncertainty("1 s.d.", is_symmetric=False)
	unc1_ele.values = points_1s_ele

	exp_1s_ele.uncertainties.append(unc1_ele)

	# 2 Sigma
	exp_2s_ele = Variable("Expected limit dielectron $\pm$ 2 s.d.", is_independent=False, is_binned=False, units="pb")
	exp_2s_ele.values = points_exp_ele

	unc2_ele = Uncertainty("2 s.d.", is_symmetric=False)
	unc2_ele.values = points_2s_ele

	exp_2s_ele.uncertainties.append(unc2_ele)


	# 1 Sigmaa
	exp_1s_mu = Variable("Expected limit dimuon $\pm$ 1 s.d.", is_independent=False, is_binned=False, units="pb")
	exp_1s_mu.values = points_exp_mu

	unc1_mu = Uncertainty("1 s.d.", is_symmetric=False)
	unc1_mu.values = points_1s_mu

	exp_1s_mu.uncertainties.append(unc1_mu)

	# 2 Sigma
	exp_2s_mu = Variable("Expected limit dimuon $\pm$ 2 s.d.", is_independent=False, is_binned=False, units="pb")
	exp_2s_mu.values = points_exp_mu

	unc2_mu = Uncertainty("2 s.d.", is_symmetric=False)
	unc2_mu.values = points_2s_mu

	exp_2s_mu.uncertainties.append(unc2_mu)

	table.add_variable(bins)
	table.add_variable(exp_1s_ele)
	table.add_variable(exp_2s_ele)
	table.add_variable(exp_1s_mu)
	table.add_variable(exp_2s_mu)

	

	return table

##add covariance matrices

table_10 = make_table_10()
table_11 = make_table_11()
table_12 = make_table_12()
table_13 = make_table_13()
table_14 = make_table_14()
table_15 = make_table_15()

figure_12a = make_figure_12a()
figure_12b = make_figure_12b()
figure_13a = make_figure_13a()
figure_13b = make_figure_13b()
figure_13c = make_figure_13c()

figure_14_obs = make_figure_14_obs()
figure_15_obs = make_figure_15_obs()

figure_14_exp = make_figure_14_exp()
figure_15_exp = make_figure_15_exp()


submission = Submission()
submission.read_abstract("input/abstract.txt")

#add links as well
submission.tables.append(table_10)
submission.tables.append(table_11)
submission.tables.append(table_12)
submission.tables.append(table_13)
submission.tables.append(table_14)
submission.tables.append(table_15)
submission.tables.append(figure_12a)
submission.tables.append(figure_12b)
submission.tables.append(figure_13a)
submission.tables.append(figure_13b)
submission.tables.append(figure_13c)

submission.tables.append(figure_14_obs)
submission.tables.append(figure_15_obs)

submission.tables.append(figure_14_exp)
submission.tables.append(figure_15_exp)

# Write output
submission.create_files("./submission/")


