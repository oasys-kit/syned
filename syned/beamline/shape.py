"""
Classes with geometrical shapes.

    * Shape: Base class for all possible geometric shapes.
    * SurfaceShape: Base class to caracterize the shape (sphere, flat, etc.) of the optical element surface
    * BoundaryShape: Base class to characterize the optical element dimensions (rectangle, etc.).

Additional classes help to define flags:
    * Convexity:  NONE = -1, UPWARD = 0, DOWNWARD = 1
    * Direction:  TANGENTIAL = 0, SAGITTAL = 1
    * Side:       SOURCE = 0, IMAGE = 1
"""
import numpy
from syned.syned_object import SynedObject
from collections import OrderedDict

class Convexity:
    NONE = -1
    UPWARD = 0
    DOWNWARD = 1

class Direction:
    TANGENTIAL = 0
    SAGITTAL = 1

class Side:
    SOURCE = 0
    IMAGE = 1

class Shape(SynedObject):
    """
    Constructor.

    """
    def __init__(self):
        SynedObject.__init__(self)

class SurfaceShape(Shape):
    """
    Constructor.

    Parameters
    ----------
    convexity : int (as defined by Convexity), optional
        NONE = -1, UPWARD = 0, DOWNWARD = 1.

    """
    def __init__(self, convexity = Convexity.UPWARD):
        Shape.__init__(self)

        self._convexity = convexity

    def get_convexity(self):
        """
        Gets the convexity flag.

        Returns
        -------
        int
            NONE = -1, UPWARD = 0, DOWNWARD = 1

        """
        return self._convexity

class BoundaryShape(Shape):
    """
    Constructor.
    """
    def __init__(self):
        Shape.__init__(self)
        
    def get_boundaries(self):
        """
        Returns the boundary shape. It must be defined in the children classes.

        Raises
        ------
        NotImplementedError


        """
        raise NotImplementedError()

#############################
# Subclasses for SurfaceShape
#############################

class Cylinder(SynedObject):
    """
    Defines that a surface shape is cylindrical in one direction.

    Usage: must be used with double inheritance in other classes (e.g. ParabolicCylinder).
    It should not be used standalone.

    Parameters
    ----------
    cylinder_direction : int, optional
        TANGENTIAL = 0, SAGITTAL = 1.

    """
    def __init__(self, cylinder_direction=Direction.TANGENTIAL):
        self._cylinder_direction = cylinder_direction
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._add_support_text([
                    ("cylinder_direction"        , "(0=tangential, 1=sagittal)", " " ),
            ] )

    def get_cylinder_direction(self):
        """
        Returns the cylinder direction.

        Returns
        -------
        int
            TANGENTIAL = 0, SAGITTAL = 1.

        """
        return self._cylinder_direction

class Conic(SurfaceShape):
    """
    Defines a conic surface shape expresses via the 10 conic coeffcients.

    Parameters
    ----------
    conic_coefficients : list, optional
        A list with the 10 coefficients.

    """
    def __init__(self, 
                 conic_coefficients=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
        SurfaceShape.__init__(self, convexity=Convexity.NONE)

        # stored as numpy array, not as list, to avoid in i/o to interpret the items as syned objects.
        self._conic_coefficients = numpy.array(conic_coefficients)


        self._set_support_text([
                    ("conic_coefficients"         , "Conic coeffs.   ", " " ),
            ] )

    def get_conic_coefficients(self):
        """
        Returns the coefficients.

        Returns
        -------
        list
            A list with the 10 coefficients.

        """
        return list(self._conic_coefficients)

class Plane(SurfaceShape):
    """
    Defines a plane surface shape.
    """
    def __init__(self):
        SurfaceShape.__init__(self, convexity=Convexity.NONE)

class Sphere(SurfaceShape):
    """
    Defines an spherical surface.

    Parameters
    ----------
        radius : float
            The sphere radius.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.

    """
    def __init__(self, radius=1.0, convexity=Convexity.UPWARD):
        SurfaceShape.__init__(self, convexity=convexity)
        self._radius = radius

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("radius"         , "Sphere radius   ", "m" ),
                    ("convexity"                  , "(0=upwards, 1=downwards)", " "),
            ] )


    @classmethod
    def create_sphere_from_radius(cls, radius=0.0, convexity=Convexity.UPWARD):
        """
        Defines an spherical surface.

        Parameters
        ----------
            radius : float
                The sphere radius.
            convexity : int (as defined by Convexity), optional
                NONE = -1, UPWARD = 0, DOWNWARD = 1.

        Returns
        -------
        instance of Sphere

        """
        return Sphere(radius, convexity)

    @classmethod
    def create_sphere_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003, convexity=Convexity.UPWARD):
        """
        Defines an spherical surface.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.

        Returns
        -------
        instance of Sphere

        """
        sphere = Sphere(convexity=convexity)
        sphere.initialize_from_p_q(p, q, grazing_angle)

        return sphere

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Defines an spherical surface.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        """
        self._radius = Sphere.get_radius_from_p_q(p, q, grazing_angle)

    @classmethod
    def get_radius_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Calculates the radius of the sphere from factory parameters (1/p+1/q=2/(R sin theta_grazing)))

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        Returns
        -------
        float
            the calculated radius.

        """
        # 1/p + 1/q = 2/(R cos(pi/2 - gr.a.))
        return (2*p*q/(p+q))/numpy.sin(grazing_angle)

    def get_radius(self):
        """
        Returns the radius of the sphere.

        Returns
        -------
        float
            The radius of the sphere.

        """
        return self._radius


