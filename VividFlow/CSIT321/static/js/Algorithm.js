
class Algorithm extends SerializableObject {
    constructor(jsonObj) {
        //call first
        super();

        this._AlgorithmName = "UntitledAlgorithm";
        this._Links = new Array();
        this._Nodes = new Array();
        this._AlgorithmID = null;
        this._UserID = null;
    }

    build_json_dict() {
        var json_dict = super.build_json_dict();
        json_dict["_AlgorithmName"] = this._AlgorithmName;
        json_dict["_Links"] = this.build_json_array(this._Links);
        json_dict["_Nodes"] = this.build_json_array(this._Nodes);
        json_dict["_AlgorithmID"] = this._AlgorithmID;
        json_dict["_UserID"] = this._UserID;
        return json_dict;
    }

    set_algorithm_name(new_name) {
        this._AlgorithmName = new_name;
    }

    get_algorithm_name() {
        return this._AlgorithmName;
    }

    relink_algorithm() {
        for (let node of this._Nodes) {
            node.relink_sockets(this);
            node.set_owner(this);
        }
        for (let link of this._Links) {
            link.relink_sockets(this);
            link.set_owner(this);
        }
    }

    get_node_by_id(node_id) {
        for( let node of this._Nodes) {
            if(node.get_object_id() == node_id) {
                return node;
            }
        }
        return null;
    }

    add_link(out_socket, in_socket) {
        var new_link = new Link;
        if (this.is_link_duplicate(out_socket, in_socket)) {
            return false;
        }
        if (new_link.create_link(out_socket, in_socket)) {
            new_link.set_owner(this);
            this._Links.push(new_link);
            return new_link;
        }
        return false;
    }

    is_link_duplicate(out_socket, in_socket) {
        if (out_socket == null || in_socket == null) {
            console.log("Add Link: Cannot create new Link, a socket in the link is empty!");
            return true;
        }
        for (let link of this._Links) {
            if (link.get_in_socket() == in_socket && link.get_out_socket() == out_socket) {
                console.log("Add Link: Cannot create new Link, duplicate Link already exists!");
                return true;
            }
        }
        return false;
    }

    destroy_node(node) {
        for (var i = 0; i < this._Nodes.length; i++) {
            if (this._Nodes[i] == node) {
                this._Nodes[i].destroy_node();
                this._Nodes.splice(i, 1);
            }
        }
    }

    destroy_link(link) {
        for (var i = 0; i < this._Links.length; i++) {
            if (this._Links[i] == link) {
                link.unlink_sockets();
                this._Links.splice(i, 1);
            }
        }
    }

    add_node(new_node) {
        if(new_node == null) {
            console.warn("Tried to add a null node to algorithm");
            return false;
        }
        this._Nodes.push(new_node);
        console.log("Added new node");
        return true;
    }
}
SerialObjectTypes.register_type("Algorithm", Algorithm);

class NodeIOSocket extends SerializableObject    {
    constructor(jsonObj) {
        //call first
        super();

        this._DataType = "Undefined";
        this._Name = "";
        this._Required = false;
        this._ArgumentNumber = -1;
        this._OwnerNodeId = -1;
        this._AssociatedLinks = [];
        this._Owner = null;
        this._drawable = null;
    }

    build_json_dict() {
        var json_dict = super.build_json_dict();
        json_dict["_ArgumentNumber"] = this._ArgumentNumber;
        json_dict["_Name"] = this._Name;
        json_dict["_DataType"] = this._DataType;
        json_dict["_OwnerNodeId"] = this._OwnerNodeId;
        json_dict["_Required"] = this._Required;
        return json_dict;
    }

    set_owner(owning_node)
    {
        if (owning_node == null) {
            console.log("Socket Possesion Error: owning node is none");
            return false;
        }
        if(owning_node.get_object_id() != this._OwnerNodeId) {
            console.log("Warning: owning node ID is not the same");
            return false;
        }

        this._Owner = owning_node;
        return true;
    }

    associate_link(new_link) {
        for(let existing_link of this._AssociatedLinks) {
            if(existing_link == new_link) {
                return false;
            }
        }
        this._AssociatedLinks.push(new_link);
    }

    set_argument_number(num) {
        this._ArgumentNumber = num;
    }

    get_drawable() {
        return this._drawable;
    }

    set_drawable(obj) {
        this._drawable = obj;
    }

    get_owner_id() {
        return this._OwnerNodeId;
    }

    get_data_type() {
        return this._DataType;
    }

    get_socket_io_type() {
        if (this._Owner.get_input_socket_by_id(this.get_object_id())) {
            return "input";
        }
        return "output";
    }

    disassociate_link(link) {
        for (var i = 0; i < this._AssociatedLinks.length; i++) {
            if (this._AssociatedLinks[i] == link) {
                this._AssociatedLinks.splice(i, 1);
            }
        }
    }

