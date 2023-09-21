"""
Base classes for optical elements with shape(s).

   * OpticalElementsWithSurfaceShape (e.g. an elliptical mirror).
   * OpticalElementsWithMultipleShapes (e.g. a lens that has two surfaces).
"""
from syned.beamline.optical_element import OpticalElement
from syned.beamline.shape import SurfaceShape

class OpticalElementsWithMultipleShapes(OpticalElement):
    """
    Constructor.

    Parameters
    ----------
    name : str
        The optical elemnt name.
    surface_shapes : list
        List with surface shapes (instances of SurfaceShape)
    boundary_shape : instance of BoundaryShape, optional
        The element shape. The default=None means no shape associated to the optical element.

    """

    def __init__(self, name="",
                 surface_shapes=None,
                 boundary_shape=None):
        super().__init__(name, boundary_shape)
        if surface_shapes is None: surface_shapes = [SurfaceShape()]
        if not isinstance(surface_shapes, list): raise ValueError("surface_shapes must of type 'list'")
        self._surface_shapes = surface_shapes

    def get_surface_shape(self, index):
        """
        Gets the surface shape.

        Parameters
        ----------
        index : int
            The index of the requested surface shape in the list.

        Returns
        -------
        instance of SurfaceShape
            The requested surface shape.

        """
        try: return self._surface_shapes[index]
        except: raise Exception("only " + str(len(self._surface_shapes)) + " shapes in OpticalElementsWithMultipleShapes")

    def set_surface_shape(self, index, surface_shape=None):
        """
        Sets a surface shape.

        Parameters
        ----------
        index : int
            The index of the surface shape to be set in the list.
        surface_shape : instances of SurfaceShape, optional
            The surface shape to be set (If None, initialize to SurfaceShape())

        """
        if surface_shape is None: surface_shape = SurfaceShape()
        try: self._surface_shapes[index] = surface_shape
        except: raise Exception("only " + str(len(self._surface_shapes)) + " shapes in OpticalElementsWithMultipleShapes")

class OpticalElementsWithSurfaceShape(OpticalElementsWithMultipleShapes):
    """
    Constructor.

    Parameters
    ----------
    name : str
        The optical elemnt name.
    surface_shape : instances of SurfaceShape
        The surface shape.
    boundary_shape : instance of BoundaryShape, optional
        The element shape. The default=None means no shape associated to the optical element.
    """
    def __init__(self, name, surface_shape=None, boundary_shape=None):
        super(OpticalElementsWithSurfaceShape, self).__init__(name=name,
                                                              boundary_shape=boundary_shape,
                                                              surface_shapes=[surface_shape])

    # these definitions are necessary to define self._surface_shape which is needed to
    # build the object instance from json files.
    @property
    def _surface_shape(self):
        return self.get_surface_shape()

    @_surface_shape.setter
    def _surface_shape(self, value):
        self.set_surface_shape(value)

    def get_surface_shape(self):
        """
        Gets the surface shape.

        Returns
        -------
        instance of SurfaceShape
            The requested surface shape.

        """
        return super(OpticalElementsWithSurfaceShape, self).get_surface_shape(index=0)

    def set_surface_shape(self, surface_shape=None):
        """
        Sets a surface shape.

        Parameters
        ----------
        surface_shape : instances of SurfaceShape, optional
            The surface shape to be set (If None, initialize to SurfaceShape())

        """
        super(OpticalElementsWithSurfaceShape, self).set_surface_shape(index=0, surface_shape=surface_shape)


if __name__=="__main__":
    from syned.beamline.shape import Cylinder, EllipticalCylinder

    oe = OpticalElementsWithSurfaceShape(name="TEST", surface_shape=Cylinder())
    print(oe.get_surface_shape())
    oe.set_surface_shape(surface_shape=EllipticalCylinder())
    print(oe.get_surface_shape())
