from syned.beamline.optical_elements.shape import SurfaceShape, BoundaryShape, OpticalElementsWithSurfaceShape

class Grating(OpticalElementsWithSurfaceShape):
    def __init__(self, name, boundary_shape=BoundaryShape(), surface_shape=SurfaceShape()):
        super().__init__(name, boundary_shape, surface_shape)
