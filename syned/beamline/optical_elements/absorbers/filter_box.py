#
# FilterBox contains a list of FilterBlock (a FilterBlock contains a list of Filter)
#
from syned.syned_object import SynedObject
from syned.beamline.optical_elements.absorbers.filter_with_density import FilterWithDensity
from syned.beamline.optical_elements.absorbers.filter_block import FilterBlock

from collections import OrderedDict

class FilterBox(SynedObject):
    """A box of attenuator blocks (or axes): an ordered list of FilterBlock objects.

    Each block is an independent attenuator unit. The selection state records
    which filter position is active in each block.
    """

    def __init__(self, filter_blocks_list=None):
        """
        Parameters
        ----------
        filter_blocks_list : list of FilterBlock, optional
            Ordered list of attenuator blocks. Defaults to empty list.
        """
        if filter_blocks_list is None:
            self._filter_blocks_list = []
        else:
            self._filter_blocks_list = filter_blocks_list

        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("filter_blocks_list",  "list of blocks (axes) of filters", ""),
            ] )


    # overwrites the SynedObject method for dealing with list
    def to_dictionary(self):
        """Return an ordered dictionary representation of this box.

        Returns
        -------
        dict
            Keys: CLASS_NAME, filter_blocks_list (list of block dictionaries).
        """
        dict_to_save = OrderedDict()
        dict_to_save.update({"CLASS_NAME":self.__class__.__name__})
        dict_to_save["filter_blocks_list"] = [el.to_dictionary() for el in self._filter_blocks_list]
        return dict_to_save

    def get_n(self):
        """Return the number of blocks (axes) in this box.

        Returns
        -------
        int
        """
        return len(self._filter_blocks_list)

    def set_n(self, n):
        """Reduces the number of blocks (axes) in this box (n must be <= self.get_n()).

        """
        if n <= self.get_n():
            self._filter_blocks_list = self._filter_blocks_list[:n]

    def get_item(self, index):
        """Return the FilterBlock at the given index.

        Parameters
        ----------
        index : int

        Returns
        -------
        FilterBlock
        """
        return self._filter_blocks_list[index]

    def get_lists_materials_thicknesses_densities(self, cumulate=False):
        """Return the materials, thicknesses and densities of all foils across all blocks.

        Parameters
        ----------
        cumulate : bool, optional
            If True, foils sharing the same material and density are merged by
            summing their thicknesses globally across all blocks, regardless of
            their position. Order of first appearance is preserved. Default is False.

        Returns
        -------
        materials : list of str
        thicknesses : list of float
            Foil thicknesses in mm.
        densities : list of float
            Foil densities in g/cm³.
        """
        materials, thicknesses, densities = [], [], []
        for block in self._filter_blocks_list:
            m, t, d = block.get_lists_materials_thicknesses_densities()
            materials.extend(m)
            thicknesses.extend(t)
            densities.extend(d)
        if cumulate:
            seen = {}
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

    def get_selection_list(self):
        """Return the active foil index for each block.

        Returns
        -------
        list of int or None
            Each entry is the selection of the corresponding FilterBlock.
        """
        return [b.get_selection() for b in self._filter_blocks_list]

    def set_selection_list(self, selection):
        """Set the active foil index for each block. Use None for no selection.

        Parameters
        ----------
        selection : list of int or None
        """
        if len(selection) != self.get_n():
            raise Exception("bad number of elements in selection: %d (must be %d)" % (len(selection), self.get_n()))
        for block, sel in zip(self._filter_blocks_list, selection):
            block.set_selection(sel)

    @classmethod
    def from_plane_json_dict(cls, att_dic):
        """Construct a FilterBox from a plain (non-syned) attenuator dictionary.
        e.g.: file: https://raw.githubusercontent.com/oasys-esrf-kit/OASYS1-ESRF-Extensions/master/orangecontrib/esrf/xoppy/data/bm05_wb_attenuators.json

        Parameters
        ----------
        att_dic : dict
            Dictionary keyed by axis name. Each value is a dict of filter entries
            (keys not starting with '_') plus an optional '_att_pos' key giving
            the active foil index for that block.

        Returns
        -------
        FilterBox
        """
        keys = list(att_dic.keys())

        block_list = []
        for i in range(len(keys)):
            items = []
            selection = 0
            for filter_key in att_dic[keys[i]].keys():
                if filter_key == "_att_pos":
                    selection = att_dic[keys[i]][filter_key]

                if filter_key[0] != "_":
                    item = att_dic[keys[i]][filter_key]
                    f = FilterWithDensity(name=item['name'],
                                          material=item['substance'],
                                          thickness=item['thickness'],
                                          density=item['density'])
                    items.append(f)

            block_list.append(FilterBlock(filters_list=items, selection=selection))

        return FilterBox(filter_blocks_list=block_list)


if __name__ == "__main__":
    if 0:
        #
        # read json syned
        #
        # syned_file_name = "/home/srio/OASYS2.0/modelling_team_scripts_and_workspaces/id11/WATTDOG/SPECTRA/id11_wattdog_attenuators_2028_syned_no_density.json"

        # syned_file_name = "/home/srio/OASYS2.0/modelling_team_scripts_and_workspaces/id11/WATTDOG/SPECTRA/id11_wattdog_attenuators_2028_syned.json"
        syned_file_name = "/tmp_14_days/srio/tmp.json"

        is_remote = 0
        from syned.util.json_tools import load_from_json_file, load_from_json_url

        if is_remote:
            syned_filterbox2 = load_from_json_url(syned_file_name)
        else:
            syned_filterbox2 = load_from_json_file(syned_file_name)



        # syned_filterbox2.set_selection_list([1,2,3,4,5,6])
        syned_filterbox2.set_selection_list([None] * syned_filterbox2.get_n())
        print(syned_filterbox2.get_selection_list(), syned_filterbox2.get_n())

        print(syned_filterbox2.info())


        m, t, d = syned_filterbox2.get_lists_materials_thicknesses_densities(cumulate=1)
        print("************* cumulated:  ")
        for i in range(len(m)):
            print(i, m[i], t[i], d[i])

