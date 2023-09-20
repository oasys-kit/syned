from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithMultipleShapes
from syned.beamline.shape import Plane

class Lens(OpticalElementsWithMultipleShapes):
    def __init__(self,
                 name="Undefined",
                 surface_shape1=None,
                 surface_shape2=None,
                 boundary_shape=None,
                 material="",
                 thickness=0.0):
        """
        Defines a lens. It is composed by two surfaces (surface_shape1 and surface_shape2) and a material
        within them.

        Parameters
        ----------
        name : str, optional
            The name of the optical element.
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

        """

        if surface_shape1 is None: surface_shape1 = Plane()
        if surface_shape2 is None: surface_shape2 = Plane()

        super(Lens, self).__init__(name=name,
                                   boundary_shape=boundary_shape,
                                   surface_shapes=[surface_shape1, surface_shape2])
        self._material = material
        self._thickness = thickness

        # support text contaning name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",                "Name" ,                                "" ),
                    ("surface_shape1",      "Surface shape 1",                      "" ),
                    ("surface_shape2",      "Surface shape 2",                      ""),
                    ("boundary_shape",      "Boundary shape",                       "" ),
                    ("material",            "Material (element, compound or name)", "" ),
                    ("thickness",           "Thickness",                            "m"),
            ] )

    def get_thickness(self):
        """
        Returns the lens thickness in m.

        Returns
        -------
        float

        """
        return self._thickness

    def get_material(self):
        """
        Returns the lens material.

        Returns
        -------
        str

        """
        return self._material

    def get_boundary_shape(self):
        """
        Returns the boundary shape.

        Returns
        -------
        instance of BoundaryShape

        """
        return self._boundary_shape

    def get_surface_shape1(self):
        """
        Returns the shape of surface 1.

        Returns
        -------
        instance of SurfaceShape

        """
        return self.get_surface_shape(index=0)

    def get_surface_shape2(self):
        """
        Returns the shape of surface 2.

        Returns
        -------
        instance of SurfaceShape

        """
        return self.get_surface_shape(index=1)

