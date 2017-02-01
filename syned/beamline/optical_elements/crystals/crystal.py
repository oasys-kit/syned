from syned.beamline.shape import SurfaceShape, OpticalElementsWithSurfaceShape

class Crystal(OpticalElementsWithSurfaceShape):
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(),
                 boundary_shape=None,
                 material="Si",
                 miller_indices=[1,1,1],
                 asymmetry_angle=0.0,
                 thickness=0.0,
                 ):

        super().__init__(name, surface_shape, boundary_shape)
        self._material = material
        self._miller_indices = miller_indices
        self._asymmetry_angle = asymmetry_angle
        self._thickness = thickness

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("material",            "Material (name)" ,       "" ),
                    ("miller_indices",      "Miller indices [h,k,l]", ""    ),
                    ("asymmetry_angle",     "Asymmetry angle",        "rad"    ),
                    ("thickness",           "Thickness",              "m"    ),
            ] )

