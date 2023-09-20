#
# this is a filter with a hole (holed-filter)
#                                  Slit     BeamStopper    Filter      HoledFilter
#       beam pass at center         Yes     No             Yes         No
#       apply attenuation           No      No             Yes         Yes
#
#
from syned.beamline.optical_elements.absorbers.absorber import Absorber

class HoledFilter(Absorber):
    """
    Filter or absorber or attenuator with a hole.

    Note that:
                                   Slit     BeamStopper    Filter      HoledFilter
        beam pass at center         Yes     No             Yes         No
        apply attenuation           No      No             Yes         Yes

    Constructor.

    Parameters
    ----------
    name : str
        The name of the optical element.
    material : str
        A string defining the material.
    thickness : float
        The filter thickness in m.
    boundary_shape : instance of BoundaryShape, optional
        Defines the geometry of the hole. if None, it is initialized to BoundaryShape().
    """
    def __init__(self,
                 name="Undefined",
                 material="Be",
                 thickness=1e-3,
                 boundary_shape=None):
        Absorber.__init__(self, name=name, boundary_shape=boundary_shape)
        self._material = material
        self._thickness = thickness


        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("material"      , "Material (symbol, formula or name)",    "" ),
                    ("thickness"     , "Thickness ",                            "m" ),
            ] )
    def get_material(self):
        """
        Returns the material name.

        Returns
        -------
        str

        """
        return self._material

    def get_thickness(self):
        """
        Retuirns the filter thickness in m.

        Returns
        -------
        float

        """
        return self._thickness
