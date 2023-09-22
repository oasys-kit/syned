
from syned.storage_ring.electron_beam import ElectronBeam
from syned.storage_ring.magnetic_structures.undulator import Undulator
from syned.storage_ring.light_source import LightSource
from syned.beamline.shape import *

from syned.beamline.optical_elements.ideal_elements.screen import Screen
from syned.beamline.optical_elements.ideal_elements.ideal_lens import IdealLens
from syned.beamline.optical_elements.absorbers.filter import Filter
from syned.beamline.optical_elements.absorbers.slit import Slit
from syned.beamline.optical_elements.absorbers.beam_stopper import BeamStopper

from syned.beamline.optical_elements.mirrors.mirror import Mirror
from syned.beamline.optical_elements.crystals.crystal import Crystal
from syned.beamline.optical_elements.gratings.grating import Grating

from syned.beamline.beamline import BeamlineElement, Beamline
from syned.beamline.element_coordinates import ElementCoordinates

from syned.util.json_tools import load_from_json_file

#
# example of setting a beamline in SYNED.
#
if __name__ == "__main__":


    print("==================== LightSource: ==================")

    src1 = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=6.0,current=0.2)

    src2 = Undulator()
    src2.set_value_from_key_name("K_horizontal",33)
    # just to be sure...
    assert (33 == src2.get_value_from_key_name("K_horizontal"))

    src = LightSource("test",src1,src2)

    # check file o/i for test
    src.to_json("tmp.json") # write to file
    tmp = load_from_json_file("tmp.json") # read from file
    print("returned class: ", type(tmp))
    print(src.to_dictionary())
    print(tmp.to_dictionary())
    assert(src.to_dictionary() == tmp.to_dictionary())


    print("==================== Optical elements: ==================")

    #
    # ideal elements
    #

    screen1 = Screen("screen1")
    lens1 = IdealLens("lens1",3.0)

    #
    # absorbers
    #
    filter1 = Filter("filter1","H2O",3.0e-6)

    slit1 = Slit(name="slit1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))

    slit2 = Slit(name="slit2")
    slit2.set_rectangle(width=3e-4,height=5e-4)
    slit2.set_circle(radius=3e-4)

    stopper1 = BeamStopper(name="stopper1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))

    stopper2 = BeamStopper(name="stopper2")

    stopper2.set_rectangle(width=3e-4,height=5e-4)
    stopper2.set_circle(radius=3e-4)

    #
    # elements with shape: mirror, gratings, crystals
    #

    mirror1 = Mirror(name="mirror1")

    crystal1 = Crystal(name="crystal1")

    grating1 = Grating(name="grating1")


    print("==================== BeamLine: ==================")

    beamline1 = Beamline()

    beamline1.set_light_source(src)

    list_oe = [screen1, lens1, filter1, slit1, slit2, stopper1, stopper2, mirror1, crystal1, grating1]
    for i, optical_element in enumerate(list_oe):
        coordinates=ElementCoordinates(p=1.1*i, q=1.2*i)
        be = BeamlineElement(optical_element=optical_element, coordinates=coordinates)
        beamline1.append_beamline_element(be)

    print(beamline1.info())

    # check file o/i for test
    beamline1.to_json("tmp_beamline1.json")
    tmp = load_from_json_file("tmp_beamline1.json")
    print("returned class: ",type(tmp))
    print(beamline1.to_dictionary())
    print(tmp.to_dictionary())
    assert(beamline1.to_dictionary() == tmp.to_dictionary())
