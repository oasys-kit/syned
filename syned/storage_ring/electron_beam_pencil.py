from syned.storage_ring.electron_beam import ElectronBeam

class ElectronBeamPencil(ElectronBeam):
    def __init__(self, energy_in_GeV, energy_spread, current):
        ElectronBeam.__init__(self,
                              energy_in_GeV=energy_in_GeV,
                              energy_spread=energy_spread,
                              current=current,
                              electrons_per_bunch=1,
                              moment_xx=0.0,
                              moment_xxp=0.0,
                              moment_xpxp=0.0,
                              moment_yy=0.0,
                              moment_yyp=0.0,
                              moment_ypyp=0.0)

