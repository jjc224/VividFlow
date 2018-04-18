#from Nodes import *
import Nodes
import Sockets
import Link
import Module
from SerializableObject import SerializableObject
from subprocess import Popen, PIPE
import random
import sys
import os
import Constants
import dbconn


class Algorithm(SerializableObject):
    _Nodes = None
    _Links = None
    _AlgorithmName = "UntitledAlgorithm"
    _AlgorithmID = None
    _UserID = None

    def __init__(self):
        super(Algorithm, self).__init__()
        self._Nodes = []
        self._Links = []

    def build_json_dict(self):
        json_dict = super(Algorithm, self).build_json_dict()
        json_dict["_AlgorithmName"] = self._AlgorithmName
        json_dict["_Links"] = self.build_json_array(self._Links)
        json_dict["_Nodes"] = self.build_json_array(self._Nodes)
        json_dict["_AlgorithmID"] = self._AlgorithmID
        json_dict["_UserID"] = self._UserID
        return json_dict

    def relink_algorithm(self):
        for node in self._Nodes:
            node.relink_sockets(self)
        for link in self._Links:
            success = link.relink_sockets(self)
            if success is False:
                self._Links.remove(link)
        pass

    def upgrade_modules(self):
        print "upgrading modules"
        for node in self._Nodes:
            if isinstance(node, Module.ModuleNode):
                bShouldUpgrade = False
                ModInDB = dbconn.db.get_latest_module_version(node._ModuleId)
                if node._ModuleVersionState == Constants.ModuleStates.InDevelopment:
                    bShouldUpgrade = True
                else:
                    if ModInDB["_ModuleVersionId"] is not node._ModuleVersionId:
                        bShouldUpgrade = True
                pass
                print "bShouldUpgrade = " + str(bShouldUpgrade)
                node.upgrade_module(ModInDB)
        pass

    def set_algorithm_userid(self, userid):
        self._UserID = userid


    def get_algorithm_name(self):
        return self._AlgorithmName

    def set_algorithm_name(self, new_name):
        if len(new_name) > 0:
            self._AlgorithmName = new_name

    def get_num_nodes(self):
        return len(self._Nodes)

    def get_num_links(self):
        return len(self._Links)

    def get_link(self, index):
        if index < len(self._Links):
            return self._Links[index]
        return None

    def get_node_by_index(self, index):
        if index < len(self._Nodes):
            return self._Nodes[index]
        return None

    def get_node_by_id(self, id):
        for node in self._Nodes:
            if node.get_object_id() == id:
                return node
        return None

    def add_node(self, new_node):
        if new_node not in self._Nodes:
            self._Nodes.append(new_node)

    def add_link(self, new_link):
        if new_link.get_in_socket_owner() not in self._Nodes:
            return False
        if new_link.get_out_socket_owner() not in self._Nodes:
            return False

        if new_link.get_in_socket() is None:
            return False
        if new_link.get_out_socket() is None:
            return False

        if new_link not in self._Links:
            self._Links.append(new_link)
            return True

    # Checks if this node is relevant to graph processing
    def is_processing_node(self, node):
        return not isinstance(node, Nodes.DataNode)

    def write_value_nodes(self, filenames):
        for node in self._Nodes:
            if isinstance(node, Nodes.ValueNode):
                sock = node.get_output_socket_by_index(0)
                filename = filenames[sock]
                node.write_value_to_file(filename)

    def get_end_nodes(self):
        end_nodes = []

        for node in self._Nodes:
            if node.is_end_node():
                end_nodes.append(node)

        return end_nodes

    # A list of nodes that don't include nodes that don't influence the dependency graph.
    def get_relevant_nodes(self):
        return [node for node in self._Nodes if self.is_processing_node(node)]

    def get_pre_req_steps(self, node, filenames, steps):
        step_pre_reqs = []
        file_pre_reqs = []

        # for each node get pre req nodes
        # for each input socket
        for i in xrange(node.get_num_input_sockets()):
            input_socket = node.get_input_socket_by_index(i)
            # for every link leading to this input, although strictly speaking there should only be 0 or 1
            for j in xrange(input_socket.get_num_links()):
                input_link = input_socket.get_link(j)
                pre_req_file = filenames[input_link.get_out_socket()]
                pre_req_node = input_link.get_out_socket_owner()
                pre_req_step = steps[pre_req_node]
                # add unique pre req steps
                if self.is_processing_node(pre_req_node):
                    if pre_req_step not in step_pre_reqs:
                        step_pre_reqs.append(pre_req_step)
                    # add unique pre req files
                    if pre_req_file not in file_pre_reqs:
                        file_pre_reqs.append(pre_req_file)

        pre_req_string = ""
        # add the prereq steps
        for pre_req in step_pre_reqs:
            pre_req_string += " " + pre_req
        # add the prereq files
        #for pre_req in file_pre_reqs:
        #    pre_req_string += " " + pre_req

        return pre_req_string.strip()

    def generate_socket_filename_map(self):
        output_index = 0
        filenames = {}
        for node in self._Nodes:
            for i in xrange(node.get_num_output_sockets()):
                socket = node.get_output_socket_by_index(i)
                filenames[socket] = str(output_index) + Sockets.SocketDataType.get_type_extension(socket.get_type())
                output_index += 1
        return filenames


    # Note: this function could be broken up into smaller functions
    # Note: this function iterates over the node list repeatedly to keep logic clear and avoid huge nesting pyramids
    #       therefore it is not as efficient as it could be
    def generate_makefile(self):
        end_nodes = self.get_end_nodes()
        filenames = {}
        steps = {}

        # TODO: method to be refactored if relevant_nodes are the same as end_nodes.
        relevant_nodes = self.get_relevant_nodes()

        # assign filenames to each output
        # Note: this is different to the other loops in that it also needs to be concerned with value nodes
        filenames = self.generate_socket_filename_map();

        # write out value nodes
        self.write_value_nodes(filenames)

        # assign each node a step name
        step_index = 0
        for node in self._Nodes:
            steps[node] = "Step" + str(step_index)
            step_index += 1

        # for each node generate a make step
        for node in relevant_nodes:
            rule_name = steps[node]
            rule_definition = rule_name + ": " + self.get_pre_req_steps(node, filenames, steps)
            print rule_definition
            command_line = "\t" + node.get_command_line()
            for i in xrange(node.get_num_input_sockets()):
                input_socket = node.get_input_socket_by_index(i)
                output_socket = None
                for j in xrange(input_socket.get_num_links()):
                    output_socket = input_socket.get_link(j).get_out_socket()
                output_node = output_socket.get_owner()
                argument_string = " -i"
                argument_string += str(input_socket.get_argument_number())
                argument_string += " "
                if isinstance(output_node, Nodes.ResourceNode):
                    argument_string += output_node.get_file_path()
                else:
                    argument_string += filenames[output_socket]
                command_line += argument_string

            for i in xrange(node.get_num_output_sockets()):
                output_socket = node.get_output_socket_by_index(i)
                argument_string = " -o"
                argument_string += str(output_socket.get_argument_number())
                argument_string += " "
                argument_string += filenames[output_socket]
                command_line += argument_string

            print command_line

        # build the main rule to run the algorithm
        final_rule = "RunAlgorithm:"
        for node in end_nodes:
            # add this node to the final rule if
            final_rule += " " + self.get_pre_req_steps(node, filenames, steps)

        print final_rule

    # Returns output and exit code of run.
    def run_makefile(self, target = None):
        cmd = ["make", "RunAlgorithm"]

        if target is not None:
            cmd.append(target)

        process  = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()

        output = ""

        if err:
            output = err
        elif out:
            output = out

        process.wait()
        return (output, process.returncode)

