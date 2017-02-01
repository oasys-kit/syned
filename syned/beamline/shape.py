from syned.beamline.optical_element import OpticalElement
import numpy


#
# main shape subclasses:
#      SurfaceShape to caracterize the shape (sphere etc.) of the optical element surface
#      BoundaryShape to characterize the optical element dimensions (rectangle, etc.)
#
class Shape(object):
    def __init__(self):
        super().__init__()

class SurfaceShape(Shape):
    def __init__(self):
        super().__init__()

class BoundaryShape(Shape):
    def __init__(self):
        super().__init__()  
        
    def get_boundaries(self):
        pass

#
# Subclasses for SurfaceShape
#


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
        #TODO: this is not generic
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



#
# subclasses for BoundaryShape
#


class Rectangle(BoundaryShape):
    def __init__(self, x_left=-0.010, x_right=0.010, y_bottom=-0.020, y_top=0.020):
        super().__init__()

        self._x_left = x_left
        self._x_right = x_right
        self._y_bottom = y_bottom
        self._y_top = y_top

    def get_boundaries(self):
        return self._x_left, self._x_right, self._y_bottom, self._y_top

    def set_boundaries(self,x_left=-0.010, x_right=0.010, y_bottom=-0.020, y_top=0.020):
        self._x_left = x_left
        self._x_right = x_right
        self._y_bottom = y_bottom
        self._y_top = y_top

    def set_width_and_length(self,width=10e-3,length=30e-3):
        self._x_left = -0.5 * width
        self._x_right = 0.5 * width
        self._y_bottom = -0.5 * length
        self._y_top = 0.5 * length



class Ellipse(BoundaryShape):
    def __init__(self, min_ax_left, min_ax_right, maj_ax_bottom, maj_ax_top):
        super().__init__()

        self._min_ax_left = min_ax_left
        self._min_ax_right = min_ax_right
        self._maj_ax_bottom = maj_ax_bottom
        self._maj_ax_top = maj_ax_top

    def get_boundaries(self):
        return self._min_ax_left, self._min_ax_right, self._maj_ax_bottom, self._maj_ax_top