from syned.beamline.shape import SurfaceShape
from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithSurfaceShape

class Mirror(OpticalElementsWithSurfaceShape):
    """
    Constructor.

    Parameters
    ----------
    name : str
        The name of the optical element.
    surface_shape : instance of SurfaceShape, optional
        The geometry of the crystal surface. if None, it is initialized to SurfaceShape().
    boundary_shape : instance of BoundaryShape, optional
        The geometry of the slit aperture. if None, it is initialized to BoundaryShape().
    coating : str, optional
        The grating coating material.
    coating_thickness : float, optional
        The grating coating thickness in m.
    """
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(),
                 boundary_shape=None,
                 coating=None,
                 coating_thickness=None):

        super().__init__(name, surface_shape, boundary_shape)
        self._coating = coating
        self._coating_thickness = coating_thickness
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",                "Name" ,                               "" ),
                    ("surface_shape",       "Surface shape",                       "" ),
                    ("boundary_shape",      "Boundary shape",                      "" ),
                    ("coating",             "Coating (element, compound or name)", "" ),
                    ("coating_thickness",   "Coating thickness",                   "m"),
            ] )

