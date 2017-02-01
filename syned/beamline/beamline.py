"""
Represents a beamline.

BeamlineComponents can be attached at positions(BeamlinePosition), i.e. longitudinal, off-axis and inclined.
We can iterate of the components, find their positions or look for a specific component.
"""

from syned.storage_ring.light_source import LightSource
from syned.beamline.beamline_element import BeamlineElement

class Beamline(object):
    def __init__(self, light_source=LightSource(), ):
        self._light_source = None
        self._beamline_elements = []

    def get_light_source(self):
        return self._light_source

    def get_beamline_elements(self):
        return self._beamline_elements

    def set_light_source(self, light_source=LightSource()):
        if not isinstance(light_source,LightSource):
            raise Exception("Input class must be of type: "+LightSource.__name__)
        else:
            self._light_source = light_source

    def append_beamline_element(self, beamline_element=BeamlineElement()):
        if not isinstance(beamline_element,BeamlineElement):
            raise Exception("Input class must be of type: "+BeamlineElement.__name__)
        else:
            self._beamline_elements.append(beamline_element)

    def get_beamline_elements_number(self):
        return len(self._beamline_elements)

    def get_beamline_element_at(self, index):
        if index >= len(self._beamline_elements):
            raise IndexError("Index " + str(index) + " out of bounds")

        return self._beamline_elements[index]