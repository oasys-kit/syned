
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

from syned.beamline.shape import Rectangle
from syned.beamline.shape import SurfaceShape
from syned.storage_ring.light_source import LightSource

from syned.beamline.beamline import Beamline
from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates

import json

def load_from_json_file(file_name):
    f = open(file_name)
    text = f.read()
    f.close()
    return load_from_json_text(text)


def load_from_json_text(text):
    return load_from_json_dictionary_recurrent(json.loads(text))


def load_from_json_dictionary_recurrent(jsn):

    # print(jsn)
    if "CLASS_NAME" in jsn.keys():
        # print("eval: tmp1 = ",jsn["ELEMENT_TYPE"]+"()")
        tmp1 = eval(jsn["CLASS_NAME"]+"()")
        print(">>>>",jsn["CLASS_NAME"],type(tmp1))
        if tmp1.keys() is not None:

            for key in tmp1.keys():
                print(">>>>processing",key ,type(jsn[key]))
                if isinstance(jsn[key],dict):
                    tmp2 = load_from_json_dictionary_recurrent(jsn[key])
                    print(">>>>2",key,type(tmp2))
                    tmp1.set_value_from_key_name(key,tmp2)
                elif isinstance(jsn[key],list):
                    #todo
                    pass
                    # for element in jsn[key]:
                    #     print(element)
                    #     tmp3 = load_from_json_dictionary_recurrent(element)
                    #     # print(">>>>3",type(tmp3))
                    #     # tmp1.set_value_from_key_name(key,tmp3)
                else:
                    tmp1.set_value_from_key_name(key,jsn[key])

def load_from_json_dictionary(jsn,double_check=False,verbose=True):

    # print(jsn)

    if "CLASS_NAME" in jsn.keys():
        # print("eval: tmp1 = ",jsn["ELEMENT_TYPE"]+"()")
        tmp1 = eval(jsn["CLASS_NAME"]+"()")
        if tmp1.keys() is not None:
            for key in tmp1.keys():
                if key in jsn.keys():
                    if verbose: print("---------- setting: ",key, "to ",jsn[key])
                    if isinstance(jsn[key],dict):
                        tmp1.set_value_from_key_name(key,load_from_json_dictionary(jsn[key]))
                    elif isinstance(jsn[key],list):
                        pass
                    else:
                        tmp1.set_value_from_key_name(key,jsn[key])



    if double_check:
        print("\n------------------------------------------------------------------------------\n")
        print(tmp1.info())

        for key in jsn.keys():
            if key != "CLASS_NAME":
                if key in tmp1.keys():
                    print(key,"  file: ",repr(jsn[key]), "object: ",repr(tmp1.get_value_from_key_name(key)) )
                else:
                    raise ValueError("Warning: Key %s in json cannot be set to object %s"%(key,tmp1.__class__.__name__))

        print("\n------------------------------------------------------------------------------\n")

    return tmp1



if __name__ == "__main__":



    src1 = ElectronBeam.initialize_as_pencil_beam(energy_in_GeV=6.0,current=0.2)
    src2 = Undulator()
    screen1 = Screen("screen1")
    lens1 = IdealLens(name="lens1",focal_y=6.0,focal_x=None,)
    filter1 = Filter("filter1","H2O",3.0e-6)
    slit1 = Slit(name="slit1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))
    stopper1 = BeamStopper(name="stopper1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))
    mirror1 = Mirror(name="mirror1",boundary_shape=Rectangle(-0.5e-3,0.5e-3,-2e-3,2e-3))
    crystal1 = Crystal(name="crystal1")
    grating1 = Grating(name="grating1")

    # #
    # mylist = [src1,src2,screen1,lens1,filter1,slit1, stopper1, mirror1,crystal1]
    # # mylist = [mirror1]
    # #
    # for i,element in enumerate(mylist):
    #     element.to_json("tmp_%d.json"%i)
    #
    # for i,element in enumerate(mylist):
    #     print("loading element %d"%i)
    #     tmp = load_from_json_file("tmp_%d.json"%i)
    #     print("\n-----------Info on: \n",tmp.info(),"----------------\n\n")
    #
    # # print(src1.to_full_dictionary())
    #
    # #
    # # test lightsource
    # #
    #
    lightsource1 = LightSource("test_source",src1,src2)
    # lightsource1.to_json("tmp_100.json")
    # print(lightsource1.info())
    #
    # tmp = load_from_json_file("tmp_100.json")
    # print("\n-----------Info on: \n",tmp.info(),"----------------\n\n")
    #
    # print( tmp.get_electron_beam().info() )
    # print( tmp.get_magnetic_structure().info() )

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





    # SCREEN1.to_json("tmp_101.json")

    BL = Beamline(lightsource1,[SCREEN1,LENS1,FILTER1,SLIT1,STOPPER1,MIRROR1,CRYSTAL1,GRATING1])
    # print(BL.to_dictionary())
    BL.to_json("tmp_102.json")
    # print(BL.info())

    BL_LOADED = load_from_json_file("tmp_102.json")
    print(type(BL_LOADED))
    # print(BL_LOADED.get_light_source().info())
    # for element in BL_LOADED.get_beamline_elements():
    #     print(element.__class__.__name__)


