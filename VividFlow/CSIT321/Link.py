import Constants
from SerializableObject import SerializableObject


class Link(SerializableObject):
    # this is the output socket that is fed into an input socket
    _Out_Socket = None
    # this is the input socket that is fed from an output socket
    _In_Socket = None
    _In_Node_Id = -1
    _Out_Node_Id = -1
    _Out_Socket_Id = -1
    _In_Socket_Id = -1

    def __init__(self, out_socket = None, in_socket = None):
        super(Link, self).__init__()
        self.create_link(out_socket, in_socket)

    def build_json_dict(self):
        json_dict = super(Link, self).build_json_dict()
        json_dict["_In_Node_Id"] = self._In_Node_Id
        json_dict["_In_Socket_Id"] = self._In_Socket_Id
        json_dict["_Out_Node_Id"] = self._Out_Node_Id
        json_dict["_Out_Socket_Id"] = self._Out_Socket_Id

        return json_dict

    def get_out_socket_owner(self):
        if self._Out_Socket is not None:
            return self._Out_Socket.get_owner()
        return None

    def get_in_socket_owner(self):
        if self._In_Socket is not None:
            return self._In_Socket.get_owner()
        return None

    def get_out_socket(self):
        if self._Out_Socket is not None:
            return self._Out_Socket
        return None

    def get_in_socket(self):
        if self._In_Socket is not None:
            return self._In_Socket
        return None

    # define as a function incase we need to support sockets that support multiple data types later
    def check_sockets_are_compatible(self, out_socket, in_socket):
        if out_socket.get_type() != in_socket.get_type():
            return False
        return True

    def create_link(self, out_socket, in_socket):
        # cleanup this link if there was a previously configured link
        self.destroy_link()

        # Check that sockets are valid
        if out_socket is None:
            return False
        if in_socket is None:
            return False

        # check that sockets do not refer to each other
        if out_socket.get_owner() is in_socket.get_owner():
            return False

        # check that sockets are compatible
        if not self.check_sockets_are_compatible(out_socket, in_socket):
            return False

        # TODO: ensure there are no cyclic links created
        self._Out_Socket = out_socket
        self._Out_Node_Id = out_socket.get_owner().get_object_id()
        self._Out_Socket_Id = out_socket.get_object_id()
        self._In_Socket = in_socket
        self._In_Node_Id = in_socket.get_owner().get_object_id()
        self._In_Socket_Id = in_socket.get_object_id()
        self._Out_Socket.associate_link(self)
        self._In_Socket.associate_link(self)
        return True

    def relink_sockets(self, algorithm):
        if algorithm is None:
            print "Relink error: algorithm is none"
            return False
        in_node = algorithm.get_node_by_id(self._In_Node_Id)
        if in_node is None:
            print "Relink error: in-node is not found"
            return False

        out_node = algorithm.get_node_by_id(self._Out_Node_Id)
        if out_node is None:
            print "Relink error: out-node is not found"
            return False

        in_socket = in_node.get_input_socket_by_id(self._In_Socket_Id)
        if in_socket is None:
            print "Relink error: in-socket is not found"
            return False

        out_socket = out_node.get_output_socket_by_id(self._Out_Socket_Id)
        if out_socket is None:
            print "Relink error: out-socket is not found"
            return False

        self._In_Socket = in_socket
        self._Out_Socket = out_socket
        out_socket.associate_link(self)
        in_socket.associate_link(self)

        pass

    def destroy_link(self):
        if self._In_Socket is not None:
            self._In_Socket.disassociate_link(self)

        if self._Out_Socket is not None:
            self._Out_Socket.disassociate_link(self)

        self._Out_Socket = None
        self._In_Socket = None

Constants.SerialObjectTypes.register_type("Link", Link)
