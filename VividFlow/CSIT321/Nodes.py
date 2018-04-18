# TODO: write destructors for NodeIOSocket, Node, Link
# TODO: check bounds on getters
# TODO: add checks to ensure that all required sockets have links
# TODO: Ensure no input sockets get multiple incoming links when creating links
# TODO: Split into multiple files
# DONE: Create a base data node that ValueNode will inherit from. Also ResourceNode will inherit from
# DONE: DataNode is the base for any non-processing node.
# TODO: Possibly create Node type for processing type nodes
# TODO: Handle properly retrieving output filenames based off output nodes
# TODO: Revisit end node identification in the presence of output nodes
# TODO: Write out value nodes
import Constants
import Sockets
from Constants import SocketDataType
from SerializableObject import SerializableObject
import dbconn
import os

class Node(SerializableObject):
    _InputSockets = None
    _OutputSockets = None
    _PosX = 0
    _PosY = 0
    _Name = None

    def __init__(self):
        super(Node, self).__init__()
        self._InputSockets = []
        self._OutputSockets = []
        self._PosX = 0
        self._PosY = 0
        self._Name = "UntitledNode"

    def get_x(self):
        return self._PosX

    def get_y(self):
        return self._PosY

    def set_y(self, new_y):
        self._PosY = new_y

    def set_x(self, new_x):
        self._PosX = new_x

    def get_name(self):
        return self._Name

    def build_json_dict(self):
        json_dict = super(Node, self).build_json_dict()
        json_dict["_Name"] = self._Name
        json_dict["_PosX"] = self._PosX
        json_dict["_PosY"] = self._PosY
        json_dict["_InputSockets"] = self.build_json_array(self._InputSockets)
        json_dict["_OutputSockets"] = self.build_json_array(self._OutputSockets)
        return json_dict

    def add_input_socket(self, new_socket):
        if new_socket is not None:
            self._InputSockets.append(new_socket)
            return True
        return False

    def is_end_node(self):
        # end_node = True
        # for socket in self._OutputSockets:
        #     if socket.get_num_links() > 0:
        #         end_node = False
        # return end_node
        return False

    def add_output_socket(self, new_socket):
        if new_socket is not None:
            self._OutputSockets.append(new_socket)
            return True
        return False

    def get_num_input_sockets(self):
        return len(self._InputSockets)

    def get_input_socket_by_id(self, id):
        for insocket in self._InputSockets:
            if insocket.get_object_id() == id:
                return insocket
        return None

    def get_output_socket_by_id(self, id):
        for outsocket in self._OutputSockets:
            if outsocket.get_object_id() == id:
                return outsocket
        return None

    def get_input_socket_by_index(self, index):
        if self._InputSockets is not None:
            if index < len(self._InputSockets):
                return self._InputSockets[index]
        return None

    def get_num_output_sockets(self):
        return len(self._OutputSockets)

    def get_output_socket_by_index(self, index):
        if self._OutputSockets is not None:
            if index < len(self._OutputSockets):
                return self._OutputSockets[index]
        return None

    def relink_sockets(self, algorithm):
        for socket in self._InputSockets:
            socket.possess(self)
        for socket in self._OutputSockets:
            socket.possess(self)

    def destroy_node(self):
        for link in self._InputSockets:
            link.destroy_socket()
        for link in self._OutputSockets:
            link.destroy_socket()

        assert len(self._InputSockets) == 0
        assert len(self._OutputSockets) == 0
Constants.SerialObjectTypes.register_type("Node", Node)


# This node type is the base class for any non-processing node
class DataNode(Node):
    pass
Constants.SerialObjectTypes.register_type("DataNode", DataNode)


# Value nodes store a string value only. This can be interpreted by the module node as String, Int or Float
class ValueNode(DataNode):
    _Value = ""
    _DataType = Sockets.SocketDataType.AnyDataType

    def build_json_dict(self):
        json_dict = super(ValueNode, self).build_json_dict()
        json_dict["_Value"] = self._Value
        json_dict["_DataType"] = self._DataType
        return json_dict

    def write_value_to_file(self, filename):
        f = open(filename, 'w')
        f.write(self._Value)
        f.close()

    def __init__(self, value = 0, data_type = Sockets.SocketDataType.UnsupportedDataType):
        super(ValueNode, self).__init__()
        self._Value = value
        new_socket = Sockets.NodeIOSocket(0, "Output", data_type, self)
        self._DataType = data_type
        self.add_input_socket(new_socket)

    def get_value(self):
        return self._Value

    def set_value(self, value):
        self._Value = value
Constants.SerialObjectTypes.register_type("ValueNode", ValueNode)

class OutputNode(DataNode):
    # The type of data that will be stored in this output
    _OutputType = SocketDataType.UnsupportedDataType

    def __init__(self):
        super(OutputNode, self).__init__()
        new_socket = Sockets.NodeIOSocket(1, "Input", Sockets.SocketDataType.AnyDataType, self)
        self.add_input_socket(new_socket)

    def build_json_dict(self):
        json_dict = super(OutputNode, self).build_json_dict()
        json_dict["_OutputType"] = self._OutputType
        return json_dict

    def is_end_node(self):
        return True
Constants.SerialObjectTypes.register_type("OutputNode", OutputNode)

class ResourceNode(DataNode):
    # The type of data that will be stored in this output
    _ResourceType = SocketDataType.UnsupportedDataType
    _ResourceID = -1

    def __init__(self):
        super(ResourceNode, self).__init__()
        new_socket = Sockets.NodeIOSocket(1, "Output", Sockets.SocketDataType.AnyDataType, self)
        self.add_input_socket(new_socket)

    def build_json_dict(self):
        json_dict = super(ResourceNode, self).build_json_dict()
        json_dict["_ResourceType"] = self._ResourceType
        json_dict["_ResourceID"] = self._ResourceID
        return json_dict

    def is_end_node(self):
        return False

    def get_file_path(self):
        record = dbconn.db.get_resource_by_id(self._ResourceID)
        if record is None:
            return ""
        path = os.path.join(Constants.Settings["resources"]["path_abs"], str(record["id"]), record["filename"])
        return path

Constants.SerialObjectTypes.register_type("ResourceNode", ResourceNode)
