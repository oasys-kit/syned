from syned.beamline.optical_elements.ideal_elements.ideal_element import IdealElement

class IdealLens(IdealElement):
    """
    Defines an ideal lens. It converts a plane wave into:
    * an spherical converging wave (if focal_x=focal_y).
    * a toroidal converging wave (if focal_x != focal_y).
    * a cylindrical wave (if focal_x or focal_y is infinity).

    Constructor.

    Parameters
    ----------
    name : str, optional
        The name of the optical element.
    focal_x : float
        The focal length in meters along the X direction.
    focal_y : float
        The focal length in meters along the Y direction.

    """
    def __init__(self, name="Undefined", focal_x=1.0, focal_y=1.0):
        IdealElement.__init__(self, name=name)
        self._focal_x = focal_x
        self._focal_y = focal_y
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name"          , "Name"                          , ""),
                    ("boundary_shape", ""                              , ""),
                    ("focal_x"       , "Focal length in x [horizontal]", "m" ),
                    ("focal_y"       , "Focal length in y [vertical]"  , "m" ),
            ] )

    def focal_x(self):
        """
        Returns the focal length in the X direction.

        Returns
        -------
        float

        """
        return self._focal_x

    def focal_y(self):
        """
        Returns the focal length in the Y direction.

        Returns
        -------
        float

        """
        return self._focal_y
