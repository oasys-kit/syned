
from syned.util.json_tools import load_from_json_file

from syned.storage_ring.electron_beam import ElectronBeam
from syned.storage_ring.magnetic_structures.undulator import Undulator
from syned.beamline.optical_elements.ideal_elements.screen import Screen
from syned.beamline.optical_elements.absorbers.slit import Slit

from syned.storage_ring.light_source import LightSource

from syned.beamline.beamline import Beamline
from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates

from syned.beamline.shape import MultiplePatch

# this is an example of a double slit (a slit with two rectangular apertures).
if __name__ == "__main__":


    # source
    src1 = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=6.0,current=0.2)
    src2 = Undulator()

    lightsource1 = LightSource("test_source",src1, src2)

    # check file o/i for test
    lightsource1.to_json("tmp.json")
    tmp = load_from_json_file("tmp.json")
    print("returned class: ",type(tmp))
    print(lightsource1.to_dictionary())
    print(tmp.to_dictionary())
    assert (lightsource1.to_dictionary() == tmp.to_dictionary())

    #optical elements
    patches = MultiplePatch()
    patches.append_rectangle(-0.02,-0.01,-0.001,0.001)
    patches.append_rectangle(0.01,0.02,-0.001,0.001)
    slit1 = Slit(name="slit1", boundary_shape=patches)

    #  check file o/i for test individual elements
    mylist = [src1, src2, slit1]
    for i,element in enumerate(mylist):
        element.to_json("tmp_%d.json"%i)

    for i, element in enumerate(mylist):
        print("\nloading element %d"%i)
        tmp = load_from_json_file("tmp_%d.json"%i)
        print("returned class: ",type(tmp))
        print(mylist[i].to_dictionary())
        print(tmp.to_dictionary())
        assert (mylist[i].to_dictionary() == tmp.to_dictionary())

    # test Beamline

    bl_slit1 = BeamlineElement(optical_element=slit1, coordinates=ElementCoordinates(p=10.0,q=3.0))
    BL = Beamline(light_source=lightsource1, beamline_elements_list=[bl_slit1])

    # check file o/i for test full beamline
    BL.to_json("tmp_bl.json")
    tmp = load_from_json_file("tmp_bl.json")
    print("returned class: ",type(tmp))
    print(BL.to_dictionary())
    print(tmp.to_dictionary())
    assert(BL.to_dictionary() == tmp.to_dictionary())

    print(BL.info())
