"""
Implement an undulator with vertical and horizontal magnetic fields.
"""
import numpy as np
import scipy.constants.codata

from syned.beamline.light_sources.insertion_device import InsertionDevice

class Undulator(InsertionDevice):

    def __init__(self, K_vertical, K_horizontal, period_length, periods_number):
        InsertionDevice.__init__(self, K_vertical, K_horizontal, period_length, periods_number)

    def resonanceWavelength(self, gamma, theta_x, theta_z):
        wavelength = (self.periodLength() / (2.0*gamma **2)) * \
                     (1 + self.K_vertical()**2 / 2.0 + self.K_horizontal()**2 / 2.0 + \
                      gamma**2 * (theta_x**2 + theta_z ** 2))

        return wavelength

    def resonanceFrequency(self, gamma, theta_x, theta_z):
        codata = scipy.constants.codata.physical_constants
        codata_c = codata["speed of light in vacuum"][0]

        frequency = codata_c / self.resonanceWavelength(gamma, theta_x, theta_z)

        return frequency

    def resonanceEnergy(self, gamma, theta_x, theta_y, harmonic=1):
        codata = scipy.constants.codata.physical_constants
        energy_in_ev = codata["Planck constant"][0] * self.resonanceFrequency(gamma, theta_x, theta_y) / codata["elementary charge"][0]

        return energy_in_ev*harmonic

    def gaussianCentralConeDivergence(self, gamma, n=1):
        return (1/gamma)*np.sqrt((1.0/(2.0*n*self.periodNumber())) * (1.0 + self.K_horizontal()**2/2.0 + self.K_vertical()**2/2.0))
