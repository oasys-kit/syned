from syned.beamline.shape import BoundaryShape
from syned.beamline.optical_elements.absorbers.absorber import Absorber

class Slit(Absorber):
    def __init__(self, name="Undefined", boundary_shape=None):
        if boundary_shape is None:
            boundary_shape = BoundaryShape()
        Absorber.__init__(self, name=name, boundary_shape=boundary_shape)
