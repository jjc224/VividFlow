import Constants
import ScheduledTask
import dbconn
import Module
import Nodes
import Algorithm
import os
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf8')

class JobWorker():
    _JobID = None
    _WorkingDir = Constants.Settings["jobs"]["path_abs_working"]
    _OutputDir = Constants.Settings["jobs"]["path_abs_output"]

    # A string containing the output of the entire process
    _RunLog = ""

    def __init__(self):
        self.setup_directories()

    def log(self, message):
        self._RunLog += "\n" + message

    def write_log(self):
        output_path = os.path.join(Constants.Settings["jobs"]["path_abs_output"], str(self._JobID), '')
        log_file = os.path.join(output_path, Constants.Settings["jobs"]["output_log_filename"])

        with open(log_file, 'a+') as outfile:
            outfile.write(self._RunLog)

        return log_file

    def setup_directories(self):
        dirs = [self._WorkingDir, self._OutputDir]

        for dir in dirs:
            if not os.path.exists(dir):
                os.makedirs(dir)

            if self._JobID is not None:
                path = os.path.join(dir, str(self._JobID))
                if not os.path.exists(path):
                    os.makedirs(path)

    def report_job_error(self, id, return_code=-1):
        job_jsonstr = dbconn.db.get_scheduled_task(id)
        job = Constants.SerialObjectTypes.build_object_from_json(job_jsonstr)
        job.mark_task_complete()
        job._ReturnCode = return_code

        self.write_log()

        finishedfiles = self.gather_finished_output_files(id)
        for file in finishedfiles:
            bAlreadyAdded = False
            for existing_record in job._OutputFiles:
                if existing_record.OutputPath == file.OutputPath:
                    bAlreadyAdded = True
            if bAlreadyAdded is False:
                job._OutputFiles.append(file)

        dbconn.db.update_scheduled_task(job)

    def gather_finished_output_files(self, id):
        output_path = os.path.join(Constants.Settings["jobs"]["path_abs_output"], str(id), '')
        onlyfiles = [f for f in os.listdir(output_path) if os.path.isfile(os.path.join(output_path, f))]
        OutputFiles = []
        for file in onlyfiles:
            filepath = os.path.join(output_path, file)
            rel_dir_index = filepath.index(os.path.join('', 'static', ''))
            OutputFiles.append(ScheduledTask.OutputFile())
            OutputFiles[-1].OutputName = file
            OutputFiles[-1].OutputPath = filepath[rel_dir_index:]
        return OutputFiles

    def run_job(self, id):
        self._JobID = id
        self.setup_directories()

        # Get ScheduledTask from DB/jsonstr.
        job_jsonstr = dbconn.db.get_scheduled_task(id)
        job = Constants.SerialObjectTypes.build_object_from_json(job_jsonstr)

        # Mark job as started.
        job.mark_task_started()
        dbconn.db.update_scheduled_task(job)

        # Get Algorithm from DB/jsonstr.
        algorithm_jsonstr = dbconn.db.get_algorithm(job._AlgorithmID)
        algorithm = Constants.SerialObjectTypes.build_object_from_json(algorithm_jsonstr)
        algorithm.relink_algorithm()

        bCompiledSuccessfully = True

        for node in algorithm.get_relevant_nodes():
            if isinstance(node, Module.ModuleNode):
                if not node.is_compiled():
                    self.log("Attempting to compile module " + node.get_name())
                    binarypath, returncode, outstream, errstream = node.compile_code()
                    if returncode != 0:
                        self.log("Error compiling module " + node.get_name())
                        self.log("Outstream:")
                        self.log(outstream)
                        self.log("Errstream:")
                        self.log(errstream)
                        self.log("End of compiler output for module " + node.get_name())
                        bCompiledSuccessfully = False
                    else:
                        self.log("Finished compiling module " + node.get_name())

        if bCompiledSuccessfully is False:
            self.log("Failed to compile modules correctly. Aborting")
            self.report_job_error(id)
            return

        # Change to working folder for algorithm makefile generation.
        old_cwd = os.getcwd()
        os.chdir(job.get_working_path())

        # Generate makefile and run the algorithm.
        algorithm.write_makefile(os.getcwd())                 # CWD changed via job.get_working_path().
        output, job._ReturnCode = algorithm.run_makefile()    # Necessary, as this works from CWD.
        os.chdir(old_cwd)                                     # Return to "root" directory for relative static output.

        self.log(output)

        output_path = os.path.join(Constants.Settings["jobs"]["path_abs_output"], str(self._JobID), '')
        rel_dir_index = output_path.index(os.path.join('', 'static', ''))

        # Write the log file out and add to the list of output files
        log_file = self.write_log()
        job._OutputFiles.append(ScheduledTask.OutputFile())
        job._OutputFiles[-1].OutputName = 'log'
        job._OutputFiles[-1].OutputPath = log_file[rel_dir_index:]

        file_socket_output_map = algorithm.generate_socket_filename_map()

        # Get output/end node filenames and append to output files array.
        node_index = 0
        for node in algorithm.get_end_nodes():
            # TODO: use socket to determine type.
            if node.get_num_input_sockets() > 0:
                for socket_index in range(node.get_num_input_sockets()):
                    socket = node.get_input_socket_by_index(socket_index)
                    file_extension = Constants.SocketDataType.get_type_extension(socket.get_type())
                    filepath = os.path.join(self._OutputDir, str(id), str(socket._OwnerNodeId) + file_extension)
                    rel_dir_index = filepath.index(os.path.join('', 'static', ''))

                    job._OutputFiles.append(ScheduledTask.OutputFile())
                    job._OutputFiles[-1].OutputName = node._Name
                    job._OutputFiles[-1].OutputPath = filepath[rel_dir_index:]

                    #get link
                    if socket.get_num_links() > 0:
                        link = socket.get_link(0)
                        output_socket = link.get_out_socket()

                        self.log( "Attempting to move file: " + str(file_socket_output_map[output_socket]))
                        # TODO: verify this works for all cases (I'm unsure that it does).
                        os.rename(os.path.join(job.get_working_path(),file_socket_output_map[output_socket]), filepath)

                node_index += 1
            else:
                print "No input sockets."

        # Algorithm run complete.
        job.mark_task_complete()
        dbconn.db.update_scheduled_task(job)

        if(job._ReturnCode != 0):
            print >> sys.stderr, 'Error: job returned exit code ' + str(job._ReturnCode) + ' (job ID = ' + str(self._JobID) + ').'


def main():
        if len(sys.argv) < 2:
            print >> sys.stderr, "Usage: python JobWorker.py <job ID>"
            return

        worker = JobWorker()
        worker._JobID = int(sys.argv[1])
        try:
            worker.run_job(worker._JobID)
        except:
            e = str(sys.exc_info()[0])
            worker.log(e)
            e = str(sys.exc_info()[1])
            worker.log(e)
            e = traceback.format_tb(sys.exc_info()[2])
            for line in e:
                worker.log(line)
            worker.report_job_error(worker._JobID, -2)

if __name__ == "__main__":
    main()