class SphericalCylinder(Sphere, Cylinder):
    """
    Constructor.

    Parameters
    ----------
    radius : float
        the radius of the circular section.
    convexity : int (as defined by Convexity), optional
        NONE = -1, UPWARD = 0, DOWNWARD = 1.
    cylinder_direction : int (as defined by Direction), optional
        NONE = -1, UPWARD = 0, DOWNWARD = 1.

    """
    def __init__(self, 
                 radius=1.0, 
                 convexity=Convexity.UPWARD, 
                 cylinder_direction=Direction.TANGENTIAL):
        Sphere.__init__(self, radius, convexity)
        Cylinder.__init__(self, cylinder_direction)

    @classmethod
    def create_spherical_cylinder_from_radius(cls, radius=0.0, convexity=Convexity.UPWARD, cylinder_direction=Direction.TANGENTIAL):
        """
        Creates a spherical cylinder.

        Parameters
        ----------
        radius : float
            the radius of the circular section.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.
        cylinder_direction : int (as defined by Direction), optional
            TANGENTIAL = 0, SAGITTAL = 1.

        Returns
        -------
        instance of SphericalCylinder

        """
        return SphericalCylinder(radius, convexity, cylinder_direction)

    @classmethod
    def create_spherical_cylinder_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003,
                                           convexity=Convexity.UPWARD, cylinder_direction=Direction.TANGENTIAL):
        """

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.
        cylinder_direction : int (as defined by Direction), optional
            TANGENTIAL = 0, SAGITTAL = 1.

        Returns
        -------
        instance of SphericalCylinder

        """
        spherical_cylinder = SphericalCylinder(convexity=convexity, cylinder_direction=cylinder_direction)
        spherical_cylinder.initialize_from_p_q(p, q, grazing_angle)

        return spherical_cylinder

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Calculates and sets the radius of curvature in the corresponding direction (tangential or sagittal.
        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        """
        if self._cylinder_direction == Direction.TANGENTIAL:
            self._radius = Sphere.get_radius_from_p_q(p, q, grazing_angle)
        elif self._cylinder_direction == Direction.SAGITTAL:
            self._radius = SphericalCylinder.get_radius_from_p_q_sagittal(p, q, grazing_angle)

    @classmethod
    def get_radius_from_p_q_sagittal(cls, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Calculates the sagittal radius from the factory parameters (1/p + 1/q = 2 sin(grazing_angle)/Rs).

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        Returns
        -------
        float
            The calculated radius.

        """
        # 1/p + 1/q = 2 cos(pi/2 - gr.a.)/r
        return (2*p*q/(p+q))*numpy.sin(grazing_angle)

class Ellipsoid(SurfaceShape):
    """
    Constructor.

    Ellipsoid: Revolution ellipsoid (rotation around major axis).
    It is defined with three parameters: axes of the ellipse and an additional parameter
    defining the position of the origin of the mirror. This additional parameter can be "p", "x0", "y0"
    or the angle beta from the ellipsoid center (tan(beta)=y0/x0). For simplicity, we store "p" in syned.

    Parameters
    ----------
    min_axis : float, optional
        the ellipse minor axis.
    maj_axis : float, optional
        the ellipse majot axis.
    p_focus : float, optional
        the distance from the first focus (source position) to the mirror pole.
    convexity : int (as defined by Convexity), optional
        NONE = -1, UPWARD = 0, DOWNWARD = 1.

    References
    ----------
    Some equations can be found here: https://github.com/srio/shadow3-docs/blob/master/doc/conics.pdf

    """
    def __init__(self, min_axis=0.0, maj_axis=0.0, p_focus=0.0, convexity=Convexity.UPWARD):
        SurfaceShape.__init__(self, convexity)

        self._min_axis = min_axis
        self._maj_axis = maj_axis
        self._p_focus  = p_focus
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("min_axis"         , "Ellipse major axis   ", "m" ),
                    ("maj_axis"         , "Ellipse minor axis   ", "m"),
                    ("min_axis"         , "Ellipse p (source-focus to pole)   ", "m"),
                    ("convexity"        , "(0=upwards, 1=downwards)", " "),
            ] )


    @classmethod
    def create_ellipsoid_from_axes(cls, min_axis=0.0, maj_axis=0.0, p_focus=0.0, convexity=Convexity.UPWARD):
        """
        Creates an ellipsoid.

        Parameters
        ----------
        min_axis : float, optional
            the ellipse minor axis.
        maj_axis : float, optional
            the ellipse majot axis.
        p_focus : float, optional
            the distance from the first focus (source position) to the mirror pole.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.

        Returns
        -------
        instance of Ellipsoid

        """
        return Ellipsoid(min_axis, maj_axis, p_focus, convexity)

    @classmethod
    def create_ellipsoid_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003, convexity=Convexity.UPWARD):
        """
        Creates an ellipsoid from factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.

        Returns
        -------
        instance of Ellipsoid

        """
        ellipsoid = Ellipsoid(convexity=convexity)
        ellipsoid.initialize_from_p_q(p, q, grazing_angle)

        return ellipsoid

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Sets the ellipsoid parameters as calculated from the factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        """
        self._min_axis, self._maj_axis = Ellipsoid.get_axis_from_p_q(p, q, grazing_angle)
        self._p_focus = p

    def initialize_from_shadow_parameters(self, axmaj=2.0, axmin=1.0, ell_the=0.003, convexity=Convexity.UPWARD):
        """
        Sets the ellipsoid parameters as calculated from the parameters used in SHADOW.

        Parameters
        ----------
        min_axis : float, optional
            the ellipse minor axis.
        maj_axis : float, optional
            the ellipse majot axis.
        ell_the : float, optional
            the angle beta from the ellipsoid center in rads.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.

        """
        tanbeta2 = numpy.tan(ell_the) ** 2
        y = axmaj * axmin / numpy.sqrt(axmin ** 2 + axmaj ** 2 * tanbeta2)
        z = y * numpy.tan(ell_the)
        c = numpy.sqrt(axmaj ** 2 - axmin ** 2)
        p = numpy.sqrt( (y + c)**2 + z**2)

        self.__init__(axmin, axmaj, p, convexity)

    def get_axes(self):
        """
        Returns the ellipsoid axes.
        Note that the third axis of the ellipsoid is the same as the minor axis (revolution ellipsoid).

        Returns
        -------
        tuple
            (minor_axis, major_axis)
        """
        return self._min_axis, self._maj_axis

    def get_p_q(self, grazing_angle=0.003):
        """
        Returns p and q for a given grazing angle.

        Parameters
        ----------
        grazing_angle : float
            The grazing angle in rad.

        Returns
        -------
        tuple
            (p, q)

        """
        return Ellipsoid.get_p_q_from_axis(self._min_axis, self._maj_axis, grazing_angle)

    # semiaxes etc
    def get_a(self):
        """
        Returns a = half of the major axis.

        Returns
        -------
        float

        """
        return 0.5 * self._maj_axis

    def get_b(self):
        """
        Returns b = half of the minor axis.

        Returns
        -------
        float

        """
        return 0.5 * self._min_axis

    def get_c(self):
        """
        Returns c = sqrt(a^2 - b^2).

        Returns
        -------
        float

        """
        return numpy.sqrt(self.get_a()**2 - self.get_b()**2)

    def get_p_focus(self):
        """
        Returns p (=p_focus).

        Returns
        -------
        float

        """
        return self._p_focus

    def get_q_focus(self):
        """
        Returns q.

        Returns
        -------
        float

        """
        return 2 * self.get_a() - self.get_p_focus()

    def get_eccentricity(self):
        """
        returns the eccentricity e = c / a.

        Returns
        -------
        float

        """
        return self.get_c() / self.get_a()

    def get_grazing_angle(self):
        """
        Returns the grazing angle.

        Returns
        -------
        float

        """
        return numpy.arcsin(self.get_b() / numpy.sqrt(self.get_p_focus() * self.get_q_focus()))

    def get_mirror_center(self):
        """
        Returns the coordinates of the mirror pole or center.

        Returns
        -------
        tuple
            (coor_along_axis_maj, coor_along_axis_min).

        """
        coor_along_axis_maj = (self.get_p_focus()**2 - self.get_q_focus()**1) / (4 * self.get_c())
        coor_along_axis_min = self.get_b * numpy.sqrt(1 - (coor_along_axis_maj / self.get_a())**2)
        return coor_along_axis_maj, coor_along_axis_min

    def get_angle_pole_from_origin(self):
        """
        Return the angle from pole to origin (beta).

        Returns
        -------
        float

        """
        x1, x2 = self.get_mirror_center()
        return numpy.arctan(x2 / x1)

    @classmethod
    def get_axis_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Calculates the ellipse axes from the factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        Returns
        -------
        tuple
            (minor_axis, major_axis).

        """
        # see calculation of ellipse axis in shadow_kernel.f90 row 3605
        min_axis = 2*numpy.sqrt(p*q)*numpy.sin(grazing_angle)
        maj_axis = (p + q)

        return min_axis, maj_axis

    @classmethod
    def get_p_q_from_axis(cls, min_axis=2.0, maj_axis=1.0, grazing_angle=0.003):
        """
        Calculates the p and q values from axis and grazing angle.

        Parameters
        ----------
        min_axis : float, optional
            the ellipse minor axis.
        maj_axis : float, optional
            the ellipse majot axis.
        grazing_angle : float, optional
            grazing angle in rad.

        Returns
        -------
        tuple
            (p, q).

        """
        a = maj_axis/2
        b = min_axis/2
        p = a + numpy.sqrt(a**2 - (b/numpy.sin(grazing_angle))**2)
        q = maj_axis - p

        return p, q

