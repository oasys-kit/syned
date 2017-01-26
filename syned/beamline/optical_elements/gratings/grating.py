from syned.beamline.optical_elements.shape import SurfaceShape, OpticalElementsWithSurfaceShape

class Grating(OpticalElementsWithSurfaceShape):
    def __init__(self, name, surface_shape=SurfaceShape()):
        super().__init__(name, surface_shape)
