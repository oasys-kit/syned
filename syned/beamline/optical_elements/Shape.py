from syned.beamline.optical_element import OpticalElement
import numpy

class Shape(object):

    def __init__(self):
        super().__init__()

class SurfaceShape(Shape):
    def __init__(self):
        super().__init__()

class Conic(SurfaceShape):
    def __init__(self, conic_coefficients=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
        self._conic_coefficients = conic_coefficients

class Plane(Conic):
    def __init__(self):
        super().__init__()

class Sphere(Conic):
    def __init__(self, radius):
        super().__init__([1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -radius**2])

    def get_radius(self):
        return numpy.sqrt(-self._conic_coefficients[9])

class Ellipsoid(Conic):
    def __init__(self):
        super().__init__()

class Paraboloid(Conic):
    def __init__(self):
        super().__init__()

class Hyperboloid(Conic):
    def __init__(self):
        super().__init__()

class Torus(SurfaceShape):
    def __init__(self):
        super().__init__()

class NumbericalMesh(SurfaceShape):
    def __init__(self):
        super().__init__()


class OpticalElementsWithSurfaceShape(OpticalElement):

    def __init__(self, name, surface_shape=SurfaceShape()):
        super().__init__(name)
        self._surface_shape = surface_shape

    def get_surface_shape(self):
        return self._surface_shape
