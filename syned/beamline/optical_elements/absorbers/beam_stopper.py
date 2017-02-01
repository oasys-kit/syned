
from syned.beamline.optical_element import OpticalElement
from syned.beamline.shape import BoundaryShape
from syned.beamline.shape import Rectangle, Ellipse

class BeamStopper(OpticalElement):
    def __init__(self, name="Undefined", boundary_shape=BoundaryShape()):
        OpticalElement.__init__(self, name=name, boundary_shape=boundary_shape)

    def set_rectangle(self,width=3e-3,height=4e-3):
        self._boundary_shape=Rectangle(-0.5*width,0.5*width,-0.5*height,0.5*height)

    def set_circle(self,radius=3e-3):
        self._boundary_shape=Ellipse(-0.5*radius,0.5*radius,-0.5*radius,0.5*radius)