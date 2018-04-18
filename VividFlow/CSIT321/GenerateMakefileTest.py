import Algorithm
from Nodes import *
from Module import ModuleNode
from Link import Link
import ScheduledTask
import dbconn
import Sockets
import json


# A class that allows an arbitrary number of input and output sockets to be created on instantiation.
# all sockets are of String type
class StringTestNode(ModuleNode):
    _Node_Name = None

    def build_json_dict(self):
        json_dict = super(StringTestNode, self).build_json_dict()
        json_dict["_Node_Name"] = self._Node_Name
        return json_dict

    def __init__(self, node_name="UntitledNode", num_inputs=0, num_outputs=0):
        super(StringTestNode, self).__init__()
        for i in xrange(num_inputs):
            new_socket = Sockets.NodeIOSocket(i+1, "Output", Sockets.SocketDataType.String, self)
            self.add_input_socket(new_socket)

        for i in xrange(num_outputs):
            new_socket = Sockets.NodeIOSocket(i+1, "Output", Sockets.SocketDataType.String, self)
            self.add_output_socket(new_socket)

        self._Node_Name = node_name

    def get_command_line(self):
        return self._Node_Name
Constants.SerialObjectTypes.register_type("StringTestNode", StringTestNode)


def test_generate_makefile():
    # create algorithm
    algotest = Algorithm.Algorithm()
    algotest.set_algorithm_name("Test Algorithm")

    # create nodes
    node1 = StringTestNode("Node1", 2, 1)
    node2 = StringTestNode("Node2", 1, 1)
    node3 = StringTestNode("Node3", 0, 1)
    node4 = StringTestNode("Node4", 0, 1)
    node5 = StringTestNode("Node5", 1, 1)
    node6 = ValueNode(23, Sockets.SocketDataType.Integer)
    algotest.add_node(node1)
    algotest.add_node(node2)
    algotest.add_node(node3)
    algotest.add_node(node4)
    algotest.add_node(node5)
    algotest.add_node(node6)

    # create 4 links
    link1 = Link(node2.get_output_socket_by_index(0), node1.get_input_socket_by_index(0))
    link2 = Link(node3.get_output_socket_by_index(0), node1.get_input_socket_by_index(1))
    link3 = Link(node4.get_output_socket_by_index(0), node2.get_input_socket_by_index(0))
    link4 = Link(node2.get_output_socket_by_index(0), node5.get_input_socket_by_index(0))
    algotest.add_link(link1)
    algotest.add_link(link2)
    algotest.add_link(link3)
    algotest.add_link(link4)

    algojsonstr = algotest.serialize_json()
    print algojsonstr

    algo_from_json = json.loads(algojsonstr)
    reconstructedalgo = Constants.SerialObjectTypes.build_object_from_json(algo_from_json)
    reconstructedalgo.relink_algorithm()
    algostr2 = reconstructedalgo.serialize_json()

    print algostr2

    # generate makefile
    algotest.generate_makefile()
    reconstructedalgo.generate_makefile()

    algostr3 = """{"ObjectType":"Algorithm","_ObjectID":"0.172865772584","_AlgorithmName":"Test Algorithm","_Links":[{"ObjectType":"Link","_ObjectID":"0.651521621056","_In_Node_Id":"0.827120327614","_In_Socket_Id":"0.215758519873","_Out_Node_Id":"0.163181502025","_Out_Socket_Id":"0.843875853078"},{"ObjectType":"Link","_ObjectID":"0.681048750489","_In_Node_Id":"0.827120327614","_In_Socket_Id":"0.737757341123","_Out_Node_Id":"0.458104304074","_Out_Socket_Id":"0.668679642163"},{"ObjectType":"Link","_ObjectID":"0.00411293361501","_In_Node_Id":"0.163181502025","_In_Socket_Id":"0.712889852252","_Out_Node_Id":"0.0418882065203","_Out_Socket_Id":"0.250475798495"},{"ObjectType":"Link","_ObjectID":"0.850493651329","_In_Node_Id":"0.66613719851","_In_Socket_Id":"0.984156732888","_Out_Node_Id":"0.163181502025","_Out_Socket_Id":"0.843875853078"}],"_Nodes":[{"ObjectType":"StringTestNode","_ObjectID":"0.827120327614","_PosX":0,"_PosY":0,"_InputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.215758519873","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.827120327614","_Required":false},{"ObjectType":"NodeIOSocket","_ObjectID":"0.737757341123","_ArgumentNumber":2,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.827120327614","_Required":false}],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.852037921872","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.827120327614","_Required":false}],"_ModuleId":null,"_Node_Name":"Node1"},{"ObjectType":"StringTestNode","_ObjectID":"0.163181502025","_PosX":0,"_PosY":0,"_InputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.712889852252","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.163181502025","_Required":false}],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.843875853078","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.163181502025","_Required":false}],"_ModuleId":null,"_Node_Name":"Node2"},{"ObjectType":"StringTestNode","_ObjectID":"0.458104304074","_PosX":0,"_PosY":0,"_InputSockets":[],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.668679642163","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.458104304074","_Required":false}],"_ModuleId":null,"_Node_Name":"Node3"},{"ObjectType":"StringTestNode","_ObjectID":"0.0418882065203","_PosX":0,"_PosY":0,"_InputSockets":[],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.250475798495","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.0418882065203","_Required":false}],"_ModuleId":null,"_Node_Name":"Node4"},{"ObjectType":"StringTestNode","_ObjectID":"0.66613719851","_PosX":0,"_PosY":0,"_InputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.984156732888","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.66613719851","_Required":false}],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.0829148269887","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.66613719851","_Required":false}],"_ModuleId":null,"_Node_Name":"Node5"},{"ObjectType":"ValueNode","_ObjectID":"0.243041239449","_PosX":0,"_PosY":0,"_InputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.468896970094","_ArgumentNumber":0,"_Name":"Output","_DataType":"Integer","_OwnerNodeId":"0.243041239449","_Required":false}],"_OutputSockets":[],"_DataType":"Integer","_Value":23}]}"""
    algo_from_js = json.loads(algostr3)
    reconjs = Constants.SerialObjectTypes.build_object_from_json(algo_from_js)
    reconjs.relink_algorithm()

    reconjs.generate_makefile()

