// These classes are created this way due to how static functions and variables are handled in javascript
///////////////////////////
// SerialObjectTypes class
///////////////////////////
class SerialObjectTypes {};
SerialObjectTypes.Types = {};
SerialObjectTypes.register_type = function (name, classref) {
    SerialObjectTypes.Types[name] = classref;
};
SerialObjectTypes.get_class = function(name) {
    return SerialObjectTypes.Types[name];
};
SerialObjectTypes.get_friendly_name = function(obj) {
    for (var prop in SerialObjectTypes.Types) {
        if(prop == obj.constructor.name) {
            return prop;
        }
    }
    console.warn("The object type " + obj.constructor.name + " is not recognized as a serializable type");
    return "Unknown";
};
SerialObjectTypes.build_object_from_json = function(jsonObj) {
    var objType = SerialObjectTypes.get_class(jsonObj.ObjectType);
    if (objType == undefined) {
        console.warn("build_object_from_json: Object type not recognized '" + jsonObj["ObjectType"] + "'");
        console.log(jsonObj);
        return null;
    }
    var newObj = new objType();
    newObj.reconstruct_from_json(jsonObj);
    return newObj;
};

///////////////////////////
// Module States class
///////////////////////////
class ModuleStates {};
ModuleStates.InDevelopment = "InDevelopment";
ModuleStates.Published = "Published";
ModuleStates.Retired = "Retired";

///////////////////////////
// SocketDataTypes class
///////////////////////////
class SocketDataTypes {};
SocketDataTypes.UnsupportedDataType = "UnsupportedDataType";
SocketDataTypes.AnyDataType = "AnyDataType";
SocketDataTypes.String = "String";
SocketDataTypes.Integer = "Integer";
SocketDataTypes.Float = "Float";
SocketDataTypes.Image = "Image";
SocketDataTypes.Video = "Video";
SocketDataTypes.Text = "Text";
SocketDataTypes.get_list = function() {
    list = [];
    for (var prop in this) {
        if(this[prop] == this.UnsupportedDataType) {
            continue;
        }
        if (typeof this[prop] != 'function') {
            list.push(this[prop])
        }
    }
    return list;
}
