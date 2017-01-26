from syned.beamline.optical_elements.shape import SurfaceShape, OpticalElementsWithSurfaceShape

class Mirror(OpticalElementsWithSurfaceShape):
    def __init__(self,
                 name,
                 boundary_shape=None,
                 surface_shape=SurfaceShape()):
        super().__init__(name, boundary_shape, surface_shape)
