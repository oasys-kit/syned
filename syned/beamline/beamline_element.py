"""
Base class for all beamline components.
Enforce to name every every component.
Every beamline component can store settings
"""
from syned.beamline.optical_element import OpticalElement
from syned.beamline.element_coordinates import ElementCoordinates

class BeamlineElement(object):
    def __init__(self, optical_element=OpticalElement(), coordinates=ElementCoordinates()):
        self._optical_element = optical_element
        self._coordinates = coordinates

    def getOpticalElement(self):
        return self._optical_element

    def getCoordinates(self):
        return self._coordinates