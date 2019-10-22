from syned.beamline.shape import SurfaceShape, BoundaryShape
from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithSurfaceShape

class Grating(OpticalElementsWithSurfaceShape):
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(),
                 boundary_shape=BoundaryShape(),
                 ruling=800e3,
                 ):
        super().__init__(name, surface_shape, boundary_shape)
        self._ruling = ruling

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",                   "Name" ,                  "" ),
                    ("surface_shape",          "Surface Shape" ,         "" ),
                    ("boundary_shape",         "Boundary Shape" ,        "" ),
                    ("ruling",                 "Ruling at center" ,      "lines/m" ),
            ] )


class GratingVLS(Grating):
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(),
                 boundary_shape=BoundaryShape(),
                 ruling=800e3,
                 ruling_coeff_linear=0.0,
                 ruling_coeff_quadratic=0.0,
                 ruling_coeff_cubic=0.0,
                 ruling_coeff_quartic=0.0,
                 coating=None,
                 coating_thickness=None,
                 ):
        super().__init__(name, surface_shape, boundary_shape)

        self._ruling = ruling
        self._ruling_coeff_linear = ruling_coeff_linear
        self._ruling_coeff_quadratic = ruling_coeff_quadratic
        self._ruling_coeff_cubic = ruling_coeff_cubic
        self._ruling_coeff_quartic = ruling_coeff_quartic
        self._coating = coating
        self._coating_thickness = coating_thickness

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",                   "Name" ,                  "" ),
                    ("surface_shape",          "Surface Shape" ,         "" ),
                    ("boundary_shape",         "Boundary Shape" ,        "" ),
                    ("ruling",                 "Ruling at center" ,      "lines/m" ),
                    ("ruling_coeff_linear",    "Ruling linear coeff",    "lines/m^2"),
                    ("ruling_coeff_quadratic", "Ruling quadratic coeff", "lines/m^3"),
                    ("ruling_coeff_cubic",     "Ruling cubic coeff",     "lines/m^4"),
                    ("ruling_coeff_quartic",   "Ruling quartic coeff",    "lines/m^5"),
                    ("coating",                "Coating (element, compound or name)", ""),
                    ("coating_thickness",      "Coating thickness", "m"),
            ] )


class GratingBlaze(GratingVLS):
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(),
                 boundary_shape=BoundaryShape(),
                 ruling=800e3,
                 ruling_coeff_linear=0.0,
                 ruling_coeff_quadratic=0.0,
                 ruling_coeff_cubic=0.0,
                 ruling_coeff_quartic=0.0,
                 coating=None,
                 coating_thickness=None,
                 blaze_angle=0.0,
                 antiblaze_angle=90.0,
                 ):
        super().__init__(name, surface_shape, boundary_shape,
                         ruling=ruling,
                         ruling_coeff_linear=ruling_coeff_linear,
                         ruling_coeff_quadratic=ruling_coeff_quadratic,
                         ruling_coeff_cubic=ruling_coeff_cubic,
                         ruling_coeff_quartic=ruling_coeff_quartic,
                         coating=coating,
                         coating_thickness=coating_thickness,
                         )
        self._blaze_angle = blaze_angle
        self._antiblaze_angle = antiblaze_angle


        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name", "Name", ""),
                    ("surface_shape", "Surface Shape", ""),
                    ("boundary_shape", "Boundary Shape", ""),
                    ("ruling", "Ruling at center", "lines/m"),
                    ("ruling_coeff_linear", "Ruling linear coeff", "lines/m^2"),
                    ("ruling_coeff_quadratic", "Ruling quadratic coeff", "lines/m^3"),
                    ("ruling_coeff_cubic", "Ruling cubic coeff", "lines/m^4"),
                    ("ruling_coeff_quartic", "Ruling quartic coeff", "lines/m^5"),
                    ("coating", "Coating (element, compound or name)", ""),
                    ("coating_thickness", "Coating thickness", "m"),
                    ("blaze_angle",      "Blaze angle",     "rad"),
                    ("antiblaze_angle",  "Antiblaze angle", "rad"),
            ] )

    def get_apex_angle(self):
        return 180 - self._blaze_angle - self._antiblaze_angle


class GratingLamellar(GratingVLS):
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(),
                 boundary_shape=BoundaryShape(),
                 ruling=800e3,
                 ruling_coeff_linear=0.0,
                 ruling_coeff_quadratic=0.0,
                 ruling_coeff_cubic=0.0,
                 coating=None,
                 coating_thickness=None,
                 height=1e-6,
                 ratio_valley_to_period=0.5,
                 ):
        super().__init__(name, surface_shape, boundary_shape,
                         ruling=ruling,
                         ruling_coeff_linear=ruling_coeff_linear,
                         ruling_coeff_quadratic=ruling_coeff_quadratic,
                         ruling_coeff_cubic=ruling_coeff_cubic,
                         coating=coating,
                         coating_thickness=coating_thickness,
                         )
        self._height = height
        self._ratio_valley_to_period = ratio_valley_to_period


        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name", "Name", ""),
                    ("surface_shape", "Surface Shape", ""),
                    ("boundary_shape", "Boundary Shape", ""),
                    ("ruling", "Ruling at center", "lines/m"),
                    ("ruling_coeff_linear", "Ruling linear coeff", "lines/m^2"),
                    ("ruling_coeff_quadratic", "Ruling quadratic coeff", "lines/m^3"),
                    ("ruling_coeff_cubic", "Ruling cubic coeff", "lines/m^4"),
                    ("ruling_coeff_quartic", "Ruling quartic coeff", "lines/m^5"),
                    ("coating", "Coating (element, compound or name)", ""),
                    ("coating_thickness", "Coating thickness", "m"),
                    ("height",            "Height",     "m"),
                    ("ratio_valley_to_period",  "Valley/period ratio", ""),
            ] )


if __name__ == "__main__":

    grating1 = Grating(name="grating1")
    # grating1.keys()
    print(grating1.info())
    # print(grating1.to_json())

    grating1 = GratingVLS(name="grating1")
    # grating1.keys()
    print(grating1.info())
    # print(grating1.to_json())

    grating1 = GratingBlaze(name="grating1")
    # grating1.keys()
    print(grating1.info())
    # print(grating1.to_json())

    grating1 = GratingLamellar(name="grating1")
    # grating1.keys()
    print(grating1.info())
    # print(grating1.to_json())


