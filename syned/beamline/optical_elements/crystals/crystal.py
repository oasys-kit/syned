from syned.beamline.shape import SurfaceShape
from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithSurfaceShape

class DiffractionGeometry:
    BRAGG = 0
    LAUE = 1

class Crystal(OpticalElementsWithSurfaceShape):
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
    material : str, optional
        The material name.
    diffraction_geometry : int (as defined in DiffractionGeometry, optional
        BRAGG = 0, LAUE = 1.
    miller_index_h : int, optional
        The Miller index H.
    miller_index_k : int, optional
        The Miller index K.
    miller_index_l : int, optional
        The Miller index L.
    asymmetry_angle : float, optional
        The asymmetry angle in rad.
    thickness : float, optional
        The crystal thickness in m.

    """
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(), # TODO: this should be None
                 boundary_shape=None,
                 material="Si",
                 diffraction_geometry=DiffractionGeometry.BRAGG,
                 miller_index_h=1,
                 miller_index_k=1,
                 miller_index_l=1,
                 asymmetry_angle=0.0,
                 thickness=0.0,
                 ):
        super().__init__(name, surface_shape, boundary_shape)
        self._material = material
        self._diffraction_geometry = diffraction_geometry
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
                    ("diffraction_geometry","Diffraction Geometry",   "" ),
                    ("miller_index_h",      "Miller index h",         "" ),
                    ("miller_index_k",      "Miller index k",         "" ),
                    ("miller_index_l",      "Miller index l",         "" ),
                    ("asymmetry_angle",     "Asymmetry angle",        "rad"),
                    ("thickness",           "Thickness",              "m"),
            ] )

