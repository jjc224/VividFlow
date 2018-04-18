import datetime
from SettingsLoader import SettingsLoader

# This class tracks all object types that are serializable and allows easy reconstruction
class SerialObjectTypes:
    #Keyed on the text name, contains the type
    Types = {}
    #Types["Unknown"] = [None]


    @staticmethod
    def register_type(friendly_name, type_info):
        if friendly_name is not None and type_info is not None:
            if SerialObjectTypes.Types.has_key(friendly_name):
                print "Duplicate type registering: " + friendly_name + ". Aborting"
                return
            SerialObjectTypes.Types[friendly_name] = [type_info]


    # this function will return the friendly name of an object type
    @staticmethod
    def get_friendly_name(object):
        objType = type(object)
        for key in SerialObjectTypes.Types:
            if SerialObjectTypes.Types[key][0].__name__ is objType.__name__:
                return key
        return "Unknown"


    # this function will return the type of object for a given friendly name
    @staticmethod
    def get_type(friendly_name):
        if SerialObjectTypes.Types.has_key(friendly_name):
            return SerialObjectTypes.Types[friendly_name][0]
        return None


    @staticmethod
    def build_object_from_json(json_object):
        object_type = SerialObjectTypes.get_type(json_object["ObjectType"])
        if object_type is None:
            print "build_object_from_json: Object type not recognized '" + json_object["ObjectType"] + "'"
            return None
        new_object = object_type()
        new_object.reconstruct_from_json(json_object)
        return new_object


class ModuleStates:
    InDevelopment = "InDevelopment"
    Published = "Published"
    Retired = "Retired"


# TODO: verify socket data types are supported when setting a socket data type
# This is a rudimentary way of specifying an enum in python 2.7
class SocketDataType:
    UnsupportedDataType = "UnsupportedDataType"
    AnyDataType = "AnyDataType"
    String = "String"
    Integer = "Integer"
    Float = "Float"
    Image = "Image"
    Video = "Video"
    Text = "Text"

    @staticmethod
    def get_type_extension(data_type):
        if data_type == SocketDataType.UnsupportedDataType:
            return ".vfunsupported"
        if data_type == SocketDataType.AnyDataType:
            return ".vfany"
        if data_type == SocketDataType.String:
            return ".vfstring"
        if data_type == SocketDataType.Integer:
            return ".vfint"
        if data_type == SocketDataType.Float:
            return ".vffloat"
        if data_type == SocketDataType.Image:
            return ".png"
        if data_type == SocketDataType.Video:
            return ".avi"
        if data_type == SocketDataType.Text:
            return ".vftxt"
        return ".vfunsupported"


class ScheduledTaskStatus:
    Pending = "Pending"
    InProgress = "InProgress"
    Completed = "Completed"


class DateTimeUtils:
    format_string = "%d/%m/%Y %H:%M:%S"
    @staticmethod
    def to_string(in_date):
        if in_date is None:
            return ""
        return in_date.strftime(DateTimeUtils.format_string)

    @staticmethod
    def from_string(in_string):
        if in_string is None or in_string == "":
            return None
        return datetime.datetime.strptime(in_string, DateTimeUtils.format_string)


Settings = SettingsLoader.load_settings()
SettingsLoader.save_settings("debugging-output-config.json", Settings)
