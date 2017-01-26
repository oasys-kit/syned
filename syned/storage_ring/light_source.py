"""
Base class for all radiation sources: bending magnet or insertion devices (wiggler, undulator)
Every source can attach settings, i.e. inherits from DriverSettingsManager.
"""

class LightSource(object):
    def __init__(self, name="Undefined"):
        self._name = name

    def name(self):
        return self._name