# TODO: write tests
#       Test links
#            Incompatible types
#            nodes not in algorithm
#            adding 2 links to an input node
#            adding links from and to the same node
#            adding links to null sockets
#       test nodes
#       test deleting links and preserving graph integrity
#       test deleting nodes and preserving graph integrity
#       test makefile generation on larger graphs
#       test value node writes
#       test different socket data types

def test_scheduled_task():
    ###############################
    # random serialization tests
    ###############################
    task = ScheduledTask.ScheduledTask()
    task.mark_task_scheduled()
    task.mark_task_started()
    task.mark_task_complete()
    task_as_str = task.serialize_json()
    task2 = Constants.SerialObjectTypes.build_object_from_json(json.loads(task_as_str))

    ###############################
    # DB tests
    ###############################
    # create a scheduled task
    id = dbconn.db.create_scheduled_task()

    # retrieve the scheduled task by id
    record = dbconn.db.get_scheduled_task(id)

    # deserialize the scheduled task
    record_obj = Constants.SerialObjectTypes.build_object_from_json(record)

    # do some operations on the scheduled task
    record_obj.mark_task_scheduled()
    record_obj.mark_task_started()
    record_obj.mark_task_complete()
    record_obj._AlgorithmID = 48

    # write the scheduled task back to the database
    dbconn.db.insert_schedtask_dict(record_obj.build_json_dict())

def test_gen_from_db():
    algo_db = dbconn.db.get_algorithm(5)
    #print algo_db

    reconstructedalgo = Constants.SerialObjectTypes.build_object_from_json(algo_db)
    reconstructedalgo.relink_algorithm()

    reconstructedalgo.generate_makefile()


if __name__ == "__main__":
    #test_generate_makefile()
    #test_scheduled_task()
    test_gen_from_db()
