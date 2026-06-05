from syned.beamline.optical_elements.absorbers.filter import Filter

class FilterWithDensity(Filter):
    """Filter with an explicit material density (extends Filter).

    Useful when the material density cannot be looked up automatically or
    differs from the tabulated bulk value (e.g. compressed foils, alloys).
    """

    def __init__(self,
                 name="Undefined",
                 material="Be",
                 thickness=1e-3,
                 density=1.0,
                 boundary_shape=None):
        """
        Parameters
        ----------
        name : str, optional
            Name of the optical element.
        material : str, optional
            Material symbol, formula, or name.
        thickness : float, optional
            Filter thickness in m.
        density : float, optional
            Material density in g/cm³.
        boundary_shape : BoundaryShape, optional
            Aperture boundary. Defaults to BoundaryShape().
        """
        Filter.__init__(self, name=name, material=material, thickness=thickness, boundary_shape=boundary_shape)
        self._density = density

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._add_support_text([
                    ("density"      , "Density",    "g/cm3" ),
            ])

    def get_density(self):
        """Return the material density in g/cm³.

        Returns
        -------
        float
        """
        return self._density

