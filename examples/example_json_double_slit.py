
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

if __name__ == "__main__":



    src1 = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=6.0,current=0.2)
    src2 = Undulator()
    screen1 = Screen("screen1")

    patches = MultiplePatch()
    patches.append_rectangle(-0.02,-0.01,-0.001,0.001)
    patches.append_rectangle(0.01,0.02,-0.001,0.001)

    slit1 = Slit(name="slit1", boundary_shape=patches)

    mylist = [src1, src2, slit1]

    #
    # test individual elements
    #

    for i,element in enumerate(mylist):
        element.to_json("tmp_%d.json"%i)

    for i, element in enumerate(mylist):
        print("\nloading element %d"%i)
        tmp = load_from_json_file("tmp_%d.json"%i)
        print("returned class: ",type(tmp))
        print(mylist[i].to_dictionary())
        print(tmp.to_dictionary())
        assert (mylist[i].to_dictionary() == tmp.to_dictionary())



    #
    # test Ligtsource
    #
    lightsource1 = LightSource("test_source",src1, src2)
    lightsource1.to_json("tmp_100.json")

    for i in [100]:
        print("\nloading element %d"%i)
        tmp = load_from_json_file("tmp_%d.json"%i)
        print("returned class: ",type(tmp))
        print(lightsource1.to_dictionary())
        print(tmp.to_dictionary())
        assert (lightsource1.to_dictionary() == tmp.to_dictionary())


    #
    # test beamline element
    #

    SLIT1       = BeamlineElement(slit1,        coordinates=ElementCoordinates(p=15.0))

    MyList = [SLIT1]

    for i,element in enumerate(MyList):

        element.to_json("tmp_%d.json"%(100+i))
        tmp = load_from_json_file("tmp_%d.json"%(100+i))
        print("returned class: ",type(tmp))
        print(element.to_dictionary())
        print(tmp.to_dictionary())
        assert (element.to_dictionary() == tmp.to_dictionary())

    #
    # test Beamline
    #

    BL = Beamline(LightSource(name="test",electron_beam=src1,magnetic_structure=src2),
                  [SLIT1])

    BL.to_json("tmp_300.json")

    #
    tmp = load_from_json_file("tmp_300.json")
    print("returned class: ",type(tmp))
    print(BL.to_dictionary())
    print(tmp.to_dictionary())
    assert(BL.to_dictionary() == tmp.to_dictionary())
