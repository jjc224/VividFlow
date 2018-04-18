import Constants
from Constants import ModuleStates
import Nodes
from SerializableObject import SerializableObject
from subprocess import Popen, PIPE
import os

class ModuleNode(Nodes.Node):
    # the unique id version of this module
    _ModuleVersionId = None
    # the id of the owner of this module
    _ModuleUserId = None
    # the user friendly version number of this module
    _ModuleVersion = 0
    # the unique id for this series of modules. Lines up with the ModuleVersionId of the initial version
    _ModuleId = None
    # the status of the module
    _ModuleVersionState = ModuleStates.InDevelopment

    def __init__(self):
        super(ModuleNode, self).__init__()
        self._ModuleVersionId = None
        self._ModuleUserId = None
        self._ModuleVersion = 0
        self._ModuleId = None
        self._ModuleVersionState = ModuleStates.InDevelopment
        self._UserID = None

    def upgrade_module(self, new_module_dict):
        oldInSockets = self._InputSockets
        oldOutSockets = self._OutputSockets
        self._InputSockets = []
        self._OutputSockets = []

        #module info
        self._ModuleVersionId = new_module_dict["_ModuleVersionId"]
        self._ModuleUserId = new_module_dict["_ModuleUserId"]
        self._ModuleVersion = new_module_dict["_ModuleVersion"]
        self._ModuleId = new_module_dict["_ModuleId"]
        self._ModuleVersionState = new_module_dict["_ModuleVersionState"]
        self._ModuleVersionId = new_module_dict["_ModuleVersionId"]
        #node info
        self._Name = new_module_dict["_Name"]
        self._UserID = new_module_dict["_UserID"]
        #serializable object info
        #self._ObjectID = new_module_dict["_ObjectID"]

        #input sockets
        for in_sock_dict in new_module_dict["_InputSockets"]:
            in_sock = Constants.SerialObjectTypes.build_object_from_json(in_sock_dict)
            in_sock._OwnerNodeId = self._ObjectID
            for old_sock in oldInSockets:
                if in_sock._Name == old_sock._Name:
                    if in_sock._DataType == old_sock._DataType:
                        #copy socket info
                        in_sock._ObjectID = old_sock._ObjectID

            self._InputSockets.append(in_sock)

        #output sockets
        for out_sock_dict in new_module_dict["_OutputSockets"]:
            out_sock = Constants.SerialObjectTypes.build_object_from_json(out_sock_dict)
            out_sock._OwnerNodeId = self._ObjectID
            for old_sock in oldOutSockets:
                if out_sock._Name == old_sock._Name:
                    if out_sock._DataType == old_sock._DataType:
                        #copy socket info
                        out_sock._ObjectID = old_sock._ObjectID

            self._OutputSockets.append(out_sock)

        pass

    def build_json_dict(self):
        json_dict = super(ModuleNode, self).build_json_dict()
        json_dict["_ModuleUserId"] = self._ModuleUserId
        json_dict["_ModuleVersionId"] = self._ModuleVersionId
        json_dict["_ModuleVersion"] = self._ModuleVersion
        json_dict["_ModuleId"] = self._ModuleId
        json_dict["_UserID"] = self._UserID
        input_sockets_list = []
        for socket in self._InputSockets:
            input_sockets_list.append(socket.build_json_dict())
        output_sockets_list = []
        for socket in self._OutputSockets:
            output_sockets_list.append(socket.build_json_dict())
        json_dict["_InputSockets"] = input_sockets_list
        json_dict["_OutputSockets"] = output_sockets_list
        return json_dict

    def set_module_userid(self,userid):
        self._UserID = userid

    def get_filename(self):
        return str(self._ModuleVersionId)

    def get_code_filename(self):
        filename = self.get_filename() + Constants.Settings["modules"]["code_file_extension"]
        fullpath = os.path.join(Constants.Settings["modules"]["path_abs_code"], filename)
        return fullpath

    def is_compiled(self):
        filepath = os.path.join(Constants.Settings["modules"]["path_abs_executables"], self.get_filename())
        return os.path.isfile(filepath) and os.access(filepath, os.X_OK)

    def get_code(self):
        filepath = self.get_code_filename()

        if not os.path.isfile(filepath):
            return None

        return file(filepath).read()

    # returns a tuple of output filename, the return code, and the output and error streams of the compiler
    def compile_code(self):
        compiler_options = "-I" + Constants.Settings["modules"]["path_abs_vividflow_lib_dir"]
        additional_args  = Constants.Settings["modules"]["additional-compiler-flags"].split(' ')
        outfile          = self.get_command_line()
        cstd             = "-std=" + Constants.Settings["modules"]["language-standard"]
        cmd              = [Constants.Settings["modules"]["compiler"], self.get_code_filename(), '-o', outfile, compiler_options, cstd]
        for arg in additional_args:
            cmd.append(arg)

        run_cmd = ""
        for item in cmd:
            run_cmd += " " + item
        print "Running command: " + run_cmd
        print "CWD: " + os.getcwd()
        process  = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        process.wait()
        return (outfile, process.returncode, out, err)

    def upload_code(self, new_code):
        if not new_code:    # Empty string, NoneType, etc.
            return None

        print self.get_code_filename()

        with open(self.get_code_filename(), 'w+') as module_code:
            module_code.write(new_code)

        #delete any existing version of the program
        try:
            os.remove(self.get_command_line())
        except:
            pass

    def get_command_line(self):
            return os.path.join(Constants.Settings["modules"]["path_abs_executables"], self.get_filename())

Constants.SerialObjectTypes.register_type("ModuleNode", ModuleNode)
