"""
Base class for electron beams.

This class is intentionally shorten for simplicity.
Usually we would need to consider also the electron distribution within the beam.
"""

from syned.syned_object import SynedObject
import scipy.constants as codata
import numpy

class ElectronBeam(SynedObject):
    def __init__(self,
                 energy_in_GeV = 1.0,
                 energy_spread = 0.0,
                 current = 0.1,
                 number_of_bunches = 400,
                 moment_xx=0.0,
                 moment_xxp=0.0,
                 moment_xpxp=0.0,
                 moment_yy=0.0,
                 moment_yyp=0.0,
                 moment_ypyp=0.0):


        self._energy_in_GeV       = energy_in_GeV
        self._energy_spread       = energy_spread
        self._current             = current
        self._number_of_bunches   = number_of_bunches

        self._moment_xx           = moment_xx
        self._moment_xxp          = moment_xxp
        self._moment_xpxp         = moment_xpxp
        self._moment_yy           = moment_yy
        self._moment_yyp          = moment_yyp
        self._moment_ypyp         = moment_ypyp

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("energy_in_GeV"      , "Electron beam energy"                  , "GeV" ),
                    ("energy_spread"      , "Electron beam energy spread (relative)", ""    ),
                    ("current"            , "Electron beam current"                 , "A"   ),
                    ("number_of_bunches"  , "Number of bunches"                     , ""    ),
                    ("moment_xx"          , "Moment (spatial^2, horizontal)"        , "m^2" ),
                    ("moment_xxp"         , "Moment (spatial-angular, horizontal)"  , "m"   ),
                    ("moment_xpxp"        , "Moment (angular^2, horizontal)"        , ""    ),
                    ("moment_yy"          , "Moment (spatial^2, vertical)"          , "m^2" ),
                    ("moment_yyp"         , "Moment (spatial-angular, vertical)"    , "m"   ),
                    ("moment_ypyp"        , "Moment (angular^2, vertical)"          , ""    ),
            ] )



    #
    # initializares
    #
    @classmethod
    def initialize_as_pencil_beam(cls, energy_in_GeV = 1.0, energy_spread = 0.0, current = 0.1):
        return ElectronBeam(energy_in_GeV=energy_in_GeV,
                            energy_spread=energy_spread,
                            current=current,
                            number_of_bunches=1)


    #
    # useful getters
    #
    def get_sigmas_real_space(self):
        return numpy.sqrt(self._moment_xx),numpy.sqrt(self._moment_yy)

    def get_sigmas_divergence_space(self):
        return numpy.sqrt(self._moment_xpxp),numpy.sqrt(self._moment_ypyp)

    def get_sigmas_horizontal(self):
        return numpy.sqrt(self._moment_xx),numpy.sqrt(self._moment_xpxp)

    def get_sigmas_vertical(self):
        return numpy.sqrt(self._moment_yy),numpy.sqrt(self._moment_ypyp)

    def get_sigmas_all(self):
        return numpy.sqrt(self._moment_xx),numpy.sqrt(self._moment_xpxp),numpy.sqrt(self._moment_yy),numpy.sqrt(self._moment_ypyp)

    #
    # setters
    #
    def set_sigmas_real_space(self,sigma_x=0.0,sigma_y=0.0):
        self._moment_xx = sigma_x**2
        self._moment_yy = sigma_y**2

    def set_sigmas_divergence_space(self,sigma_xp=0.0,sigma_yp=0.0):
        self._moment_xpxp = sigma_xp**2
        self._moment_ypyp = sigma_yp**2

    def set_sigmas_horizontal(self,sigma_x=0.0,sigma_xp=0.0):
        self._moment_xx = sigma_x**2
        self._moment_xpxp = sigma_xp**2

    def set_sigmas_vertical(self,sigma_y=0.0,sigma_yp=0.0):
        self._moment_yy = sigma_y**2
        self._moment_ypyp = sigma_yp**2

    def set_sigmas_all(self,sigma_x=0.0,sigma_xp=0.0,sigma_y=0.0,sigma_yp=0.0):
        self._moment_xx = sigma_x**2
        self._moment_xpxp = sigma_xp**2
        self._moment_yy = sigma_y**2
        self._moment_ypyp = sigma_yp**2

    def set_energy_from_gamma(self, gamma):
        self._energy_in_GeV = (gamma / 1e9) * (codata.m_e *  codata.c**2 / codata.e)

    #
    # some easy calculations
    #
    def gamma(self):
        return self.lorentz_factor()

    def lorentz_factor(self):
        return 1e9*self._energy_in_GeV / (codata.m_e *  codata.c**2 / codata.e)

    def electron_speed(self):
        return numpy.sqrt(1.0 - 1.0 / self.lorentz_factor() ** 2)



    #
    #dictionnary interface, info etc
    #

if __name__ == "__main__":

    a = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=6.0,current=0.2)


#    a.to_dictionary()


    # fd = a.to_full_dictionary()
    # dict = a.to_dictionary()
    #
    # print(dict)
    #
    # for key in fd:
    #     print(key,fd[key][0])
    #
    # for key in fd:
    #     print(key,dict[key])
    #
    # print(a.keys())
    # print(a.info())
