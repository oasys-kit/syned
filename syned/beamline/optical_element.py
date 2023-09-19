"""
Base class for an optical element.
"""
from syned.syned_object import SynedObject

class OpticalElement(SynedObject):
    """
    Constructor.

    Parameters
    ----------
    name : str
        The element name.
    boundary_shape : instance of BoundaryShape, optional
        The element shape. The default=None means no shape associated to the optical element.
    """
    def __init__(self, name="Undefined", boundary_shape=None):
        self._name = name
        self._boundary_shape = boundary_shape

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name", "Name", ""),
                    ("boundary_shape"      , "", "" ),
            ] )

    def get_name(self):
        """
        returns the optical element name.

        Returns
        -------
        str

        """
        return self._name

    def get_boundary_shape(self):
        """
        Returns the boundary shape.

        Returns
        -------
        None or instance of BoundaryShape

        """
        return self._boundary_shape
