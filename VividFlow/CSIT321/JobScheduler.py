#!/usr/bin/python2.7
import ScheduledTask
import Constants
import dbconn
import threading
import time
import subprocess


class JobSchedulerThread(threading.Thread):
    bContinueRunning = True;
    def run(self):
        print "JobScheduler running"
        while self.bContinueRunning:
            print "Checking for jobs"
            TryAndRunJob()
            time.sleep(Constants.Settings["job_scheduler"]["check_frequency"])

def TryAndRunJob():
    newTask = dbconn.db.get_one_scheduled_task_with_status(Constants.ScheduledTaskStatus.Pending)
    if newTask is not None:
        countInProgressTasks = dbconn.db.count_scheduled_tasks_with_status(Constants.ScheduledTaskStatus.InProgress)
        if countInProgressTasks < Constants.Settings["job_scheduler"]["max_concurrent_jobs"]:
            print "Running job: " + newTask["_ScheduledTaskID"]
            RunWorker(newTask["_ScheduledTaskID"])

def RunWorker(scheduledTaskId):
    print "running worker"
    subprocess.Popen(['python', 'JobWorker.py', str(scheduledTaskId)])

def StartJobSchedulerAsThread():
    scheduler = JobSchedulerThread()
    scheduler.daemon = True
    scheduler.start()
    return scheduler

def JobSchedulerDaemonMainLoop():
    bContinueRunning = True
    while bContinueRunning:
        TryAndRunJob()
        time.sleep(Constants.Settings["job_scheduler"]["check_frequency"])

if __name__ == '__main__':
    StartJobSchedulerAsThread()
    while threading.active_count() > 1:
        time.sleep(0.1)
