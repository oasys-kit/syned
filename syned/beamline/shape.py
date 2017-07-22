
import numpy
from syned.syned_object import SynedObject

#
# main shape subclasses:
#      SurfaceShape to caracterize the shape (sphere etc.) of the optical element surface
#      BoundaryShape to characterize the optical element dimensions (rectangle, etc.)
#
class Shape(SynedObject):
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

class Plane(SurfaceShape):
    def __init__(self):
        super().__init__()

class Sphere(Conic):
    def __init__(self, radius):
        super().__init__()

        #TODO not correct, it is for centered sphere only
        self._conic_coefficients = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -self.radius**2]

    def get_radius(self):
        #TODO: this is not generic
        return numpy.sqrt(-self._conic_coefficients[9])

class Ellipsoid(SurfaceShape):
    def __init__(self, min_axis=0.0, maj_axis=0.0):
        super().__init__()

        self._min_axis = min_axis
        self._maj_axis = maj_axis

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003):
        self._min_axis, self._maj_axis = Ellipsoid.get_axis_from_p_q(p, q, grazing_angle)

    def get_p_q(self, grazing_angle=0.003):
        return Ellipsoid.get_p_q_from_axis(self._min_axis, self._maj_axis, grazing_angle)

    @classmethod
    def get_axis_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003):
        # see calculation of ellipse axis in shadow_kernel.f90 row 3605
        min_axis = 2*numpy.sqrt(p*q)*numpy.cos((0.5*numpy.pi) - grazing_angle)
        maj_axis = (p + q)

        return min_axis, maj_axis

    @classmethod
    def get_p_q_from_axis(cls, min_axis=2.0, maj_axis=1.0, grazing_angle=0.003):
        a = maj_axis/2
        b = min_axis/2
        p = a + numpy.sqrt(a**2 - (b/numpy.sin(grazing_angle))**2)
        q = maj_axis - p

        return p, q


class Paraboloid(SurfaceShape):
    def __init__(self, paraboloid_parameter):
        super().__init__()

        self._paraboloid_parameter = paraboloid_parameter

class Hyperboloid(SurfaceShape):
    def __init__(self, min_axis=0.0, maj_axis=0.0):
        super().__init__()

        self._min_axis = min_axis
        self._maj_axis = maj_axis

class Torus(SurfaceShape):
    def __init__(self, min_radius=0.0, maj_radius=0.0):
        super().__init__()

        self._min_radius = min_radius
        self._maj_radius = maj_radius

class NumbericalMesh(SurfaceShape):
    def __init__(self):
        super().__init__()



#
# subclasses for BoundaryShape
#


class Rectangle(BoundaryShape):
    def __init__(self, x_left=-0.010, x_right=0.010, y_bottom=-0.020, y_top=0.020):
        super().__init__()

        self._x_left   = x_left
        self._x_right  = x_right
        self._y_bottom = y_bottom
        self._y_top    = y_top

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("x_left    "      , "x (width) minimum (signed)   ", "m" ),
                    ("x_right   "      , "x (width) maximum (signed)   ", "m" ),
                    ("y_bottom  "      , "y (length) minimum (signed)  ", "m" ),
                    ("y_top     "      , "y (length) maximum (signed)  ", "m" ),
            ] )

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

        self._min_ax_left   = min_ax_left
        self._min_ax_right  = min_ax_right
        self._maj_ax_bottom = maj_ax_bottom
        self._maj_ax_top    = maj_ax_top
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("min_ax_left   "      , "x (width) semiaxis starts (signed)  ", "m" ),
                    ("min_ax_right  "      , "x (width) semiaxis ends (signed)    ", "m" ),
                    ("maj_ax_bottom "      , "y (length) semiaxis starts (signed) ", "m" ),
                    ("maj_ax_top    "      , "y (length) semiaxis ends (signed)   ", "m" ),
            ] )

    def get_boundaries(self):
        return self._min_ax_left, self._min_ax_right, self._maj_ax_bottom, self._maj_ax_top

    def get_axis(self):
        return numpy.abs(self._min_ax_right-self._min_ax_left), numpy.abs(self._maj_ax_top-self._maj_ax_bottom)

if __name__=="__main__":

    ell = Ellipsoid()
    ell.initialize_from_p_q(20, 10, 0.2618)

    print (ell._min_axis/2, ell._maj_axis/2)

    ell = Ellipsoid(min_axis=ell._min_axis, maj_axis=ell._maj_axis)

    print(ell.get_p_q(0.2618))