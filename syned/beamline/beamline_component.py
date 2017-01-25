"""
Base class for all beamline components.
Enforce to name every every component.
Every beamline component can store settings
"""

class BeamlineComponent(object):
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name