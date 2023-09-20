"""
Implement an undulator with vertical and horizontal magnetic fields.
"""
import numpy
import scipy.constants as codata

cte = codata.e/(2*numpy.pi*codata.electron_mass*codata.c)

from syned.storage_ring.magnetic_structures.insertion_device import InsertionDevice

class Undulator(InsertionDevice):
    """
    Constructor.

    Parameters
    ----------
    K_vertical : float, optional
        The deflection K parameter corresponding to magnetic field in the vertical direction.
    K_horizontal : float, optional
        The deflection K parameter corresponding to magnetic field in the horizontal direction.
    period_length : float, optional
        The ID period in m.
    number_of_periods : float, optional
        The number of periods. It may be a float, considering that number_of_periods = ID_length / period_length.

    """

    def __init__(self,
                 K_vertical = 0.0,
                 K_horizontal = 0.0,
                 period_length = 0.0,
                 number_of_periods = 1.0):
        InsertionDevice.__init__(self, K_vertical, K_horizontal, period_length, number_of_periods)

    def resonance_wavelength(self, gamma, theta_x=0.0, theta_z=0.0, harmonic=1.0):
        """
        Returns the resonant wavelength in m.

        Parameters
        ----------
        gamma : float
            The gamma or Lorentz factor of the electron beam.
        theta_x : float, optional
            The angle along the horizontal direction in rad.
        theta_z : float, optional
            The angle along the vertical direction in rad.
        harmonic : float, optional
            The harmonic number (1,2,3...) to be considered.

        Returns
        -------
        float


        """
        wavelength = (self.period_length() / (2.0 * gamma **2)) * \
                     (1 + self.K_vertical()**2 / 2.0 + self.K_horizontal()**2 / 2.0 + \
                      gamma**2 * (theta_x**2 + theta_z**2))

        return wavelength / harmonic

    def resonance_frequency(self, gamma, theta_x=0.0, theta_z=0.0, harmonic=1.0):
        """
        Returns the resonant frequency in Hz.

        Parameters
        ----------
        gamma : float
            The gamma or Lorentz factor of the electron beam.
        theta_x : float, optional
            The angle along the horizontal direction in rad.
        theta_z : float, optional
            The angle along the vertical direction in rad.
        harmonic : float, optional
            The harmonic number (1,2,3...) to be considered.

        Returns
        -------
        float


        """
        frequency = codata.c / self.resonance_wavelength(gamma, theta_x, theta_z)

        return frequency * harmonic

    def resonance_energy(self, gamma, theta_x=0.0, theta_z=0.0, harmonic=1.0):
        """
        Returns the resonant energy in eV.

        Parameters
        ----------
        gamma : float
            The gamma or Lorentz factor of the electron beam.
        theta_x : float, optional
            The angle along the horizontal direction in rad.
        theta_z : float, optional
            The angle along the vertical direction in rad.
        harmonic : float, optional
            The harmonic number (1,2,3...) to be considered.

        Returns
        -------
        float


        """
        energy_in_ev = codata.h * self.resonance_frequency(gamma, theta_x, theta_z) / codata.e

        return energy_in_ev*harmonic

    def gaussian_central_cone_aperture(self, gamma, n=1.0):
        """
        Returns the approximated angular width (sigma) in rad of the central cone.

        Parameters
        ----------
        gamma : float
            The gamma or Lorentz factor of the electron beam.
        n : float, optional
            The harmonic number (1,2,3...) to be considered.

        Returns
        -------
        float

        References
        ----------
        Eq. 15 in https://xdb.lbl.gov/Section2/Sec_2-1.html

        """
        return (1/gamma)*numpy.sqrt((1.0/(2.0*n*self.number_of_periods())) * (1.0 + self.K_horizontal()**2/2.0 + self.K_vertical()**2/2.0))

    @classmethod
    def initialize_as_vertical_undulator(cls, K = 0.0, period_length = 0.0, periods_number = 1.0, **params):
        """
        Create an undulator with vertical magnetic field.

        Parameters
        ----------
        K : float, optional
            The deflection K parameter corresponding to magnetic field in the vertical direction.
        period_length : float, optional
            The ID period in m.
        periods_number : float, optional
            The number of periods. It may be a float, considering that number_of_periods = ID_length / period_length.
        params : other parameters accepted by Undulator.

        Returns
        -------
        instance of Undulator

        """
        return cls(K_vertical=K,
                   K_horizontal=0.0,
                   period_length=period_length,
                   number_of_periods=periods_number, **params)
    #
    #
    #

    def get_sigmas_radiation(self, gamma, harmonic=1.0):
        """
        Returns the approximated radiation sigmas (size and divergence).

        Parameters
        ----------
        gamma : float
            The gamma or Lorentz factor of the electron beam.
        harmonic : float, optional
            The harmonic number (1,2,3...) to be considered.

        Returns
        -------
        tuple
            (sigma_in_real_space [m], sigma_in_divergence_space [rad])

        References
        ----------

        See formulas 25 & 30 in Elleaume (Onuki & Elleaume) for the calculated sizes of the photon undulator beam.
        Onuki & Elleaume "Undulators, Wigglers and Their Applications" (2002) CRC Press.


        """
        # calculate sizes of the photon undulator beam
        # see formulas 25 & 30 in Elleaume (Onuki & Elleaume)
        photon_energy = self.resonance_energy(gamma,harmonic=harmonic)
        lambdan = 1e-10 * codata.h * codata.c / codata.e * 1e10 / photon_energy  # in m
        sigma_r = 2.740 / 4 / numpy.pi * numpy.sqrt(lambdan * self.number_of_periods() * self.period_length())
        sigma_r_prime =  0.69 * numpy.sqrt(lambdan / (self.length()))
        return sigma_r, sigma_r_prime

    def get_resonance_ring(self, gamma, harmonic=1.0, ring_order=1):
        """
        Return the angular position of the rings at resonance.

        Parameters
        ----------
        gamma : float
            The gamma or Lorentz factor of the electron beam.
        harmonic : float, optional
            The harmonic number (1,2,3...) to be considered.
        ring_order : int, optional
            The ring order (1,2,3...)

        Returns
        -------
        float
            The angular position in rad.

        """
        K_value = numpy.sqrt( self.K_vertical()**2 + self.K_horizontal()**2)
        return 1.0 / gamma * numpy.sqrt( ring_order / harmonic * (1 + 0.5 * K_value**2) )


    def undulator_full_emitted_power(self, gamma, ring_current):
        """
        Returns the total emitted power by an undulator.

        Parameters
        ----------
        gamma : float
            The gamma or Lorentz factor of the electron beam.
        ring_current : float
            The current of the electron beam in A.

        Returns
        -------
        float
            The power in W.

        References
        ----------
        Eq. 18 in https://xdb.lbl.gov/Section2/Sec_2-1.html

        """
        ptot = (self.number_of_periods() / 6) * codata.value('characteristic impedance of vacuum') * \
               ring_current * codata.e * 2 * numpy.pi * codata.c * gamma**2 * \
               (self.K_vertical()**2 + self.K_horizontal()**2) / self.period_length()
        return ptot

    def get_photon_sizes_and_divergences(self, syned_electron_beam, harmonic=1):
        """
        Return the photon beam sizes and divergences.

        They are calculates as a convolution of the radiation sigmas (get_sigmas_radiation()) and
        the electron beam sizes.

        Parameters
        ----------
        syned_electron_beam : instance of ElectronBeam
            The electron bean used to get the electron beam sizes and electron energy.
        harmonic : int
            The harmonic number (1,2,3...).

        Returns
        -------
        tuple
            (Sx [m], Sz [m], Sxp [rad], Szp [rad])

        """
        sr,srp = self.get_sigmas_radiation(syned_electron_beam.gamma(), harmonic=harmonic)
        sx,sxp,sz,szp = syned_electron_beam.get_sigmas_all()

        Sx = numpy.sqrt( sx**2 + sr**2)
        Sz = numpy.sqrt( sz**2 + sr**2)
        Sxp = numpy.sqrt( sxp**2 + srp**2)
        Szp = numpy.sqrt( szp**2 + srp**2)

        return Sx,Sz,Sxp,Szp

    def get_K_from_photon_energy(self, photon_energy, gamma, harmonic=1):
        """
        Calculate K for a given resonance energy.

        Parameters
        ----------
        photon_energy : float
            The photon energy in eV.
        gamma : float
            The electron gamma (Lorentz factor).
        harmonic : int
            The harmonic number.

        Returns
        -------
        float

        """
        m2ev = codata.c * codata.h / codata.e
        wavelength = harmonic * m2ev / photon_energy
        return numpy.sqrt(2 * (((wavelength * 2 * gamma**2) / self.period_length()) - 1))

    def approximated_coherent_fraction_horizontal(self, syned_electron_beam, harmonic=1):
        """
        Gets the approximated coherent fraction at resonance in the horizontal direction.

        It is calculated as the ratio of the phase space of the coherent emission (zero emittance) over
        the actual emission (finite emittance).

        Parameters
        ----------
        syned_electron_beam : instance of ElectronBeam
            The electron bean used to get the electron beam sizes and electron energy.
        harmonic : int
            The harmonic number (1,2,3...).

        Returns
        -------
        float

        """
        Sx,Sy,Sxp,Syp = self.get_photon_sizes_and_divergences(syned_electron_beam, harmonic=harmonic)
        srad,sradp = self.get_sigmas_radiation(syned_electron_beam.gamma(), harmonic=harmonic)
        return srad * sradp / ( Sx * Sxp)

    def approximated_coherent_fraction_vertical(self, syned_electron_beam,harmonic=1):
        """
        Gets the approximated coherent fraction at resonance in the vertical direction.

        It is calculated as the ratio of the phase space of the coherent emission (zero emittance) over
        the actual emission (finite emittance).

        Parameters
        ----------
        syned_electron_beam : instance of ElectronBeam
            The electron bean used to get the electron beam sizes and electron energy.
        harmonic : int
            The harmonic number (1,2,3...).

        Returns
        -------
        float

        """
        Sx,Sy,Sxp,Syp = self.get_photon_sizes_and_divergences(syned_electron_beam, harmonic=harmonic)
        srad,sradp = self.get_sigmas_radiation(syned_electron_beam.gamma(), harmonic=harmonic)
        return srad * sradp / ( Sy * Syp)

    def approximated_coherent_fraction(self, syned_electron_beam, harmonic=1):
        """
        Gets the approximated coherent fraction at resonance.

        It is calculated as the product of the horizontal and vertical coherent fractions.

        Parameters
        ----------
        syned_electron_beam : instance of ElectronBeam
            The electron bean used to get the electron beam sizes and electron energy.
        harmonic : int
            The harmonic number (1,2,3...).

        Returns
        -------
        float

        """
        return self.approximated_coherent_fraction_horizontal(syned_electron_beam, harmonic=harmonic) * \
               self.approximated_coherent_fraction_vertical(syned_electron_beam, harmonic=harmonic)


