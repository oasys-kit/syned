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
                 number_of_bunches = 400, # TODO: not used, to be removed (with care!)
                 moment_xx=0.0,
                 moment_xxp=0.0,
                 moment_xpxp=0.0,
                 moment_yy=0.0,
                 moment_yyp=0.0,
                 moment_ypyp=0.0):
        """
        Defines an electron beam at a given point of the storage ring.

        Parameters
        ----------
        energy_in_GeV : float, optional
            The electron energy in GeV.
        energy_spread : float, optional
            The electron energy spread (in a fraction of the energy_in_GeV).
        current : float, optional
            The electron beam current intensity in A.
        number_of_bunches : float, optional
            The number of bunches in the storage ring.
        moment_xx : float, optional
            The <x^2> moment.
        moment_xxp : float, optional
            The <x x'> moment.
        moment_xpxp : float, optional
            The <x'^2> moment.
        moment_yy : float, optional
            The <y^2> moment.
        moment_yyp : float, optional
            The <y y'> moment.
        moment_ypyp : float, optional
            The <y'^2> moment.
        """


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
    def initialize_as_pencil_beam(cls, energy_in_GeV = 1.0, energy_spread = 0.0, current = 0.1, **params):
        """
        Creates an electron pencil beam.

        Parameters
        ----------
        energy_in_GeV : float, optional
            The electron energy in GeV.
        energy_spread : float, optional
            The electron energy spread (in a fraction of the energy_in_GeV).
        current : float, optional
            The electron beam current intensity in A.
        params :
            other keyword parameters accepted by ElectronBeam (if used, the result may not be a pencil beam.)

        Returns
        -------
        instance of ElectronBeam

        """
        return cls(energy_in_GeV=energy_in_GeV,
                   energy_spread=energy_spread,
                   current=current,
                   number_of_bunches=1,
                   **params)


    #
    # useful getters
    #
    def get_sigmas_real_space(self):
        """
        Returns the sigmas in real space.

        Returns
        -------
        tuple
            (sigma_x, sigma_y)

        """
        return numpy.sqrt(self._moment_xx),\
               numpy.sqrt(self._moment_yy)

    def get_sigmas_divergence_space(self):
        """
        Returns the sigmas in divergence (angle) space.

        Returns
        -------
        tuple
            (sigma_x', sigma_y')

        """
        return numpy.sqrt(self._moment_xpxp),\
               numpy.sqrt(self._moment_ypyp)

    def get_sigmas_horizontal(self):
        """
        Returns the sigmas in horizontal direction.

        Returns
        -------
        tuple
            (sigma_x, sigma_x')

        """
        return numpy.sqrt(self._moment_xx),\
               numpy.sqrt(self._moment_xpxp)

    def get_sigmas_vertical(self):
        """
        Returns the sigmas in vertical direction.

        Returns
        -------
        tuple
            (sigma_y, sigma_y')

        """
        return numpy.sqrt(self._moment_yy),\
               numpy.sqrt(self._moment_ypyp)

    def get_sigmas_all(self):
        """
        Returns all sigmas.

        Returns
        -------
        tuple
            (sigma_x, sigma_x', sigma_y, sigma_y')

        """
        return numpy.sqrt(self._moment_xx),\
               numpy.sqrt(self._moment_xpxp),\
               numpy.sqrt(self._moment_yy),\
               numpy.sqrt(self._moment_ypyp)

    def get_moments_horizontal(self):
        """
        Returns the moments in the horizontal direction.

        Returns
        -------
        tuple
            ( <x^2>, <x x'>, <x'^2>)

        """
        return self._moment_xx, self._moment_xxp, self._moment_xpxp

    def get_moments_vertical(self):
        """
        Returns the moments in the vertical direction.

        Returns
        -------
        tuple
            ( <y^2>, <y y'>, <y'^2>)

        """
        return self._moment_yy, self._moment_yyp, self._moment_ypyp

    def get_moments_all(self):
        """
        Returns all moments.

        Returns
        -------
        tuple
            ( <x^2>, <x x'>, <x'^2>, <y^2>, <y y'>, <y'^2>)

        """
        return self._moment_xx, self._moment_xxp, self._moment_xpxp, self._moment_yy, self._moment_yyp, self._moment_ypyp

    def get_twiss_no_dispersion_horizontal(self):
        """
        Returns the Twiss parameters in horizontal direction.
        (The energy disperion is not considered.)

        Returns
        -------
        tuple
            (emittance_x, alpha_x, beta_x).

        """
        emittance_x = numpy.sqrt(self._moment_xx * self._moment_xpxp - self._moment_xxp**2)
        alpha_x = -self._moment_xxp / emittance_x
        beta_x = self._moment_xx / emittance_x
        return emittance_x, alpha_x, beta_x

    def get_twiss_no_dispersion_vertical(self):
        """
        Returns the Twiss parameters in vertical direction.
        (The energy disperion is not considered.)

        Returns
        -------
        tuple
            (emittance_y, alpha_y, beta_y).

        """
        emittance_y = numpy.sqrt(self._moment_yy * self._moment_ypyp - self._moment_yyp**2)
        alpha_y = -self._moment_yyp / emittance_y
        beta_y = self._moment_yy / emittance_y
        return emittance_y,alpha_y,beta_y

    def get_twiss_no_dispersion_all(self):
        """
        Returns all Twiss parameters.
        (The energy disperion is not considered.)

        Returns
        -------
        tuple
            (emittance_x, alpha_x, beta_x, emittance_y, alpha_y, beta_y).

        """
        ex, ax, bx =  self.get_twiss_no_dispersion_horizontal()
        ey, ay, by = self.get_twiss_no_dispersion_vertical()
        return ex, ax, bx, ey, ay, by

    def energy(self):
        """
        Returns the electron energy in GeV.

        Returns
        -------
        float

        """
        return self._energy_in_GeV

    def current(self):
        """
        Returns the electron current in A.

        Returns
        -------
        float

        """
        return self._current

    #
    # setters
    #
    def set_sigmas_real_space(self, sigma_x=0.0, sigma_y=0.0):
        """
        Sets the electron beam parameters in real space from the sigma values.

        Parameters
        ----------
        sigma_x : float, optional
            The sigma in horizontal direction.
        sigma_y : float, optional
            The sigma in vertical direction.

        """
        self._moment_xx = sigma_x**2
        self._moment_yy = sigma_y**2

    def set_sigmas_divergence_space(self, sigma_xp=0.0, sigma_yp=0.0):
        """
        Sets the electron beam parameters in divergence space from the sigma values.

        Parameters
        ----------
        sigma_xp : float, optional
            The sigma in horizontal direction.
        sigma_yp : float, optional
            The sigma in vertical direction.

        """
        self._moment_xpxp = sigma_xp**2
        self._moment_ypyp = sigma_yp**2

    def set_sigmas_horizontal(self, sigma_x=0.0, sigma_xp=0.0):
        """
        Sets the electron beam parameters from the sigma values in horizontal direction.

        Parameters
        ----------
        sigma_x : float, optional
            The sigma in real space.
        sigma_xp : float, optional
            The sigma in divergence space.

        """
        self._moment_xx = sigma_x**2
        self._moment_xpxp = sigma_xp**2

    def set_sigmas_vertical(self, sigma_y=0.0, sigma_yp=0.0):
        """
        Sets the electron beam parameters from the sigma values in vertical direction.

        Parameters
        ----------
        sigma_y : float, optional
            The sigma in real space.
        sigma_yp : float, optional
            The sigma in divergence space.

        """
        self._moment_yy = sigma_y**2
        self._moment_ypyp = sigma_yp**2

    def set_sigmas_all(self, sigma_x=0.0, sigma_xp=0.0, sigma_y=0.0, sigma_yp=0.0):
        """
        Sets the electron beam parameters from the sigma values in both horizontal and vertical direction.

        Parameters
        ----------
        sigma_x : float, optional
            The sigma in real space (horizontal).
        sigma_xp : float, optional
            The sigma in divergence space (horizontal).
        sigma_y : float, optional
            The sigma in real space (vertical).
        sigma_yp : float, optional
            The sigma in divergence space (vertical).

        """
        self._moment_xx = sigma_x**2
        self._moment_xpxp = sigma_xp**2
        self._moment_yy = sigma_y**2
        self._moment_ypyp = sigma_yp**2

    def set_energy_from_gamma(self, gamma):
        """
        Sets the electron energy from the gamma value (Lorentz factor).

        Parameters
        ----------
        gamma : float

        """
        self._energy_in_GeV = (gamma / 1e9) * (codata.m_e *  codata.c**2 / codata.e)

    def set_moments_horizontal(self, moment_xx, moment_xxp, moment_xpxp):
        """
        Sets the moments in the horizontal direction.

        Parameters
        ----------
        moment_xx : float
            The <x^2> moment.
        moment_xxp : float
            The <x x'> moment.
        moment_xpxp : float,
            The <x'^2> moment.

        """
        self._moment_xx   = moment_xx
        self._moment_xxp  = moment_xxp
        self._moment_xpxp = moment_xpxp

    def set_moments_vertical(self, moment_yy, moment_yyp, moment_ypyp):
        """
        Sets the moments in the vertical direction.

        Parameters
        ----------
        moment_yy : float
            The <y^2> moment.
        moment_yyp : float
            The <y y'> moment.
        moment_ypyp : float
            The <y'^2> moment.

        """
        self._moment_yy   = moment_yy
        self._moment_yyp  = moment_yyp
        self._moment_ypyp = moment_ypyp

    def set_moments_all(self, moment_xx, moment_xxp, moment_xpxp, moment_yy, moment_yyp, moment_ypyp):
        """
        Sets the moments.

        Parameters
        ----------
        moment_xx : float
            The <x^2> moment.
        moment_xxp : float
            The <x x'> moment.
        moment_xpxp : float,
            The <x'^2> moment.
        moment_yy : float
            The <y^2> moment.
        moment_yyp : float
            The <y y'> moment.
        moment_ypyp : float
            The <y'^2> moment.

        """
        self.set_moments_horizontal(moment_xx,moment_xxp,moment_xpxp)
        self.set_moments_vertical(moment_yy,moment_yyp,moment_ypyp)

    def set_twiss_horizontal(self, emittance_x, alpha_x, beta_x, eta_x=0, etap_x=0):
        """
        Sets the electron beam parameters from the Twiss values in the horizontal direction.

        Parameters
        ----------
        emittance_x : float
            The emittance value in horizontal.
        alpha_x : float
            The alpha value in horizontal.
        beta_x : float
            The beta value in horizontal.
        eta_x : float, optional
            The eta value in horizontal.
        etap_x : float, optional
            The eta' value in horizontal.

        """
        gamma_x = (1 + alpha_x**2) / beta_x
        self._moment_xx   = beta_x   * emittance_x + eta_x**2 * self._energy_spread**2
        self._moment_xxp  = -alpha_x * emittance_x + eta_x * etap_x * self._energy_spread ** 2
        self._moment_xpxp = gamma_x  * emittance_x + etap_x**2 * self._energy_spread ** 2

    def set_twiss_vertical(self, emittance_y, alpha_y, beta_y, eta_y=0, etap_y=0):
        """
        Sets the electron beam parameters from the Twiss values in the vertical direction.

        Parameters
        ----------
        emittance_y : float
            The emittance value in vertical.
        alpha_x : float
            The alpha value in vertical.
        beta_x : float
            The beta value in vertical.
        eta_x : float, optional
            The eta value.
        etap_x : float, optional
            The eta' value in vertical.

        """
        gamma_y = (1 + alpha_y**2) / beta_y
        self._moment_yy   = beta_y   * emittance_y + eta_y**2 * self._energy_spread**2
        self._moment_yyp  = -alpha_y * emittance_y + eta_y * etap_y * self._energy_spread ** 2
        self._moment_ypyp = gamma_y  * emittance_y + etap_y**2 * self._energy_spread ** 2

    def set_twiss_all(self, emittance_x, alpha_x, beta_x, eta_x, etap_x,
                           emittance_y, alpha_y, beta_y, eta_y, etap_y):
        """
        Sets the electron beam parameters from the Twiss values.

        Parameters
        ----------
        emittance_x : float
            The emittance value in horizontal.
        alpha_x : float
            The alpha value in horizontal.
        beta_x : float
            The beta value in horizontal.
        eta_x : float
            The eta value in horizontal.
        etap_x : float
            The eta' value in horizontal.
        emittance_y : float
            The emittance value in vertical.
        alpha_x : float
            The alpha value in vertical.
        beta_x : float
            The beta value in vertical.
        eta_x : float
            The eta value.
        etap_x : float
            The eta' value in vertical.

        """
        self.set_twiss_horizontal(emittance_x,alpha_x,beta_x,eta_x,etap_x)
        self.set_twiss_vertical(emittance_y,alpha_y,beta_y,eta_y,etap_y)

    #
    # some easy calculations
    #
    def gamma(self):
        """
        returns the Gamma or Lorentz factor.

        Returns
        -------
        float

        """
        return self.lorentz_factor()

    def lorentz_factor(self):
        """
        returns the Gamma or Lorentz factor.

        Returns
        -------
        float

        """
        return 1e9 * self._energy_in_GeV / (codata.m_e *  codata.c**2 / codata.e)

    def electron_speed(self):
        """
        Returns the electron velocity in c units.

        Returns
        -------
        float

        """
        return numpy.sqrt(1.0 - 1.0 / self.lorentz_factor() ** 2)



    #
    #dictionnary interface, info etc
    #

if __name__ == "__main__":

    a = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=2.0,current=0.5, energy_spread=0.00095)

    a.set_twiss_horizontal(70e-12, 0.827, 0.34, 0, 0 ) #0.0031, -0.06)
    a.set_twiss_vertical(  70e-12, -10.7, 24.26, 0, 0.0)

    print("twiss data: 70e-12, 0.827, 0.34, 70e-12, -10.7, 24.26,")
    print("sigmas: ",a.get_sigmas_all())
    print("moments: ",a.get_moments_all())
    print("twiss: ",a.get_twiss_no_dispersion_all())


    s = a.get_sigmas_all()
    a.set_sigmas_all(s[0],s[1],s[2],s[3])

    print("\n\nsigmas: ",a.get_sigmas_all())
    print("moments: ",a.get_moments_all())
    print("twiss: ",a.get_twiss_no_dispersion_all())


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
