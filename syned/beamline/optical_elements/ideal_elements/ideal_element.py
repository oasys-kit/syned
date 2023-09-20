from syned.beamline.optical_element import OpticalElement

class IdealElement(OpticalElement):
    def __init__(self, name="Undefined", boundary_shape=None):
        """
        Base for ideal optical elements (e.g., screen, ideal lenses).

        Parameters
        ----------
        name : str, optional
            The name of the optical element.
        boundary_shape : instance of BoundaryShape, optional
            The geometry of the slit aperture. if None, it is initialized to BoundaryShape().

        """
        OpticalElement.__init__(self, name=name, boundary_shape=boundary_shape)