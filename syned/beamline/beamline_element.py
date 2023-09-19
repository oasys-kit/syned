"""
Base class for all beamline elements. A beamline element is composed by an optical element (instance of OpticalElement)
and its position in th ebeamline (an instance of ElementCoordinates).
"""

from syned.syned_object import SynedObject
from syned.beamline.optical_element import OpticalElement
from syned.beamline.element_coordinates import ElementCoordinates

class BeamlineElement(SynedObject):
    """
    Constructor

    Parameters
    ----------
    optical_element : instance of OpticalElement
    coordinates : instance of ElementCoordinates
    """
    def __init__(self, optical_element=OpticalElement(), coordinates=ElementCoordinates()):
        self._optical_element = optical_element
        self._coordinates = coordinates
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("optical_element",       "Optical Element",      ""),
                    ("coordinates",           "Element coordinates",  ""),
            ] )

    def get_optical_element(self):
        """
        Returns the optical element.

        Returns
        -------
        instance of OpticalElement

        """
        return self._optical_element

    def get_coordinates(self):
        """
        Returns the element coordinates.

        Returns
        -------
        instance of ElementCoordinates

        """
        return self._coordinates

    def set_optical_element(self, value):
        """
        Sets the optical element.

        Parameters
        ----------
        value : instance of OpticalElement

        """
        if isinstance(value, OpticalElement):
            self._optical_element = value
        else:
            raise Exception("entry is not an instance of OpticalElement")

    def set_coordinates(self, value):
        """
        Sets the coordinates.

        Parameters
        ----------
        value : instance of ElementCoordinates.

        """
        if isinstance(value, ElementCoordinates):
            self._coordinates = value
        else:
            raise Exception("entry is not an instance of ElementCoordinates")
