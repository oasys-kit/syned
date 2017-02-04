from syned.beamline.shape import SurfaceShape, BoundaryShape
from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithSurfaceShape

class Grating(OpticalElementsWithSurfaceShape):
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(),
                 boundary_shape=BoundaryShape(),
                 ruling = 800e3
                 ):
        super().__init__(name, surface_shape, boundary_shape)
        self._ruling = ruling

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",                "Name" ,                  "" ),
                    ("surface_shape",       "Surface Shape" ,         "" ),
                    ("boundary_shape",      "Boundary Shape" ,        "" ),
                    ("ruling",              "Ruling at center" ,      "lines/m^3" ),
            ] )

