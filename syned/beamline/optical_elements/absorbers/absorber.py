
from syned.beamline.optical_element import OpticalElement
from syned.beamline.shape import BoundaryShape

class Absorber(OpticalElement):
    """
    Base class for optical element category "absorbers" (filters, slits, etc.)

    Constructor.

    Parameters
    ----------
    name : str
        The name of the optical element.
    boundary_shape : instance of BoundaryShape, optional
        if None, it is initialized to BoundaryShape().

    """
    def __init__(self, name="Undefined", boundary_shape=None):
        if boundary_shape is None: boundary_shape = BoundaryShape()
        OpticalElement.__init__(self, name=name, boundary_shape=boundary_shape)
