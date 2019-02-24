from expression import *
class Regle:
    def __init__(self,id=0,premisses=[],conclusion=[],):
        self.id = None
        self.premisses = None
        self.conclusion = None
    def __str__(self):
        toReturn='id--'+str(self.id)+'--prem--'
        for prem in self.premisses :
            toReturn+=(prem+'--')
        toReturn+=('--conc--'+self.conclusion)
        return toReturn

class Fait:
    def __init__(self, fait=None):
        self.fait = fait