class EllipticalCylinder(Ellipsoid, Cylinder):
    """
    Constructor.

    Parameters
    ----------
    min_axis : float, optional
        the ellipse minor axis.
    maj_axis : float, optional
        the ellipse majot axis.
    p_focus : float, optional
        the distance from the first focus (source position) to the mirror pole.
    convexity : int (as defined by Convexity), optional
        NONE = -1, UPWARD = 0, DOWNWARD = 1.
    cylinder_direction : int (as defined by Direction), optional
        TANGENTIAL = 0, SAGITTAL = 1.

    """
    def __init__(self, 
                 min_axis=0.0, 
                 maj_axis=0.0, 
                 p_focus=0.0,
                 convexity=Convexity.UPWARD,
                 cylinder_direction=Direction.TANGENTIAL):
        Ellipsoid.__init__(self, min_axis, maj_axis, p_focus, convexity)
        Cylinder.__init__(self, cylinder_direction)

    @classmethod
    def create_elliptical_cylinder_from_axes(cls, min_axis=0.0, maj_axis=0.0, p_focus=0.0,
                                             convexity=Convexity.UPWARD, cylinder_direction=Direction.TANGENTIAL):
        """
        Returns an EllipticalCylinder instance from main parameters.

        Parameters
        ----------
        min_axis : float, optional
            the ellipse minor axis.
        maj_axis : float, optional
            the ellipse majot axis.
        p_focus : float, optional
            the distance from the first focus (source position) to the mirror pole.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.
        cylinder_direction : int (as defined by Direction), optional
            TANGENTIAL = 0, SAGITTAL = 1.

        Returns
        -------
        instance of EllipticalCylinder

        """
        return EllipticalCylinder(min_axis, maj_axis, p_focus, convexity, cylinder_direction)

    @classmethod
    def create_elliptical_cylinder_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003,
                                            convexity=Convexity.UPWARD, cylinder_direction=Direction.TANGENTIAL):
        """
        Returns an EllipticalCylinder instance from factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.
        cylinder_direction : int (as defined by Direction), optional
            TANGENTIAL = 0, SAGITTAL = 1.

        Returns
        -------
        instance of EllipticalCylinder

        """
        elliptical_cylinder = EllipticalCylinder(convexity=convexity, cylinder_direction=cylinder_direction)
        elliptical_cylinder.initialize_from_p_q(p, q, grazing_angle)

        return elliptical_cylinder

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Sets the ellipsoid parameters for given factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        """
        if self._cylinder_direction == Direction.SAGITTAL: raise NotImplementedError("Operation not possible for SAGITTAL direction")

        super().initialize_from_p_q(p, q, grazing_angle)

    def get_p_q(self, grazing_angle=0.003):
        """
        Returns p and q distances for a given grazing angle.

        Parameters
        ----------
        grazing_angle : float
            The grazing angle in rad.

        Returns
        -------
        tuple
            (p, q).

        """
        if self._cylinder_direction == Direction.SAGITTAL: raise NotImplementedError("Operation not possible for SAGITTAL direction")

        return super().get_p_q(grazing_angle)

class Hyperboloid(SurfaceShape):
    """
    Constructor.

    Hyperboloid: Revolution hyperboloid (two sheets: rotation around major axis).
    It is defined with three parameters: axes of the hyperbola and an additional parameter
    defining the position of the origin of the mirror. This additional parameter can be "p", "x0", "y0"
    or the angle beta from the ellipsoid center (tan(beta)=y0/x0). For simplicity, we store "p" in syned.

    Parameters
    ----------
    min_axis : float, optional
        the hyperbola minor axis.
    maj_axis : float, optional
        the hyperbola majot axis.
    p_focus : float, optional
        the distance from the first focus (source position) to the mirror pole.
    convexity : int (as defined by Convexity), optional
        NONE = -1, UPWARD = 0, DOWNWARD = 1.

    References
    ----------
    Some equations can be found here: https://github.com/srio/shadow3-docs/blob/master/doc/conics.pdf

    """
    def __init__(self, min_axis=0.0, maj_axis=0.0, p_focus=0.0, convexity=Convexity.UPWARD):
        SurfaceShape.__init__(self, convexity)

        self._min_axis = min_axis
        self._maj_axis = maj_axis
        self._p_focus  = p_focus
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("min_axis"         , "Hyperbola major axis   ", "m" ),
                    ("maj_axis"         , "Hyperbola minor axis   ", "m"),
                    ("min_axis"         , "Hyperbola p (source-focus to pole)   ", "m"),
                    ("convexity"        , "(0=upwards, 1=downwards)", " "),
            ] )

    @classmethod
    def create_hyperboloid_from_axes(cls, min_axis=0.0, maj_axis=0.0, p_focus=0.0, convexity=Convexity.UPWARD):
        """
        Creates an hyperboloid from main parameters.

        Parameters
        ----------
        min_axis : float, optional
            the ellipse minor axis.
        maj_axis : float, optional
            the ellipse majot axis.
        p_focus : float, optional
            the angle beta from the hyperbola center in rads.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.

        Returns
        -------
        instance of Hyperboloid

        """
        return Hyperboloid(min_axis, maj_axis, p_focus, convexity)

    @classmethod
    def create_hyperboloid_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003, convexity=Convexity.UPWARD):
        """
        Creates an hyperboloid from factory parameters.

        Parameters
        ----------
        p : float, optional
           distance source-optical element.
        q : float, optional
           distance optical element to focus.
        grazing_angle : float, optional
           grazing angle in rad.
        convexity : int (as defined by Convexity), optional
           NONE = -1, UPWARD = 0, DOWNWARD = 1.

        Returns
        -------
        instance of Hyoerboloid

        """
        hyperboloid = Hyperboloid(convexity=convexity)
        hyperboloid.initialize_from_p_q(p, q, grazing_angle)

        return hyperboloid

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Sets the hyperboloid parameters as calculated from the factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        """
        self._min_axis, self._maj_axis = Hyperboloid.get_axis_from_p_q(p, q, grazing_angle)
        self._p_focus = p

    # TODO:
    def initialize_from_shadow_parameters(self, axmaj=2.0, axmin=1.0, ell_the=0.003, convexity=Convexity.UPWARD):
        """
           Sets the hyperboloid parameters as calculated from the parameters used in SHADOW.
           Note that in SHADOW3 the definition of the hyperbola from the factory parameters is buggy.

        Raises
        ------
        NotImplementedError

        """
        raise NotImplementedError("TODO")

    def get_axes(self):
        """
        Returns the hyperboloid axes.
        Note that the third axis of the ellipsoid is the same as the minor axis (revolution ellipsoid).

        Returns
        -------
        tuple
            (minor_axis, major_axis)
        """
        return self._min_axis, self._maj_axis

    def get_p_q(self, grazing_angle=0.003):
        """
        Returns p and q for a given grazing angle.

        Parameters
        ----------
        grazing_angle : float
            The grazing angle in rad.

        Returns
        -------
        tuple
            (p, q)

        """
        return Hyperboloid.get_p_q_from_axis(self._min_axis, self._maj_axis, grazing_angle)

    # semiaxes etc
    def get_a(self):
        """
        Returns a = half of the major axis.

        Returns
        -------
        float

        """
        return 0.5 * self._maj_axis

    def get_b(self):
        """
        Returns b = half of the minor axis.

        Returns
        -------
        float

        """
        return 0.5 * self._min_axis

    def get_c(self):
        """
        Returns c = sqrt(a^2 + b^2).

        Returns
        -------
        float

        """
        return numpy.sqrt(self.get_a()**2 + self.get_b()**2)

    def get_p_focus(self):
        """
        Returns p (=p_focus).

        Returns
        -------
        float

        """
        return self._p_focus

    def get_q_focus(self):
        """
        Returns q.

        Returns
        -------
        float

        """
        return self.get_p_focus() - 2 * self.get_a()

    def get_eccentricity(self):
        """
        returns the eccentricity e = c / a.

        Returns
        -------
        float

        """
        return self.get_c / self.get_a()

    def get_grazing_angle(self):
        """
        Returns the grazing angle.

        Returns
        -------
        float

        """
        return numpy.arcsin(self.get_b() / numpy.sqrt(self.get_p_focus() * self.get_q_focus()))


    def get_mirror_center(self):  #TODO:
        """
        Returns the coordinates of the mirror pole or center.

        Raises
        ------
        NotImplementedError

        """
        raise NotImplementedError("TODO")

    def get_angle_pole_from_origin(self):  #TODO:
        """
        Return the angle from pole to origin (beta).

        Raises
        ------
        NotImplementedError

        """
        raise NotImplementedError("TODO")

    @classmethod
    def get_axis_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003, branch_sign=+1):
        """
        Calculates the hyperbola axes from the factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.
        branch_sign : int
            +1 (positive) or -1 (negative) branch.

        Returns
        -------
        tuple
            (minor_axis, major_axis).

        """
        min_axis = 2*numpy.sqrt(p*q)*numpy.sin(grazing_angle)
        maj_axis = (p - q) * branch_sign

        return min_axis, maj_axis

    # TODO:
    @classmethod
    def get_p_q_from_axis(cls, min_axis=2.0, maj_axis=1.0, grazing_angle=0.003):
        """
        Calculates the p and q values from axis and grazing angle.

        Raises
        ------
        NotImplementedError

        """
        raise NotImplementedError("TODO")

