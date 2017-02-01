
from syned.storage_ring.electron_beam import ElectronBeam
from syned.storage_ring.magnetic_structures.undulator import Undulator
from syned.beamline.optical_elements.ideal_elements.screen import Screen
from syned.beamline.optical_elements.ideal_elements.lens import IdealLens
from syned.beamline.optical_elements.absorbers.filter import Filter
from syned.beamline.optical_elements.absorbers.slit import Slit
from syned.beamline.optical_elements.absorbers.beam_stopper import BeamStopper
from syned.beamline.optical_elements.mirrors.mirror import Mirror
from syned.beamline.optical_elements.gratings.grating import Grating

from syned.beamline.shape import Rectangle

import json

def from_json(input_variable,double_check=True):
    if isinstance(input_variable,str):
        f = open(input_variable)
        text = f.read()
        f.close()
    else:
        text = input_variable


    jsn = json.loads(text)

    # print(jsn)

    if "ELEMENT_TYPE" in jsn.keys():
        # print("eval: tmp1 = ",jsn["ELEMENT_TYPE"]+"()")
        tmp1 = eval(jsn["ELEMENT_TYPE"]+"()")
        if tmp1.keys() is not None:
            for key in tmp1.keys():
                if key in jsn.keys():
                    tmp1.set_value_from_key_name(key,jsn[key])



    if double_check:
        print("\n------------------------------------------------------------------------------\n")
        print(tmp1.info())

        for key in jsn.keys():
            if key != "ELEMENT_TYPE":
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
    mirror1 = Mirror(name="mirror1")
    crystal1 = Grating(name="crystal1")
    grating1 = Grating(name="grating1")

    mylist = [src1,src2,screen1,lens1,filter1,stopper1,mirror1,crystal1]

    for i,element in enumerate(mylist):
        element.to_json("tmp_%d.json"%i)

    for i,element in enumerate(mylist):
        print("loading element %d"%i)
        tmp = from_json("tmp_%d.json"%i,double_check=True)



