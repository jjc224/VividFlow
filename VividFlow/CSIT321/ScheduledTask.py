from Constants import ScheduledTaskStatus
import Constants
from SerializableObject import SerializableObject
from datetime import datetime
import os
import json

class OutputFile(SerializableObject):
    OutputName = ""
    OutputPath = ""
    def __init__(self):
        super(OutputFile, self).__init__()
        self.OutputName = ""
        self.OutputPath = ""

    def build_json_dict(self):
        json_dict = super(OutputFile, self).build_json_dict()
        json_dict["OutputName"] = self.OutputName
        json_dict["OutputPath"] = self.OutputPath
        return json_dict
Constants.SerialObjectTypes.register_type("OutputFile", OutputFile)


class ScheduledTask(SerializableObject):
    # the database id number of this scheduled task
    _ScheduledTaskID = None
    # the algorithm id that this task is for
    _AlgorithmID = None
    # the time the job was ScheduledTask
    _TimeScheduled = None
    # the time the job entered the "InProgress" state and began processing
    _TimeStarted = None
    # the time the job completed
    _TimeCompleted = None
    # the current status of the job
    _TaskStatus = ScheduledTaskStatus.Pending
    # the return code from the makefile
    _ReturnCode = 0
    # an array of OutFiles that will show all output files
    _OutputFiles = []

    def __init__(self):
        super(ScheduledTask, self).__init__()
        self._OutputFiles = []

    def build_json_dict(self):
        json_dict = super(ScheduledTask, self).build_json_dict()
        json_dict["_ScheduledTaskID"] = self._ScheduledTaskID
        json_dict["_AlgorithmID"] = self._AlgorithmID
        json_dict["_TimeScheduled"] = Constants.DateTimeUtils.to_string(self._TimeScheduled)
        json_dict["_TimeStarted"] = Constants.DateTimeUtils.to_string(self._TimeStarted)
        json_dict["_TimeCompleted"] = Constants.DateTimeUtils.to_string(self._TimeCompleted)
        json_dict["_TaskStatus"] = self._TaskStatus
        json_dict["_ReturnCode"] = self._ReturnCode
        json_dict["_OutputFiles"] = self.build_json_array(self._OutputFiles)
        return json_dict

    def reconstruct_from_json(self, json_obj):
        super(ScheduledTask, self).reconstruct_from_json(json_obj)
        self._TimeScheduled = Constants.DateTimeUtils.from_string(json_obj["_TimeScheduled"])
        self._TimeStarted = Constants.DateTimeUtils.from_string(json_obj["_TimeStarted"])
        self._TimeCompleted = Constants.DateTimeUtils.from_string(json_obj["_TimeCompleted"])

    def mark_task_complete(self):
        self._TimeCompleted = datetime.now()
        self._TaskStatus = ScheduledTaskStatus.Completed

    def mark_task_scheduled(self):
        self._TimeScheduled = datetime.now()
        self._TaskStatus = ScheduledTaskStatus.Pending

    def mark_task_started(self):
        self._TimeStarted = datetime.now()
        self._TaskStatus = ScheduledTaskStatus.InProgress

    def get_working_path(self):
        return os.path.join(Constants.Settings["jobs"]["path_abs_working"], self._ScheduledTaskID, '')    # NOTE: final argument / empty string imposes system-independent delimeter at the end.

    def set_algorithm_id(self, algoid):
        self._AlgorithmID = algoid
Constants.SerialObjectTypes.register_type("ScheduledTask", ScheduledTask)
