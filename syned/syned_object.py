import copy
from collections import OrderedDict
try:
    import json_tricks as json # to save numpy arrays
except:
    import json

# TODO: although basic functionality is implemented, the use of exec should be replace by introspection tools
class SynedObject(object):

    # ---------------------------------------------------------------------------------------------------------
    # This override is necessary to avoid TypeError: cannot pickle '_thread.lock' object while duplicating
    # that occurs while enabling/disabling connectors
    #
    # When an attribute is an object that contains non pickable attributes, we make a shallow copy of it
    # ---------------------------------------------------------------------------------------------------------

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
                try:              setattr(result, k, copy.deepcopy(v, memodict))
                except TypeError: setattr(result, k, copy.copy(v))
        return result

    """
    This is the base object for SYNED.

    It includes the methods of the common interface to allow json file input/output and info mechanism

    These standard methods are:
        * keys()
        * to_dictionary()
        * to_full_dictionary()
        * to_json()
        * info()
        * set_value_from_key_name()
        * get_value_from_key_name()

    """

    def _set_support_text(self, text):
        ordered_support_dict = OrderedDict()
        for e in text:
            ordered_support_dict[e[0]] = (e[1], e[2])
        self._support_dictionary = ordered_support_dict

    def _add_support_text(self, text):
        try:
            for e in text:
                self._support_dictionary[e[0]] = (e[1], e[2])
        except:
            self._set_support_text(text)

    #
    # this is the common interface to allow json file input/output and info mechanism
    #
    # standard methods are:
    #   keys
    #   to_dictionary
    #   to_full_dictionary
    #   to_json
    #   info
    #   set_value_from_key_name
    #   get_value_from_key_name
    #
    def keys(self):
        """
        Returns the keys of the supporting doctionary.
        Returns
        -------
        list
            A list of keys.

        """
        try:
            return self._support_dictionary.keys()
        except:
            return None

    def to_dictionary(self):
        """
        Returns a dictionary with the object fields.

        Some dictionary keys may contain SYNED instances. Use to_full_dictionary to recurrently expand these objects
        in their basic ingredients.

        Returns
        -------
        dict
            A dictionary with the data.

        """
        dict_to_save = OrderedDict()
        dict_to_save.update({"CLASS_NAME":self.__class__.__name__})

        try:
            if self.keys() is not None:
                for key in self.keys():
                    tmp1 = eval("self._%s" % (key) )
                    if isinstance(tmp1,SynedObject):
                        dict_to_save[key] = tmp1.to_dictionary()
                    else:
                        dict_to_save[key] = tmp1
        except:
            pass

        return dict_to_save

    def to_full_dictionary(self):
        """
        Returns a dictionary with the object fields, including other syned objects embedded or list of elements.

        The "full" means that the SYNED instances found are recurrently expanded in their basic ingredients.

        Returns
        -------
        dict

        """
        dict_to_save = OrderedDict()
        dict_to_save.update({"CLASS_NAME":self.__class__.__name__})
        try:
            if self.keys() is not None:
                for key in self.keys():
                    tmp1 = eval("self._%s" % (key) )
                    if isinstance(tmp1, SynedObject):
                        dict_to_save[key] = tmp1.to_full_dictionary()
                    else:
                        mylist = []
                        mylist.append(tmp1)
                        mylist.append(self._support_dictionary[key])
                        dict_to_save[key] = mylist # [tmp1,self._support_dictionary[key]]
        except:
            print("** Warning: failed to load/write one or multiple items in ", self.keys())

        return dict_to_save

    def to_json(self, file_name=None):
        """
        Writes a json file with the SYNED object data.

        Parameters
        ----------
        file_name : str
            The file name

        Returns
        -------
        str
            JSON formatted str. The result of json.dumps()

        """
        dict1 = OrderedDict()
        dict1.update(self.to_dictionary())

        jsn1 = json.dumps(dict1, indent=4, separators=(',', ': '))
        if file_name != None:
            f = open(file_name,'w')
            f.write(jsn1)
            f.close()
            print("File written to disk: %s"%(file_name))
        return jsn1

    def info_recurrent(self, fd, prefix="    "):
        """
        Get text info of recurrent SYNED objects.

        Parameters
        ----------
        fd : dict
            The dictionary with SYNED data.
        prefix : str, optional
            Prefix to indent recursive items.

        Returns
        -------
        str

        """
        text = ""
        prefix1 = prefix
        for key in fd.keys():
            if isinstance(fd[key],OrderedDict):
                text += prefix1 + self.info_recurrent(fd[key], prefix=prefix1)
            elif isinstance(fd[key],str):
                text += prefix1 + "-------%s---------\n"%fd[key]
            elif isinstance(fd[key],list):
                if isinstance(fd[key][0],OrderedDict):
                    for element in fd[key]:
                        text += self.info_recurrent(element, prefix=prefix1)
                elif isinstance(fd[key][0],list):
                    for i,element in enumerate(fd[key][0]):
                        try:
                            # text += "****\n"
                            text += prefix1 + element.info()
                        except:
                            text += ("%s%s[%d]: %s\n" %(prefix1, key, i, repr(element))) # used for conic coefficients
                else:
                    text += prefix1 + prefix1 + '%s: %s %s # %s\n' %(key,  repr(fd[key][0]), fd[key][1][1], fd[key][1][0])
            else:
                pass
        return text

    def info(self):
        """
        Get text info of recurrent SYNED objects.

        Returns
        -------
        str

        """
        return self.info_recurrent( self.to_full_dictionary() )

    def set_value_from_key_name(self,key,value):
        """
        Sets a value using its key value.

        Parameters
        ----------
        key : str
            The key for the value to modify.
        value
            The new value

        """
        if key in self.keys():
            try:
                exec("self._%s = value" % (key))
                # print("Set variable %s to value: "%key + repr(value))
            except:
                raise ValueError("Cannot set variable %s to value: "%key + repr(value) )
        else:
            raise ValueError("Key %s not accepted by class %s"%(key,self.__class__.__name__))

    def get_value_from_key_name(self, key):
        """
        Gets a value using its key value.

        Parameters
        ----------
        key : str
            The key for the value to retrieve.

        """
        try:
            value = eval("self._%s" % (key))
            return value
        except:
            raise ValueError("Cannot get variable %s: "%key)

    def duplicate(self):
        """
        Returns a copy of the SYNED object instance.

        Returns
        -------
        SynedObject instance
            A copy of the object instance.

        """
        return copy.deepcopy(self)
