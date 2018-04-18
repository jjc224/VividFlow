class SerializableObject {
    constructor() {
        this._ObjectID = "0.0"
        this.generate_object_id();
        this._Owner = null;
    }

    build_json_dict() {
        var json_dict = {};
        json_dict["ObjectType"] = SerialObjectTypes.get_friendly_name(this);
        json_dict["_ObjectID"] = this._ObjectID;
        return json_dict;
    }

    serialize_json() {
        return JSON.stringify(this.build_json_dict());
    }

    build_json_array(array) {
        var serialized_list = [];
        for ( let item of array) {
            serialized_list.push(item.build_json_dict());
        }
        return serialized_list;
    }

    reconstruct_from_json(jsonObj) {
        for (var prop in jsonObj) {
            if( this.hasOwnProperty(prop)) {
                if(Array.isArray(jsonObj[prop]))
                {
                    var tempArray = new Array();
                    for (var item in jsonObj[prop]) {
                        var newObj = SerialObjectTypes.build_object_from_json(jsonObj[prop][item]);
                        if (newObj != null)
                        {
                            tempArray.push(newObj);
                        }
                    }
                    this[prop] = tempArray;
                }
                else{
                    this[prop] = jsonObj[prop];
                }
            }
            else {
                if(prop == "ObjectType")
                {
                    //safe to ignore this property
                }
                else {
                    console.warn("JSON Reconstructor Warning: property '" + prop + "' does not exist on object of type '" + this.constructor.name + "'");
                }
            }
        }
    }

    get_object_id() {
        return this._ObjectID;
    }

    generate_object_id() {
        this._ObjectID = Math.random().toString();
    }

    set_owner(owner) {
        this._Owner = owner;
    }

    get_owner() {
        return this._Owner;
    }
}
SerialObjectTypes.register_type("SerializableObject", SerializableObject);
