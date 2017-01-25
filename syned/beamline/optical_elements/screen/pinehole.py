from syned.beamline.optical_element import OpticalElement

class PineHole(OpticalElement):
    def __init__(self, name):
        OpticalElement.__init__(self, name=name)
