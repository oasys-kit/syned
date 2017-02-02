from syned.syned_object import SynedObject

class OpticalElement(SynedObject):
    def __init__(self, name="Undefined", boundary_shape=None):
        self._name = name
        self._boundary_shape = boundary_shape

        # TODO check name
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    # ("name"      ,           "to define ", "" ),
                    ("boundary_shape"      , "to define ", "" ),
            ] )

    def get_name(self):
        return self._name

    def get_boundary_shape(self):
        return self._boundary_shape
