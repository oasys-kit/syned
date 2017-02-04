from syned.beamline.shape import SurfaceShape
from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithSurfaceShape

class Crystal(OpticalElementsWithSurfaceShape):
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(),
                 boundary_shape=None,
                 material="Si",
                 miller_index_h=1,
                 miller_index_k=1,
                 miller_index_l=1,
                 asymmetry_angle=0.0,
                 thickness=0.0,
                 ):

        super().__init__(name, surface_shape, boundary_shape)
        self._material = material
        self._miller_index_h = miller_index_h
        self._miller_index_k = miller_index_k
        self._miller_index_l = miller_index_l
        self._asymmetry_angle = asymmetry_angle
        self._thickness = thickness

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",                "Name" ,                  "" ),
                    ("surface_shape",       "Surface Shape" ,         "" ),
                    ("boundary_shape",      "Boundary Shape" ,        "" ),
                    ("material",            "Material (name)" ,       "" ),
                    ("miller_index_h",      "Miller index h",         "" ),
                    ("miller_index_k",      "Miller index k",         "" ),
                    ("miller_index_l",      "Miller index l",         "" ),
                    ("asymmetry_angle",     "Asymmetry angle",        "rad"),
                    ("thickness",           "Thickness",              "m"),
            ] )

