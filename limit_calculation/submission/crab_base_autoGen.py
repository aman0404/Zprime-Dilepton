import os
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'limits_m1000_negRL_3M_exp_singleBin_combB_8_20240921_125802'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True


config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'dummyPSet.py'
config.JobType.scriptExe= 'runLimits'
config.JobType.scriptArgs= ['dummy=dummy.py','tarFile=gridPack.tar','outputTag=m1000_negRL_3M_exp_singleBin_combB','mass=8','nIter=3000000','nToys=10','expected=1','config=mumu_2LB','inject=0']
config.JobType.inputFiles= ['gridPack.tar',os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/combine','FrameworkJobReport.xml']
config.JobType.outputFiles= ['expectedLimit_mumu_2LB_m1000_negRL_3M_exp_singleBin_combB_8.root']
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 5000

config.section_("Data")
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = 500
config.Data.outputPrimaryDataset = 'm1000_negRL_3M_exp_singleBin_combB'
config.Data.outputDatasetTag = 'test'
config.Data.outLFNDirBase = '/store/user/amkaur/limits/mumu_2LB'
 
config.section_("Site")
config.Site.storageSite = "T2_US_Purdue"
#config.Site.blacklist = ["T3_US_UCR","T3_MX_Cinvestav","T3_TW_NTU_HEP"]
config.section_("User")
