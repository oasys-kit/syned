"""
Base class for electron beams.
Every electron beam can carry settings, i.e. inherits DriverSettingManager.

This class is intentionally shorten for simplicity.
Usually we would need to consider also the electron distribution within the beam.
"""

from collections import OrderedDict

class ElectronBeam(object):
    def __init__(self,
                 energy_in_GeV = 1.0,
                 energy_spread = 0.0,
                 current = 0.1,
                 electrons_per_bunch = 400,
                 moment_xx=0.0,
                 moment_xxp=0.0,
                 moment_xpxp=0.0,
                 moment_yy=0.0,
                 moment_yyp=0.0,
                 moment_ypyp=0.0):


        self._energy_in_GeV       = energy_in_GeV
        self._energy_spread       = energy_spread
        self._current             = current
        self._electrons_per_bunch = electrons_per_bunch

        self._moment_xx           = moment_xx
        self._moment_xxp          = moment_xxp
        self._moment_xpxp         = moment_xpxp
        self._moment_yy           = moment_yy
        self._moment_yyp          = moment_yyp
        self._moment_ypyp         = moment_ypyp

    # useful methods
    def gamma(self):
        #TODO: get the physical constant from a central repository
        return self._energy_in_GeV/0.51099890221e-03 # Relative Energy

    def to_dictionary(self):
        #returns a dictionary with the variable names as keys, and a tuple with value, unit and doc string
        mytuple = [ ("energy_in_GeV"      ,( self._energy_in_GeV       ,"GeV",  "Electron beam energy"                   ) ),
                    ("energy_spread"      ,( self._energy_spread       ,""   ,  "Electron beam energy spread (relative)" ) ),
                    ("current"            ,( self._current             ,"A"  ,  "Electron beam current"                  ) ),
                    ("electrons_per_bunch",( self._electrons_per_bunch ,""   ,  "Number of electrons per bunch"          ) ),
                    ("moment_xx"          ,( self._moment_xx           ,"m^2",  "Moment (spatial^2, horizontal)"         ) ),
                    ("moment_xxp"         ,( self._moment_xxp          ,"m"  ,  "Moment (spatial-angular, horizontal)"   ) ),
                    ("moment_xpxp"        ,( self._moment_xpxp         ,""   ,  "Moment (angular^2, horizontal)"         ) ),
                    ("moment_yy"          ,( self._moment_yy           ,"m^2",  "Moment (spatial^2, vertical)"           ) ),
                    ("moment_yyp"         ,( self._moment_yyp          ,"m"  ,  "Moment (spatial-angular, vertical)"     ) ),
                    ("moment_ypyp"        ,( self._moment_ypyp         ,""   ,  "Moment (angular^2, vertical)"           ) )]
        return(OrderedDict(mytuple))

    @classmethod
    def initialize_as_pencil_beam(cls, energy_in_GeV = 1.0, energy_spread = 0.0, current = 0.1):
        return ElectronBeam(energy_in_GeV=energy_in_GeV,
                            energy_spread=energy_spread,
                            current=current,
                            electrons_per_bunch=1)