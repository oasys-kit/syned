
from syned.storage_ring.electron_beam import ElectronBeam
from syned.storage_ring.magnetic_structures.undulator import Undulator
from syned.storage_ring.light_source import LightSource


from syned.beamline.optical_elements.ideal_elements.screen import Screen
from syned.beamline.optical_elements.ideal_elements.lens import IdealLens
from syned.beamline.optical_elements.absorbers.filter import Filter
from syned.beamline.optical_elements.absorbers.slit import Slit
from syned.beamline.optical_elements.absorbers.beam_stopper import BeamStopper

from syned.beamline.optical_elements.mirrors.mirror import Mirror
from syned.beamline.optical_elements.gratings.grating import Grating

from syned.beamline.beamline import BeamlineElement, Beamline
from syned.beamline.element_coordinates import ElementCoordinates

if __name__ == "__main__":


    print("==================== LightSource: ==================")


    src1 = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=6.0,current=0.2)
    src2 = Undulator()
    src = LightSource("test",src1,src2)

    for key in src1.keys():
        print(key,src1.to_dictionary()[key])

    for key in src2.keys():
        print(key,src2.to_dictionary()[key])


    print(src1.keys())
    print(src2.keys())

    print(src1.info())
    print(src2.info())


    print(src.info())


    src2.set_value_from_key_name("K_horizontal",33)

    print(src.info())
    assert (33,src2.get_value_from_key_name("K_horizontal"))

    src1.to_json("tmp_src1.json")
    src2.to_json("tmp_src2.json")



    print("==================== BeamLine elements: ==================")

    #
    # ideal elements
    #

    screen1 = Screen("screen1")

    screen1.keys()
    print(screen1.info())
    print(screen1.to_json())


    lens1 = IdealLens("lens1",3.0)

    lens1.keys()
    print(lens1.info())
    print(lens1.to_json())



    #
    # absorbers
    #
    filter1 = Filter("filter1","H2O",3.0e-6)

    filter1.keys()
    print(filter1.info())
    print(filter1.to_json())
    # print(filter1._support_dictionary)

    #slit1 = Slit.initialize_as_rectangle("slit1",2e-3,4e-3)
    from syned.beamline.shape import Rectangle
    slit1 = Slit(name="slit1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))

    slit1.keys()
    print(slit1.info())
    print(slit1.to_json())

    slit2 = Slit(name="slit2")

    slit2.set_rectangle(width=3e-4,height=5e-4)
    slit2.set_circle(radius=3e-4)
    print(slit2.info())
    print(slit2.to_json())


    stopper1 = BeamStopper(name="stopper1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))

    stopper1.keys()
    print(stopper1.info())
    print(stopper1.to_json())

    stopper2 = BeamStopper(name="stopper2")

    stopper2.set_rectangle(width=3e-4,height=5e-4)
    stopper2.set_circle(radius=3e-4)
    print(stopper2.info())
    print(stopper2.to_json())

    #
    # elements with shape: mirror, gratings, crystals
    #

    mirror1 = Mirror(name="mirror1")

    mirror1.keys()
    print(mirror1.info())
    print(mirror1.to_json())


    crystal1 = Grating(name="crystal1")

    crystal1.keys()
    print(crystal1.info())
    print(crystal1.to_json())


    grating1 = Grating(name="grating1")

    grating1.keys()
    print(grating1.info())
    print(grating1.to_json())


    print("==================== BeamLine: ==================")

    beamline1 = Beamline()
    beamline1.set_light_source(src)
    beamline1.append_beamline_element(BeamlineElement(screen1,coordinates=ElementCoordinates(100.0)))

    print(beamline1.info())
