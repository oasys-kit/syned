"""
Base class for all optical elements
"""
from syned.beamline.beamline_component import BeamlineComponent

class OpticalElement(BeamlineComponent):
    def __init__(self, name="Undefined"):
        BeamlineComponent.__init__(self, name)
