
from syned.beamline.optical_element import OpticalElement
from syned.beamline.optical_elements.shape import BoundaryShape


class Slit(OpticalElement):
    def __init__(self, name="Undefined", boundary_shape=BoundaryShape()):
        OpticalElement.__init__(self, name=name, boundary_shape=boundary_shape)

class BeamStopper(OpticalElement):
    def __init__(self, name="Undefined", boundary_shape=BoundaryShape()):
        OpticalElement.__init__(self, name=name, boundary_shape=boundary_shape)

class Filter(OpticalElement):
    def __init__(self,
                 name="Undefined",
                 material="Be",
                 thickness=1e-3):
        OpticalElement.__init__(self, name=name)
        self._material = material
        self._thickness = thickness

    def get_material(self):
        return self._material

    def get_thickness(self):
        return self._thickness
