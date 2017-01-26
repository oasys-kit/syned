
from syned.storage_ring.light_source import LightSource
from collections import OrderedDict

class BendingMagnet(LightSource):
    def __init__(self, name, radius, magnetic_field, length):
        """
        Constructor.
        :param radius: Physical Radius/curvature of the magnet in m
        :param magnetic_field: Magnetic field strength in T
        :param length: physical length of the bending magnet (along the arc) in m.
        """
        LightSource.__init__(self, name)
        self._radius         = radius
        self._magnetic_field = magnetic_field
        self._length         = length

    #
    #methods for practical calculations
    #
    def horizontal_divergence(self):
        return self.length()/self.radius()

    def to_dictionary(self):
        #returns a dictionary with the variable names as keys, and a tuple with value, unit and doc string
        mytuple = [ ("radius"              ,( self._radius              ,"m",  "Bending magnet physical radius" ) ),
                    ("magnetic_field"      ,( self._magnetic_field      ,"T",  "Bending magnet magnetic field"  ) ),
                    ("length"              ,( self._length              ,"m",  "Bending magnet arc length"      ) )]
        return(OrderedDict(mytuple))