"""
Represents a beamline.

BeamlineComponents can be attached at positions(BeamlinePosition), i.e. longitudinal, off-axis and inclined.
We can iterate of the components, find their positions or look for a specific component.
"""

from syned.syned_object import SynedObject
from syned.storage_ring.light_source import LightSource
from syned.beamline.beamline_element import BeamlineElement

from collections import OrderedDict

class Beamline(SynedObject):
    def __init__(self, light_source=LightSource(), beamline_elements_list=[]):
        self._light_source = light_source
        self._beamline_elements_list = beamline_elements_list

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("light_source",       "Light Source",      ""),
                    ("beamline_elements",  "Beamline Elements", ""),
            ] )


    # overwrites the SynedObject method for dealing with list
    def to_dictionary(self):
        dict_to_save = OrderedDict()
        dict_to_save.update({"CLASS_NAME":self.__class__.__name__})

        dict_to_save["light_source"] = self._light_source.to_dictionary()
        dict_to_save["beamline_elements"] = [el.to_dictionary() for el in self._beamline_elements_list]

        return dict_to_save



    def get_light_source(self):
        return self._light_source

    def get_beamline_elements(self):
        return self._beamline_elements_list

    def set_light_source(self, light_source=LightSource()):
        if not isinstance(light_source,LightSource):
            raise Exception("Input class must be of type: "+LightSource.__name__)
        else:
            self._light_source = light_source

    def append_beamline_element(self, beamline_element=BeamlineElement()):
        if not isinstance(beamline_element,BeamlineElement):
            raise Exception("Input class must be of type: "+BeamlineElement.__name__)
        else:
            self._beamline_elements_list.append(beamline_element)

    def get_beamline_elements_number(self):
        return len(self._beamline_elements_list)

    def get_beamline_element_at(self, index):
        if index >= len(self._beamline_elements_list):
            raise IndexError("Index " + str(index) + " out of bounds")

        return self._beamline_elements_list[index]

    def duplicate(self):
        beamline_elements_list = []
        for beamline_element in self._beamline_elements_list:
            beamline_elements_list.append(beamline_element)

        return Beamline(light_source=self._light_source,
                        beamline_elements_list = beamline_elements_list)
