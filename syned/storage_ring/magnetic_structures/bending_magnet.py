"""
Base class for a Bending Magnet


"""
from syned.storage_ring.magnetic_structure import MagneticStructure
import numpy
import scipy.constants as codata

class BendingMagnet(MagneticStructure):
    def __init__(self, radius=1.0, magnetic_field=1.0, length=1.0):
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

        # support text contaning name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("radius"          , "Radius of bending magnet" , "m"    ),
                    ("magnetic_field"  , "Magnetic field",            "T"    ),
                    ("length"          , "Bending magnet length",     "m"   ),
            ] )

    #
    #methods for practical calculations
    #
    @classmethod
    def initialize_from_magnetic_field_divergence_and_electron_energy(cls,magnetic_field=1.0,divergence=1e-3,electron_energy_in_GeV=1.0):
        """
        Constructor from  magnetic field divergence and electron energy
        :param magnetic_field: in T
        :param divergence: in rad
        :param electron_energy_in_GeV: in GeV
        :return:
        """
        magnetic_radius = cls.calculate_magnetic_radius(magnetic_field, electron_energy_in_GeV)
        return BendingMagnet(magnetic_radius,magnetic_field,numpy.abs(divergence * magnetic_radius))

    @classmethod
    def initialize_from_magnetic_radius_divergence_and_electron_energy(cls,magnetic_radius=10.0,divergence=1e-3,electron_energy_in_GeV=1.0):
        """
        Constructor from  magnetic radius, divergence and electron energy
        :param magnetic_radius: in m
        :param divergence: in rad
        :param electron_energy_in_GeV: in GeV
        :return:
        """
        magnetic_field = cls.calculate_magnetic_field(magnetic_radius, electron_energy_in_GeV)
        return BendingMagnet(magnetic_radius,magnetic_field,numpy.abs(divergence * magnetic_radius))


    def length(self):
        """
        return length in m
        :return:
        """
        return self._length

    def magnetic_field(self):
        """
        return magnetic field in T
        :return:
        """
        return self._magnetic_field

    def radius(self):
        """
        return radius in m
        :return:
        """
        return self._radius

    def horizontal_divergence(self):
        """
        return horizontal divergence in rad
        :return:
        """
        return numpy.abs(self.length()/self.radius())

    def get_magnetic_field(self, electron_energy_in_GeV):
        """
        calculates magnetic field from magnetic radius and electron energy
        :param electron_energy_in_GeV:
        :return:
        """
        return BendingMagnet.calculate_magnetic_field(self._radius, electron_energy_in_GeV)

    def get_magnetic_radius(self, electron_energy_in_GeV):
        """
        calculates magnetic radius from magnetic field and electron energy
        :param electron_energy_in_GeV:
        :return:
        """
        return BendingMagnet.calculate_magnetic_radius(self._magnetic_field, electron_energy_in_GeV)


    def get_critical_energy(self, electron_energy_in_GeV, method=1):
        """
        Calculates critical energy
        :param electron_energy_in_GeV:
        :param method: 0= uses magnetic radius, 1=uses magnetic field
        :return: Photon Critical energy in eV
        """

        if method == 0:
            return BendingMagnet.calculate_critical_energy(self._radius, electron_energy_in_GeV)
        else:
            return BendingMagnet.calculate_critical_energy_from_magnetic_field(self._magnetic_field, electron_energy_in_GeV)



    # for equations, see for example https://people.eecs.berkeley.edu/~attwood/srms/2007/Lec09.pdf
    @classmethod
    def calculate_magnetic_field(cls, magnetic_radius, electron_energy_in_GeV):
        """
        Calculates magnetic field
        :param magnetic_radius:
        :param electron_energy_in_GeV:
        :return: magnetic field in T
        """
        # return 3.334728*electron_energy_in_GeV/magnetic_radius
        return 1e9 / codata.c * electron_energy_in_GeV / magnetic_radius

    @classmethod
    def calculate_magnetic_radius(cls, magnetic_field, electron_energy_in_GeV):
        """
        Calculates magnetic radius
        :param magnetic_field:
        :param electron_energy_in_GeV:
        :return:
        """
        # return 3.334728*electron_energy_in_GeV/magnetic_field
        return 1e9 / codata.c * electron_energy_in_GeV / magnetic_field

    @classmethod
    def calculate_critical_energy(cls, magnetic_radius, electron_energy_in_GeV):
        """
        Calculates critical energy
        :param magnetic_radius:
        :param electron_energy_in_GeV:
        :return:
        """
        # omega = 3 g3 c / (2r)
        gamma = 1e9 * electron_energy_in_GeV / (codata.m_e *  codata.c**2 / codata.e)
        critical_energy_J = 3 * codata.c * codata.hbar * gamma**3 / (2 * numpy.abs(magnetic_radius))
        critical_energy_eV = critical_energy_J / codata.e
        return critical_energy_eV

    @classmethod
    def calculate_critical_energy_from_magnetic_field(cls, magnetic_field, electron_energy_in_GeV):
        """
        Calculates critical energy
        :param magnetic_field:
        :param electron_energy_in_GeV:
        :return:
        """
        # omega = 3 g3 c / (2r)
        magnetic_radius = cls.calculate_magnetic_radius(magnetic_field, electron_energy_in_GeV)
        return cls.calculate_critical_energy(magnetic_radius, electron_energy_in_GeV)


if __name__ == "__main__":
    print("input for ESRF: ")
    B = BendingMagnet.calculate_magnetic_field(25.0,6.04)
    print(">> B = ",B)
    print(">> R = ",BendingMagnet.calculate_magnetic_radius(B,6.04))
    print(">> Ec = ",BendingMagnet.calculate_critical_energy(25.0,6.04))
    print(">> Ec = ",BendingMagnet.calculate_critical_energy_from_magnetic_field(B, 6.04))
    BB = BendingMagnet.calculate_magnetic_radius (BendingMagnet.calculate_magnetic_radius (B,6.04),6.04)
    RR = BendingMagnet.calculate_magnetic_radius(BendingMagnet.calculate_magnetic_field(25.0,6.04), 6.04)
    assert(BB == B)
    assert(RR == 25.0)


    print("input for ALS: ")
    B = BendingMagnet.calculate_magnetic_field(5.0,1.9)
    print(">> B = ",B)
    print(">> R = ",BendingMagnet.calculate_magnetic_radius (B,1.9))
    print(">> Ec = ",BendingMagnet.calculate_critical_energy(5.0,1.9))
    print(">> Ec = ",BendingMagnet.calculate_critical_energy_from_magnetic_field(B, 1.9))
    BB = BendingMagnet.calculate_magnetic_radius (BendingMagnet.calculate_magnetic_radius (B,1.9),1.9)
    RR = BendingMagnet.calculate_magnetic_radius(BendingMagnet.calculate_magnetic_field(5.0, 1.9), 1.9)
    assert(BB == B)
    assert(RR == 5.0)