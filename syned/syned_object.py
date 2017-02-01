from collections import OrderedDict
import json

# TODO: although basic functionality is implemented, the use of exec should be replace by introspection tools
class SynedObject(object):

    def _set_support_text(self,text):
        ordered_support_dict = OrderedDict()
        for e in text:
            ordered_support_dict[e[0]] = (e[1], e[2])
        self._support_dictionary = ordered_support_dict


    #
    # this is the common interface to allow json file input/output and info mechanism
    #
    # standard methods are:
    #   keys
    #   to_dictionary
    #   to_json
    #   info
    #   set_value_from_key_name
    #   get_value_from_key_name
    #
    def keys(self):
        try:
            return self._support_dictionary.keys()
        except:
            return None

    def to_dictionary(self):
        dict_to_save = OrderedDict()
        dict_to_save.update({"CLASS_NAME":self.__class__.__name__})
        try:
            for key in self.keys():
                tmp1 = eval("self._%s" % (key) )
                if isinstance(tmp1,SynedObject):
                    dict_to_save[key] = tmp1.to_dictionary()
                else:
                    dict_to_save[key] = tmp1
                    # exec("dict_to_save['%s'] = self._%s" % (key, key))
        except:
            pass

        return dict_to_save

    def to_json(self,file_name=None):
        dict1 = OrderedDict()
        dict1.update(self.to_dictionary())

        jsn1 = json.dumps(dict1, indent=4, separators=(',', ': '))
        if file_name != None:
            f = open(file_name,'w')
            f.write(jsn1)
            f.close()
            print("File written to disk: %s"%(file_name))
        return jsn1

    def info(self):
        text = str(self.__class__.__name__) + "\n"

        try:
            fd = self.to_dictionary()
            for key in self.keys():
                text += '    %s (%s): ' %(key, self._support_dictionary[key][1]) + repr(fd[key]) + "\n"
        except:
            pass

        return text

    def set_value_from_key_name(self,key,value):
        try:
            exec("self._%s = value" % (key))
            # print("Set variable %s to value: "%key + repr(value))
        except:
            raise ValueError("Cannot set variable %s to value: "%key + repr(value) )

    def get_value_from_key_name(self,key):
        try:
            value = eval("self._%s" % (key))
            return value
        except:
            raise ValueError("Cannot get variable %s: "%key)


