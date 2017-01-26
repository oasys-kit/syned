
from syned.beamline.optical_element import OpticalElement
from syned.beamline.optical_elements.shape import BoundaryShape

class BeamStopper(OpticalElement):
    def __init__(self, name="Undefined", boundary_shape=BoundaryShape()):
        OpticalElement.__init__(self, name=name, boundary_shape=boundary_shape)