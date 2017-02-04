from syned.beamline.shape import SurfaceShape
from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithSurfaceShape

class Mirror(OpticalElementsWithSurfaceShape):
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

