from syned.beamline.optical_elements.refractors.lens import Lens

class CRL(Lens):
    """
    Defines a Compound refractive lens (CRL). It is composed by a number (n_lens) of identical lenses.

    Constructor.

    Parameters
    ----------
    name : str, optional
        The name of the optical element.
    n_lens : int, optional
        The number of (identical) lenses.
    surface_shape1 : instance of SurfaceShape, optional
        The geometry of the lens surface 1. if None, it is initialized to SurfaceShape().
    surface_shape2 : instance of SurfaceShape, optional
        The geometry of the lens surface 2. if None, it is initialized to SurfaceShape().
    boundary_shape : instance of BoundaryShape, optional
        The geometry of the slit aperture. if None, it is initialized to BoundaryShape().
    material : str
        A string defining the material within the two surfaces.
    thickness : float
        The distance between the two surfaces at the center of the lens in m.
    piling_thickness : float, optional
        The piling distance in m, or spatial periodicity in the stack. In other words, the distance from the
        lens1-surface1 to the lens2-surface1.

    """
    def __init__(self,
                 name="Undefined",
                 n_lens=1,
                 surface_shape1=None,
                 surface_shape2=None,
                 boundary_shape=None,
                 material="",
                 thickness=0.0,
                 piling_thickness=0.0):
        super().__init__(name=name,
                         surface_shape1=surface_shape1,
                         surface_shape2=surface_shape2,
                         boundary_shape=boundary_shape,
                         material=material,
                         thickness=thickness)
        self._n_lens           = n_lens
        self._piling_thickness = piling_thickness

        # support text contaning name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",                "Name" ,                                "" ),
                    ("n_lens",              "N Lens" ,                              "" ),
                    ("surface_shape1",      "Surface shape 1",                      "" ),
                    ("surface_shape2",      "Surface shape 2",                      "" ),
                    ("boundary_shape",      "Boundary shape",                       "" ),
                    ("material",            "Material (element, compound or name)", "" ),
                    ("thickness",           "Thickness",                            "m"),
                    ("piling_thickness",    "Piling Thickness",                     "m")
            ] )

    def get_n_lens(self):
        """
        Returns the number of lenses.

        Returns
        -------
        int

        """
        return self._n_lens

    def get_piling_thickness(self):
        """
        Returns the piling thickness.

        Returns
        -------
        float

        """
        return self._piling_thickness