    destroy_socket() {
        console.log(this._AssociatedLinks);
        for (var i = 0; i < this._AssociatedLinks.length; i++) {
            var parent_algo = this._AssociatedLinks[i].get_owner();
            if (parent_algo == null) {
                console.log("Socket has no owner");
            }
            console.log(this._AssociatedLinks[i]);
            parent_algo.destroy_link(this._AssociatedLinks[i]);
            i--;
        }
        console.log(this._AssociatedLinks);
    }
}
SerialObjectTypes.register_type("NodeIOSocket", NodeIOSocket);

class Node extends SerializableObject {
    constructor(jsonObj) {
        //call last
        super(jsonObj);

        this._InputSockets = new Array();
        this._OutputSockets = new Array();
        this._PosX = 0;
        this._PosY = 0;
        this._Name = "UntitledNode"
    }

    get_display_name() {
        return this._Name;
    }

    set_name(new_name) {
        this._Name = new_name;
    }

    build_json_dict() {
        var json_dict = super.build_json_dict();
        json_dict["_Name"] = this._Name;
        json_dict["_PosX"] = this._PosX;
        json_dict["_PosY"] = this._PosY;
        json_dict["_InputSockets"] = this.build_json_array(this._InputSockets);
        json_dict["_OutputSockets"] = this.build_json_array(this._OutputSockets);
        return json_dict;
    }

    relink_sockets() {
        for (let socket of this._InputSockets) {
            socket.set_owner(this);
        }
        for (let socket of this._OutputSockets) {
            socket.set_owner(this);
        }
    }

    get_input_socket_by_id(socket_id) {
        for (let socket of this._InputSockets) {
            if(socket.get_object_id() == socket_id) {
                return socket;
            }
        }
        return null;
    }

    get_output_socket_by_id(socket_id) {
        for (let socket of this._OutputSockets) {
            if(socket.get_object_id() == socket_id) {
                return socket;
            }
        }
        return null;
    }

    get_x() {
        return this._PosX;
    }

    get_y() {
        return this._PosY;
    }

    destroy_node() {
        for (var i = 0; i < this._InputSockets.length; i++) {
            this._InputSockets[i].destroy_socket();
        }
        for (var i = 0; i < this._OutputSockets.length; i++) {
            this._OutputSockets[i].destroy_socket();
        }
        this._InputSockets = null;
        this._OutputSockets = null;
    }

}
SerialObjectTypes.register_type("Node", Node);

class DataNode extends Node {
    constructor(jsonObj) {
        //call last
        super(jsonObj);
    }
}
SerialObjectTypes.register_type("DataNode", DataNode);

class ValueNode extends DataNode {
    constructor(jsonObj) {
        //call last
        super(jsonObj);

        this._DataType = "";
        this._Value = "";
    }

    build_json_dict() {
        var json_dict = super.build_json_dict();
        json_dict["_DataType"] = this._DataType;
        json_dict["_Value"] = this._Value;
        return json_dict;
    }

    set_value_type(new_type) {
        this._DataType = new_type;
        // Update socket if it exists
        if (this._OutputSockets.length > 0) {
            this._OutputSockets[0]._DataType = new_type;
            this._OutputSockets[0]._Name = new_type + " Value";
        }
    }

    set_value(new_value) {
        this._Value = new_value;
    }

    get_value() {
        return this._Value;
    }

    get_value_type() {
        return this._DataType;
    }

    add_socket() {
        var sock = new NodeIOSocket();
        sock._DataType = this._DataType;
        sock._Name = this._DataType + " Value";
        sock._Required = false;
        sock._ArgumentNumber = 1;
        sock._OwnerNodeId = this.get_object_id();
        sock._AssociatedLinks = [];
        sock._Owner = this;
        this._OutputSockets.push(sock);
    }
}
SerialObjectTypes.register_type("ValueNode", ValueNode);

class ModuleNode extends Node {
    constructor(jsonObj) {
        //call last
        super(jsonObj);

        //# the unique id version of this module
        this._ModuleVersionId = null;
        //# the id of the owner of this module
        this._ModuleUserId = null;
        //# the user friendly version number of this module
        this._ModuleVersion = 1;
        //# the unique id for this series of modules. Lines up with the ModuleVersionId of the initial version
        this._ModuleId = null;
        //# the status of the module
        this._ModuleVersionState = ModuleStates.InDevelopment;
        this._UserID = null;
    }

