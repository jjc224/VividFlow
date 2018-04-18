#!/usr/bin/python2.7
import os
import sys
from daemonize import Daemonize
import JobScheduler

def main():
      scheduler = JobScheduler.JobSchedulerDaemonMainLoop()

if __name__ == '__main__':
        myname=os.path.basename(sys.argv[0])
        pidfile='/var/run/%s' % myname       # any name
        daemon = Daemonize(app=myname,pid=pidfile, action=main)
        daemon.start()
