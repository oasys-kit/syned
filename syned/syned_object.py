from collections import OrderedDict
import json

# TODO: although basic functionality is implemented, the use of exec should be replace by introspection tools
class SynedObject(object):

    def _set_support_text(self,text):
        ordered_support_dict = OrderedDict()
        for e in text:
            ordered_support_dict[e[0]] = (e[1], e[2])
        self._support_dictionary = ordered_support_dict


    def keys(self):
        return self._support_dictionary.keys()

    def to_dictionary(self):
        dict_to_save = OrderedDict()
        for key in self.keys():
            exec("dict_to_save['%s'] = self._%s" % (key, key))
        return dict_to_save

    def info(self):
        fd = self.to_dictionary()
        text = str(self.__class__.__name__) + "\n"
        for key in self.keys():
            text += '    %s (%s): %f \n' %(key, self._support_dictionary[key][1],fd[key])
        return text

    def set_value_from_key_name(self,key,value):
        try:
            exec("self._%s = value" % (key))
            print("Set variable %s to value: "%key + repr(value))
        except:
            raise ValueError("Cannot set variable %s to value: "%key + repr(value) )

    def get_value_from_key_name(self,key):
        try:
            value = 0
            exec("value = self._%s" % (key))
            return value
        except:
            raise ValueError("Cannot get variable %s: "%key)

    def dump_json(self,file_name=None):
        dict1 = OrderedDict()
        dict1.update({"ELEMENT_TYPE":self.__class__.__name__})
        dict1.update(self.to_dictionary())

        jsn1 = json.dumps(dict1, indent=4, separators=(',', ': '))
        if file_name != None:
            f = open(file_name,'w')
            f.write(jsn1)
            f.close()
            print("File written to disk: %s"%(file_name))
        print(jsn1 )
        return jsn1