    mark_as_new_version() {
        let bShouldMarkAsNewVersion = true;
        if(this._ModuleVersionId == null) {
            bShouldMarkAsNewVersion = false;
        }
        if(this._ModuleVersionState == ModuleStates.Retired) {
            bShouldMarkAsNewVersion = false;
        }
        if(this._ModuleVersionState == ModuleStates.InDevelopment) {
            bShouldMarkAsNewVersion = false;
        }
        if (bShouldMarkAsNewVersion) {
                this._ModuleVersionId = null;
                this._ModuleVersion += 1;
                this._ModuleVersionState = ModuleStates.InDevelopment;
                console.log("Module marked as new version");
                return true;
        }
        return false;
    }

    mark_as_modified() {
        if (this._ModuleVersionState == ModuleStates.Published) {
            return this.mark_as_new_version();
        }
        else if (this._ModuleVersionState == ModuleStates.Retired) {
            return false;
        }
        return false;
    }

    get_id() {
        return this._ModuleId;
    }

    publish() {
        if(this.get_state() != ModuleStates.InDevelopment) {
            console.warn("Cannot publish a module that is not currently in state InDevelopment");
            return;
        }

        this._ModuleVersionState = ModuleStates.Published;
    }

    //uses a trick of the serialisation system to create a deep copy of the node, and then clear all link associations and generate new object ids
    create_node_instance() {
        let serialized_node = this.serialize_json();
        let new_node = SerialObjectTypes.build_object_from_json(JSON.parse(serialized_node));
        new_node.generate_object_id();
        for ( let insock of new_node._InputSockets) {
            insock.generate_object_id();
            insock._OwnerNodeId = new_node._ObjectID;
        }
        for ( let outsock of new_node._OutputSockets) {
            outsock.generate_object_id();
            outsock._OwnerNodeId = new_node._ObjectID;
        }
        return new_node;
    }

    get_version() {
        return this._ModuleVersion;
    }

    get_state() {
        return this._ModuleVersionState;
    }

    get_module_version_id() {
        return this._ModuleVersionId;
    }

    get_user_id() {
        return this._ModuleUserId;
    }

    build_json_dict() {
        var json_dict = super.build_json_dict();
        json_dict["_ModuleVersionId"] = this._ModuleVersionId;
        json_dict["_ModuleVersion"] = this._ModuleVersion;
        json_dict["_ModuleId"] = this._ModuleId;
        json_dict["_ModuleUserId"] = this._ModuleUserId;
        json_dict["_ModuleVersionState"] = this._ModuleVersionState;
        var inputSocketsList = [];
        for ( let insock of this._InputSockets) {
            inputSocketsList.push(insock.build_json_dict());
        }
        var outputSocketsList = [];
        for ( let outsock of this._OutputSockets) {
            outputSocketsList.push(outsock.build_json_dict());
        }
        json_dict["_InputSockets"] = inputSocketsList;
        json_dict["_OutputSockets"] = outputSocketsList;
        json_dict["_UserID"] = this._UserID;
        return json_dict;
    }
}
SerialObjectTypes.register_type("ModuleNode", ModuleNode);

class OutputNode extends DataNode {
    constructor(jsonObj) {
        //call last
        super(jsonObj);
        //The type of data that will be stored in this output
        this._OutputType = SocketDataTypes.UnsupportedDataType
    }

    build_json_dict() {
        var json_dict = super.build_json_dict();
        json_dict["_OutputType"] = this._OutputType;
        return json_dict;
    }

    set_output_type(new_type) {
        this._OutputType = new_type;
        // Update socket if it exists
        if (this._InputSockets.length > 0) {
            this._InputSockets[0]._DataType = new_type;
            this._InputSockets[0]._Name = new_type + " Value";
        }
    }

    get_output_type() {
        return this._OutputType;
    }

    add_socket() {
        var sock = new NodeIOSocket();
        sock._DataType = this._OutputType;
        sock._Name = this._OutputType + " Value";
        sock._Required = false;
        sock._ArgumentNumber = 1;
        sock._OwnerNodeId = this.get_object_id();
        sock._AssociatedLinks = [];
        sock._Owner = this;
        this._InputSockets.push(sock);
    }
}
SerialObjectTypes.register_type("OutputNode", OutputNode);

class ResourceNode extends DataNode {
    constructor(jsonObj) {
        //call last
        super(jsonObj);
        // //The type of data that will be stored in this output
        this._ResourceType = SocketDataTypes.UnsupportedDataType;
        this._ResourceID = -1;
    }

    build_json_dict() {
        var json_dict = super.build_json_dict();
        json_dict["_ResourceType"] = this._ResourceType;
        json_dict["_ResourceID"] = this._ResourceID;
        return json_dict;
    }

    set_resource_type(new_type) {
        this._ResourceType = new_type;
    }

    set_resource(new_id, new_name, new_type) {
        this._ResourceID = new_id;
        this.set_name(new_name);
        this.set_resource_type(new_type);
    }

