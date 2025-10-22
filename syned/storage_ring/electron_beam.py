"""
Base class for electron beams.

This class is intentionally shorten for simplicity.
Usually we would need to consider also the electron distribution within the beam.
"""
import scipy.constants as codata
import numpy
import warnings

from syned.util import deprecated
from syned.syned_object import SynedObject


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
                 moment_ypyp=0.0,
                 dispersion_x=0.0,
                 dispersion_y=0.0,
                 dispersionp_x=0.0,
                 dispersionp_y=0.0
                 ):
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
        dispersion_x : float, optional
            The eta_x parameter, spatial dispersion
        dispersion_y : float, optional
            The eta_y parameter, spatial dispersion
        dispersionp_x : float, optional
            The eta'_x parameter, angular dispersion
        dispersionp_y : float, optional
            The eta'_y parameter, angular dispersion
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
        self._dispersion_x        = dispersion_x
        self._dispersion_y        = dispersion_y
        self._dispersionp_x       = dispersionp_x
        self._dispersionp_y       = dispersionp_y

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
                    ("dispersion_x"       , "Dispersion (horizontal)", ""),
                    ("dispersion_y"       , "Dispersion (vertical)", ""),
                    ("dispersionp_x"      , "Dispersion Derivative (horizontal)", ""),
                    ("dispersionp_y"      , "Dispersion Derivative (vertical)", ""),
        ] )

    # ------------------------------------------------------------------------
    # initializares and class methods
    # ------------------------------------------------------------------------

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

    @classmethod
    def _emittance_without_dispersion(cls, moment_ss, moment_sa, moment_aa):
        return numpy.sqrt(moment_ss * moment_aa - moment_sa**2)

    @classmethod
    def _emittance_with_dispersion(cls, moment_ss, moment_sa, moment_aa,  energy_spread, dispersion_s, dispersion_a):
        return numpy.sqrt((moment_ss + (dispersion_s * energy_spread) ** 2) * (moment_aa + (dispersion_a * energy_spread) ** 2) -
                          (moment_sa + dispersion_s * dispersion_a * energy_spread ** 2) ** 2)

    @classmethod
    def _get_twiss_from_moments(cls, moment_ss, moment_sa, moment_aa):
        emittance = cls._emittance_without_dispersion(moment_ss, moment_sa, moment_aa)
        if emittance == 0.0:
            warnings.warn(message="All moments are 0.0 and the calculation is not possible. \u03b5 = \u03b1 = \u03b2 = \u03b3 = 0.0 is returned.",
                          category=UserWarning, stacklevel=2)
            return 0.0, 0.0, 0.0, 0.0
        else:
            alpha     = -moment_sa / emittance
            beta      = moment_ss / emittance
            gamma     = (1 + alpha**2) / beta

            alpha = 0.0 if alpha == 0 else alpha # to avoid -0.0

            return emittance, alpha, beta, gamma

    @classmethod
    def _get_moments_from_twiss_without_dispersion(cls, emittance, alpha, beta):
        if beta == 0:
            warnings.warn(message="With \u03b2 = 0.0 the calculation of \u03b3 is not possible. \u03b3 = 0.0 is used.",
                          category=UserWarning, stacklevel=2)
            gamma = 0.0
        else:
            gamma = (1 + alpha ** 2) / beta

        moment_ss = beta * emittance
        moment_sa = -alpha * emittance
        moment_aa = gamma * emittance

        moment_sa = 0.0 if moment_sa == 0 else moment_sa  # to avoid -0.0

        return moment_ss, moment_sa, moment_aa

    @classmethod
    def _get_moments_with_dispersion(cls, moment_ss, moment_sa, moment_aa, energy_spread, dispersion_s, dispersion_a):
        moment_ss_disp = moment_ss + (dispersion_s * energy_spread) ** 2
        moment_sa_disp = moment_sa + dispersion_s * dispersion_a * (energy_spread ** 2)
        moment_aa_disp = moment_aa + (dispersion_a * energy_spread) ** 2

        return moment_ss_disp, moment_sa_disp, moment_aa_disp


    # --- GETTERS
    #     # ---------------------------------------------------------------------------------------------------------------------------------------------
    #
    def get_sigmas_horizontal(self, dispersion=True):
        """
        Returns the sigmas in horizontal direction.

        Returns
        -------
        tuple
            (sigma_x, sigma_x')

        """

        moment_xx, _, moment_xpxp = self.get_moments_horizontal(dispersion)

        return numpy.sqrt(moment_xx), numpy.sqrt(moment_xpxp)

    def get_sigmas_vertical(self, dispersion=True):
        """
        Returns the sigmas in vertical direction.

        Returns
        -------
        tuple
            (sigma_y, sigma_y')

        """
        moment_yy, _, moment_ypyp = self.get_moments_vertical(dispersion)

        return numpy.sqrt(moment_yy), numpy.sqrt(moment_ypyp)

    def get_sigmas_all(self, dispersion=True):
        """
        Returns all sigmas.

        Returns
        -------
        tuple
            (sigma_x, sigma_x', sigma_y, sigma_y')

        """

        sigma_x, sigmap_x = self.get_sigmas_horizontal(dispersion)
        sigma_y, sigmap_y = self.get_sigmas_vertical(dispersion)

        return sigma_x, sigmap_x, sigma_y, sigmap_y

    def get_moments_horizontal(self, dispersion=True):
        """
        Returns the moments in the horizontal direction.

        Returns
        -------
        tuple
            ( <x^2>, <x x'>, <x'^2>)

        """
        if not dispersion: return self._moment_xx, self._moment_xxp, self._moment_xpxp
        else:              return self._get_moments_with_dispersion(self._moment_xx,
                                                                    self._moment_xxp,
                                                                    self._moment_xpxp,
                                                                    self._energy_spread,
                                                                    self._dispersion_x,
                                                                    self._dispersionp_x)

    def get_moments_vertical(self, dispersion=True):
        """
        Returns the moments in the vertical direction.

        Returns
        -------
        tuple
            ( <y^2>, <y y'>, <y'^2>)

        """

        if not dispersion: return self._moment_yy, self._moment_yyp, self._moment_ypyp
        else:              return self._get_moments_with_dispersion(self._moment_yy,
                                                                   self._moment_yyp,
                                                                   self._moment_ypyp,
                                                                   self._energy_spread,
                                                                   self._dispersion_y,
                                                                   self._dispersionp_y)

    def get_moments_all(self, dispersion=True):
        """
        Returns all moments.

        Returns
        -------
        tuple
            ( <x^2>, <x x'>, <x'^2>, <y^2>, <y y'>, <y'^2>)

        """

        moment_xx, moment_xxp, moment_xpxp = self.get_moments_horizontal(dispersion)
        moment_yy, moment_yyp, moment_ypyp = self.get_moments_vertical(dispersion)

        return moment_xx, moment_xxp, moment_xpxp, moment_yy, moment_yyp, moment_ypyp

    def get_dispersion_horizontal(self):
        return self._dispersion_x, self._dispersionp_x

    def get_dispersion_vertical(self):
        return self._dispersion_y, self._dispersionp_y

    def get_dispersion_all(self):
        dispersion_x, dispersionp_x = self.get_dispersion_horizontal()
        dispersion_y, dispersionp_y = self.get_dispersion_vertical()

        return dispersion_x, dispersionp_x, dispersion_y, dispersionp_y

    def get_twiss_horizontal(self):
        """
        Returns the Twiss parameters in horizontal direction.
        (The energy disperion is considered.)

        Returns
        -------
        tuple
            (emittance_x, alpha_x, beta_x).

        """

        ex, ax, bx, _ = self._get_twiss_from_moments(moment_ss=self._moment_xx,
                                                     moment_aa=self._moment_xpxp,
                                                     moment_sa=self._moment_xxp)

        return ex, ax, bx

    def get_twiss_vertical(self):
        """
        Returns the Twiss parameters in vertical direction.
        (The energy disperion is not considered.)

        Returns
        -------
        tuple
            (emittance_y, alpha_y, beta_y).

        """
        ey, ay, by, _ = self._get_twiss_from_moments(moment_ss=self._moment_yy,
                                                     moment_aa=self._moment_ypyp,
                                                     moment_sa=self._moment_yyp)

        return ey, ay, by

    def get_twiss_all(self):
        """
        Returns all Twiss parameters.
        (The energy disperion is not considered.)

        Returns
        -------
        tuple
            (emittance_x, alpha_x, beta_x, emittance_y, alpha_y, beta_y).

        """
        ex, ax, bx = self.get_twiss_horizontal()
        ey, ay, by = self.get_twiss_vertical()

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
        self.set_moments_horizontal(moment_xx=sigma_x ** 2, moment_xxp=0.0, moment_xpxp=sigma_xp ** 2)

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

        self.set_moments_vertical(moment_yy=sigma_y**2, moment_yyp=0.0, moment_ypyp=sigma_yp**2)

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
        self.set_sigmas_horizontal(sigma_x, sigma_xp)
        self.set_sigmas_vertical(  sigma_y, sigma_yp)

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
        self._moment_xx     = moment_xx
        self._moment_xxp    = moment_xxp
        self._moment_xpxp   = moment_xpxp

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
        self._moment_yy     = moment_yy
        self._moment_yyp    = moment_yyp
        self._moment_ypyp   = moment_ypyp

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
        self.set_moments_horizontal(moment_xx, moment_xxp, moment_xpxp)
        self.set_moments_vertical(moment_yy, moment_yyp, moment_ypyp)

    def set_dispersion_horizontal(self, eta_x, etap_x):
        """
        Sets the horizontal dispersion values.

        Parameters
        ----------
        eta_x : float
            The eta value in horizontal.
        etap_x : float
            The eta' value in horizontal.
        """
        self._dispersion_x  = eta_x
        self._dispersionp_x = etap_x

    def set_dispersion_vertical(self, eta_y, etap_y):
        """
        Sets the vertical dispersion values.

        Parameters
        ----------
        eta_y : float
            The eta value in vertical.
        etap_y : float
            The eta' value in vertical.

        """
        self._dispersion_y  = eta_y
        self._dispersionp_y = etap_y

    def set_dispersion_all(self, eta_x, etap_x, eta_y, etap_y):
        """
        Sets the dispersion values.

        Parameters
        ----------
        eta_x : float
            The eta value in horizontal.
        etap_x : float
            The eta' value in horizontal.
        eta_y : float
            The eta value in vertical.
        etap_y : float
            The eta' value in vertical.

        """
        self.set_dispersion_horizontal(eta_x, etap_x)
        self.set_dispersion_vertical(eta_y, etap_y)

    def set_twiss_horizontal(self, emittance_x, alpha_x, beta_x, **kwargs):
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
        moment_xx, moment_xxp, moment_xpxp = self._get_moments_from_twiss_without_dispersion(emittance_x,  alpha_x, beta_x)

        self._moment_xx     = moment_xx
        self._moment_xxp    = moment_xxp
        self._moment_xpxp   = moment_xpxp

        # RETROCOMPATIBILITY
        eta_x  = kwargs.get("eta_x", 0.0)
        etap_x = kwargs.get("etap_x", 0.0)

        if eta_x != 0.0 or etap_x != 0.0:
            warnings.warn(message="Setting dispersion parameters with `set_twiss_horizontal(..., eta_x, etap_x)` is deprecated "
                                  "and will be removed in a future version. "
                                  "Use `set_dispersion_horizontal(eta_x, etap_x)` separately instead.",
                          category=DeprecationWarning, stacklevel=2)
            self.set_dispersion_horizontal(0.0 if eta_x is None else eta_x,
                                           0.0 if etap_x is None else etap_x)

    def set_twiss_vertical(self, emittance_y, alpha_y, beta_y, **kwargs):
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
        moment_yy, moment_yyp, moment_ypyp = self._get_moments_from_twiss_without_dispersion(emittance_y,  alpha_y, beta_y)

        self._moment_yy     = moment_yy
        self._moment_yyp    = moment_yyp
        self._moment_ypyp   = moment_ypyp

        # RETROCOMPATIBILITY
        eta_y  = kwargs.get("eta_y", 0.0)
        etap_y = kwargs.get("etap_y", 0.0)

        if eta_y != 0.0 or etap_y != 0.0:
            warnings.warn(message="Setting dispersion parameters with `set_twiss_vertical(..., eta_y, etap_y)` is deprecated "
                                  "and will be removed in a future version. "
                                  "Use `set_dispersion_vertical(eta_y, etap_y)` separately instead.",
                          category=DeprecationWarning, stacklevel=2)

            self.set_dispersion_vertical(0.0 if eta_y is None else eta_y,
                                         0.0 if etap_y is None else etap_y)

    def set_twiss_all(self, emittance_x, alpha_x, beta_x, emittance_y, alpha_y, beta_y, **kwargs):
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
        emittance_y : float
            The emittance value in vertical.
        alpha_y : float
            The alpha value in vertical.
        beta_y : float
            The beta value in vertical.

        """
        self.set_twiss_horizontal(emittance_x, alpha_x, beta_x, **kwargs)
        self.set_twiss_vertical(emittance_y, alpha_y, beta_y, **kwargs)

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

    def emittance(self, dispersion=True):
        if not dispersion:
            emittance_x = self._emittance_without_dispersion(self._moment_xx, self._moment_xxp, self._moment_xpxp)
            emittance_y = self._emittance_without_dispersion(self._moment_yy, self._moment_yyp, self._moment_ypyp)
        else:
            emittance_x = self._emittance_with_dispersion(self._moment_xx, self._moment_xxp, self._moment_xpxp, self._energy_spread, self._dispersion_x, self._dispersionp_x)
            emittance_y = self._emittance_with_dispersion(self._moment_yy, self._moment_yyp, self._moment_ypyp, self._energy_spread, self._dispersion_y, self._dispersionp_y)

        return emittance_x, emittance_y

    #
    # dictionnary interface, info etc
    #
    def has_dispersion(self):
        return (self._dispersion_x != 0 or
                self._dispersion_y != 0 or
                self._dispersionp_x != 0 or
                self._dispersionp_y != 0)

    #
    # backcompatibility (deprecated)
    #
    @deprecated("Use `get_twiss_all()` instead")
    def get_twiss_no_dispersion_all(self): return self.get_twiss_all()

    @deprecated("Use `get_twiss_horizontal()` instead")
    def get_twiss_no_dispersion_horizontal(self): return self.get_twiss_horizontal()

    @deprecated("Use `get_twiss_vertical()` instead")
    def get_twiss_no_dispersion_vertical(self): return self.get_twiss_vertical()


if __name__ == "__main__":


    # checks

    if 1: # twiss
        a = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=2.0, current=0.5, energy_spread=0.00095)

        # Twiss emittance, alpha, beta, gamma
        e_x = 70e-12
        a_x = 0.827
        b_x = 0.34
        eta_x = 0.0031
        etap_x = -0.06
        e_y = 70e-12
        a_y = -10.7
        b_y = 24.26
        eta_y = 0.0
        etap_y = 0.0

        a.set_twiss_horizontal(e_x, a_x, b_x, eta_x=eta_x, etap_x=etap_x)
        a.set_twiss_vertical(e_y, a_y, b_y, eta_y=eta_y, etap_y=etap_y)
        # a.set_dispersion_all(eta_x=eta_x, etap_x=etap_x, eta_y=eta_y, etap_y=etap_y)


        print("INPUTS: ")
        print("H twiss data: emittance, alpha, beta", e_x, a_x, b_x) #
        print("V twiss data: emittance, alpha, beta", e_y, a_y, b_y) # , eta_y, etap_y)
        print("H dispersion data: eta, eta'",  eta_x, etap_x)
        print("V dispersion data: eta, eta'",  eta_y, etap_y)

        print("NO DISPERSION: ")
        print("twiss H: ", a.get_twiss_horizontal())
        print("twiss V: ", a.get_twiss_vertical())
        print("twiss H, V: ", a.get_twiss_all())
        print("sigmas H, V: ", a.get_sigmas_all())
        print("moments H, V: ", a.get_moments_all())

        print("WITH DISPERSION: ")
        print("twiss H: ", a.get_twiss_horizontal())
        print("twiss V: ", a.get_twiss_vertical())
        print("twiss H, V: ", a.get_twiss_all())
        print("sigmas H, V: ", a.get_sigmas_all(dispersion=True))
        print("moments H, V: ", a.get_moments_all(dispersion=True))

    if 1: # moments, sigmas

        print(">>>> set moments (alpha=0): 1e-6,0,9e-6,16e-6,0,36e-6")
        a = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=2.0, current=0.5, energy_spread=0.00095)
        a.set_moments_all(1e-6, 0, 9e-6, 16e-6, 0, 36e-6)
        print("has_dispersion: ", a.has_dispersion())
        print("moments: ", a.get_moments_all(dispersion=True))
        print("sigmas: ", a.get_sigmas_all(dispersion=True))

        print(">>>> set sigmas (alpha=0): 1e-6,2e-6,3e-6")
        a = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=2.0, current=0.5, energy_spread=0.00095)
        a.set_sigmas_all(1e-6, 2e-6, 3e-6, 4e-6)
        print("has_dispersion: ", a.has_dispersion())
        print("moments: ", a.get_moments_all(dispersion=True))
        print("sigmas: ", a.get_sigmas_all(dispersion=True))

        print(">>>> set moments (alpha!=0): 1e-6,4e-6,9e-6,16e-6,25e-6,36e-6")
        a = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=2.0, current=0.5, energy_spread=0.00095)
        a.set_moments_all(1e-6, 4e-6, 9e-6, 16e-6, 25e-6, 36e-6)
        print("has_dispersion: ", a.has_dispersion())
        print("moments: ", a.get_moments_all(dispersion=True))
        print("sigmas: ", a.get_sigmas_all(dispersion=True))

    if 1:  # ESRF-ID01 (checked vs Accelerator Tools)

        e_x = 1.41e-10
        e_y = 1e-11
        a_x = -0.0022927
        a_y = -0.0010488
        b_x = 6.8987
        b_y = 2.6589
        eta_x = 0.0014291
        eta_y = -3.1352e-18
        etap_x = -3.1205e-06
        etap_y = 1.7067e-18
        a = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=6.0, current=0.2, energy_spread=0.00095)
        a.set_twiss_horizontal(e_x, a_x, b_x)  # , eta_x, etap_x)
        a.set_twiss_vertical(e_y, a_y, b_y)  # , eta_y, etap_y)
        a.set_dispersion_all(eta_x=eta_x, etap_x=etap_x, eta_y=eta_y, etap_y=etap_y)

        gammaX = 0.14496
        gammaY = 0.37609


        print("has_dispersion: ", a.has_dispersion())
        print("Twiss: ", a.get_twiss_all())
        # xx = 9.734e-10
        # xxp = 3.1889e-13
        # xpxp = 2.0415e-11
        # yy = 2.6589e-11
        # yyp = 1.0488e-14
        # ypyp = 3.7609e-12
        print("moments (with dispersion): ", a.get_moments_all(dispersion=True))
        print("moments (without dispersion): ", a.get_moments_all(dispersion=True))
        # sigma x = 3.1199e-05
        # sigma x' = 4.5183e-06
        # sigma y = 5.1565e-06
        # sigma y' = 1.9393e-06
        print("sigmas (with dispersion): ", a.get_sigmas_all(dispersion=True))
        print("sigmas (without dispersion): ", a.get_sigmas_all(dispersion=True))
