"""
Base class for LighSource, which contains:
    - a name
    - an electron beam
    - a magnetic structure

"""
from syned.syned_object import SynedObject
from syned.storage_ring.magnetic_structure import MagneticStructure
from syned.storage_ring.electron_beam import ElectronBeam

class LightSource(SynedObject):
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
        return self._name

    def get_electron_beam(self):
        return self._electron_beam

    def get_magnetic_structure(self):
        return self._magnetic_structure




if __name__ == "__main__":

    from syned.storage_ring.magnetic_structures.undulator import Undulator

    eb = ElectronBeam.initialize_as_pencil_beam( energy_in_GeV=2.0,energy_spread=0.0,current=0.5)
    ms = Undulator.initialize_as_vertical_undulator( K=1.8, period_length=0.038, periods_number=56.0 )

    light_source = LightSource(name="",electron_beam=eb,magnetic_structure=ms)

    print(light_source.info())