if __name__ == "__main__":

    a = Undulator(number_of_periods=61.5, period_length=0.057)
    a.set_K_vertical_from_magnetic_field(0.187782)

    print(a._K_vertical)

    print (a.resonance_energy(gamma=5870.8540997356595))

    fd = a.to_full_dictionary()
    dict = a.to_dictionary()

    print(dict)

    for key in fd:
        print(key,fd[key][0])

    for key in fd:
        print(key,dict[key])

    print(a.keys())
    print(a.info())


    print("####### derived quantities ##########")

    from syned.storage_ring.electron_beam import ElectronBeam
    ebeam = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=2.0,energy_spread=0.0,current=0.5)

    sigmas_radiation = a.get_sigmas_radiation(ebeam.gamma(),harmonic=1.0)
    print("sigmas radiation [m rad]:",sigmas_radiation)


    ring = a.get_resonance_ring(ebeam.gamma(), harmonic=1.0, ring_order=1)
    print("first ring at [rad]:",ring)

    pow = a.undulator_full_emitted_power(ebeam.gamma(), ebeam.current())
    print("Total emission [W]",pow)

    sizes = a.get_photon_sizes_and_divergences(ebeam,harmonic=1)
    print("Sizes: ",sizes)

    print("Resonance: ",a.resonance_energy(ebeam.gamma()))

    print("K at 444 eV",a.get_K_from_photon_energy(444.0,ebeam.gamma()))
    print("K at 200 eV", a.get_K_from_photon_energy(200.0, ebeam.gamma()))

    print("CF H V HV: ",
          a.approximated_coherent_fraction_horizontal(ebeam,harmonic=1),
          a.approximated_coherent_fraction_vertical(ebeam, harmonic=1),
          a.approximated_coherent_fraction(ebeam, harmonic=1),)