#    def run_makefile(self, target = None):
#        Config = Constants.AlgoConfig
#        makefile_path = Config.Paths['Makefiles'] + Config.Prefixes['Makefiles'] + str(self._AlgorithmID)
#
#        # Write makefile.
#        with open(makefile_path, 'w') as makefile:
#            makefile.write(makefile_buffer)
#
#        cmd = ['make', '-f', makefile_path]
#
#        if target is not None:
#            cmd.append(target)
#
#        process  = Popen(cmd, stdout=PIPE, stderr=PIPE)
#        out, err = process.communicate()
#
#        if err:
#            output = err
#        elif out:
#            output = out
#
#        process.wait()
#        os.remove(makefile_path)    # NOTE: for testing purposes, less manual cleaning.
#
#        return (output, process.returncode)

    def write_makefile(self, path):
        # Retrieve makefile from STDOUT and redirect into a specific path.
        old_stdout = sys.stdout
        sys.stdout = open(os.path.join(path, 'Makefile'), 'w')
        self.generate_makefile()
        sys.stdout.close()
        sys.stdout = old_stdout

    # Returns the output given by algorithm run.
    def get_run_output(self):
        return self.run_makefile("RunAlgorithm")[0]
Constants.SerialObjectTypes.register_type("Algorithm", Algorithm)
