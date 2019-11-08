"""
Implement an undulator with vertical and horizontal magnetic fields.
"""
import numpy
import scipy.constants as codata

cte = codata.e/(2*numpy.pi*codata.electron_mass*codata.c)

from syned.storage_ring.magnetic_structures.insertion_device import InsertionDevice

class Undulator(InsertionDevice):

    def __init__(self,
                 K_vertical = 0.0,
                 K_horizontal = 0.0,
                 period_length = 0.0,
                 number_of_periods = 1.0):
        InsertionDevice.__init__(self, K_vertical, K_horizontal, period_length, number_of_periods)

    def resonance_wavelength(self, gamma, theta_x=0.0, theta_z=0.0, harmonic=1.0):
        wavelength = (self.period_length() / (2.0*gamma **2)) * \
                     (1 + self.K_vertical()**2 / 2.0 + self.K_horizontal()**2 / 2.0 + \
                      gamma**2 * (theta_x**2 + theta_z ** 2))

        return wavelength/harmonic

    def resonance_frequency(self, gamma, theta_x=0.0, theta_z=0.0, harmonic=1.0):
        frequency = codata.c / self.resonance_wavelength(gamma, theta_x, theta_z)

        return frequency*harmonic

    def resonance_energy(self, gamma, theta_x=0.0, theta_z=0.0, harmonic=1.0):
        energy_in_ev = codata.h * self.resonance_frequency(gamma, theta_x, theta_z) / codata.e

        return energy_in_ev*harmonic

    def gaussian_central_cone_aperture(self, gamma, n=1.0):
        return (1/gamma)*numpy.sqrt((1.0/(2.0*n*self.number_of_periods())) * (1.0 + self.K_horizontal()**2/2.0 + self.K_vertical()**2/2.0))

    @classmethod
    def initialize_as_vertical_undulator(cls, K = 0.0, period_length = 0.0, periods_number = 1.0):
        return Undulator(K_vertical=K,
                         K_horizontal=0.0,
                         period_length=period_length,
                         number_of_periods=periods_number)
    #
    #
    #

    def get_sigmas_radiation(self, gamma, harmonic=1.0):
        # calculate sizes of the photon undulator beam
        # see formulas 25 & 30 in Elleaume (Onuki & Elleaume)
        photon_energy = self.resonance_energy(gamma,harmonic=harmonic)
        lambdan = 1e-10 * codata.h * codata.c / codata.e * 1e10 / photon_energy  # in m
        sigma_r = 2.740 / 4 / numpy.pi * numpy.sqrt(lambdan * self.number_of_periods() * self.period_length())
        sigma_r_prime =  0.69 * numpy.sqrt(lambdan / (self.length()))
        return sigma_r, sigma_r_prime

    def get_resonance_ring(self, gamma, harmonic=1.0, ring_order=1):
        K_value = numpy.sqrt( self.K_vertical()**2 + self.K_horizontal()**2)
        return 1.0/gamma*numpy.sqrt( ring_order / harmonic * (1+0.5*K_value**2) )


    def undulator_full_emitted_power(self, gamma, ring_current):
        ptot = (self.number_of_periods()/6) * codata.value('characteristic impedance of vacuum') * \
               ring_current * codata.e * 2 * numpy.pi * codata.c * gamma**2 * \
               (self.K_vertical()**2+self.K_horizontal()**2) / self.period_length()
        return ptot

    def get_photon_sizes_and_divergences(self,syned_electron_beam,harmonic=1):
        sr,srp = self.get_sigmas_radiation(syned_electron_beam.gamma(),harmonic=harmonic)
        sx,sz,sxp,szp = syned_electron_beam.get_sigmas_all()

        Sx = numpy.sqrt( sx**2 + sr**2)
        Sz = numpy.sqrt( sz**2 + sr**2)
        Sxp = numpy.sqrt( sxp**2 + srp**2)
        Szp = numpy.sqrt( szp**2 + srp**2)

        return Sx,Sz,Sxp,Szp

    def get_K_from_photon_energy(self,photon_energy,gamma,harmonic=1):
        m2ev = codata.c * codata.h / codata.e
        wavelength = harmonic * m2ev / photon_energy
        return numpy.sqrt(2*(((wavelength*2*gamma**2)/self.period_length())-1))

    def approximated_coherent_fraction_horizontal(self,syned_electron_beam,harmonic=1):
        Sx,Sy,Sxp,Syp = self.get_photon_sizes_and_divergences(syned_electron_beam,harmonic=harmonic)
        srad,sradp = self.get_sigmas_radiation(syned_electron_beam.gamma(),harmonic=harmonic)
        return srad * sradp / ( Sx * Sxp)

    def approximated_coherent_fraction_vertical(self,syned_electron_beam,harmonic=1):
        Sx,Sy,Sxp,Syp = self.get_photon_sizes_and_divergences(syned_electron_beam,harmonic=harmonic)
        srad,sradp = self.get_sigmas_radiation(syned_electron_beam.gamma(),harmonic=harmonic)
        return srad * sradp / ( Sy * Syp)

    def approximated_coherent_fraction(self,syned_electron_beam,harmonic=1):
        return self.approximated_coherent_fraction_horizontal(syned_electron_beam,harmonic=harmonic) * \
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