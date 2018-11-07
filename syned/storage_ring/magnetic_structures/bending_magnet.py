"""
Base class for a Bending Magnet


"""
from syned.storage_ring.magnetic_structure import MagneticStructure
import scipy.constants as codata

class BendingMagnet(MagneticStructure):
    def __init__(self, radius, magnetic_field, length):
        """
        Constructor.
        :param radius: Physical Radius/curvature of the magnet in m
        :param magnetic_field: Magnetic field strength in T
        :param length: physical length of the bending magnet (along the arc) in m.
        """
        MagneticStructure.__init__(self)
        self._radius         = radius
        self._magnetic_field = magnetic_field
        self._length         = length

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("radius"          , "Radius of bending magnet" , "m"    ),
                    ("magnetic_field"  , "Magnetic field",            "T"    ),
                    ("length"          , "Bending magnet length",     "m"   ),
            ] )

    #
    #methods for practical calculations
    #

    def length(self):
        return self._length

    def magnetic_field(self):
        return self._magnetic_field

    def radius(self):
        return self._radius

    def horizontal_divergence(self):
        return self.length()/self.radius()

    def get_magnetic_field(self, electron_energy_in_GeV):
        return BendingMagnet.calculate_magnetic_field(self._radius, electron_energy_in_GeV)

    def get_magnetic_radius(self, electron_energy_in_GeV):
        return BendingMagnet.calculate_magnetic_radius(self._magnetic_field, electron_energy_in_GeV)

    def get_critical_energy(self, electron_energy_in_GeV):
        return BendingMagnet.calculate_critical_energy(self._radius, electron_energy_in_GeV)

    # for equations, see for example https://people.eecs.berkeley.edu/~attwood/srms/2007/Lec09.pdf
    @classmethod
    def calculate_magnetic_field(cls, magnetic_radius, electron_energy_in_GeV):
        # return 3.334728*electron_energy_in_GeV/magnetic_radius
        gamma = 1e9 * electron_energy_in_GeV / (codata.m_e *  codata.c**2 / codata.e)
        # B = gamma m c / e / R ; note that c approximated the electron velocity!
        return gamma * codata.m_e * codata.c / codata.e / magnetic_radius

    @classmethod
    def calculate_magnetic_radius(cls, magnetic_field, electron_energy_in_GeV):
        # return 3.334728*electron_energy_in_GeV/magnetic_field
        gamma = 1e9 * electron_energy_in_GeV / (codata.m_e *  codata.c**2 / codata.e)
        # R = gamma m c / e / B ; note that c approximated the electron velocity!
        return gamma * codata.m_e * codata.c / codata.e / magnetic_field

    @classmethod
    def calculate_critical_energy(cls, magnetic_radius, electron_energy_in_GeV):
        # omega = 3 g3 c / (2r)
        gamma = 1e9 * electron_energy_in_GeV / (codata.m_e *  codata.c**2 / codata.e)
        critical_energy_J = 3 * codata.c * codata.hbar * gamma**3 / (2 * magnetic_radius)
        critical_energy_eV = critical_energy_J / codata.e
        return critical_energy_eV

if __name__ == "__main__":
    print("input for ESRF: ")
    print(">> B = ",BendingMagnet.calculate_magnetic_field(25.0,6.04))
    print(">> R = ",BendingMagnet.calculate_magnetic_radius(0.85,6.04))
    print(">> Ec = ",BendingMagnet.calculate_critical_energy(23.7,6.04))
