
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
from syned.beamline.shape import Conic
from syned.beamline.shape import Plane
from syned.beamline.shape import SurfaceShape
from syned.beamline.shape import BoundaryShape
from syned.storage_ring.light_source import LightSource

from syned.beamline.beamline import Beamline
from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates

from collections import OrderedDict


import json
from urllib.request import urlopen



def load_from_json_file(file_name):
    f = open(file_name)
    text = f.read()
    f.close()
    return load_from_json_text(text)

def load_from_json_url(file_url):
    u = urlopen(file_url)
    ur = u.read()
    url = ur.decode(encoding='UTF-8')
    return load_from_json_text(url)


def load_from_json_text(text):
    return load_from_json_dictionary_recurrent(json.loads(text))


def load_from_json_dictionary_recurrent(jsn,verbose=False):

    if verbose: print(jsn.keys())
    if "CLASS_NAME" in jsn.keys():
        if verbose: print("FOUND CLASS NAME: ",jsn["CLASS_NAME"])

        try:
            tmp1 = eval(jsn["CLASS_NAME"]+"()")
            if verbose: print(">>>>",jsn["CLASS_NAME"],type(tmp1))
        except:
            raise RuntimeError("Error evaluating: "+jsn["CLASS_NAME"]+"()")


        if tmp1.keys() is not None:

            for key in tmp1.keys():
                if verbose: print(">>>>processing",key ,type(jsn[key]))
                if isinstance(jsn[key],dict):
                    if verbose: print(">>>>>>>>dictionary found, starting recurrency",key ,type(jsn[key]))
                    tmp2 = load_from_json_dictionary_recurrent(jsn[key])
                    if verbose: print(">>>>2",key,type(tmp2))
                    tmp1.set_value_from_key_name(key,tmp2)
                elif isinstance(jsn[key],list):
                    if verbose: print(">>>>>>>>LIST found, starting recurrency",key ,type(jsn[key]))
                    out_list_of_objects = []
                    for element in jsn[key]:
                        if isinstance(element,dict):
                            if verbose: print(">>>>>>>>LIST found, starting recurrency",key ,type(element))
                            tmp3 = load_from_json_dictionary_recurrent(element)
                            if verbose: print(">>>>3",type(tmp3))
                            out_list_of_objects.append(tmp3)
                    if verbose: print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",out_list_of_objects)
                    tmp1.set_value_from_key_name(key,out_list_of_objects)
                        # tmp1.set_value_from_key_name(key,tmp2)
                else:
                    if verbose: print(">>>>>>> settingng value for key: ",key," to: ",repr(jsn[key]))
                    tmp1.set_value_from_key_name(key,jsn[key])

        return tmp1
# def load_from_json_dictionary(jsn,double_check=False,verbose=True):
#
#     # print(jsn)
#
#     if "CLASS_NAME" in jsn.keys():
#         # print("eval: tmp1 = ",jsn["ELEMENT_TYPE"]+"()")
#         tmp1 = eval(jsn["CLASS_NAME"]+"()")
#         if tmp1.keys() is not None:
#             for key in tmp1.keys():
#                 if key in jsn.keys():
#                     if verbose: print("---------- setting: ",key, "to ",jsn[key])
#                     if isinstance(jsn[key],dict):
#                         tmp1.set_value_from_key_name(key,load_from_json_dictionary(jsn[key]))
#                     elif isinstance(jsn[key],list):
#                         pass
#                     else:
#                         tmp1.set_value_from_key_name(key,jsn[key])
#
#
#
#     if double_check:
#         print("\n------------------------------------------------------------------------------\n")
#         print(tmp1.info())
#
#         for key in jsn.keys():
#             if key != "CLASS_NAME":
#                 if key in tmp1.keys():
#                     print(key,"  file: ",repr(jsn[key]), "object: ",repr(tmp1.get_value_from_key_name(key)) )
#                 else:
#                     raise ValueError("Warning: Key %s in json cannot be set to object %s"%(key,tmp1.__class__.__name__))
#
#         print("\n------------------------------------------------------------------------------\n")
#
#     return tmp1
#
#

if __name__ == "__main__":
    file_in = "/scisoft/xop2.4/extensions/shadowvui/shadow3-scripts/ESRF-LIGHTSOURCES/ESRF_ID1_EBS_ppu27_9.json"
    syned_obj = load_from_json_file(file_in)
    print(syned_obj.info())

    file_url = "https://raw.githubusercontent.com/srio/shadow3-scripts/master/ESRF-LIGHTSOURCES/ESRF_ID1_EBS_ppu27_9.json"
    syned_obj = load_from_json_url(file_url)
    print(syned_obj.info())

