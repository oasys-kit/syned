"""

Represents an ideal lens.

"""
from syned.beamline.optical_element import OpticalElement


class IdealLens(OpticalElement):
    def __init__(self, name="Undefined", focal_y=1.0, focal_x=None, ):
        OpticalElement.__init__(self, name=name)
        self._focal_y = focal_y
        self._focal_x = focal_x
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("focal_y"      , "Focal length in y [vertical]",    "m" ),
                    ("focal_x"      , "Focal length in x [horizontal]", "m" ),
            ] )

    def focal_x(self):
        return self._focal_x

    def focal_y(self):
        return self._focal_y
