"""
Base class for a Bending Magnet


"""
from syned.storage_ring.magnetic_structure import MagneticStructure
import numpy
import scipy.constants as codata

class BendingMagnet(MagneticStructure):
    """
    Constructor.

    Parameters
    ----------
    radius : float, optional
        Physical Radius/curvature of the magnet in m.
    magnetic_field : float, optional
         Magnetic field strength in T.
    length : float, optional
        physical length of the bending magnet (along the arc) in m.

    """
    def __init__(self, radius=1.0, magnetic_field=1.0, length=1.0):
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
    def initialize_from_magnetic_field_divergence_and_electron_energy(cls,
                                                                      magnetic_field=1.0,
                                                                      divergence=1e-3,
                                                                      electron_energy_in_GeV=1.0,
                                                                      **params):
        """
        Returns an bending magnet from the magnetic field and electron energy.

        Parameters
        ----------
        magnetic_field : float, optional
             Magnetic field strength in T.
        divergence : float, optional
            The beam divergence also corresponding to the BM angle in rad.
        electron_energy_in_GeV : float, optional
            The electron beam energy in GeV.

        params :
            Other parameters accepted by BendingMagnet.

        Returns
        -------
        instance of BendingMagnet

        """
        magnetic_radius = cls.calculate_magnetic_radius(magnetic_field, electron_energy_in_GeV)

        return cls(magnetic_radius, magnetic_field, numpy.abs(divergence * magnetic_radius), **params)

    @classmethod
    def initialize_from_magnetic_radius_divergence_and_electron_energy(cls,
                                                                       magnetic_radius=10.0,
                                                                       divergence=1e-3,
                                                                       electron_energy_in_GeV=1.0,
                                                                       **params):
        """
        Returns an bending magnet from the magnetic radius and electron energy.

        Parameters
        ----------
        magnetic_radius : float, optional
             Magnetic radius in m.
        divergence : float, optional
            The beam divergence also corresponding to the BM angle in rad.
        electron_energy_in_GeV : float, optional
            The electron beam energy in GeV.

        params :
            Other parameters accepted by BendingMagnet.

        Returns
        -------
        instance of BendingMagnet

        """
        magnetic_field = cls.calculate_magnetic_field(magnetic_radius, electron_energy_in_GeV)

        return cls(magnetic_radius,magnetic_field,numpy.abs(divergence * magnetic_radius), **params)


    def length(self):
        """
        returns the BM length in m.

        Returns
        -------
        float

        """
        return self._length

    def magnetic_field(self):
        """
        Returns the bagnetic field in T.

        Returns
        -------
        float

        """
        return self._magnetic_field

    def radius(self):
        """
        Returns the BM radius in m.

        Returns
        -------
        float

        """
        return self._radius

    def horizontal_divergence(self):
        """
        returns the horizontal divergence in rad.

        Returns
        -------
        float

        """
        return numpy.abs(self.length()/self.radius())

    def get_magnetic_field(self, electron_energy_in_GeV):
        """
        returns magnetic field in T (from the magnetic radius and electron energy).

        Parameters
        ----------
        electron_energy_in_GeV : float, optional
            The electron beam energy in GeV.

        Returns
        -------
        float

        """
        return BendingMagnet.calculate_magnetic_field(self._radius, electron_energy_in_GeV)

    def get_magnetic_radius(self, electron_energy_in_GeV):
        """
        Calculates magnetic radius (from the magnetic field and electron energy).

        Parameters
        ----------
        electron_energy_in_GeV : float, optional
            The electron beam energy in GeV.

        Returns
        -------
        float

        """
        return BendingMagnet.calculate_magnetic_radius(self._magnetic_field, electron_energy_in_GeV)


    def get_critical_energy(self, electron_energy_in_GeV, method=1):
        """
        Returns the photon critical energy in eV.

        Parameters
        ----------
        electron_energy_in_GeV : float, optional
            The electron beam energy in GeV.
        method : int, optional
            0= uses magnetic radius, 1=uses magnetic field

        Returns
        -------
        float

        """
        if method == 0:
            return BendingMagnet.calculate_critical_energy(self._radius, electron_energy_in_GeV)
        else:
            return BendingMagnet.calculate_critical_energy_from_magnetic_field(self._magnetic_field, electron_energy_in_GeV)



    # for equations, see for example https://people.eecs.berkeley.edu/~attwood/srms/2007/Lec09.pdf
    @classmethod
    def calculate_magnetic_field(cls, magnetic_radius, electron_energy_in_GeV):
        """
        Calculates magnetic field from magnetic radius and electron energy.

        Parameters
        ----------
        magnetic_radius : float
             Magnetic radius in m.
        electron_energy_in_GeV : float
            The electron beam energy in GeV.

        Returns
        -------
        float
            The magnetic field in T.

        References
        ----------
        See, for example, https://people.eecs.berkeley.edu/~attwood/srms/2007/Lec09.pdf

        """
        # return 3.334728*electron_energy_in_GeV/magnetic_radius
        return 1e9 / codata.c * electron_energy_in_GeV / magnetic_radius

    @classmethod
    def calculate_magnetic_radius(cls, magnetic_field, electron_energy_in_GeV):
        """
        Calculates magnetic radius from magnetic field and electron energy.

        Parameters
        ----------
        magnetic_field : float
             Magnetic field in T.
        electron_energy_in_GeV : float
            The electron beam energy in GeV.

        Returns
        -------
        float
            The magnetic radius in m.

        References
        ----------
        See, for example, https://people.eecs.berkeley.edu/~attwood/srms/2007/Lec09.pdf

        """
        # return 3.334728*electron_energy_in_GeV/magnetic_field
        return 1e9 / codata.c * electron_energy_in_GeV / magnetic_field

    @classmethod
    def calculate_critical_energy(cls, magnetic_radius, electron_energy_in_GeV):
        """
        Calculates the photon critical energy from magnetic radius and electron energy.

        Parameters
        ----------
        magnetic_radius : float
             Magnetic radius in m.
        electron_energy_in_GeV : float
            The electron beam energy in GeV.

        Returns
        -------
        float
            The photon critical energy in eV.

        References
        ----------
        See, for example, https://people.eecs.berkeley.edu/~attwood/srms/2007/Lec09.pdf

        """
        # omega = 3 g3 c / (2r)
        gamma = 1e9 * electron_energy_in_GeV / (codata.m_e *  codata.c**2 / codata.e)
        critical_energy_J = 3 * codata.c * codata.hbar * gamma**3 / (2 * numpy.abs(magnetic_radius))
        critical_energy_eV = critical_energy_J / codata.e
        return critical_energy_eV

    @classmethod
    def calculate_critical_energy_from_magnetic_field(cls, magnetic_field, electron_energy_in_GeV):
        """
        Calculates the photon critical energy from magnetic field and electron energy.

        Parameters
        ----------
        magnetic_field : float
             Magnetic field in T.
        electron_energy_in_GeV : float
            The electron beam energy in GeV.

        Returns
        -------
        float
            The critical energy in eV.

        References
        ----------
        See, for example, https://people.eecs.berkeley.edu/~attwood/srms/2007/Lec09.pdf

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
