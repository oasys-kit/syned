
from syned.util.json_tools import load_from_json_file

from syned.storage_ring.electron_beam import ElectronBeam
from syned.storage_ring.magnetic_structures.undulator import Undulator
from syned.beamline.optical_elements.ideal_elements.screen import Screen
from syned.beamline.optical_elements.ideal_elements.lens import IdealLens
from syned.beamline.optical_elements.absorbers.filter import Filter
from syned.beamline.optical_elements.absorbers.slit import Slit
from syned.beamline.optical_elements.absorbers.beam_stopper import BeamStopper
from syned.beamline.optical_elements.mirrors.mirror import Mirror
from syned.beamline.optical_elements.crystals.crystal import Crystal
from syned.beamline.optical_elements.gratings.grating import Grating

from syned.beamline.shape import SurfaceShape, Conic, Ellipsoid, Plane
from syned.beamline.shape import Rectangle
from syned.storage_ring.light_source import LightSource

from syned.beamline.beamline import Beamline
from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates



if __name__ == "__main__":



    src1 = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=6.0,current=0.2)
    src2 = Undulator()
    screen1 = Screen("screen1")
    lens1 = IdealLens(name="lens1",focal_y=6.0,focal_x=None,)
    filter1 = Filter("filter1","H2O",3.0e-6)
    slit1 = Slit(name="slit1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))
    stopper1 = BeamStopper(name="stopper1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))
    mirror1 = Mirror(name="mirror1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))
    crystal1 = Crystal(name="crystal1",surface_shape=Plane())
    grating1 = Grating(name="grating1",surface_shape=Conic())

    mylist = [src1,src2,screen1,lens1,filter1,slit1, stopper1, mirror1, grating1, crystal1]

    #
    # test individual elements
    #

    for i,element in enumerate(mylist):
        element.to_json("tmp_%d.json"%i)

    for i,element in enumerate(mylist):
        print("loading element %d"%i)
        tmp = load_from_json_file("tmp_%d.json"%i)
        print("returned class: ",type(tmp))



    #
    # test Ligtsource
    #
    lightsource1 = LightSource("test_source",src1,src2)
    lightsource1.to_json("tmp_100.json")

    tmp = load_from_json_file("tmp_100.json")
    print("returned class: ",type(tmp))
    print("\n-----------Info on: \n",tmp.info(),"----------------\n\n")

    print( tmp.get_electron_beam().info() )
    print( tmp.get_magnetic_structure().info() )

    #
    # test full beamline
    #

    SCREEN1     = BeamlineElement(screen1,      coordinates=ElementCoordinates(p=11.0))
    LENS1       = BeamlineElement(lens1,        coordinates=ElementCoordinates(p=12.0))
    FILTER1     = BeamlineElement(filter1,      coordinates=ElementCoordinates(p=13.0))
    SLIT1       = BeamlineElement(slit1,        coordinates=ElementCoordinates(p=15.0))
    STOPPER1    = BeamlineElement(stopper1,     coordinates=ElementCoordinates(p=16.0))
    MIRROR1     = BeamlineElement(mirror1,      coordinates=ElementCoordinates(p=17.0))
    GRATING1    = BeamlineElement(grating1,     coordinates=ElementCoordinates(p=18.0))
    CRYSTAL1    = BeamlineElement(crystal1,     coordinates=ElementCoordinates(p=19.0))

    MyList = [SCREEN1,LENS1,FILTER1,SLIT1,STOPPER1,MIRROR1,CRYSTAL1,GRATING1]


    #
    # test BeamlineElement
    #


    for i,element in enumerate(MyList):

        element.to_json("tmp_%d.json"%(100+i))
        tmp = load_from_json_file("tmp_%d.json"%(100+i))
        print("returned class: ",type(tmp))
        print("\n-----------Info on: \n",tmp.info(),"----------------\n\n")

    #
    # test Beamline
    #

    BL = Beamline(LightSource(name="test",electron_beam=src1,magnetic_structure=src2),
                  [SCREEN1,LENS1,FILTER1,SLIT1,STOPPER1,MIRROR1,CRYSTAL1,GRATING1])

    BL.to_json("tmp_200.json")

    #
    tmp = load_from_json_file("tmp_200.json")
    print("returned class: ",type(tmp))


    print(tmp.get_light_source().info())
    for element in tmp.get_beamline_elements():
        print("list element class: ",type(element))
        print(element.info())
    #
    #
    print("\n-----------Info on: \n",tmp.info(),"----------------\n\n")