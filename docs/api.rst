.. currentmodule:: syned

===========
Package API
===========
This page lists main classes in this package.


``syned`` classes.

main
----
``syned`` Base class

.. autosummary::
   :toctree: generated/

   syned_object

beamline
--------
``syned.beamline`` A beamline is made by a light_source and one or several beamline_element

.. autosummary::
   :toctree: generated/

   syned.beamline.beamline

light source
------------
Light source = Electron beam + magnetic structure

* ``syned.storage_ring.light_source`` Electron beam + magnetic structure

   .. autosummary::
      :toctree: generated/

      syned.storage_ring.light_source

* ``syned.storage_ring.empty_light_source`` Empty light source

   .. autosummary::
      :toctree: generated/

      syned.storage_ring.empty_light_source

eletron beam
-------------
Electron beam

``syned.storage_ring.electron_beam`` Electron beam

.. autosummary::
   :toctree: generated/

   syned.storage_ring.electron_beam

magnetic structures
-------------------
Magnetic structures


``syned.storage_ring.magnetic_structures`` Magnetic structures

.. autosummary::
   :toctree: generated/

   syned.storage_ring.magnetic_structure
   syned.storage_ring.magnetic_structures.bending_magnet
   syned.storage_ring.magnetic_structures.insertion_device
   syned.storage_ring.magnetic_structures.undulator
   syned.storage_ring.magnetic_structures.wiggler



beamline element
----------------
``syned.beamline.beamline_element`` A beamline element is made by an optical_element and the element_coordinates

.. autosummary::
   :toctree: generated/

   syned.beamline.beamline_element

* ``syned.beamline.optical_element`` optical element
.. autosummary::
   :toctree: generated/

   syned.beamline.optical_element
   syned.beamline.optical_element_with_surface_shape

* ``syned.beamline.element_coordinates`` element coordinates
.. autosummary::
   :toctree: generated/

   syned.beamline.element_coordinates


optical elements
----------------

``syned.beamline.optical_elements`` Optical elements

* ``syned.beamline.optical_elements.ideal_elements`` ideal_element, screen, ideal_lens
.. autosummary::
   :toctree: generated/

   syned.beamline.optical_elements.ideal_elements.ideal_element
   syned.beamline.optical_elements.ideal_elements.screen
   syned.beamline.optical_elements.ideal_elements.ideal_lens


* ``syned.beamline.optical_elements.absorbers`` absorber, beam_stopper, filter, holed_filter, slit
.. autosummary::
   :toctree: generated/

   syned.beamline.optical_elements.absorbers.absorber
   syned.beamline.optical_elements.absorbers.beam_stopper
   syned.beamline.optical_elements.absorbers.filter
   syned.beamline.optical_elements.absorbers.holed_filter
   syned.beamline.optical_elements.absorbers.slit

* ``syned.beamline.optical_elements.crystals`` crystals

.. autosummary::
   :toctree: generated/

   syned.beamline.optical_elements.crystals.crystal

* ``syned.beamline.optical_elements.gratings`` gratings

.. autosummary::
   :toctree: generated/

   syned.beamline.optical_elements.gratings.grating


* ``syned.beamline.optical_elements.mirrors`` mirrors

.. autosummary::
   :toctree: generated/

   syned.beamline.optical_elements.mirrors.mirror

* ``syned.beamline.optical_elements.refractors`` interface, lens, crl

.. autosummary::
   :toctree: generated/

   syned.beamline.optical_elements.refractors.interface
   syned.beamline.optical_elements.refractors.lens
   syned.beamline.optical_elements.refractors.crl


geometrical shapes
------------------
``syned.beamline.shape`` Utilities for defining geometrical surface shapes and boundary shapes

``syned.beamline.shape.Shape`` Base class
   .. autosummary::
      :toctree: generated/

      syned.beamline.shape.Shape

* ``syned.beamline.shape.SurfaceShape`` Surface shape classes
   .. autosummary::
      :toctree: generated/

      syned.beamline.shape.SurfaceShape
      syned.beamline.shape.Cylinder
      syned.beamline.shape.Conic
      syned.beamline.shape.Plane
      syned.beamline.shape.Sphere
      syned.beamline.shape.SphericalCylinder
      syned.beamline.shape.Ellipsoid
      syned.beamline.shape.EllipticCylinder
      syned.beamline.shape.Hyperboloid
      syned.beamline.shape.HyperbolicCylinder
      syned.beamline.shape.Paraboloid
      syned.beamline.shape.ParabolicCylinder
      syned.beamline.shape.Toroid
      syned.beamline.shape.NumericalMesh

* ``syned.beamline.shape.BoundaryShape`` Boundary shape classes
   .. autosummary::
      :toctree: generated/

      syned.beamline.shape.BoundaryShape
      syned.beamline.shape.Rectangle
      syned.beamline.shape.Ellipse
      syned.beamline.shape.Circle
      syned.beamline.shape.Polygon
      syned.beamline.shape.DoubleRectangle
      syned.beamline.shape.DoubleEllipse
      syned.beamline.shape.DoubleCircle
      syned.beamline.shape.MultiplePatch
      syned.beamline.shape.TwoEllipses

* Others
   .. autosummary::
      :toctree: generated/

      syned.beamline.shape.Convexity
      syned.beamline.shape.Direction
      syned.beamline.shape.Side