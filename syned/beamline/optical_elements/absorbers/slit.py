
from syned.beamline.shape import BoundaryShape
from syned.beamline.shape import Rectangle, Ellipse, Circle

from syned.beamline.optical_elements.absorbers.absorber import Absorber

class Slit(Absorber):
    """
    Slit or aperture.

    Constructor.

    Note that:
                                   Slit     BeamStopper    Filter      HoledFilter
        beam pass at center         Yes     No             Yes         No
        apply attenuation           No      No             Yes         Yes

    Parameters
    ----------
    name : str
        The name of the optical element.
    boundary_shape : instance of BoundaryShape, optional
        The geometry of the slit aperture. if None, it is initialized to BoundaryShape().

    """
    def __init__(self, name="Undefined", boundary_shape=None):
        if boundary_shape is None:
            boundary_shape = BoundaryShape()
        Absorber.__init__(self, name=name, boundary_shape=boundary_shape)

    def set_rectangle(self,width=3e-3,height=4e-3,center_x=0.0,center_y=0.0):
        """
        Sets the aperture as a rectangle.

        Parameters
        ----------
        width : float, optional
            The rectangle width.
        length : float, optional
            The rectangle length.
        center_x : float, optional
            The center coordinate X.
        center_y : float, optional
            The center coordinate Y.

        """
        self._boundary_shape=Rectangle(-0.5*width+center_x,0.5*width+center_x,-0.5*height+center_y,0.5*height+center_y)

    def set_circle(self,radius=3e-3,center_x=0.0,center_y=0.0):
        """
        Sets the aperture as a circle.

        Parameters
        ----------
        radius : float
            The radius of the circle.
        center_x : float
            The x coordinate of the center of the circle.
        center_y   : float
            The y coordinate of the center of the circle.

        """
        self._boundary_shape=Circle(radius,center_x,center_y)

    def set_ellipse(self,width=3e-3,height=4e-3,center_x=0.0,center_y=0.0):
        """
        Sets the aperture as an ellipse.

        Parameters
        ----------
        width : float, optional
            The ellipse width (2a).
        height : float, optional
            The ellipse height (2b).
        center_x : float, optional
            The ellipse center coordinate X.
        center_y : float, optional
            The ellipse center coordinate Y.

        """
        self._boundary_shape=Ellipse(-0.5*width+center_x,0.5*width+center_x,-0.5*height+center_y,0.5*height+center_y)