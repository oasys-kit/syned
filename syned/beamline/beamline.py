"""
Represents a beamline. The beamline is composed by a light source ans a list of beamline elements.
"""

from syned.syned_object import SynedObject
from syned.storage_ring.light_source import LightSource
from syned.storage_ring.empty_light_source import EmptyLightSource
from syned.beamline.beamline_element import BeamlineElement

from collections import OrderedDict

class Beamline(SynedObject):
    """
    Constructor.

    Parameters
    ----------
    light_source : instance of LightSource
        The light source
    beamline_elements_list : list
        The beamline elements (each one an instance of BeamlineElement).
    """
    def __init__(self, light_source=LightSource(), beamline_elements_list=None):
        self._light_source = light_source
        if beamline_elements_list is None:
            self._beamline_elements_list = []
        else:
            self._beamline_elements_list = beamline_elements_list

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("light_source",       "Light Source",      ""),
                    ("beamline_elements_list",  "Beamline Elements", ""),
            ] )


    # overwrites the SynedObject method for dealing with list
    def to_dictionary(self):
        """
        Returns a dictionary with the object fields.

        Returns
        -------
        dict
            A dictionary with the data.

        """
        dict_to_save = OrderedDict()
        dict_to_save.update({"CLASS_NAME":self.__class__.__name__})

        dict_to_save["light_source"] = self._light_source.to_dictionary()
        dict_to_save["beamline_elements_list"] = [el.to_dictionary() for el in self._beamline_elements_list]

        return dict_to_save



    def get_light_source(self):
        """
        Returns the light source

        Returns
        -------
        instance of LightSource

        """
        return self._light_source

    def get_beamline_elements(self):
        """
        returns the beamline elements.

        Returns
        -------
        list

        """
        return self._beamline_elements_list

    def set_light_source(self, light_source=LightSource()):
        """
        Sets a light source.

        Parameters
        ----------
        light_source : instance of LightSource

        """
        if not (isinstance(light_source,LightSource) or isinstance(light_source,EmptyLightSource)):
            raise Exception("Input class must be of type: "+LightSource.__name__+" or "+EmptyLightSource.__name__)
        else:
            self._light_source = light_source

    def append_beamline_element(self, beamline_element=BeamlineElement()):
        """
        Appends a beamline element.

        Parameters
        ----------
        beamline_element : instance of BeamlineElement.

        """
        if not isinstance(beamline_element,BeamlineElement):
            raise Exception("Input class must be of type: "+BeamlineElement.__name__)
        else:
            self._beamline_elements_list.append(beamline_element)

    def get_beamline_elements_number(self):
        """
        Gets the number of beamline elements stored.

        Returns
        -------
        int

        """
        return len(self._beamline_elements_list)

    def get_beamline_element_at(self, index):
        """
        gets an individual beamline element.

        Parameters
        ----------
        index : int
            The index of the beamline element to be retrieved.

        Returns
        -------
        instance of BeamlineElement
            The wanted beamline element (referenced, not copied).

        """
        if index >= len(self._beamline_elements_list):
            raise IndexError("Index " + str(index) + " out of bounds")

        return self._beamline_elements_list[index]

    # TODO: remove: probably this is not needed, as the deepcopy in SynedObject makes the work.
    def duplicate(self):
        """
        Returns a copy of the beamline element instance.

        Returns
        -------
        BeamlineElement  instance
            A copy of the object instance.

        """
        beamline_elements_list = []
        for beamline_element in self._beamline_elements_list:
            beamline_elements_list.append(beamline_element)

        return Beamline(light_source=self._light_source,
                        beamline_elements_list = beamline_elements_list)