    add_socket() {
        var sock = new NodeIOSocket();
        sock._DataType = SocketDataTypes.AnyDataType;
        sock._Name = "File";
        sock._Required = false;
        sock._ArgumentNumber = 1;
        sock._OwnerNodeId = this.get_object_id();
        sock._AssociatedLinks = [];
        sock._Owner = this;
        this._OutputSockets.push(sock);
    }
}
SerialObjectTypes.register_type("ResourceNode", ResourceNode);


class StringTestNode extends ModuleNode {
    constructor(jsonObj) {
        //call last
        super(jsonObj);

        this._Node_Name = "";
    }

    build_json_dict() {
        var json_dict = super.build_json_dict();
        json_dict["_Node_Name"] = this._Node_Name;
        return json_dict;
    }

    get_display_name() {
        return this._Node_Name;
    }
}
SerialObjectTypes.register_type("StringTestNode", StringTestNode);

class Link extends SerializableObject {
    constructor(jsonObj) {
        //call last
        super(jsonObj);

        this._In_Socket = null;
        this._Out_Socket = null;
        this._In_Node_Id = -1;
        this._In_Socket_Id = -1;
        this._Out_Node_Id = -1;
        this._Out_Socket_Id = -1;
    }

    build_json_dict() {
        var json_dict = super.build_json_dict();
        json_dict["_In_Node_Id"] = this._In_Node_Id;
        json_dict["_In_Socket_Id"] = this._In_Socket_Id;
        json_dict["_Out_Node_Id"] = this._Out_Node_Id;
        json_dict["_Out_Socket_Id"] = this._Out_Socket_Id;
        return json_dict;
    }

    relink_sockets(algorithm) {
        if(algorithm == null) {
            console.error("LinkReassociation: Algorithm is null. cannot relink sockets");
            return false;
        }

        let in_node = algorithm.get_node_by_id(this._In_Node_Id);
        if(in_node == null) {
            console.error("LinkReassociation: could not find in-node by id");
            return false;
        }

        let out_node = algorithm.get_node_by_id(this._Out_Node_Id);
        if(out_node == null) {
            console.error("LinkReassociation: could not find out-node by id");
            return false;
        }
        let in_socket = in_node.get_input_socket_by_id(this._In_Socket_Id);
        if(in_socket == null) {
            console.error("LinkReassociation: could not find in-socket by id");
            return false;
        }

        let out_socket = out_node.get_output_socket_by_id(this._Out_Socket_Id);
        if(out_socket == null) {
            console.error("LinkReassociation: could not find out-socket by id");
            return false;
        }

        this._In_Socket = in_socket;
        this._Out_Socket = out_socket;
        this._Out_Socket.associate_link(this);
        this._In_Socket.associate_link(this);
    }

    create_link(out_socket, in_socket) {
        // Check out_socket is not empty
        if (in_socket == null) {
            console.log("Link: Cannot create link, input socket missing!");
            return false;
        }

        // Check out_socket is not empty
        if (out_socket == null) {
            console.log("Link: Cannot create link, output socket missing!");
            return false;
        }

        // Check sockets are not the same
        if (in_socket == out_socket) {
            console.log("Link: Cannot create link, both sockets are the same!");
            return false;
        }

        // Check Sockets are compatible
        if (out_socket.get_data_type() != in_socket.get_data_type()) {
            if (out_socket.get_data_type() == "AnyDataType" || in_socket.get_data_type() == "AnyDataType") {
                console.log("AnyDataType");
            } else {
                console.log("Link: Cannot create link, socket data types different!");
                return false;
            }
        }

        // Check sockets are not the same io type
        console.log(out_socket.get_socket_io_type(), in_socket.get_socket_io_type());
        if (out_socket.get_socket_io_type() == in_socket.get_socket_io_type()) {
            console.log("Link: Cannot create link, socket io types are the same!");
            return false;
        }

        this._Out_Socket = out_socket;
        this._Out_Node_Id = out_socket.get_owner_id();
        this._Out_Socket_Id = out_socket.get_object_id();
        this._In_Socket = in_socket;
        this._In_Node_Id = in_socket.get_owner_id();
        this._In_Socket_Id = in_socket.get_object_id();
        this._Out_Socket.associate_link(this);
        this._In_Socket.associate_link(this);
        return true;
    }

    get_in_socket() {
        return this._In_Socket;
    }

    get_out_socket() {
        return this._Out_Socket;
    }

    unlink_sockets() {
        if (this._In_Socket != null)
            this._In_Socket.disassociate_link(this);
        if (this._Out_Socket != null)
            this._Out_Socket.disassociate_link(this);
        this._Out_Socket = null;
        this._In_Socket = null;
    }

    destroy_link() {
        // Destroy from algorithm
        this._Owner.destroy_link(this);
    }

}
SerialObjectTypes.register_type("Link", Link);
