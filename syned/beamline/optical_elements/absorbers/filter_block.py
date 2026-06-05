#
# FilterBlock contains a list of Filters
#
from syned.syned_object import SynedObject
from collections import OrderedDict

class FilterBlock(SynedObject):
    """A single attenuator block (axis): an ordered list of Filter (or FilterWithDensity) foils.

    All foils in a block are physically stacked and inserted together as one unit.
    """

    def __init__(self, filters_list=None, selection=None):
        """
        Parameters
        ----------
        filters_list : list of FilterWithDensity, optional
            Ordered list of foils that make up this block. Defaults to empty list.
        selection : int or None, optional
            Index of the active foil. None means no foil selected.
        """
        if filters_list is None:
            self._filters_list = []
        else:
            self._filters_list = filters_list

        self._selection = selection
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("filters_list",  "Filters list", ""),
                    ("selection",     "selected foil index", ""),
            ] )


    # # overwrites the SynedObject method for dealing with list
    def to_dictionary(self):
        """Return an ordered dictionary representation of this block.

        Returns
        -------
        dict
            Keys: CLASS_NAME, filters_list (list of filter dictionaries), selection.
        """
        dict_to_save = OrderedDict()
        dict_to_save.update({"CLASS_NAME":self.__class__.__name__})
        dict_to_save["filters_list"] = [el.to_dictionary() for el in self._filters_list]
        dict_to_save["selection"] = self._selection
        return dict_to_save

    def get_n(self):
        """Return the number of foils in this block.

        Returns
        -------
        int
        """
        return len(self._filters_list)

    def set_n(self, n):
        """Reduces the number of foils in this block (n must be <= self.get_n()).

        """
        if n <= self.get_n():
            tmp = [self._filters_list[i] for i in range(n) ]
            self._filters_list = tmp

    def get_selection(self):
        """Return the index of the active foil, or None if no foil is selected."""
        return self._selection

    def set_selection(self, selection):
        """Set the index of the active foil. Use None for no selection."""
        self._selection = selection

    def duplicate_using_selected_only(self):
        """Return a new FilterBlock containing only the currently selected foil."""
        return FilterBlock(filters_list=[self.get_selected_item()], selection=0)

    def get_item(self, index):
        """Return the foil at the given index.

        Parameters
        ----------
        index : int

        Returns
        -------
        FilterWithDensity
        """
        return self._filters_list[index]

    def get_selected_item(self):
        """Return the foil at the index defined in selection.

        Returns
        -------
        Filter instance

        Raises
        ------
        ValueError
            If selection is None.
        """
        if self._selection is None:
            raise ValueError("no foil selected (selection is None)")
        return self._filters_list[self._selection]

    def get_lists_materials_thicknesses_densities(self, cumulate=False, use_selected_only=0):
        """Return the materials, thicknesses and densities of all foils in this block.

        Parameters
        ----------
        cumulate : bool, optional
            If True, foils sharing the same material and density are merged by
            summing their thicknesses, regardless of their position in the list.
            Order of first appearance is preserved. Default is False.

        use_selected_only : bool, optional
            If False, consider all the foils. If True, use only the selected foil.

        Returns
        -------
        materials : list of str
        thicknesses : list of float
            Foil thicknesses in mm.
        densities : list of float
            Foil densities in g/cm³.
        """
        if use_selected_only:
            item = self.get_selected_item()
            materials   = [item.get_material()]
            thicknesses = [item.get_thickness()]
            try:
                densities = [item.get_density()]
            except Exception:
                densities = ['?']
            return materials, thicknesses, densities

        else:
            materials   = [f.get_material()  for f in self._filters_list]
            thicknesses = [f.get_thickness() for f in self._filters_list]
            try:
                densities   = [f.get_density()   for f in self._filters_list]
            except Exception:
                densities = ['?'] * len(materials)
            if cumulate:
                seen = {}  # (material, density) -> index in output lists
                cum_mat, cum_thick, cum_dens = [], [], []
                for mat, thick, dens in zip(materials, thicknesses, densities):
                    key = (mat, dens)
                    if key in seen:
                        cum_thick[seen[key]] += thick
                    else:
                        seen[key] = len(cum_mat)
                        cum_mat.append(mat)
                        cum_thick.append(thick)
                        cum_dens.append(dens)
                return cum_mat, cum_thick, cum_dens
            return materials, thicknesses, densities


if __name__ == "__main__":
    if 0:
        from syned.beamline.optical_elements.absorbers.filter import Filter
        f1 = Filter(name='f1', material='Si',)
        f2 = Filter(name='f2', material='W', )
        f3 = Filter(name='f3', material='K', )
        f4 = Filter(name='f4', material='K',)
        f5 = Filter(name='f5', material='Ag',)

        bf = FilterBlock(filters_list=[f1,f2,f3,f4], selection=1)

        print(bf.info())
        print(bf.to_dictionary())
        m, t, d = bf.get_lists_materials_thicknesses_densities(cumulate=1)
        for i in range(len(m)):
            print(i, m[i], t[i], d[i])

        print("selected: ", bf.get_selection(), bf.get_selected_item())
        print("selected m, t, d: ", bf.get_lists_materials_thicknesses_densities(cumulate=1, use_selected_only=1))

        bf_selected = bf.duplicate_using_selected_only()

        print(bf_selected.info())


