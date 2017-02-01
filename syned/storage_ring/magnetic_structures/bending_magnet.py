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
