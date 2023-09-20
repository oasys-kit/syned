from syned.beamline.shape import SurfaceShape, BoundaryShape
from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithSurfaceShape

class Grating(OpticalElementsWithSurfaceShape):
    """
    Constructor.

    Parameters
    ----------
    name : str, optional
        The name of the optical element.
    surface_shape : instance of SurfaceShape, optional
        The geometry of the crystal surface. if None, it is initialized to SurfaceShape().
    boundary_shape : instance of BoundaryShape, optional
        The geometry of the slit aperture. if None, it is initialized to BoundaryShape().
    ruling : float, optional
        The grating ruling in lines/m.

    """
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
    """
    Constructor.

    Parameters
    ----------
    name : str, optional
        The name of the optical element.
    surface_shape : instance of SurfaceShape, optional
        The geometry of the optical element surface. if None, it is initialized to SurfaceShape().
    boundary_shape : instance of BoundaryShape, optional
        The geometry of the slit aperture. if None, it is initialized to BoundaryShape().
    ruling : float, optional
        The grating ruling polinomial coefficient of 0th order [lines/m].
    ruling_coeff_linear : float, optional
        The grating ruling polinomial coefficient of 1th order [lines/m^2].
    ruling_coeff_quadratic : float, optional
        The grating ruling polinomial coefficient of 2th order [lines/m^3].
    ruling_coeff_cubic : float, optional
        The grating ruling polinomial coefficient of 3th order [lines/m^4].
    ruling_coeff_quartic : float, optional
        The grating ruling polinomial coefficient of 4th order [lines/m^5].
    coating : str, optional
        The grating coating material.
    coating_thickness : float, optional
        The grating coating thickness in m.

    """
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
    """
    Constructor.

    Parameters
    ----------
    name : str, optional
        The name of the optical element.
    surface_shape : instance of SurfaceShape, optional
        The geometry of the crystal surface. if None, it is initialized to SurfaceShape().
    boundary_shape : instance of BoundaryShape, optional
        The geometry of the slit aperture. if None, it is initialized to BoundaryShape().
    ruling : float, optional
        The grating ruling polinomial coefficient of 0th order [lines/m].
    ruling_coeff_linear : float, optional
        The grating ruling polinomial coefficient of 1th order [lines/m^2].
    ruling_coeff_quadratic : float, optional
        The grating ruling polinomial coefficient of 2th order [lines/m^3].
    ruling_coeff_cubic : float, optional
        The grating ruling polinomial coefficient of 3th order [lines/m^4].
    ruling_coeff_quartic : float, optional
        The grating ruling polinomial coefficient of 4th order [lines/m^5].
    coating : str, optional
        The grating coating material.
    coating_thickness : float, optional
        The grating coating thickness in m.
    blaze_angle : float, optional
        The blaze angle in rad.
    antiblaze_angle : float, optional
        The anti-blaze angle in rad.

    """
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
    """
    Constructor.

    Parameters
    ----------
    name : str, optional
        The name of the optical element.
    surface_shape : instance of SurfaceShape, optional
        The geometry of the crystal surface. if None, it is initialized to SurfaceShape().
    boundary_shape : instance of BoundaryShape, optional
        The geometry of the slit aperture. if None, it is initialized to BoundaryShape().
    ruling : float, optional
        The grating ruling polinomial coefficient of 0th order [lines/m].
    ruling_coeff_linear : float, optional
        The grating ruling polinomial coefficient of 1th order [lines/m^2].
    ruling_coeff_quadratic : float, optional
        The grating ruling polinomial coefficient of 2th order [lines/m^3].
    ruling_coeff_cubic : float, optional
        The grating ruling polinomial coefficient of 3th order [lines/m^4].
    ruling_coeff_quartic : float, optional
        The grating ruling polinomial coefficient of 4th order [lines/m^5].
    coating : str, optional
        The grating coating material.
    coating_thickness : float, optional
        The grating coating thickness in m.
    height : str, optional
        The height of the grating lamella in m.
    ratio_valley_to_period : float, optional
        The grating ration valley to period.

    """

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
                 ratio_valley_to_period=0.5, # TODO: is better to define ratio valley to height?
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


