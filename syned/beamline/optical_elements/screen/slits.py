from syned.beamline.optical_element import OpticalElement

class Slits(OpticalElement):
    def __init__(self, name):
        OpticalElement.__init__(self, name=name)