from syned.beamline.optical_element import OpticalElement
from syned.beamline.shape import SurfaceShape

class OpticalElementsWithMultipleShapes(OpticalElement):

    def __init__(self, name="",
                 surface_shapes=None,
                 boundary_shape=None):
        super().__init__(name, boundary_shape)
        if surface_shapes is None: surface_shapes = [SurfaceShape()]
        if not isinstance(surface_shapes, list): raise ValueError("surface_shapes must of type 'list'")
        self._surface_shapes = surface_shapes

    def get_surface_shape(self, index):
        try: return self._surface_shapes[index]
        except: raise Exception("only " + str(len(self._surface_shapes)) + " shapes in OpticalElementsWithMultipleShapes")

    def set_surface_shape(self, index, surface_shape=None):
        if surface_shape is None: surface_shape = SurfaceShape()
        try: self._surface_shapes[index] = surface_shape
        except: raise Exception("only " + str(len(self._surface_shapes)) + " shapes in OpticalElementsWithMultipleShapes")

class OpticalElementsWithSurfaceShape(OpticalElementsWithMultipleShapes):

    def __init__(self, name, surface_shape=None, boundary_shape=None):
        super(OpticalElementsWithSurfaceShape, self).__init__(name=name,
                                                              boundary_shape=boundary_shape,
                                                              surface_shapes=[surface_shape])

    def get_surface_shape(self):
        return super(OpticalElementsWithSurfaceShape, self).get_surface_shape(index=0)

    def set_surface_shape(self, surface_shape=None):
        super(OpticalElementsWithSurfaceShape, self).set_surface_shape(index=0, surface_shape=surface_shape)


if __name__=="__main__":
    from syned.beamline.shape import Cylinder, EllipticalCylinder

    oe = OpticalElementsWithSurfaceShape(name="TEST", surface_shape=Cylinder())
    print(oe.get_surface_shape())
    oe.set_surface_shape(surface_shape=EllipticalCylinder())
    print(oe.get_surface_shape())
