from HiggsAnalysis.CombinedLimit.PhysicsModel import *

class CIInterference(PhysicsModel):
    def __init__(self):
        PhysicsModel.__init__(self)

    def doParametersOfInterest(self):
        self.modelBuilder.doVar("r[1,0,10000]")
        self.modelBuilder.doSet('POI','r')
 
        self.modelBuilder.factory_( "expr::sig_func(\"@0-sqrt(@0)\", r)")
        self.modelBuilder.factory_(  "expr::b_func(\"1-sqrt(@0)\", r)")
        self.modelBuilder.factory_(  "expr::sbi_func(\"sqrt(@0)\", r)")            

        self.modelBuilder.out.Print()

    def getYieldScale(self,bin,process):
        if process == "sig": return "sig_func"
        elif process == "DY": return "b_func"
        elif process == "int": return "sbi_func"
        else:
            return 1

CIInterference = CIInterference()
