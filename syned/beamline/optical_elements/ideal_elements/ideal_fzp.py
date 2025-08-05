import numpy
from syned.beamline.optical_elements.ideal_elements.ideal_element import IdealElement

class IdealFZP(IdealElement):
    """
    Defines an ideal Fresnel Zone Plate.

    Constructor.

    Parameters
    ----------
    name : str, optional
        The name of the optical element.
    focusing_direction : int
        0=None, 1=x (sagittal), 2=z (meridional), 3=2D focusing.
    focal : float
        The focal length in meters.
    nominal_wavelength : float
        The nominal wavelength in m for where the focal length is defined.
    diameter : float
        The FZP diameter in m.

    """
    def __init__(self,
                 name="Undefined",
                 focusing_direction=3,  # 0=None, 1=x (sagittal), 2=z (meridional), 3=2D focusing.
                 focal=1.0,                 #  focal distance (m)
                 nominal_wavelength=1e-10,  # nominal wavelength in m
                 # r0=10.0e-6,                #  inner zone radius (m)
                 diameter=0.001,            # FZP diameter in m
                 ):
        IdealElement.__init__(self, name=name)
        self._focusing_direction = focusing_direction
        self._focal = focal
        self._nominal_wavelength = nominal_wavelength
        self._diameter = diameter

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name"              , "Name"                , ""),
                    ("boundary_shape"    , ""                    , ""),
                    ("focusing_direction", "Focusing direction: 0=None, 1=1D along X, 2=1D along Z, 3=2D", ""),
                    ("focal"             , "Focal length"        , "m"),
                    ("nominal_wavelength", "Nominal wavelength"  , "m"),
                    ("diameter"          , "FZP diameter"        , "m"),
            ] )

    def focusing_direction(self):
        """
        Returns the focusing direction.

        Returns
        -------
        int
            0=None,
            1=1D along X,
            2=1D along Z,
            3=2D.
        """
        return self._focusing_direction

    def focal(self):
        """
        Returns the focal length.

        Returns
        -------
        float

        """
        return self._focal

    def nominal_wavelength(self):
        """
        Returns the nominal wavelength.

        Returns
        -------
        float

        """
        return self._nominal_wavelength

    def diameter(self):
        """
        Returns the FZP diameter.

        Returns
        -------
        float

        """
        return self._diameter

    #
    # calculated. The exact expression is rn = sqrt( n lambda f + (n lambda / 2)**2 )
    #
    def rn(self):
        return 0.5 * self.diameter()

    def r0(self):
        """
        Returns the innermost radius (approximated calculation r0=sqrt(wavelength * focal)).

        Returns
        -------
        float

        """
        return numpy.sqrt(self.nominal_wavelength() * self.focal())

    def r0_exact(self):
        """
        Returns the innermost radius (exact calculation r0=sqrt(wavelength * focal + (wavelength/2)**2)).

        Returns
        -------
        float

        """
        return numpy.sqrt(self.nominal_wavelength() * self.focal() + (0.5 * self.nominal_wavelength())**2)

    def n_vs_r(self, r): # approximated if f >> diameter; eq 855 in Michette
        """
        Returns the zone number for a given distance r (approximated calculation).

        Returns
        -------
        float

        """
        return (r ** 2 / self.nominal_wavelength() / self.focal())

    def n_exact_vs_r(self, r): # Exact, solving n from rn = sqrt( n lambda f + (n lambda / 2)**2 )
        """
        Returns the zone number for a given distance r
        (exact calculation solving n from rn = sqrt( n lambda f + (n lambda / 2)**2).

        Returns
        -------
        float

        """
        nn = -2 * self.focal() + 2 * numpy.sqrt(self.focal()**2 + r**2)
        return nn / self.nominal_wavelength()

    def n(self):
        """
        Returns the zone number for a outermost zone (approximated calculation).

        Returns
        -------
        float

        """
        return self.n_vs_r( self.rn() )

    def n_exact(self):
        """
        Returns the zone number for a outermost zone (exact calculation using n_exact_vs_r() ).

        Returns
        -------
        float

        """
        return self.n_exact_vs_r(self.rn())

if __name__ == "__main__":
    fzp = IdealFZP(
        name = "Undefined",
        focusing_direction = 3,  # 0=None, 1=x (sagittal), 2=z (meridional), 3=2D focusing.
        focal = 1.0,  # focal distance (m)
        nominal_wavelength = 1e-10,  # nominal wavelength in m
        diameter = 0.001,  # FZP diameter in m
    )

    print(fzp.info())
    print("r0, r0_exact: ", fzp.r0(), fzp.r0_exact())
    print("rn: ", fzp.rn())
    print("n, n_exact: ", fzp.n(), fzp.n_exact())


