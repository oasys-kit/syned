class OpticalElement(object):
    def __init__(self, name, boundary_shape=None):
        self._name = name
        self._boundary_shape = boundary_shape

    def get_name(self):
        return self._name

    def get_boundary_shape(self):
        return self._boundary_shape
