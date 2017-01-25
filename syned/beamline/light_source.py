"""
Base class for all radiation sources: bending magnet or insertion devices (wiggler, undulator)
Every source can attach settings, i.e. inherits from DriverSettingsManager.
"""

from syned.beamline.beamline_component import BeamlineComponent

class LightSource(BeamlineComponent):
    def __init__(self, name="Undefined"):
        BeamlineComponent.__init__(self, name)
