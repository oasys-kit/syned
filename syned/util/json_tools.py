"""
Functions to read/write syned objects in json files.

Notes
-----
The elements that are not explicitely imported in the code that follows, but they MUST be imported
to define the objects at run time.
To import more elements, yoy can use the exec_command keyword.

"""
from syned.storage_ring.electron_beam import ElectronBeam
from syned.storage_ring.magnetic_structures.undulator import Undulator
from syned.storage_ring.magnetic_structures.wiggler import Wiggler
from syned.storage_ring.magnetic_structures.bending_magnet import BendingMagnet
from syned.storage_ring.magnetic_structure import MagneticStructure
from syned.beamline.optical_elements.ideal_elements.screen import Screen
from syned.beamline.optical_elements.ideal_elements.ideal_lens import IdealLens
from syned.beamline.optical_elements.absorbers.filter import Filter
from syned.beamline.optical_elements.absorbers.slit import Slit
from syned.beamline.optical_elements.absorbers.beam_stopper import BeamStopper
from syned.beamline.optical_elements.absorbers.holed_filter import HoledFilter
from syned.beamline.optical_elements.mirrors.mirror import Mirror
from syned.beamline.optical_elements.crystals.crystal import Crystal
from syned.beamline.optical_elements.gratings.grating import Grating
from syned.beamline.optical_elements.gratings.grating import GratingVLS
from syned.beamline.optical_elements.gratings.grating import GratingBlaze
from syned.beamline.optical_elements.gratings.grating import GratingLamellar

from syned.beamline.shape import BoundaryShape
from syned.beamline.shape import Rectangle, Ellipse, Circle
from syned.beamline.shape import MultiplePatch
from syned.beamline.shape import DoubleRectangle, DoubleEllipse, DoubleCircle

from syned.beamline.shape import SurfaceShape
from syned.beamline.shape import Conic, Plane, Sphere, SphericalCylinder
from syned.beamline.shape import Ellipsoid, EllipticalCylinder
from syned.beamline.shape import Paraboloid, ParabolicCylinder
from syned.beamline.shape import Hyperboloid, HyperbolicCylinder
from syned.beamline.shape import Toroid

from syned.storage_ring.light_source import LightSource
from syned.storage_ring.empty_light_source import EmptyLightSource

from syned.beamline.beamline import Beamline
from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates

from collections import OrderedDict

try:
    import json_tricks as json # to save numpy arrays
except:
    import json
from urllib.request import urlopen

def load_from_json_file(file_name, exec_commands=None):
    """
    Function to load a syned object from a json file.

    Parameters
    ----------
    file_name : str
        The file name.
    exec_commands : str
        The commands (typically import...) to be executed before accesing the file.

    Returns
    -------
    instance of SynedObject

    """
    f = open(file_name)
    text = f.read()
    f.close()
    return load_from_json_text(text, exec_commands=exec_commands)

def load_from_json_url(file_url, exec_commands=None):
    """
    Function to load a syned object from a remote json file.

    Parameters
    ----------
    file_url : str
        The URL with the file name.
    exec_commands : str
        The commands (typically import...) to be executed before accesing the file.

    Returns
    -------
    instance of SynedObject

    """
    u = urlopen(file_url)
    ur = u.read()
    url = ur.decode(encoding='UTF-8')
    return load_from_json_text(url, exec_commands=exec_commands)

def load_from_json_text(text, exec_commands=None):
    """
    Function to load a syned object from a json txt.

    Parameters
    ----------
    text : str
        The text with the corresponding info.
    exec_commands : str
        The commands (typically import...) to be executed before accesing the file.

    Returns
    -------
    instance of SynedObject

    """
    return load_from_json_dictionary_recurrent(json.loads(text), exec_commands=exec_commands)

def load_from_json_dictionary_recurrent(jsn, verbose=False, exec_commands=None):
    """
    Function to convert a dictionary (got from json file) into a syned object.

    Parameters
    ----------
    jsn : dict
        The dictionary with json file information.
    verbose : boolean, optional
        Define or not verbose output.
    exec_commands : str
        The commands (typically import...) to be executed before accesing the file.

    Returns
    -------
    instance of SynedObject

    """
    if isinstance(exec_commands, list):
        for command in exec_commands:
            if verbose: print(">>>>",command)
            exec(command)
    elif isinstance(exec_commands, str):
        if verbose: print(">>>>", exec_commands)
        exec(exec_commands)

    if verbose: print(jsn.keys())
    if "CLASS_NAME" in jsn.keys():
        if verbose: print("FOUND CLASS NAME: ",jsn["CLASS_NAME"])
        if verbose: print(">>>>eval: ", jsn["CLASS_NAME"])
        try:
            tmp1 = eval(jsn["CLASS_NAME"]+"()")
        except:
            raise RuntimeError("Error evaluating: "+jsn["CLASS_NAME"]+"() ** you could use the exec_command keyword to import it at run time **")


        if tmp1.keys() is not None:

            for key in tmp1.keys():
                if verbose: print(">>>>processing",key ,type(jsn[key]))
                if isinstance(jsn[key],dict):
                    if verbose: print(">>>>>>>>dictionary found, starting recurrency",key ,type(jsn[key]))
                    tmp2 = load_from_json_dictionary_recurrent(jsn[key],exec_commands=exec_commands)
                    if verbose: print(">>>>2",key,type(tmp2))
                    tmp1.set_value_from_key_name(key,tmp2)
                elif isinstance(jsn[key], list):
                    if verbose: print(">>>>>>>>LIST found, starting recurrency",key ,type(jsn[key]))
                    out_list_of_objects = []
                    for element in jsn[key]:
                        if isinstance(element, dict):
                            if verbose: print(">>>>>>>>LIST found, starting recurrency",key ,type(element))
                            tmp3 = load_from_json_dictionary_recurrent(element, exec_commands=exec_commands)
                            if verbose: print(">>>>3",type(tmp3))
                            out_list_of_objects.append(tmp3)
                        else:
                            print("***** Failed to load", element)
                    if verbose: print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",out_list_of_objects)
                    tmp1.set_value_from_key_name(key,out_list_of_objects)
                        # tmp1.set_value_from_key_name(key,tmp2)
                else:
                    if verbose: print(">>>>>>> setting value for key: ",key," to: ",repr(jsn[key]))
                    tmp1.set_value_from_key_name(key,jsn[key])

        return tmp1


if __name__ == "__main__":

    file_url = "http://ftp.esrf.fr/pub/scisoft/syned/lightsources/ESRF_ID01_EBS_PPU35_22.json"
    syned_obj = load_from_json_url(file_url)
    print(syned_obj.info())


    #
    # file_url = "/home/manuel/Oasys/ALSU-IR-BM.json"
    # syned_obj = load_from_json_file(file_url)
    # print(syned_obj.info())

    # file_url = "/home/manuel/Oasys/bl.json"
    # syned_obj = load_from_json_file(file_url)
    # print(syned_obj.info())
