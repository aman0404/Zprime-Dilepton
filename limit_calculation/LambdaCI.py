from HiggsAnalysis.CombinedLimit.PhysicsModel import *

class CIlambda(PhysicsModel):
    def __init__(self):
        PhysicsModel.__init__(self)

    def doParametersOfInterest(self):
        self.modelBuilder.doVar('Lambda[0,0,50000]')
        self.modelBuilder.doSet('POI','Lambda')
            
        self.modelBuilder.factory_('expr::calcLambda("1./@0 * 1./@0 + 1./@0 * 1./@0 * 1./@0 * 1./@0",Lambda)')

        self.modelBuilder.out.Print()

    def getYieldScale(self,bin,process):

        return 'calcLambda' if self.DC.isSignal[process] else 1

CIlambda = CIlambda()
