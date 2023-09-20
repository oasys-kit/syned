"""
Base class for LighSource, which contains:
    - a name
    - an electron beam
    - a magnetic structure

"""
from syned.syned_object import SynedObject


class EmptyLightSource(SynedObject):
    """
    Defines an empty light source. This is for creating "movable" beamlines (using Beamline()). These are beamlines
    that do not have a particular light source.

    Parameters
    ----------
    name : str, optional
        The name of the (empty) light source.

    """
    def __init__(self, name="Empty"):
        self._name               = name
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",              "Name",""),
            ] )


    def get_name(self):
        """
        Returns the name of the light source.

        Returns
        -------
        str

        """
        return self._name

