"""
Base class for LighSource, which contains:
    - a name
    - an electron beam
    - a magnetic structure

"""

from syned.storage_ring.magnetic_structure import MagneticStructure
from syned.storage_ring.electron_beam import ElectronBeam

class LightSource(object):
    def __init__(self, name="Undefined", electron_beam=ElectronBeam(), magnetic_structure=MagneticStructure()):
        self._name = name
        self._electron_beam = electron_beam
        self._magnetic_structure = magnetic_structure

    def get_name(self):
        return self._name

    def get_electron_beam(self):
        return self._electron_beam

    def get_magnetic_structure(self):
        return self._magnetic_structure

    def info(self):
        return self._electron_beam.info() + self._magnetic_structure.info()