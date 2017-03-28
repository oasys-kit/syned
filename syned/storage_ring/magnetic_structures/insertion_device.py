"""

Base class for all insertion devices: wiggler, undulator

"""

from numpy import pi
import scipy.constants as codata

from syned.storage_ring.magnetic_structure import MagneticStructure

class InsertionDevice(MagneticStructure):
    def __init__(self,
                 K_vertical       = 0.0,
                 K_horizontal      = 0.0,
                 period_length     = 0.0,
                 number_of_periods = 1):
        MagneticStructure.__init__(self)

        self._K_vertical = K_vertical
        self._K_horizontal = K_horizontal
        self._period_length = period_length
        self._number_of_periods = number_of_periods

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("K_vertical"          , "K value (vertical)"  , ""    ),
                    ("K_horizontal"        , "K value (horizontal)", ""    ),
                    ("period_length"       , "Period length"       , "m"   ),
                    ("number_of_periods"   , "Number of periods"   , ""    ),
            ] )

    def K_vertical(self):
        return self._K_vertical

    def K_horizontal(self):
        return self._K_horizontal

    def period_length(self):
        return self._period_length

    def number_of_periods(self):
        return self._number_of_periods


    #
    # some easy calculations
    #

    def K(self):
        return self.K_vertical()

    def length(self):
        return self.number_of_periods() * self.period_length()

    def _magnetic_field_from_K(self, K):
        return K * 2 * pi * codata.m_e * codata.c / (codata.e * self.period_length())

    def magnetic_field_vertical(self):
        return self._magnetic_field_from_K(self.K_vertical())

    def magnetic_field_horizontal(self):
        return self._magnetic_field_from_K(self.K_horizontal())


