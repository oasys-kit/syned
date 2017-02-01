"""
Represents an ideal lens.
"""
from syned.beamline.optical_element import OpticalElement

class Screen(OpticalElement):
    def __init__(self, name="Undefined"):
        OpticalElement.__init__(self, name=name)