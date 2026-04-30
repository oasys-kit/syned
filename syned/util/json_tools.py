"""
Functions to read/write syned objects in json files.

Notes
-----
Common syned classes are imported at module level so they are available when
loading json files.  To load objects from other packages (e.g. shadow4), pass
their import statements via the ``exec_commands`` keyword, or use
:func:`get_exec_commands_for_package` to generate them automatically.
"""

import json_tricks # to save numpy arrays
import pkgutil, importlib, inspect

from urllib.request import urlopen

import syned

def get_exec_commands_for_package(package):
    """
    Build a string of import statements for all classes defined in a package.

    Walks every submodule of ``package`` with pkgutil and collects classes
    whose ``__module__`` matches the submodule name (i.e. classes defined
    there, not re-exported ones).  The resulting string can be passed as
    ``exec_commands`` to the json loaders so they can instantiate objects by
    class name.

    Parameters
    ----------
    package : module
        The top-level package to inspect (e.g. ``import mypackage; get_exec_commands_for_package(mypackage)``).

    Returns
    -------
    str
        Newline-separated ``from <module> import <Class>, ...`` statements.
    """
    lines = []
    for _, modname, _ in pkgutil.walk_packages(
            path=package.__path__,
            prefix=package.__name__ + '.',
            onerror=lambda x: None):
        try:
            module = importlib.import_module(modname)
            names = [name for name, obj in inspect.getmembers(module, inspect.isclass)
                     if obj.__module__ == modname]
            if names:
                lines.append("from {} import {}".format(modname, ", ".join(names)))
        except Exception:
            pass
    return "\n".join(lines)

def load_from_json_file(file_name, exec_commands=None):
    """
    Function to load a syned object from a json file.

    Parameters
    ----------
    file_name : str
        The file name.
    exec_commands : str
        The commands (typically import...) to be executed before accessing the file.

    Returns
    -------
    instance of SynedObject

    """
    if exec_commands is None:
        exec_commands = get_exec_commands_for_package(syned)
    else:
        exec_commands = exec_commands + "\n" + get_exec_commands_for_package(syned)

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
    if exec_commands is None:
        exec_commands = get_exec_commands_for_package(syned)
    else:
        exec_commands = exec_commands + "\n" + get_exec_commands_for_package(syned)
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
    if exec_commands is None:
        exec_commands = get_exec_commands_for_package(syned)
    else:
        exec_commands = exec_commands + "\n" + get_exec_commands_for_package(syned)
    return load_from_json_dictionary_recurrent(json_tricks.loads(text), exec_commands=exec_commands)

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
            NOT_FOUND = "--------NOT-FOUND--------"
            for key in tmp1.keys():
                stored_value = jsn.get(key, NOT_FOUND)
                if str(stored_value) != NOT_FOUND:
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


'''if __name__ == "__main__":

    file_url = "https://raw.githubusercontent.com/oasys-esrf-kit/modelling_team_scripts_and_workspaces/refs/heads/main/id20/ESRF_ID20_EBS_CPMU19_2.5m.json"
    syned_obj = load_from_json_url(file_url)
    print(syned_obj.info())



    file_url = "/home/srio/Oasys2/tmp_sy.json"
    syned_obj = load_from_json_file(file_url)
    print(syned_obj.info())'''

