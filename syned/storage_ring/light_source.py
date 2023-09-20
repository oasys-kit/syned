"""


"""
from syned.syned_object import SynedObject
from syned.storage_ring.magnetic_structure import MagneticStructure
from syned.storage_ring.electron_beam import ElectronBeam

class LightSource(SynedObject):
    """
    Base class for LighSource. A light source contains:
    * a name
    * an electron beam
    * a magnetic structure

    Parameters
    ----------
    name : str, optional
        The light source name.
    electron_beam : instance of ElectronBeam, optional
        The electron beam. If None, it is initialized with ElectronBeam().
    magnetic_structure : instance of MagneticStructure, optional
        The electron beam. If None, it is initialized with MagneticStructure().

    """
    def __init__(self, name="Undefined", electron_beam=None, magnetic_structure=None):
        self._name = name
        if electron_beam is None:
            self._electron_beam = ElectronBeam()
        else:
            self._electron_beam      = electron_beam
        if magnetic_structure is None:
            self._magnetic_structure = MagneticStructure()
        else:
            self._magnetic_structure = magnetic_structure
        # support text containg name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",              "Name",""),
                    ("electron_beam",     "Electron Beam",""),
                    ("magnetic_structure","Magnetic Strtructure",""),
            ] )


    def get_name(self):
        """
        Returns the name of the light source.

        Returns
        -------
        str

        """
        return self._name

    def get_electron_beam(self):
        """
        Returns the electron beam.

        Returns
        -------
        instance of ElectronBeam

        """
        return self._electron_beam

    def get_magnetic_structure(self):
        """
        Returns the magnetic structure.

        Returns
        -------
        instance of MagneticStructure

        """
        return self._magnetic_structure




if __name__ == "__main__":

    from syned.storage_ring.magnetic_structures.undulator import Undulator

    eb = ElectronBeam.initialize_as_pencil_beam( energy_in_GeV=2.0,energy_spread=0.0,current=0.5)
    ms = Undulator.initialize_as_vertical_undulator( K=1.8, period_length=0.038, periods_number=56.0 )

    light_source = LightSource(name="",electron_beam=eb,magnetic_structure=ms)

    print(light_source.info())

