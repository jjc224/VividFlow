import json
import Constants
import inspect
import random

class SerializableObject(object):
    _ObjectID = None

    def __init__(self):
        self.generate_object_id()

    def build_json_dict(self):
        json_dict = {}
        json_dict["ObjectType"] = Constants.SerialObjectTypes.get_friendly_name(self)
        json_dict["_ObjectID"] = self._ObjectID
        return json_dict

    def get_object_id(self):
        return self._ObjectID

    def generate_object_id(self):
        self._ObjectID = str(random.random())

    def serialize_json(self):
        json_dict = self.build_json_dict()
        json_str = json.dumps(json_dict)
        return json_str

    def build_json_array(self, array):
        serialized_list = []
        for item in array:
            serialized_list.append(item.build_json_dict())
        return serialized_list

    def __get_member_variables(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        members = [a[0] for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
        return members

    def reconstruct_from_json(self, json_obj):
        attributes = self.__get_member_variables()
        for key in json_obj:
            if key in attributes:
                if isinstance(json_obj[key], list):
                    tempList = []
                    for item in json_obj[key]:
                        new_obj = Constants.SerialObjectTypes.build_object_from_json(item)
                        if new_obj is not None:
                            tempList.append(new_obj)
                    self.__setattr__(key, tempList)
                else:
                    self.__setattr__(key, json_obj[key])
            else:
                if key == "ObjectType":
                    # safe to ignore this property
                    pass
                else:
                    print "JSON Reconstructor Warning: property '" + key + "' does not exist on object of type '" + type(self).__name__ + "'"
        pass

Constants.SerialObjectTypes.register_type("SerializableObject", SerializableObject)
