import Constants
from Constants import SocketDataType
from SerializableObject import SerializableObject


class NodeIOSocket(SerializableObject):
    _ArgumentNumber = 0
    _Name = "Undefined"
    _DataType = SocketDataType.UnsupportedDataType
    _OwnerNode = None
    _OwnerNodeId = 0
    _AssociatedLinks = []
    _Required = False

    def __init__(self, argument_number = 0, name = "", data_type = SocketDataType.UnsupportedDataType, owner = None):
        super(NodeIOSocket, self).__init__()
        self._ArgumentNumber = argument_number
        self._Name = name
        self._DataType = data_type
        self._OwnerNode = owner
        if owner is not None:
            self._OwnerNodeId = owner.get_object_id()
        self._AssociatedLinks = []

    def build_json_dict(self):
        json_dict = super(NodeIOSocket, self).build_json_dict()
        json_dict["_ArgumentNumber"] = self._ArgumentNumber
        json_dict["_Name"] = self._Name
        json_dict["_DataType"] = self._DataType
        json_dict["_OwnerNodeId"] = self._OwnerNodeId;
        json_dict["_Required"] = self._Required
        return json_dict

    def get_argument_number(self):
        return self._ArgumentNumber

    def get_name(self):
        return self._Name

    def get_type(self):
        return self._DataType

    def get_owner(self):
        return self._OwnerNode

    def get_num_links(self):
        return len(self._AssociatedLinks)

    def get_link(self, index):
        if index < self.get_num_links():
            return self._AssociatedLinks[index]
        return None

    def associate_link(self, link):
        if link not in self._AssociatedLinks:
            self._AssociatedLinks.append(link)
            return True
        return False

    def disassociate_link(self, link):
        if link in self._AssociatedLinks:
            self._AssociatedLinks.remove(link)
            return True
        return False

    def possess(self, owning_node):
        if owning_node is None:
            print "Socket Possesion Error: owning node is none"
            return False
        if owning_node.get_object_id() != self._OwnerNodeId:
            print "Warning: owning node ID is not the same"
            return False

        self._OwnerNode = owning_node
        return True

    def destroy_socket(self):
        for link in self._AssociatedLinks:
            link.destroy_link()
        assert len(self._AssociatedLinks) == 0
Constants.SerialObjectTypes.register_type("NodeIOSocket", NodeIOSocket)