class HyperbolicCylinder(Hyperboloid, Cylinder):
    """
    Constructor.

    Parameters
    ----------
    min_axis : float, optional
        the ellipse minor axis.
    maj_axis : float, optional
        the ellipse majot axis.
    p_focus : float, optional
        the distance from the first focus (source position) to the mirror pole.
    convexity : int (as defined by Convexity), optional
        NONE = -1, UPWARD = 0, DOWNWARD = 1.
    cylinder_direction : int (as defined by Direction), optional
        TANGENTIAL = 0, SAGITTAL = 1.

    """
    def __init__(self, 
                 min_axis=0.0, 
                 maj_axis=0.0, 
                 p_focus=0.0,
                 convexity=Convexity.UPWARD, 
                 cylinder_direction=Direction.TANGENTIAL):
        Hyperboloid.__init__(self, min_axis, maj_axis, p_focus, convexity)
        Cylinder.__init__(self, cylinder_direction)


    @classmethod
    def create_hyperbolic_cylinder_from_axes(cls, min_axis=0.0, maj_axis=0.0, p_focus=0.0,
                                             convexity=Convexity.UPWARD, cylinder_direction=Direction.TANGENTIAL):
        """
         Returns an HyperbolicCylinder instance from main parameters.

         Parameters
         ----------
         min_axis : float, optional
             the ellipse minor axis.
         maj_axis : float, optional
             the ellipse majot axis.
         p_focus : float, optional
             the distance from the first focus (source position) to the mirror pole.
         convexity : int (as defined by Convexity), optional
             NONE = -1, UPWARD = 0, DOWNWARD = 1.
         cylinder_direction : int (as defined by Direction), optional
             TANGENTIAL = 0, SAGITTAL = 1.

         Returns
         -------
         instance of HyperbolicCylinder

         """
        return HyperbolicCylinder(min_axis, maj_axis, p_focus, convexity, cylinder_direction)

    @classmethod
    def create_hyperbolic_cylinder_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003,
                                            convexity=Convexity.UPWARD, cylinder_direction=Direction.TANGENTIAL):
        """
        Returns an HyperbolicCylinder instance from factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.
        cylinder_direction : int (as defined by Direction), optional
            TANGENTIAL = 0, SAGITTAL = 1.

        Returns
        -------
        instance of HyperbolicCylinder

        """
        hyperbolic_cylinder = HyperbolicCylinder(convexity=convexity, cylinder_direction=cylinder_direction)
        hyperbolic_cylinder.initialize_from_p_q(p, q, grazing_angle)

        return hyperbolic_cylinder

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Sets the hyperboloid parameters for given factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        """
        if self._cylinder_direction == Direction.SAGITTAL: raise NotImplementedError("Operation not possible for SAGITTAL direction")

        super().initialize_from_p_q(p, q, grazing_angle)

    def get_p_q(self, grazing_angle=0.003):
        """
        Returns p and q distances for a given grazing angle.

        Parameters
        ----------
        grazing_angle : float
            The grazing angle in rad.

        Returns
        -------
        tuple
            (p, q).

        """
        if self._cylinder_direction == Direction.SAGITTAL: raise NotImplementedError("Operation not possible for SAGITTAL direction")

        return super().get_p_q(grazing_angle)

class Paraboloid(SurfaceShape):
    """
    Constructor.

    Paraboloid: Revolution paraboloid (rotation around symmetry axis).

    It is defined with three parameters: the parabola_parameter and two more parameters
    defining the position of the origin of the mirror.

    The parabola_parameter = 2 * focal_length = - 0.5 * ccc_9 / ccc_2

    The additional parameter can be the focal distances
    ("p" or "q", one is infinity), "x0", "y0" or the grazing angle.
    Here, we selected the at_infinity and the finite focal distance p or q or distance from
    the mirror pole to focus (pole to focus).

    The parabola equation is:

    ccc_2 y^2 + ccc_9 z = 0 or

    y^2 = -ccc_9/ccc_2 z = 2 parabola_parameter z = 4 focal_length z

    The focus is at (0, 0, focal_length).

    The directrix is at (0, 0, -focal_length).

    The distance from the directrix to focus is 2 * focal_length.

    The radius of curvature at the vertex is 2 * focal_length.

    Parameters
    ----------
    parabola_parameter : float, optional
        parabola_parameter = 2 * focal_length = - 0.5 * ccc_9 / ccc_2. Equation: y^2 = 2 parabola_parameter z.
    at_infinity : int (as defined by Side), optional
        SOURCE = 0, IMAGE = 1.
    pole_to_focus : float, optional
        The p distance.
    convexity : int (as defined by Convexity), optional
        NONE = -1, UPWARD = 0, DOWNWARD = 1.

    References
    ----------
    https://en.wikipedia.org/wiki/Parabola

    https://doi.org/10.1107/S1600577522004593

    Some equations can be found here: https://github.com/srio/shadow3-docs/blob/master/doc/conics.pdf

    """
    def __init__(self,
                 parabola_parameter=0.0,
                 at_infinity=Side.SOURCE,
                 pole_to_focus=None,
                 convexity=Convexity.UPWARD):
        SurfaceShape.__init__(self, convexity)

        self._parabola_parameter = parabola_parameter
        self._at_infinity = at_infinity
        self._pole_to_focus = pole_to_focus
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("parabola_parameter"         , "Parabola parameter   ", "m" ),
                    ("at_infinity"                , "(0=source, 1=image)", " " ),
                    ("pole_to_focus"              , "pole to focus", "m"),
                    ("convexity"                  , "(0=upwards, 1=downwards)", " "),
            ] )

    @classmethod
    def create_paraboloid_from_parabola_parameter(cls, parabola_parameter=0.0, at_infinity=Side.SOURCE,
                                                  pole_to_focus=None, convexity=Convexity.UPWARD):
        """
        Create a paraboloid.

        Parameters
        ----------
        parabola_parameter : float, optional
            parabola_parameter = 2 * focal_distance = - 0.5 * ccc_9 / ccc_2.
        at_infinity : int (as defined by Side), optional
            SOURCE = 0, IMAGE = 1.
        pole_to_focus : float, optional
            The p distance.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.

        Returns
        -------
        instance of Paraboloid

        """
        return Paraboloid(parabola_parameter, at_infinity=at_infinity, pole_to_focus=pole_to_focus, convexity=convexity)

    @classmethod
    def create_paraboloid_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003,
                                   at_infinity=Side.SOURCE, convexity=Convexity.UPWARD):
        """
        Creates a paraboloid from the factory parameters.

        Parameters
        ----------
        p : float
            The distance p (used if at_infinity=Side.IMAGE)
        q : float
            The distance q (used if at_infinity=Side.SOURCE)
        grazing_angle : float
            The distance p
        at_infinity : int (as defined by Side), optional
            SOURCE = 0, IMAGE = 1.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.

        Returns
        -------
        instance of Paraboloid

        """
        paraboloid = Paraboloid(convexity=convexity)
        paraboloid.initialize_from_p_q(p, q, grazing_angle=grazing_angle, at_infinity=at_infinity)

        return paraboloid

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003, at_infinity=Side.SOURCE):
        """
        Sets the paraboloid parameters as calculated from the factory parameters.

        Parameters
        ----------
        p : float
            The distance p (used if at_infinity=Side.IMAGE)
        q : float
            The distance q (used if at_infinity=Side.SOURCE)
        grazing_angle : float
            The distance p
        at_infinity : int (as defined by Side), optional
            SOURCE = 0, IMAGE = 1.

        Returns
        -------
        instance of Paraboloid

        """
        self._parabola_parameter = Paraboloid.get_parabola_parameter_from_p_q(p=p, q=q, grazing_angle=grazing_angle, at_infinity=at_infinity)
        self._at_infinity = at_infinity
        if at_infinity == Side.SOURCE:
            self._pole_to_focus = q
        elif at_infinity == Side.IMAGE:
            self._pole_to_focus = p

    @classmethod
    def get_parabola_parameter_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003, at_infinity=Side.SOURCE):
        """
        Calculates the parabola parameter from the factory parameters.

        Parameters
        ----------
        p : float
            The distance p (used if at_infinity=Side.IMAGE)
        q : float
            The distance q (used if at_infinity=Side.SOURCE)
        grazing_angle : float
            The distance p
        at_infinity : int (as defined by Side), optional
            SOURCE = 0, IMAGE = 1.

        Returns
        -------
        float
            The parabola parameter.

        """
        if at_infinity == Side.IMAGE:
            return 2*p*(numpy.sin(grazing_angle))**2
        elif at_infinity == Side.SOURCE:
            return 2*q*(numpy.sin(grazing_angle))**2

    def get_parabola_parameter(self):
        """
        Returns the parabola parameter.

        Returns
        -------
        float

        """
        return self._parabola_parameter

    def get_at_infinity(self):
        """
        Returns the "at_infinity" flag.

        Returns
        -------
        int (as defined by Side)
            SOURCE = 0, IMAGE = 1.

        """
        return self._at_infinity

    def get_pole_to_focus(self):
        """
        Returns the distance from focus to pole.

        Returns
        -------
        float

        """
        return self._pole_to_focus

    def get_grazing_angle(self):
        """
        Returns the grazing angle.

        Returns
        -------
        float

        """
        return numpy.arcsin( numpy.sqrt( self.get_parabola_parameter() / (2 * self.get_pole_to_focus())))


class ParabolicCylinder(Paraboloid, Cylinder):
    """
    Constructor.

    Parameters
    ----------
        parabola_parameter : float, optional
            parabola_parameter = 2 * focal_distance = - 0.5 * ccc_9 / ccc_2.
        at_infinity : int (as defined by Side), optional
            SOURCE = 0, IMAGE = 1.
        pole_to_focus : float, optional
            The p distance.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.
        cylinder_direction : int (as defined by Direction), optional
            TANGENTIAL = 0, SAGITTAL = 1.

    """
    def __init__(self,
                 parabola_parameter=0.0,
                 at_infinity=Side.SOURCE,
                 pole_to_focus=None,
                 convexity=Convexity.UPWARD,
                 cylinder_direction=Direction.TANGENTIAL):
        Paraboloid.__init__(self, parabola_parameter=parabola_parameter, at_infinity=at_infinity,
                            pole_to_focus=pole_to_focus, convexity=convexity)
        Cylinder.__init__(self, cylinder_direction)

    @classmethod
    def create_parabolic_cylinder_from_parabola_parameter(cls,
                                                          parabola_parameter=0.0,
                                                          at_infinity=Side.SOURCE,
                                                          pole_to_focus=None,
                                                          convexity=Convexity.UPWARD,
                                                          cylinder_direction=Direction.TANGENTIAL):
        """
        Returns a ParabolicCylinder instance.

        Parameters
        ----------
        parabola_parameter : float, optional
            parabola_parameter = 2 * focal_distance = - 0.5 * ccc_9 / ccc_2.
        at_infinity : int (as defined by Side), optional
            SOURCE = 0, IMAGE = 1.
        pole_to_focus : float, optional
            The p distance.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.
        cylinder_direction : int (as defined by Direction), optional
            TANGENTIAL = 0, SAGITTAL = 1.

        Returns
        -------
        instance of ParabolicCylinder

        """
        return ParabolicCylinder(parabola_parameter, at_infinity, pole_to_focus, convexity, cylinder_direction)

    @classmethod
    def create_parabolic_cylinder_from_p_q(cls,
                                           p=2.0,
                                           q=1.0,
                                           grazing_angle=0.003,
                                           at_infinity=Side.SOURCE,
                                           convexity=Convexity.UPWARD,
                                           cylinder_direction=Direction.TANGENTIAL):
        """
        Returns a ParabolicCylinder instance from factory parameters.

        Parameters
        ----------
        p : float
            The distance p (used if at_infinity=Side.IMAGE)
        q : float
            The distance q (used if at_infinity=Side.SOURCE)
        grazing_angle : float
            The distance p
        at_infinity : int (as defined by Side), optional
            SOURCE = 0, IMAGE = 1.
        convexity : int (as defined by Convexity), optional
            NONE = -1, UPWARD = 0, DOWNWARD = 1.
        cylinder_direction : int (as defined by Direction), optional
            TANGENTIAL = 0, SAGITTAL = 1.

        Returns
        -------
        instance of ParabolicCylinder

        """
        parabolic_cylinder = ParabolicCylinder(convexity=convexity, cylinder_direction=cylinder_direction)
        parabolic_cylinder.initialize_from_p_q(p, q, grazing_angle, at_infinity)

        return parabolic_cylinder

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003, at_infinity=Side.SOURCE):
        """
        Sets the parameters calculated from factory parameters.

        Parameters
        ----------
        p : float
            The distance p (used if at_infinity=Side.IMAGE)
        q : float
            The distance q (used if at_infinity=Side.SOURCE)
        grazing_angle : float
            The distance p
        at_infinity : int (as defined by Side), optional
            SOURCE = 0, IMAGE = 1.

        Returns
        -------
        instance of ParabolicCylinder

        """
        if self._cylinder_direction == Direction.SAGITTAL:
            raise NotImplementedError("Operation not possible for SAGITTAL direction")

        return super().initialize_from_p_q(p, q, grazing_angle, at_infinity)

class Toroid(SurfaceShape):
    """
    Creator.

    Parameters
    ----------
    min_radius : float, optional
        The toroid minor radius
    maj_radius : float, optional
        The toroid major radius. Note that this is the "optical" major radius at the farest surface from the center
        of the toroid. Indeed, it corresponds to the "toroid major radius" plus the min_radius.

    """
    def __init__(self, min_radius=0.0, maj_radius=0.0):
        SurfaceShape.__init__(self, convexity=Convexity.NONE)
        
        self._min_radius = min_radius
        self._maj_radius = maj_radius

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("min_radius"         , "Minor radius r   ", "m" ),
                    ("maj_radius"         , "Major (optical) radius R (R=Ro+r)", "m" ),
            ] )

    @classmethod
    def create_toroid_from_radii(cls, min_radius=0.0, maj_radius=0.0):
        """
        returns a Toroid from main parameters (radii).

        Parameters
        ----------
        min_radius : float, optional
            The toroid minor radius
        maj_radius : float, optional
            The toroid major radius. Note that this is the "optical" major radius at the farest surface from the center
            of the toroid. Indeed, it corresponds to the "toroid major radius" plus the min_radius.

        Returns
        -------
        instance of Toroid

        """
        return Toroid(min_radius, maj_radius)

    @classmethod
    def create_toroid_from_p_q(cls, p=2.0, q=1.0, grazing_angle=0.003):
        """
        returns a Toroid from factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        Returns
        -------
        instance of Toroid

        """
        R = 2 / numpy.sin(grazing_angle) * p * q / (p + q)
        r = 2 * numpy.sin(grazing_angle) * p * q / (p + q)
        return Toroid(min_radius=r, maj_radius=R)

    def get_radii(self):
        """
        Returns the radii.

        Returns
        -------
        tuple
            (min_radius, maj_radius).

        """
        return self._min_radius, self._maj_radius

    def get_min_radius(self):
        """
        Returns the minor radius.

        Returns
        -------
        float

        """
        return self._min_radius

    def get_maj_radius(self):
        """
        Returns the major (optical) radius.

        Returns
        -------
        float

        """
        return self._maj_radius

    def initialize_from_p_q(self, p=2.0, q=1.0, grazing_angle=0.003):
        """
        Sets the parameters calculated from the factory parameters.

        Parameters
        ----------
        p : float, optional
            distance source-optical element.
        q : float, optional
            distance optical element to focus.
        grazing_angle : float, optional
            grazing angle in rad.

        """
        self._maj_radius = Sphere.get_radius_from_p_q(p, q, grazing_angle)
        self._min_radius = SphericalCylinder.get_radius_from_p_q_sagittal(p, q, grazing_angle)

        # FROM SHADOW3:
        #! C
        #! C NOTE : The major radius is the in reality the radius of the torus
        #! C max. circle. The true major radius is then
        #! C
        #        R_MAJ	=   R_MAJ - R_MIN
        self._maj_radius -= self._min_radius


# This is exactly the same as OasysSurfaceData
# class OasysSurfaceData(object):
class NumericalMesh(SurfaceShape):
    """
    Implements an optical surface from a numerical mesh.

    Constructor.

    Parameters
    ----------
    xx : numpy array, optional
        The x vector.
    yy : numpy array, optional
        The y vector.
    zz : numpy array, optional
        The z (2D) array.
    surface_data_file : str, optional
        a file name from where the dara may come.

    Notes
    -----
    This is exactly the same as OasysSurfaceData class OasysSurfaceData(object), with added methods.

    """
    def __init__(self,
                 xx=None,
                 yy=None,
                 zz=None,
                 surface_data_file=None):
        self._xx = xx
        self._yy = yy
        self._zz = zz
        self._surface_data_file=surface_data_file

    def has_surface_data(self):
        """
        Returns True is data is loaded.

        Returns
        -------
        boolean

        """
        return not (self._xx is None or self._yy is None or self._zz is None)

    def has_surface_data_file(self):
        """
        Returns True is data file is set.

        Returns
        -------
        boolean

        """
        return not self._surface_data_file is None


##############################
# subclasses for BoundaryShape
##############################


class Rectangle(BoundaryShape):
    """
    Constructor.

    Parameters
    ----------
    x_left : float, optional
        The coordinate (signed) of the minimum (left) along the X axis.
    x_right : float, optional
        The coordinate (signed) of the maximum (right) along the X axis.
    y_bottom : float, optional
        The coordinate (signed) of the minimum (left) along the Y axis.
    y_top : float, optional
        The coordinate (signed) of the maximum (right) along the Y axis.
    """
    def __init__(self, x_left=-0.010, x_right=0.010, y_bottom=-0.020, y_top=0.020):
        super().__init__()

        self._x_left   = x_left
        self._x_right  = x_right
        self._y_bottom = y_bottom
        self._y_top    = y_top

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("x_left"          , "x (width) minimum (signed)   ", "m" ),
                    ("x_right"         , "x (width) maximum (signed)   ", "m" ),
                    ("y_bottom"        , "y (length) minimum (signed)  ", "m" ),
                    ("y_top"           , "y (length) maximum (signed)  ", "m" ),
            ] )

    def get_boundaries(self):
        """
        Return the rectangle coordinates.

        Returns
        -------
        tuple
            (x_left, x_right, y_bottom, y_top).

        """
        return self._x_left, self._x_right, self._y_bottom, self._y_top

    def set_boundaries(self,x_left=-0.010, x_right=0.010, y_bottom=-0.020, y_top=0.020):
        """
        Sets the rectangle coordinates.

        Parameters
        ----------
        x_left : float, optional
            The coordinate (signed) of the minimum (left) along the X axis.
        x_right : float, optional
            The coordinate (signed) of the maximum (right) along the X axis.
        y_bottom : float, optional
            The coordinate (signed) of the minimum (left) along the Y axis.
        y_top : float, optional
            The coordinate (signed) of the maximum (right) along the Y axis.

        """
        self._x_left = x_left
        self._x_right = x_right
        self._y_bottom = y_bottom
        self._y_top = y_top

    def set_width_and_length(self,width=10e-3,length=30e-3):
        """
        Sets the rectangle parameters from width and length (centered at the origin).

        Parameters
        ----------
        width : float, optional
            The rectangle width.
        length : float, optional
            The rectangle length.

        """
        self._x_left = -0.5 * width
        self._x_right = 0.5 * width
        self._y_bottom = -0.5 * length
        self._y_top = 0.5 * length

class Ellipse(BoundaryShape):
    """
    Constructor.

    Parameters
    ----------
    a_axis_min : float, optional
        The coordinate (signed) of the minimum (left) along the major axis.
    a_axis_max : float, optional
        The coordinate (signed) of the maximum (right) along the major axis.
    b_axis_min : float, optional
        The coordinate (signed) of the minimum (left) along the minor axis.
    b_axis_max : float, optional
        The coordinate (signed) of the maximum (right) along the minor axis.

    """
    def __init__(self, a_axis_min=-10e-6, a_axis_max=10e-6, b_axis_min=-5e-6, b_axis_max=5e-6):
        super().__init__()

        self._a_axis_min   = a_axis_min
        self._a_axis_max  = a_axis_max
        self._b_axis_min = b_axis_min
        self._b_axis_max    = b_axis_max
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("a_axis_min"         , "x (width) axis starts (signed)  ", "m" ),
                    ("a_axis_max"        , "x (width) axis ends (signed)    ", "m" ),
                    ("b_axis_min"       , "y (length) axis starts (signed) ", "m" ),
                    ("b_axis_max"          , "y (length) axis ends (signed)   ", "m" ),
            ] )

    def get_boundaries(self):
        """
        Returns the coordinates of the ellipse.

        Returns
        -------
        tuple
            (a_axis_min, a_axis_max, b_axis_min, b_axis_max).

        """
        return self._a_axis_min, self._a_axis_max, self._b_axis_min, self._b_axis_max

    def get_axis(self):
        """
        Returns the length of the ellipse axes.

        Returns
        -------
        tuple
            (a_length, b_length).

        """
        return numpy.abs(self._a_axis_max - self._a_axis_min), numpy.abs(self._b_axis_max - self._b_axis_min)


class TwoEllipses(BoundaryShape):
    """
    Constructor.

    Parameters
    ----------
    a1_axis_min : float, optional
        The coordinate (signed) of the minimum (left) along the major axis of ellipse 1.
    a1_axis_max : float, optional
        The coordinate (signed) of the maximum (right) along the major axis of ellipse 1.
    b1_axis_min : float, optional
        TThe coordinate (signed) of the minimum (left) along the minor axis of ellipse 1.
    b1_axis_max : float, optional
        The coordinate (signed) of the maximum (right) along the minor axis of ellipse 1.
    a2_axis_min : float, optional
        The coordinate (signed) of the minimum (left) along the major axis of ellipse 2.
    a2_axis_max : float, optional
        The coordinate (signed) of the maximum (right) along the major axis of ellipse 2.
    b2_axis_min : float, optional
        TThe coordinate (signed) of the minimum (left) along the minor axis of ellipse 2.
    b2_axis_max : float, optional
        The coordinate (signed) of the maximum (right) along the minor axis of ellipse 2.

    """
    def __init__(self,
                 a1_axis_min=-10e-6, a1_axis_max=10e-6, b1_axis_min=-5e-6, b1_axis_max=5e-6,
                 a2_axis_min=-20e-6, a2_axis_max=20e-6, b2_axis_min=-8e-6, b2_axis_max=8e-6):
        super().__init__()

        self._a1_axis_min = a1_axis_min
        self._a1_axis_max = a1_axis_max
        self._b1_axis_min = b1_axis_min
        self._b1_axis_max = b1_axis_max
        self._a2_axis_min = a2_axis_min
        self._a2_axis_max = a2_axis_max
        self._b2_axis_min = b2_axis_min
        self._b2_axis_max = b2_axis_max
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("a1_axis_min", "x (width) axis 1 starts (signed)  ", "m" ),
                    ("a1_axis_max", "x (width) axis 1 ends (signed)    ", "m" ),
                    ("b1_axis_min", "y (length) axis 1 starts (signed) ", "m" ),
                    ("b1_axis_max", "y (length) axis 1 ends (signed)   ", "m" ),
                    ("a2_axis_min", "x (width) axis 2 starts (signed)  ", "m"),
                    ("a2_axis_max", "x (width) axis 2 ends (signed)    ", "m"),
                    ("b2_axis_min", "y (length) axis 2 starts (signed) ", "m"),
                    ("b2_axis_max", "y (length) axis 2 ends (signed)   ", "m"),
            ] )

    def get_boundaries(self):
        """
        Return the coordinates of the ellipses.

        Returns
        -------
        tuple
            (a1_axis_min, a1_axis_max, b1_axis_min, b1_axis_max, a2_axis_min, a2_axis_max, b2_axis_min, b2_axis_max).

        """
        return \
            self._a1_axis_min, self._a1_axis_max, self._b1_axis_min, self._b1_axis_max, \
            self._a2_axis_min, self._a2_axis_max, self._b2_axis_min, self._b2_axis_max

    def get_axis(self):
        """
        Returns the lengths of the axes of the two ellipses.

        Returns
        -------
        tuple
            (a1_length, b1_length, a2_length, b2_length).

        """
        return \
            numpy.abs(self._a1_axis_max - self._a1_axis_min), numpy.abs(self._b1_axis_max - self._b2_axis_min), \
            numpy.abs(self._a2_axis_max - self._a2_axis_min), numpy.abs(self._b2_axis_max - self._b2_axis_min)


class Circle(BoundaryShape):
    """
    Constructor.

    Parameters
    ----------
    radius : float
        The radius of the circle.
    x_center : float
        The x coordinate of the center of the circle.
    y_center   : float
        The y coordinate of the center of the circle.

    """
    def __init__(self,radius=50e-6,x_center=0.0,y_center=0.0):
        super().__init__()

        self._radius = radius
        self._x_center = x_center
        self._y_center = y_center
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("radius"              , "radius  ", "m" ),
                    ("x_center"            , "x center (signed)    ", "m" ),
                    ("y_center"            , "y center (signed)    ", "m" ),
            ] )

    def get_boundaries(self):
        """
        Returns the circle parameters.

        Returns
        -------
        tuple
            (radius, x_center, y_center).

        """
        return self._radius, self._x_center, self._y_center

    def set_boundaries(self, radius=1.0, x_center=0.0, y_center=0.0):
        """
        Sets the circle parameters.

        Parameters
        ----------
        radius : float
            The radius of the circle.
        x_center : float
            The x coordinate of the center of the circle.
        y_center   : float
            The y coordinate of the center of the circle.

        """
        self._radius = radius
        self._x_center = x_center
        self._y_center = y_center

    def get_radius(self):
        """
        Returns the radius of the circle.

        Returns
        -------
        float

        """
        return self._radius

    def get_center(self):
        """
        Returns the coordinates of the circle.

        Returns
        -------
        list
            [x_center, y_center]

        """
        return [self._x_center,self._y_center]

class Polygon(BoundaryShape):
    """
    Constructor.

    Parameters
    ----------
    x : list, optional
        A list with the X coordinates of the patch vertices.
    y : list, optional
        A list with the Y coordinates of the patch vertices.

    """
    def __init__(self,x=[],y=[]):
        super().__init__()

        self._x = numpy.array(x)
        self._y = numpy.array(y)
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("x"            , "x vertices    ", "m" ),
                    ("y"            , "y vertices    ", "m" ),
            ] )

    def get_boundaries(self):
        """
        Returns the coordinates of the patch vertices.

        Returns
        -------
        tuple
            (list_of_x_coordinates, list_of_y_coordinates).

        """
        return self._x, self._y

    def set_boundaries(self, x, y):
        """
        Sets the coordinates of the patch vertices.

        Parameters
        ----------
        x : list
            A list with the X coordinates of the patch vertices.
        y : list
            A list with the Y coordinates of the patch vertices.

        """
        self._x = numpy.array(x)
        self._y = numpy.array(y)

    def get_number_of_vertices(self):
        """
        Returns the number of vertices.

        Returns
        -------
        int

        """
        n = numpy.array(self._x).size
        if (numpy.abs(self._x[0] - self._x[-1]) < 1e-10)  and (numpy.abs(self._y[0] - self._y[-1]) < 1e-10):
            # print(">>>>> same first and last point")
            n -= 1
        return n

    def get_polygon(self):
        """
        Returns the vertices arranges as a polugon.

        Returns
        -------
        list
            [[x0,y0], [x1,y1], ...]

        """
        polygon = []
        for i in range(self.get_number_of_vertices()):
            polygon.append([self._x[i], self._y[i]])

        return polygon

    def check_inside_vector(self, x0, y0):
        """
        Checks if a set of points are inside the patch (closed as polygon).

        Parameters
        ----------
        x0 : numpy array
            The X coordinates of the points to check.
        y0 : numpy array
            The Y coordinates of the points to check.

        Returns
        -------
        numpy array
            0=No, 1=Yes (inside).

        References
        ----------
        https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python

        """
        # see https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
        poly = self.get_polygon()
        n = len(poly)
        x = numpy.array(x0)
        y = numpy.array(y0)

        inside = numpy.zeros(x.size, numpy.bool_)
        p2x = 0.0
        p2y = 0.0
        xints = 0.0
        p1x, p1y = poly[0]

        for i in range(n + 1):
            p2x, p2y = poly[i % n]

            idx = numpy.nonzero((y > min(p1y, p2y)) & (y <= max(p1y, p2y)) & (x <= max(p1x, p2x)))[0]
            if len(idx > 0): # added intuitively by srio TODO: make some tests to compare with self.check_insize
                if p1y != p2y:
                    xints = (y[idx] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x:
                    inside[idx] = ~inside[idx]
                else:
                    idxx = idx[x[idx] <= xints]
                    inside[idxx] = ~inside[idxx]

            p1x, p1y = p2x, p2y
        return inside

    def check_inside(self, x, y):
        """
        Checks if a set of points are inside the patch (closed as polygon).

        Parameters
        ----------
        x0 : list
            The X coordinates of the points to check.
        y0 : list
            The Y coordinates of the points to check.

        Returns
        -------
        numpy array
            0=No, 1=Yes (inside).

        References
        ----------
        https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python

        """
        return [self.check_inside_one_point(xi, yi) for xi, yi in zip(x, y)]

    def check_inside_one_point(self, x0, y0):
        """
        Checks if a single point is inside the patch (closed as polygon).

        Parameters
        ----------
        x0 : float
            The X coordinate pf the point to check.
        y0 : float
            The Y coordinate pf the point to check.

        Returns
        -------
        boolean

        References
        ----------
        https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python

        """
        # see https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
        poly = self.get_polygon()
        x = x0
        y = y0
        n = len(poly)
        inside = False
        p2x = 0.0
        p2y = 0.0
        xints = 0.0
        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def check_outside(self, x0, y0):
        """
        Checks if a set of points are outside the patch (closed as polygon).

        Parameters
        ----------
        x0 : list
            The X coordinates of the points to check.
        y0 : list
            The Y coordinates of the points to check.

        Returns
        -------
        numpy array
            0=No, 1=Yes (outside).

        References
        ----------
        https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python

        """
        inside = self.check_inside(x0, y0)
        if isinstance(inside, list):
            out = []
            for item in inside:
                out.append(not(item))
        else:
            out = not(inside)

        return out


class MultiplePatch(BoundaryShape):
    """
    Constructor.

    Parameters
    ----------
    patch_list : list
        A list of patches (each one can be a Circle, Rectangle, Polygon, etc.)

    """
    def __init__(self, patch_list=None):
        super().__init__()

        if patch_list is None:
            self._patch_list = []
        else:
            self._patch_list = patch_list
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("patch_list",  "Multiple Patch", ""),
            ])


    # overwrites the SynedObject method for dealing with list
    def to_dictionary(self):
        """
        Gets the dictionary with the multiple patch parameters.

        Returns
        -------
        dict

        """
        dict_to_save = OrderedDict()
        dict_to_save.update({"CLASS_NAME":self.__class__.__name__})

        dict_to_save["patch_list"] = [el.to_dictionary() for el in self._patch_list]

        return dict_to_save


    def reset(self):
        """
        Removes all existing patches.
        """
        self._patch_list = []

    def get_number_of_patches(self):
        """
        Returns the number of stored patches.

        Returns
        -------
        int

        """
        return len(self._patch_list)

    def get_boundaries(self):
        """
        Returns a list with the concatenated boundaries of the sotred patches.

        Returns
        -------
        list

        """
        boundaries_list = []
        for i in range(self.get_number_of_patches()):
            boundaries_list.extend(list(self._patch_list[i].get_boundaries()))
        return tuple(boundaries_list)

    def append_patch(self,patch=BoundaryShape()):
        """
        Append a patch.

        Parameters
        ----------
        patch : instance of Rectangle, Circle, etc.

        """
        self._patch_list.append(patch)

    def append_rectangle(self,x_left=-0.010,x_right=0.010,y_bottom=-0.020,y_top=0.020):
        """
        Appends a rectangle.

        Parameters
        ----------
        x_left : float, optional
            The coordinate (signed) of the minimum (left) along the X axis.
        x_right : float, optional
            The coordinate (signed) of the maximum (right) along the X axis.
        y_bottom : float, optional
            The coordinate (signed) of the minimum (left) along the Y axis.
        y_top : float, optional
            The coordinate (signed) of the maximum (right) along the Y axis.


        """
        self.append_patch(Rectangle(x_left=x_left, x_right=x_right, y_bottom=y_bottom, y_top=y_top))

    def append_circle(self,radius, x_center=0.0, y_center=0.0):
        """
        Appends a circle.

        Parameters
        ----------
        radius : float
            The radius of the circle.
        x_center : float
            The x coordinate of the center of the circle.
        y_center   : float
            The y coordinate of the center of the circle.

        """
        self.append_patch(Circle(radius, x_center=x_center, y_center=y_center))

    def append_ellipse(self,a_axis_min, a_axis_max, b_axis_min, b_axis_max):
        """
        Appends an ellipse.

        Parameters
        ----------
        a_axis_min : float, optional
            The coordinate (signed) of the minimum (left) along the major axis.
        a_axis_max : float, optional
            The coordinate (signed) of the maximum (right) along the major axis.
        b_axis_min : float, optional
            TThe coordinate (signed) of the minimum (left) along the minor axis.
        b_axis_max : float, optional
            The coordinate (signed) of the maximum (right) along the minor axis.

        """
        self.append_patch(Ellipse(a_axis_min, a_axis_max, b_axis_min, b_axis_max))

    def append_polygon(self,x, y):
        """
        Appends a polygon.

        Parameters
        ----------
        x : list
            The polygon X coordinates.
        y : list
            The polygon Y coordinates.

        Returns
        -------

        """
        self.append_patch(Polygon(x, y))

    def get_patches(self):
        """
        Returns a list with the patches.

        Returns
        -------
        list

        """
        return self._patch_list

    def get_patch(self, index):
        """
        Returns the patch corresponding to a given index.

        Parameters
        ----------
        index : int
            The index of the wanted patch.

        Returns
        -------
        instance of BoundaryShape (Circle, Rectangle, etc.).

        """
        return self.get_patches()[index]

    def get_name_of_patch(self,index):
        """
        Returns the name of the patch with a given index.

        Parameters
        ----------
        index : int
            The index of the wanted patch.

        Returns
        -------
        str

        """
        return self._patch_list[index].__class__.__name__

class DoubleRectangle(MultiplePatch):
    """
    Constructor.

    Parameters
    ----------
    x_left1 : float, optional
        The coordinate (signed) of the minimum (left) along the X axis of rectangle 1.
    x_right1 : float, optional
        The coordinate (signed) of the maximum (right) along the X axis of rectangle 1.
    y_bottom1 : float, optional
        The coordinate (signed) of the minimum (left) along the Y axis of rectangle 1.
    y_top1 : float, optional
        The coordinate (signed) of the maximum (right) along the Y axis  of rectangle 1.
    x_left2 : float, optional
        The coordinate (signed) of the minimum (left) along the X axis of rectangle 2.
    x_right2 : float, optional
        The coordinate (signed) of the maximum (right) along the X axis of rectangle 2.
    y_bottom2 : float, optional
        The coordinate (signed) of the minimum (left) along the Y axis of rectangle 2.
    y_top2 : float, optional
        The coordinate (signed) of the maximum (right) along the Y axis  of rectangle 2.
    """
    def __init__(self, x_left1=-0.010, x_right1=0.0, y_bottom1=-0.020, y_top1=0.0,
                        x_left2=-0.010, x_right2=0.010, y_bottom2=-0.001, y_top2=0.020):
        super().__init__()
        self.reset()
        self.append_patch(Rectangle(x_left=x_left1, x_right=x_right1, y_bottom=y_bottom1, y_top=y_top1))
        self.append_patch(Rectangle(x_left=x_left2, x_right=x_right2, y_bottom=y_bottom2, y_top=y_top2))

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("x_left1"          , "x (width) minimum (signed)   ", "m" ),
                    ("x_right1"         , "x (width) maximum (signed)   ", "m" ),
                    ("y_bottom1"        , "y (length) minimum (signed)  ", "m" ),
                    ("y_top1"           , "y (length) maximum (signed)  ", "m" ),
                    ("x_left2"          , "x (width) minimum (signed)   ", "m" ),
                    ("x_right2"         , "x (width) maximum (signed)   ", "m" ),
                    ("y_bottom2"        , "y (length) minimum (signed)  ", "m" ),
                    ("y_top2"           , "y (length) maximum (signed)  ", "m" ),
            ] )

    def set_boundaries(self,x_left1=-0.010, x_right1=0.0, y_bottom1=-0.020, y_top1=0.0,
                        x_left2=-0.010, x_right2=0.010, y_bottom2=-0.001, y_top2=0.020):
        self._patch_list[0].set_boundaries(x_left1, x_right1, y_bottom1, y_top1)
        self._patch_list[1].set_boundaries(x_left2, x_right2, y_bottom2, y_top2)

class DoubleEllipse(MultiplePatch):
    """
    Constructor.

    Parameters
    ----------
    a_axis_min1 : float, optional
        The coordinate (signed) of the minimum (left) along the major axis of ellipse 1.
    a_axis_max1 : float, optional
        The coordinate (signed) of the maximum (right) along the major axis of ellipse 1.
    b_axis_min1 : float, optional
        The coordinate (signed) of the minimum (left) along the minor axis of ellipse 1.
    b_axis_max1 : float, optional
        The coordinate (signed) of the maximum (right) along the minor axis of ellipse 1.
    a_axis_min2 : float, optional
        The coordinate (signed) of the minimum (left) along the major axis of ellipse 2.
    a_axis_max2 : float, optional
        The coordinate (signed) of the maximum (right) along the major axis of ellipse 2.
    b_axis_min2 : float, optional
        The coordinate (signed) of the minimum (left) along the minor axis of ellipse 2.
    b_axis_max2 : float, optional
        The coordinate (signed) of the maximum (right) along the minor axis of ellipse 2.

    """
    def __init__(self, a_axis_min1=-0.010, a_axis_max1=0.0,   b_axis_min1=-0.020, b_axis_max1=0.0,
                       a_axis_min2=-0.010, a_axis_max2=0.010, b_axis_min2=-0.001, b_axis_max2=0.020):

        super().__init__()
        self.reset()
        self.append_patch(Ellipse(a_axis_min1, a_axis_max1, b_axis_min1, b_axis_max1))
        self.append_patch(Ellipse(a_axis_min2, a_axis_max2, b_axis_min2, b_axis_max2))
        self._set_support_text([
                    ("a_axis_min1"         , "x (width) axis starts (signed)  ", "m" ),
                    ("a_axis_max1"         , "x (width) axis ends (signed)    ", "m" ),
                    ("b_axis_min1"         , "y (length) axis starts (signed) ", "m" ),
                    ("b_axis_max1"         , "y (length) axis ends (signed)   ", "m" ),
                    ("a_axis_min2"         , "x (width) axis starts (signed)  ", "m" ),
                    ("a_axis_max2"         , "x (width) axis ends (signed)    ", "m" ),
                    ("b_axis_min2"         , "y (length) axis starts (signed) ", "m" ),
                    ("b_axis_max2"         , "y (length) axis ends (signed)   ", "m" ),
            ] )
    def set_boundaries(self,a_axis_min1=-0.010, a_axis_max1=0.0,   b_axis_min1=-0.020, b_axis_max1=0.0,
                            a_axis_min2=-0.010, a_axis_max2=0.010, b_axis_min2=-0.001, b_axis_max2=0.020):
        """
        Sets the coordinates of the ellipses.

        Parameters
        ----------
        a_axis_min1 : float, optional
            The coordinate (signed) of the minimum (left) along the major axis of ellipse 1.
        a_axis_max1 : float, optional
            The coordinate (signed) of the maximum (right) along the major axis of ellipse 1.
        b_axis_min1 : float, optional
            The coordinate (signed) of the minimum (left) along the minor axis of ellipse 1.
        b_axis_max1 : float, optional
            The coordinate (signed) of the maximum (right) along the minor axis of ellipse 1.
        a_axis_min2 : float, optional
            The coordinate (signed) of the minimum (left) along the major axis of ellipse 2.
        a_axis_max2 : float, optional
            The coordinate (signed) of the maximum (right) along the major axis of ellipse 2.
        b_axis_min2 : float, optional
            The coordinate (signed) of the minimum (left) along the minor axis of ellipse 2.
        b_axis_max2 : float, optional
            The coordinate (signed) of the maximum (right) along the minor axis of ellipse 2.

        """
        self._patch_list[0].set_boundaries(a_axis_min1,a_axis_max1,b_axis_min1,b_axis_max1)
        self._patch_list[1].set_boundaries(a_axis_min2,a_axis_max2,b_axis_min2,b_axis_max2)

class DoubleCircle(MultiplePatch):
    """
    Constructor.

    Parameters
    ----------
    radius1 : float
        The radius of the circle 1.
    x_center1 : float
        The x coordinate of the center of the circle 1.
    y_center1   : float
        The y coordinate of the center of the circle 1.
    radius2 : float
        The radius of the circle 2.
    x_center2 : float
        The x coordinate of the center of the circle 2.
    y_center2   : float
        The y coordinate of the center of the circle 2.

    """
    def __init__(self, radius1=50e-6,x_center1=0.0,y_center1=0.0,
                       radius2=50e-6,x_center2=100e-6,y_center2=100e-6):
        super().__init__()
        self.reset()
        self.append_patch(Circle(radius1,x_center1,y_center1))
        self.append_patch(Circle(radius2,x_center2,y_center2))
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("radius1"              , "radius  ", "m" ),
                    ("x_center1"            , "x center (signed)    ", "m" ),
                    ("y_center1"            , "y center (signed)    ", "m" ),
                    ("radius2"              , "radius  ", "m" ),
                    ("x_center2"            , "x center (signed)    ", "m" ),
                    ("y_center2"            , "y center (signed)    ", "m" ),
            ] )
    def set_boundaries(self,radius1=50e-6,x_center1=0.0,y_center1=0.0,
                            radius2=50e-6,x_center2=100e-6,y_center2=100e-6):
        """
        Sets the coordinates of the circles.

        Parameters
        ----------
        radius1 : float
            The radius of the circle 1.
        x_center1 : float
            The x coordinate of the center of the circle 1.
        y_center1   : float
            The y coordinate of the center of the circle 1.
        radius2 : float
            The radius of the circle 2.
        x_center2 : float
            The x coordinate of the center of the circle 2.
        y_center2   : float
            The y coordinate of the center of the circle 2.

        """
        self._patch_list[0].set_boundaries(radius1,x_center1,y_center1)
        self._patch_list[1].set_boundaries(radius2,x_center2,y_center2)



if __name__=="__main__":



    p = 20
    q = 10
    theta_graz = 0.003

    #
    # sphere
    #
    # sph = Sphere()
    sph = Sphere.create_sphere_from_p_q(10, 10, 0.021)
    print(sph.info())

    #
    # Ellipsoid
    #
    ell = Ellipsoid()
    ell.initialize_from_p_q(p, q, theta_graz)


    #
    # toroid
    #
    par = Toroid.create_toroid_from_p_q(p=p, q=q, grazing_angle=theta_graz)
    print("inputs  p, q, theta_graz: ", p, q, theta_graz)
    radii = par.get_radii()
    print("toroid radii: ", radii )
    R =  2 / numpy.sin(theta_graz) * p * q / (p + q)
    r =  2 * numpy.sin(theta_graz) * p * q / (p + q)
    assert ((radii[0] - R) < 1e-10 )
    assert ((radii[0] - r) < 1e-10 )
    print(par.info())

    #
    # paraboloid
    #
    at_infinity = Side.SOURCE

    par = Paraboloid.create_paraboloid_from_p_q(p=p, q=q, grazing_angle=theta_graz, at_infinity=at_infinity, convexity=Convexity.UPWARD)
    print("inputs  p, q, theta_graz: ", p, q, theta_graz, at_infinity)
    print ("parabola p or q: ",par.get_pole_to_focus())
    print("parabola par: ", par.get_parabola_parameter())
    print("parabola grazing_angle: ", par.get_grazing_angle())
    if par.get_at_infinity() == Side.SOURCE:
        assert (numpy.abs(q - par.get_pole_to_focus()) < 1e-10 )
    else:
        assert (numpy.abs(p - par.get_pole_to_focus()) < 1e-10)
    assert (numpy.abs(theta_graz - par.get_grazing_angle()) < 1e-10)
    print(par.info())

    #
    # parabolic cylinder: TODO: check that the info is not good for double inheritage
    #
    a = Cylinder()
    print(a.info())
    print(a.to_dictionary())

    parC = ParabolicCylinder(par, a)
    print(parC.info())



    #
    # some other checks...
    #

    # conic coeffs.
    ccc = Conic()
    print(ccc.get_conic_coefficients())
    print(ccc.info())
    ccc.to_json("tmp.json")
    from syned.util.json_tools import load_from_json_file
    tmp = load_from_json_file("tmp.json")
    print("returned class: ",type(tmp))
    print(ccc.to_dictionary())
    print(tmp.to_dictionary())
    # from deepdiff import DeepDiff # use this because  == gives an error
    # assert (len(DeepDiff(ccc.to_dictionary(), tmp.to_dictionary())) == 0)




    # circle
    circle = Circle(3.0)
    print(circle.get_radius(),circle.get_center())
    print(circle.get_boundaries())



    # patches
    patches = MultiplePatch()

    patches.append_rectangle(-0.02,-0.01,-0.001,0.001)
    patches.append_rectangle(0.01,0.02,-0.001,0.001)
    patches.append_polygon([-0.02,-0.02,0.02,0.02], [-0.02,0.02,0.02,-0.02])

    print(patches.get_number_of_patches(),patches.get_boundaries())
    for patch in patches.get_patches():
        print(patch.info())
    print("Patch 0 is: ",patches.get_name_of_patch(0))
    print("Patch 1 is: ",patches.get_name_of_patch(1))
    print(patches.get_boundaries())


    # double rectangle
    double_rectangle = DoubleRectangle()
    double_rectangle.set_boundaries(-0.02,-0.01,-0.001,0.001,0.01,0.02,-0.001,0.001)
    print("Rectangle 0 is: ",double_rectangle.get_name_of_patch(0))
    print("Rectangle 1 is: ",double_rectangle.get_name_of_patch(1))
    print(double_rectangle.get_boundaries())

    # polygon
    angle = numpy.linspace(0, 2 * numpy.pi, 5)
    x = numpy.sin(angle) + 0.5
    y = numpy.cos(angle) + 0.5
    poly = Polygon(x=x, y=y)
    print(poly.info())
    print("vertices: ", poly.get_number_of_vertices())
    if False:
        from srxraylib.plot.gol import plot,set_qt
        set_qt()
        plot(x,y)
    print(poly.get_polygon())
    print("inside? : ", poly.check_inside([0.5,0],[0.5,5]))
    print("outside? : ", poly.check_outside([0.5, 0], [0.5, 5]))


    # multiple patches
    patches = MultiplePatch()
    patches.append_polygon(numpy.array([-1,-1,1,1]),numpy.array([-1,1,1,-1]))
    x = [-0.00166557,  0.12180897, -0.11252591, -0.12274196,  0.00586896, -0.12999401, -0.12552975, -0.0377907,  -0.01094828, -0.13689862]
    y = [ 0.16279557, -0.00085991,  0.01349174, -0.01371226,  0.01480265, -0.04810334, 0.07198068, -0.03725407,  0.13301309, -0.00296213]
    x = numpy.array(x)
    y = numpy.array(y)
    patch = patches.get_patch(0)
    # print(patch.check_inside(x,y))
    for i in range(x.size):
        tmp = patch.check_inside_one_point(x[i], y[i])
        print(x[i], y[i], tmp )
    print("inside? : ", patch.check_inside(x, y), type(patch.check_inside(x, y)))
    print("inside? : ", patch.check_inside_vector(x, y), type(patch.check_inside_vector(x, y)))
