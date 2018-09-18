"""
Base class for LighSource, which contains:
    - a name
    - an electron beam
    - a magnetic structure

"""
from syned.syned_object import SynedObject


class EmptyLightSource(SynedObject):
    def __init__(self, name="Empty"):
        self._name               = name
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",              "Name",""),
            ] )


    def get_name(self):
        return self._name

