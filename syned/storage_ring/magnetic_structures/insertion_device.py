"""

Base class for all insertion devices: wiggler, undulator

"""

from numpy import pi
import scipy.constants as codata

from syned.storage_ring.magnetic_structure import MagneticStructure

class InsertionDevice(MagneticStructure):
    """
    Base clase for the Insertion Device (ID) (common class for wigglers and undulators).

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
                 K_vertical        = 0.0,
                 K_horizontal      = 0.0,
                 period_length     = 0.0,
                 number_of_periods = 1.0):
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
        """
        Returns K vertical.

        Returns
        -------
        float

        """
        return self._K_vertical

    def K_horizontal(self):
        """
        Returns K horizontal.

        Returns
        -------
        float

        """
        return self._K_horizontal

    def period_length(self):
        """
        Returns the ID period in m.

        Returns
        -------
        float

        """
        return self._period_length

    def number_of_periods(self):
        """
        Returns the number of periods.

        Returns
        -------
        float

        """
        return self._number_of_periods


    #
    # some easy calculations
    #

    def K(self):
        """
        Returns K vertical.

        Returns
        -------
        float

        """
        return self.K_vertical()

    def length(self):
        """
        Returns the ID length in m.

        Returns
        -------
        float

        """
        return self.number_of_periods() * self.period_length()

    def magnetic_field_vertical(self):
        """
        Returns the peak magnetic field in T in the vertical direction.

        Returns
        -------
        float

        """
        return self.__magnetic_field_from_K(self.K_vertical())

    def magnetic_field_horizontal(self):
        """
        Returns the peak magnetic field in T in the horizontal direction.

        Returns
        -------
        float

        """
        return self.__magnetic_field_from_K(self.K_horizontal())

    def set_K_vertical_from_magnetic_field(self, B_vertical):
        """
        Set the vertical K value given the corresponding peak magnetic field.

        Parameters
        ----------
        B_vertical : float
            Peak magnetic field in T.

        """
        self._K_vertical = self.__K_from_magnetic_field(B_vertical)

    def set_K_horizontal_from_magnetic_field(self, B_horizontal):
        """
        Set the horizontal K value given the corresponding peak magnetic field.

        Parameters
        ----------
        B_vertical : float
            Peak magnetic field in T.

        """
        self._K_horizontal = self.__K_from_magnetic_field(B_horizontal)

    def __magnetic_field_from_K(self, K):
        return K * 2 * pi * codata.m_e * codata.c / (codata.e * self.period_length())

    def __K_from_magnetic_field(self, B):
        return B /(2 * pi * codata.m_e * codata.c / (codata.e * self.period_length()))
