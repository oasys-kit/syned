from syned.beamline.optical_element import OpticalElement
from syned.beamline.shape import SurfaceShape



class OpticalElementsWithSurfaceShape(OpticalElement):

    def __init__(self, name, surface_shape=None, boundary_shape=None, ):
        super().__init__(name, boundary_shape)
        if surface_shape is None:
            surface_shape = SurfaceShape
        self._surface_shape = surface_shape

    def get_surface_shape(self):
        return self._surface_shape

    def set_surface_shape(self,surface_shape=SurfaceShape()):
        self._surface_shape = surface_shape