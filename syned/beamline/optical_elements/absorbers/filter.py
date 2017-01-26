
from syned.beamline.optical_element import OpticalElement

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
