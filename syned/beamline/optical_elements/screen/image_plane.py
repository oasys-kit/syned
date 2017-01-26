__author__ = 'labx'

from syned.beamline.optical_elements import OpticalElement

class ImagePlane(OpticalElement):
    def __init__(self, name):
        OpticalElement.__init__(self, name=name)
