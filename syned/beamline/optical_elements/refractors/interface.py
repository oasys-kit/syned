from syned.beamline.shape import SurfaceShape
from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithSurfaceShape

class Interface(OpticalElementsWithSurfaceShape):
    def __init__(self,
                 name="Undefined",
                 surface_shape=SurfaceShape(),
                 boundary_shape=None,
                 material_object=None,
                 material_image=None,):
        """
        Defines an interface (a surface with different materials in side 1 and side 2).

        Parameters
        ----------
        name : str, optional
            The name of the optical element.
        surface_shape : instance of SurfaceShape, optional
            The geometry of the crystal surface. if None, it is initialized to SurfaceShape().
        boundary_shape : instance of BoundaryShape, optional
            The geometry of the slit aperture. if None, it is initialized to BoundaryShape().
        material_object : str, optional
            The material in side 1 (object side).
        material_image : str, optional
            The material in side 2 (object image).

        """

        super().__init__(name, surface_shape, boundary_shape)
        self._material_object = material_object
        self._material_image = material_image
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",                "Name" ,                               "" ),
                    ("surface_shape",       "Surface shape",                       "" ),
                    ("boundary_shape",      "Boundary shape",                      "" ),
                    ("material_object",     "Material in object side (element, compound, name or refraction index)", "" ),
                    ("material_image",      "Material in image side (element, compound, name or refraction index)", ""),
           ] )

    def get_material_object(self):
        """
        Returns the material of side 1 (object).

        Returns
        -------
        str

        """
        return self._material_object

    def get_material_image(self):
        """
        Returns the material of side 2 (image).

        Returns
        -------
        str

        """
        return self._material_image