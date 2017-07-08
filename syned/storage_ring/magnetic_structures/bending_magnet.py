"""
Base class for a Bending Magnet


"""
from syned.storage_ring.magnetic_structure import MagneticStructure

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
    def horizontal_divergence(self):
        return self.length()/self.radius()

    def get_magnetic_field(self, electron_energy_in_GeV):
        return BendingMagnet.calculate_magnetic_field(self._radius, electron_energy_in_GeV)

    def get_magnetic_radius(self, electron_energy_in_GeV):
        return BendingMagnet.calculate_magnetic_radius(self._magnetic_field, electron_energy_in_GeV)

    @classmethod
    def calculate_magnetic_field(cls, magnetic_radius, electron_energy_in_GeV):
        return 3.334728*electron_energy_in_GeV/magnetic_radius

    @classmethod
    def calculate_magnetic_radius(cls, magnetic_field, electron_energy_in_GeV):
        return 3.334728*electron_energy_in_GeV/magnetic_field