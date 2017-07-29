"""
Represents an ideal lens.
"""
from syned.beamline.optical_elements.ideal_elements.ideal_element import IdealElement

class Screen(IdealElement):
    def __init__(self, name="Undefined"):
        IdealElement.__init__(self, name=name)