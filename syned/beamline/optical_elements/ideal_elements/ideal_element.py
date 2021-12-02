from syned.beamline.optical_element import OpticalElement

class IdealElement(OpticalElement):
    def __init__(self, name="Undefined", boundary_shape=None):
        OpticalElement.__init__(self, name=name, boundary_shape=boundary_shape)