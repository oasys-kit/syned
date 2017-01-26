
from syned.beamline.optical_element import OpticalElement
from syned.beamline.optical_elements.shape import Shape


class Slit(OpticalElement):
    def __init__(self, name="Undefined", shape=Shape()):
        OpticalElement.__init__(self, name=name)
        self._shape = shape

    def get_shape(self):
        return self._shape


class BeamStopper(OpticalElement):
    def __init__(self, name="Undefined", shape=Shape()):
        OpticalElement.__init__(self, name=name)
        self._shape = shape

    def get_shape(self):
        return self._shape


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
