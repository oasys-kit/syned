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
    #   to_full_dictionary
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
        except:
            pass

        return dict_to_save

    def to_full_dictionary(self):
        dict_to_save = OrderedDict()
        dict_to_save.update({"CLASS_NAME":self.__class__.__name__})
        try:
            for key in self.keys():
                tmp1 = eval("self._%s" % (key) )
                if isinstance(tmp1,SynedObject):
                    dict_to_save[key] = tmp1.to_full_dictionary()
                else:
                    mylist = []
                    mylist.append(tmp1)
                    mylist.append(self._support_dictionary[key])
                    dict_to_save[key] = mylist # [tmp1,self._support_dictionary[key]]
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


    def info_recurrent(self,fd,prefix="    "):
        text = ""
        for key in fd.keys():
            if isinstance(fd[key],OrderedDict):
                text += prefix + self.info_recurrent(fd[key])
            elif isinstance(fd[key],str):
                text += prefix + "-------%s---------\n"%fd[key]
            elif isinstance(fd[key],list):
                if isinstance(fd[key][0],OrderedDict):
                    for element in fd[key]:
                        text += self.info_recurrent(element,prefix="    ")
                elif isinstance(fd[key][0],list):
                    for i,element in enumerate(fd[key][0]):
                        text += element.info()
                else:
                    text += prefix + '    %s: %s %s # %s\n' %(key,  repr(fd[key][0]), fd[key][1][1], fd[key][1][0])
            else:
                pass
        return text

    def info(self):
        return self.info_recurrent( self.to_full_dictionary() )


    def set_value_from_key_name(self,key,value):
        if key in self.keys():
            try:
                exec("self._%s = value" % (key))
                # print("Set variable %s to value: "%key + repr(value))
            except:
                raise ValueError("Cannot set variable %s to value: "%key + repr(value) )
        else:
            raise ValueError("Key %s not accepted by class %s"%(key,self.__class__.__name__))


    def get_value_from_key_name(self,key):
        try:
            value = eval("self._%s" % (key))
            return value
        except:
            raise ValueError("Cannot get variable %s: "%key)



