"""

Represents an ideal lens.

"""
from syned.beamline.optical_elements.ideal_elements.ideal_element import IdealElement


class IdealLens(IdealElement):
    def __init__(self, name="Undefined", focal_x=1.0, focal_y=1.0):
        IdealElement.__init__(self, name=name)
        self._focal_x = focal_x
        self._focal_y = focal_y
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("focal_x"      , "Focal length in x [horizontal]", "m" ),
                    ("focal_y"      , "Focal length in y [vertical]",    "m" ),
            ] )

    def focal_x(self):
        return self._focal_x

    def focal_y(self):
        return self._focal_y
